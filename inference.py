import os
import numpy as np
import time
import librosa
from pathlib import Path
import onnxruntime

import torch

from utilities import (create_folder, get_filename, RegressionPostProcessor, 
    write_events_to_midi)
# from .models import Regress_onset_offset_frame_velocity_CRNN, Note_pedal
# from .pytorch_utils import move_data_to_device, forward
import config


from torchlibrosa.stft import Spectrogram, LogmelFilterBank


def move_data_to_device(x):
    if 'float' in str(x.dtype):
        x = torch.Tensor(x)
    elif 'int' in str(x.dtype):
        x = torch.LongTensor(x)
    else:
        return x

    # return x.to(device)
    return x


def append_to_dict(dict, key, value):
    if key in dict.keys():
        dict[key].append(value)
    else:
        dict[key] = [value]
 

def output_to_dict(note_output,pedal_output):
    full_output_dict = {
            'reg_onset_output': note_output[0], 
            'reg_offset_output': note_output[1], 
            'frame_output': note_output[2], 
            'velocity_output': note_output[3],
            'reg_pedal_onset_output': pedal_output[0], 
            'reg_pedal_offset_output': pedal_output[1],
            'pedal_frame_output': pedal_output[2]
            }
    return full_output_dict



def forward(model, x, 
                batch_size,
                setProgressBarValue,
                setProgressBarVisibility,
                setProgressBarFullValue,
                logUpdate = print,
                frames_per_second=100):
    """Forward data to model in mini-batch. 
    
    Args: 
      model: object
      x: (N, segment_samples)
      batch_size: int

    Returns:
      output_dict: dict, e.g. {
        'frame_output': (segments_num, frames_num, classes_num),
        'onset_output': (segments_num, frames_num, classes_num),
        ...}
    """
    sample_rate = 16000
    window_size = 2048
    hop_size = sample_rate // frames_per_second
    mel_bins = 229
    fmin = 30
    fmax = sample_rate // 2

    window = 'hann'
    center = True
    pad_mode = 'reflect'
    ref = 1.0
    amin = 1e-10
    top_db = None

    # midfeat = 1792
    # momentum = 0.01

        # Spectrogram extractor
    spectrogram_extractor = Spectrogram(n_fft=window_size, 
            hop_length=hop_size, win_length=window_size, window=window, 
            center=center, pad_mode=pad_mode, freeze_parameters=True)

        # Logmel feature extractor
    logmel_extractor = LogmelFilterBank(sr=sample_rate, 
            n_fft=window_size, n_mels=mel_bins, fmin=fmin, fmax=fmax, ref=ref, 
            amin=amin, top_db=top_db, freeze_parameters=True)

    output_dict = {}
    # device = next(model.parameters()).device
    
    pointer = 0
    total_segments = int(np.ceil(len(x) / batch_size))
    setProgressBarFullValue(total_segments)
    setProgressBarVisibility(True)
    while True:
        logUpdate('Segment {} / {}'.format(pointer, total_segments))
        setProgressBarValue(pointer)
        if pointer >= len(x):
            break

        batch_waveform = move_data_to_device(x[pointer : pointer + batch_size])
        pointer += batch_size

        
        batch_waveform = spectrogram_extractor(batch_waveform)
        batch_waveform = logmel_extractor(batch_waveform)

            # note_output,pedal_output = model(batch_waveform)
        note_output,pedal_output = model(None,{'input':to_numpy(batch_waveform).astype(np.float32)})
        batch_output_dict = output_to_dict(note_output,pedal_output)

        for key in batch_output_dict.keys():
            append_to_dict(output_dict, key, batch_output_dict[key])

    for key in output_dict.keys():
        output_dict[key] = np.concatenate(output_dict[key], axis=0)

    setProgressBarVisibility(False)

    return output_dict


def to_numpy(tensor):
    return tensor.detach().cpu().numpy() if tensor.requires_grad else tensor.cpu().numpy()




class PianoTranscription(object):
    def __init__(self, model,checkpoint_path=None, 
        segment_samples=16000*10, device=torch.device('cuda')):
        """Class for transcribing piano solo recording.

        Args:
          model_type: str
          checkpoint_path: str
          segment_samples: int
          device: 'cuda' | 'cpu'
        """
        # if not checkpoint_path: 
        #     checkpoint_path='{}/piano_transcription_inference_data/note_F1=0.9677_pedal_F1=0.9186.pth'.format(str(Path.home()))
        # print('Checkpoint path: {}'.format(checkpoint_path))

        # if not os.path.exists(checkpoint_path) or os.path.getsize(checkpoint_path) < 1.6e8:
        #     create_folder(os.path.dirname(checkpoint_path))
        #     print('Total size: ~165 MB')
        #     zenodo_path = 'https://zenodo.org/record/4034264/files/CRNN_note_F1%3D0.9677_pedal_F1%3D0.9186.pth?download=1'
        #     os.system('wget -O "{}" "{}"'.format(checkpoint_path, zenodo_path))

        print('Using {} for inference.'.format(device))

        self.segment_samples = segment_samples
        self.frames_per_second = config.frames_per_second
        self.classes_num = config.classes_num
        self.onset_threshold = 0.3
        self.offset_threshod = 0.3
        self.frame_threshold = 0.1
        self.pedal_offset_threshold = 0.2



        # self.onnx_session = onnxruntime.InferenceSession(checkpoint_path)
        # self.onnx_session = onnxruntime.InferenceSession("/content/full_model.onnx")
        self.model = model
        # print("loaded model")


    def transcribe(self, audio, midi_path,
                            setProgressBarValue,
                            setProgressBarVisibility,
                            setProgressBarFullValue,
                            logUpdate=print):
        """Transcribe an audio recording.

        Args:
          audio: (audio_samples,)
          midi_path: str, path to write out the transcribed MIDI.

        Returns:
          transcribed_dict, dict: {'output_dict':, ..., 'est_note_events': ...}

        """
        audio = audio[None, :]  # (1, audio_samples)

        # Pad audio to be evenly divided by segment_samples
        audio_len = audio.shape[1]
        pad_len = int(np.ceil(audio_len / self.segment_samples))\
            * self.segment_samples - audio_len

        audio = np.concatenate((audio, np.zeros((1, pad_len))), axis=1)

        # Enframe to segments
        segments = self.enframe(audio, self.segment_samples)
        """(N, segment_samples)"""

        # Forward
        output_dict = forward(self.model, segments, batch_size=1,
                                            setProgressBarValue=setProgressBarValue,
                                            setProgressBarFullValue=setProgressBarFullValue,
                                            setProgressBarVisibility=setProgressBarVisibility,
                                            logUpdate=logUpdate,
                                            frames_per_second=self.frames_per_second)
        """{'reg_onset_output': (N, segment_frames, classes_num), ...}"""

        # Deframe to original length
        for key in output_dict.keys():
            output_dict[key] = self.deframe(output_dict[key])[0 : audio_len]
        """output_dict: {
          'reg_onset_output': (N, segment_frames, classes_num), 
          'reg_offset_output': (N, segment_frames, classes_num), 
          'frame_output': (N, segment_frames, classes_num), 
          'velocity_output': (N, segment_frames, classes_num)}"""

        # Post processor
        post_processor = RegressionPostProcessor(self.frames_per_second, 
            classes_num=self.classes_num, onset_threshold=self.onset_threshold, 
            offset_threshold=self.offset_threshod, 
            frame_threshold=self.frame_threshold, 
            pedal_offset_threshold=self.pedal_offset_threshold)

        # Post process output_dict to MIDI events
        (est_note_events, est_pedal_events) = \
            post_processor.output_dict_to_midi_events(output_dict)

        # Write MIDI events to file
        if midi_path:
            write_events_to_midi(start_time=0, note_events=est_note_events, 
                pedal_events=est_pedal_events, midi_path=midi_path)
            logUpdate('Write out to {}'.format(midi_path))

        transcribed_dict = {
            'output_dict': output_dict, 
            'est_note_events': est_note_events,
            'est_pedal_events': est_pedal_events}

        return transcribed_dict

    def enframe(self, x, segment_samples):
        """Enframe long sequence to short segments.

        Args:
          x: (1, audio_samples)
          segment_samples: int

        Returns:
          batch: (N, segment_samples)
        """
        assert x.shape[1] % segment_samples == 0
        batch = []

        pointer = 0
        while pointer + segment_samples <= x.shape[1]:
            batch.append(x[:, pointer : pointer + segment_samples])
            pointer += segment_samples // 2

        batch = np.concatenate(batch, axis=0)
        return batch

    def deframe(self, x):
        """Deframe predicted segments to original sequence.

        Args:
          x: (N, segment_frames, classes_num)

        Returns:
          y: (audio_frames, classes_num)
        """
        if x.shape[0] == 1:
            return x[0]

        else:
            x = x[:, 0 : -1, :]
            """Remove an extra frame in the end of each segment caused by the
            'center=True' argument when calculating spectrogram."""
            (N, segment_samples, classes_num) = x.shape
            assert segment_samples % 4 == 0

            y = []
            y.append(x[0, 0 : int(segment_samples * 0.75)])
            for i in range(1, N - 1):
                y.append(x[i, int(segment_samples * 0.25) : int(segment_samples * 0.75)])
            y.append(x[-1, int(segment_samples * 0.25) :])
            y = np.concatenate(y, axis=0)
            return y