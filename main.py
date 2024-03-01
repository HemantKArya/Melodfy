from PySide6.QtWidgets import QApplication, QWidget,QFileDialog,QMessageBox
from PySide6.QtCore import QAbstractListModel,Qt,QThreadPool,QRunnable,Slot,Signal,QObject,QSize
from PySide6.QtGui import QTextOption

from inference import PianoTranscription
from utilities import load_audio
from config import sample_rate
from mainui import Ui_Form
import sys
import onnxruntime
import os
import numpy as np
import qtawesome as qta
from threading import Thread
from queue import Queue
import time



itemQueue = Queue()
isReady = False



print('Loading model...')
ort_session = onnxruntime.InferenceSession("./models/model.onnx")
c = PianoTranscription(model=ort_session.run,device='cpu')
print('Model loaded')

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

class Worker(QRunnable,):
    def __init__(self, outputDirectory=None):
        super(Worker, self).__init__()
        self.signals = WorkerSignals()
        self.outputDirectory = outputDirectory
    
    def logUpdate(self,text):
        self.signals.loggingUpdateSignal.emit(str(text))
    
    def setProgressBarVisibility(self,visibility):
        self.signals.setProgressBarVisibilitySignal.emit(visibility)
    
    def setProgressBarValue(self,value):
        self.signals.setProgressBarValueSignal.emit(value)
    
    def setProgressBarFullValue(self,value):
        self.signals.setProgressBarFullValueSignal.emit(value)
    
    @Slot()
    def run(self):
        global isReady
        while isReady:
            _item = itemQueue.get()
            self.signals.setItemAsProcessingSignal.emit(_item)
            basename = os.path.basename(_item[0]).split(".")[0] + '.mid'
            self.outputDirectory2 = self.outputDirectory if self.outputDirectory not in [None,""] else getDirectoryPathFromFilePath(_item[0])
            self.outputDirectory2 = os.path.abspath(os.path.join(self.outputDirectory2,basename))
            audio, _ = load_audio(_item[0], sr=sample_rate, mono=True)

            c.transcribe(audio,self.outputDirectory2,
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
            if self._data[index.row()][2]==1:
                return qta.icon('fa5s.check-circle',color="#00ff00")
            elif self._data[index.row()][2]==-1:
                return qta.icon('fa5s.hourglass-half',color="#ffff00")
            return qta.icon('fa5s.music',color="#fffafa")

    def rowCount(self, index):
        return len(self._data)

class Main_UI(QWidget, Ui_Form):
    def __init__(self):
        super(Main_UI, self).__init__()
        self.setupUi(self)
        
        
        self.threadpool = QThreadPool()
        # self.logBrowser.setWordWrapMode()
        # print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())
        self.progressBar.setVisible(False)
        # self.progressBar.setMinimum(1)
        self.logBrowser.setText("")
        self.listModel = ListModel()
        self.listQueue.setModel(self.listModel)
        self.singleBtn.setIcon(qta.icon('mdi.music-box',color="#fffafa"))
        self.singleBtn.setIconSize(QSize(25,25))
        self.multipleBtn.setIcon(qta.icon('mdi.music-box-multiple',color="#fffafa"))
        self.multipleBtn.setIconSize(QSize(25,25))
        self.folderBtn.setIcon(qta.icon('mdi.folder-music',color="#fffafa"))
        self.folderBtn.setIconSize(QSize(25,25))
        self.outputDirBtn.setIcon(qta.icon('mdi.folder',color="#fffafa"))
        self.outputDirBtn.setIconSize(QSize(25,25))
        self.startBtn.setIcon(qta.icon('ph.play',color="#fffafa"))
        self.startBtn.setIconSize(QSize(25,25))
        self.resetItemsBtn.setIcon(qta.icon('mdi.restart',color="#fffafa"))
        self.resetItemsBtn.setIconSize(QSize(15,15))
        self.githubBtn.setIcon(qta.icon('ph.github-logo',color="#fffafa"))
        self.githubBtn.setIconSize(QSize(25,25))


        self.singleBtn.clicked.connect(self.onSingleBtnClicked)
        self.multipleBtn.clicked.connect(self.onBatchBtnClicked)
        self.folderBtn.clicked.connect(self.onFolderBtnClicked)
        self.outputDirBtn.clicked.connect(self.setOutputDirectory)
        self.startBtn.clicked.connect(self.onStartBtn)
        self.resetItemsBtn.clicked.connect(self.resetItems)
        
    

        self.logBrowser.verticalScrollBar().setVisible(False)
        self.outputDirectory = None
        
    def updateLog(self,text):
        self.logBrowser.setText(self.logBrowser.toPlainText()+"     "+str(text)+"\n")
        self.logBrowser.verticalScrollBar().setValue(self.logBrowser.verticalScrollBar().maximum())
    
    def returnFileName(self,filepath):
        if os.path.isfile(filepath):
            return os.path.basename(filepath)
        else:
            return None

    def onSingleBtnClicked(self):
        self.filePath = QFileDialog.getOpenFileName(self,"Open Audio file", filter="Audio Files (*.mp3 *.wav)")
        if self.filePath[0] not in [None,""]:
            self.updateLog(self.filePath[0])
            self.addSingleFileToQueue(self.filePath[0])
    def onBatchBtnClicked(self):
        self.filePaths = QFileDialog.getOpenFileNames(self,"Open Audio files", filter="Audio Files (*.mp3 *.wav)")
        if self.filePaths[0] not in [None,""]:
            self.updateLog(self.filePaths[0])
            self.addMultipleFilesToQueue(self.filePaths[0])
    def onFolderBtnClicked(self):
        self.folderPath = QFileDialog.getExistingDirectory(self,"Open Audio folder")
        if self.folderPath not in [None,""]:
            self.updateLog(self.folderPath)
            self.audioFiles = self.getAllAudioFilesFromFolder(self.folderPath)
            self.updateLog(self.audioFiles)
            self.addMultipleFilesToQueue(self.audioFiles)
    def getAllAudioFilesFromFolder(self,folderPath):
        audioFiles = []
        try:
            for root, dirs, files in os.walk(folderPath):
                for file in files:
                    if file.endswith(".mp3") or file.endswith(".wav"):
                        audioFiles.append(os.path.normpath(os.path.join(root, file)))
        except Exception as e:
            self.updateLog(e)
        return audioFiles
    def addSingleFileToQueue(self,filepath):
        itemQueue.put((filepath,0))
        self.listModel._data.append((filepath,self.returnFileName(filepath),0))
        self.listModel.layoutChanged.emit()
    def addMultipleFilesToQueue(self,filepaths):
        for filepath in filepaths:
            self.addSingleFileToQueue(filepath)
        self.listModel.layoutChanged.emit()
    def setOutputDirectory(self):
        self.outputDirectory = QFileDialog.getExistingDirectory(self,"Select output directory")
        self.updateLog(self.outputDirectory)
    
    def onStartBtn(self):
        global isReady
        isReady = True
        if itemQueue.qsize()>0:
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
                "font: bold 14px;}\nQPushButton{\n"
"background-color: #ff8838;\n"
"color: #f6fcf2;font: bold;\n"
" min-width: 5em;\n"
" padding: 3px;\n"
"border:none;\n"
"border-radius:10px;\n"
"}")
            self.dlg.show()

    def setBtnEnable(self):
        self.startBtn.setEnabled(True)
        self.resetItemsBtn.setEnabled(True)
    
    def setItemAsProcessing(self,item):
        self.updateLog("Exporting "+item[0]+" to "+str(self.outputDirectory))
        _idx = self.listModel._data.index((item[0],self.returnFileName(item[0]),0))
        self.listModel._data[_idx] = (item[0],self.returnFileName(item[0]),-1)
        self.listModel.layoutChanged.emit()

    def setItemAsProcessed(self,item):
        self.updateLog("Exported "+item[0]+" to "+str(self.outputDirectory))
        _idx = self.listModel._data.index((item[0],self.returnFileName(item[0]),-1))
        self.listModel._data[_idx] = (item[0],self.returnFileName(item[0]),1)
        self.listModel.layoutChanged.emit()
    
    def setProgressBarVisibility(self,visibility):
        self.progressBar.setVisible(visibility)
    
    def setProgressBarValue(self,value):
        self.progressBar.setValue(value)

    def setProgressBarFullValue(self,value):
        self.progressBar.setMaximum(value)

    def resetItems(self):
        self.listModel._data = []
        with itemQueue.mutex:
            itemQueue.queue.clear()
        self.listModel.layoutChanged.emit()
        self.logBrowser.setText("x=x=x=x=x=x=x=Reset=x=x=x=x=x=x=x\n")



app = QApplication(sys.argv)
window = Main_UI()
window.show()
app.exec()