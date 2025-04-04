try:
    import pyi_splash
except:
    pass

from PySide6.QtWidgets import QApplication, QWidget,QFileDialog,QMessageBox
from PySide6.QtCore import QAbstractListModel,Qt,QThreadPool,QRunnable,Slot,Signal,QObject,QSize
from PySide6.QtGui import QTextOption,QIcon

from inference import PianoTranscription
from utilities import load_audio
from config import sample_rate
from mainui import Ui_Form
import sys
from onnxruntime import InferenceSession, get_available_providers
import os
import qtawesome as qta
from queue import Queue
import time
import webbrowser


model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models', 'model.onnx')
ffmpeg_path = "ffmpeg"
window_logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'melodfy_logo_rounded.png')

itemQueue = Queue()
isReady = False

# Temporary placeholder for logger with buffering
class TemporaryLogger:
    def __init__(self):
        self.log_buffer = []

    def log(self, message):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        formatted_message = f"[{timestamp}] {message}"
        print(formatted_message)  # Keep printing to the console for debugging
        self.log_buffer.append(formatted_message)

    def flush_to_logger(self, logger_instance):
        for message in self.log_buffer:
            logger_instance.log(message)
        self.log_buffer = []

logger = TemporaryLogger()  # Initialize a temporary logger to buffer logs

class Logger(QObject):
    logSignal = Signal(str)

    def __init__(self, logBrowser):
        super(Logger, self).__init__()
        self.logBrowser = logBrowser
        self.logSignal.connect(self.updateLog)

    def log(self, message):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        formatted_message = f"[{timestamp}] {message}"
        print(formatted_message)  # Keep printing to the console for debugging
        self.logSignal.emit(formatted_message)

    def updateLog(self, message):
        self.logBrowser.append(message)
        self.logBrowser.verticalScrollBar().setValue(self.logBrowser.verticalScrollBar().maximum())



def downloadModel():
    import requests
    url = 'https://huggingface.co/krystv/piano_inference_onnx/resolve/main/model.onnx'
    logger.log("Downloading model from Hugging Face...")
    r = requests.get(url, allow_redirects=True)
    open(model_path, 'wb').write(r.content)
    logger.log("Model downloaded successfully.")

if not os.path.exists(model_path):
    downloadModel()
else:
    logger.log("Model already present")

def get_onnxruntime_session(model_path):
    logger.log("Checking available ONNX Runtime providers...")
    available_providers = get_available_providers()
    logger.log(f"Available providers: {available_providers}")

    if "CUDAExecutionProvider" in available_providers:
        logger.log("Using CUDAExecutionProvider for GPU inference.")
        return InferenceSession(model_path, providers=["CUDAExecutionProvider", "CPUExecutionProvider"])
    elif "DmlExecutionProvider" in available_providers:
        logger.log("Using DmlExecutionProvider for GPU inference.")
        return InferenceSession(model_path, providers=['DmlExecutionProvider', "CPUExecutionProvider"])
    else:
        logger.log("No GPU provider available. Falling back to CPU.")
        return InferenceSession(model_path, providers=["CPUExecutionProvider"])

try:
    logger.log("Loading model...")
    ort_session = get_onnxruntime_session(model_path)
except Exception as e:
    logger.log(f"Error loading model: {e}")
    downloadModel()
    ort_session = get_onnxruntime_session(model_path)

c = PianoTranscription(model=ort_session.run)
logger.log("Model loaded successfully.")

try:
    pyi_splash.close()
except:
    pass

def getDirectoryPathFromFilePath(filepath):
    return os.path.dirname(filepath)

class WorkerSignals(QObject):
    setItemAsProcessingSignal = Signal(object)
    setItemAsProcessedSignal = Signal(object)
    loggingUpdateSignal = Signal(str)
    setProgressBarVisibilitySignal = Signal(bool)
    setProgressBarValueSignal = Signal(int)
    setProgressBarFullValueSignal = Signal(int)
    setBtnEnableSignal = Signal()

class Worker(QRunnable):
    def __init__(self, outputDirectory=None):
        super(Worker, self).__init__()
        self.signals = WorkerSignals()
        self.outputDirectory = outputDirectory

    def logUpdate(self, text):
        logger.log(text)

    def setProgressBarVisibility(self, visibility):
        self.signals.setProgressBarVisibilitySignal.emit(visibility)

    def setProgressBarValue(self, value):
        self.signals.setProgressBarValueSignal.emit(value)

    def setProgressBarFullValue(self, value):
        self.signals.setProgressBarFullValueSignal.emit(value)

    @Slot()
    def run(self):
        global isReady
        while isReady:
            _item = itemQueue.get()
            self.signals.setItemAsProcessingSignal.emit(_item)
            basename = os.path.basename(_item[0]).split(".")[0] + '.mid'
            self.outputDirectory2 = self.outputDirectory if self.outputDirectory not in [None, ""] else getDirectoryPathFromFilePath(_item[0])
            self.outputDirectory2 = os.path.abspath(os.path.join(self.outputDirectory2, basename))
            audio, _ = load_audio(_item[0], sr=sample_rate, mono=True, ffmpeg_path=ffmpeg_path)

            logger.log(f"Processing file: {_item[0]}")
            c.transcribe(audio, self.outputDirectory2,
                         logUpdate=self.logUpdate,
                         setProgressBarVisibility=self.setProgressBarVisibility,
                         setProgressBarValue=self.setProgressBarValue,
                         setProgressBarFullValue=self.setProgressBarFullValue)

            self.signals.setItemAsProcessedSignal.emit(_item)
            if itemQueue.empty():
                isReady = False
        self.signals.setBtnEnableSignal.emit()

class ListModel(QAbstractListModel):
    def __init__(self, data=None, parent=None):
        super(ListModel, self).__init__(parent)
        self._data = data or []

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self._data[index.row()][1]
        if role == Qt.DecorationRole:
            if self._data[index.row()][2] == 1:
                return qta.icon('fa5s.check-circle', color="#00ff00")
            elif self._data[index.row()][2] == -1:
                return qta.icon('fa5s.hourglass-half', color="#ffff00")
            return qta.icon('fa5s.music', color="#fffafa")

    def rowCount(self, index):
        return len(self._data)

class Main_UI(QWidget, Ui_Form):
    def __init__(self):
        super(Main_UI, self).__init__()
        self.setupUi(self)

        self.logger = Logger(self.logBrowser)  # Initialize the logger
        self.threadpool = QThreadPool()
        self.progressBar.setVisible(False)
        self.logBrowser.setText("")
        self.listModel = ListModel()
        self.listQueue.setModel(self.listModel)
        self.singleBtn.setIcon(qta.icon('mdi.music-box', color="#fffafa"))
        self.singleBtn.setIconSize(QSize(25, 25))
        self.multipleBtn.setIcon(qta.icon('mdi.music-box-multiple', color="#fffafa"))
        self.multipleBtn.setIconSize(QSize(25, 25))
        self.folderBtn.setIcon(qta.icon('mdi.folder-music', color="#fffafa"))
        self.folderBtn.setIconSize(QSize(25, 25))
        self.outputDirBtn.setIcon(qta.icon('mdi.folder', color="#fffafa"))
        self.outputDirBtn.setIconSize(QSize(25, 25))
        self.startBtn.setIcon(qta.icon('ph.play', color="#fffafa"))
        self.startBtn.setIconSize(QSize(25, 25))
        self.resetItemsBtn.setIcon(qta.icon('mdi.restart', color="#fffafa"))
        self.resetItemsBtn.setIconSize(QSize(15, 15))
        self.githubBtn.setIcon(qta.icon('ph.github-logo', color="#fffafa"))
        self.githubBtn.setIconSize(QSize(25, 25))

        self.singleBtn.clicked.connect(self.onSingleBtnClicked)
        self.multipleBtn.clicked.connect(self.onBatchBtnClicked)
        self.folderBtn.clicked.connect(self.onFolderBtnClicked)
        self.outputDirBtn.clicked.connect(self.setOutputDirectory)
        self.startBtn.clicked.connect(self.onStartBtn)
        self.resetItemsBtn.clicked.connect(self.resetItems)
        self.githubBtn.clicked.connect(self.openGithubRepo)

        self.logBrowser.verticalScrollBar().setVisible(False)
        self.outputDirectory = None

        self.logger.log("Application started.")

    def updateLog(self, text):
        self.logger.log(text)

    def returnFileName(self, filepath):
        if os.path.isfile(filepath):
            return os.path.basename(filepath)
        else:
            return None

    def onSingleBtnClicked(self):
        self.filePath = QFileDialog.getOpenFileName(self, "Open Audio file", filter="Audio Files (*.mp3 *.wav)")
        if self.filePath[0] not in [None, ""]:
            self.updateLog(self.filePath[0])
            self.addSingleFileToQueue(self.filePath[0])

    def onBatchBtnClicked(self):
        self.filePaths = QFileDialog.getOpenFileNames(self, "Open Audio files", filter="Audio Files (*.mp3 *.wav)")
        if self.filePaths[0] not in [None, ""]:
            self.updateLog(self.filePaths[0])
            self.addMultipleFilesToQueue(self.filePaths[0])

    def onFolderBtnClicked(self):
        self.folderPath = QFileDialog.getExistingDirectory(self, "Open Audio folder")
        if self.folderPath not in [None, ""]:
            self.updateLog(self.folderPath)
            self.audioFiles = self.getAllAudioFilesFromFolder(self.folderPath)
            self.updateLog(self.audioFiles)
            self.addMultipleFilesToQueue(self.audioFiles)

    def getAllAudioFilesFromFolder(self, folderPath):
        audioFiles = []
        try:
            for root, dirs, files in os.walk(folderPath):
                for file in files:
                    if file.endswith(".mp3") or file.endswith(".wav"):
                        audioFiles.append(os.path.normpath(os.path.join(root, file)))
        except Exception as e:
            self.updateLog(e)
        return audioFiles

    def addSingleFileToQueue(self, filepath):
        itemQueue.put((filepath, 0))
        self.listModel._data.append((filepath, self.returnFileName(filepath), 0))
        self.listModel.layoutChanged.emit()

    def addMultipleFilesToQueue(self, filepaths):
        for filepath in filepaths:
            self.addSingleFileToQueue(filepath)
        self.listModel.layoutChanged.emit()

    def setOutputDirectory(self):
        self.outputDirectory = QFileDialog.getExistingDirectory(self, "Select output directory")
        self.updateLog(self.outputDirectory)

    def onStartBtn(self):
        global isReady
        isReady = True
        if itemQueue.qsize() > 0:
            self.worker = Worker(self.outputDirectory)
            self.worker.signals.setItemAsProcessingSignal.connect(self.setItemAsProcessing)
            self.worker.signals.setItemAsProcessedSignal.connect(self.setItemAsProcessed)
            self.worker.signals.loggingUpdateSignal.connect(self.updateLog)
            self.worker.signals.setProgressBarVisibilitySignal.connect(self.setProgressBarVisibility)
            self.worker.signals.setProgressBarValueSignal.connect(self.setProgressBarValue)
            self.worker.signals.setProgressBarFullValueSignal.connect(self.setProgressBarFullValue)
            self.worker.signals.setBtnEnableSignal.connect(self.setBtnEnable)
            self.threadpool.start(self.worker)
            self.startBtn.setEnabled(False)
            self.resetItemsBtn.setEnabled(False)
        else:
            self.updateLog("No items to process")
            self.dlg = QMessageBox(self)
            self.dlg.setText("No items to process")
            self.dlg.setIcon(QMessageBox.Warning)
            self.dlg.setWindowTitle("0 Items in Queue")
            self.dlg.setStandardButtons(QMessageBox.Ok)

            self.dlg.setStyleSheet(u"QMessageBox{\n"
                                   u"font: bold 14px;}\nQPushButton{\n"
                                   u"background-color: #ff8838;\n"
                                   u"color: #f6fcf2;font: bold;\n"
                                   u" min-width: 5em;\n"
                                   u" padding: 3px;\n"
                                   u"border:none;\n"
                                   u"border-radius:10px;\n"
                                   u"}")
            self.dlg.show()

    def setBtnEnable(self):
        self.startBtn.setEnabled(True)
        self.resetItemsBtn.setEnabled(True)

    def setItemAsProcessing(self, item):
        self.updateLog("Exporting " + item[0] + " to " + str(self.outputDirectory))
        _idx = self.listModel._data.index((item[0], self.returnFileName(item[0]), 0))
        self.listModel._data[_idx] = (item[0], self.returnFileName(item[0]), -1)
        self.listModel.layoutChanged.emit()

    def setItemAsProcessed(self, item):
        self.updateLog("Exported " + item[0] + " to " + str(self.outputDirectory))
        _idx = self.listModel._data.index((item[0], self.returnFileName(item[0]), -1))
        self.listModel._data[_idx] = (item[0], self.returnFileName(item[0]), 1)
        self.listModel.layoutChanged.emit()

    def setProgressBarVisibility(self, visibility):
        self.progressBar.setVisible(visibility)

    def setProgressBarValue(self, value):
        self.progressBar.setValue(value)

    def setProgressBarFullValue(self, value):
        self.progressBar.setMaximum(value)

    def resetItems(self):
        self.listModel._data = []
        with itemQueue.mutex:
            itemQueue.queue.clear()
        self.listModel.layoutChanged.emit()
        self.logBrowser.setText("-------------------Reset--------------------\n")

    def openGithubRepo(self):
        webbrowser.open('https://github.com/HemantKArya/Melodfy')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(window_logo_path))
    window = Main_UI()
    logger.flush_to_logger(window.logger)  # Flush buffered logs to the actual logger
    logger = window.logger  # Assign the actual logger instance to the global scope
    logger.log("Application initialized.")
    window.setWindowIcon(QIcon(window_logo_path))
    window.show()
    app.exec()