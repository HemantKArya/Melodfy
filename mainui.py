# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainuipJNucK.ui'
##
## Created by: Qt User Interface Compiler version 6.6.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QListView, QProgressBar, QPushButton, QSizePolicy,
    QSpacerItem, QTextBrowser, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(840, 597)
        font = QFont()
        font.setPointSize(10)
        Form.setFont(font)
        Form.setStyleSheet(u"\n"
"background-color: rgb(21, 21, 35);\n"
"color: #8e8fa5;\n"
"\n"
"")
        self.verticalLayout_2 = QVBoxLayout(Form)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.frame = QFrame(Form)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(0, 60))
        self.frame.setMaximumSize(QSize(16777215, 60))
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.frame)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(-1, 0, -1, 0)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.titleLabel = QLabel(self.frame)
        self.titleLabel.setObjectName(u"titleLabel")
        font1 = QFont()
        font1.setFamilies([u"Bahnschrift SemiLight Condensed"])
        font1.setPointSize(28)
        font1.setBold(True)
        font1.setStyleStrategy(QFont.PreferDefault)
        self.titleLabel.setFont(font1)
        self.titleLabel.setStyleSheet(u"color: #e7e7e7;")

        self.horizontalLayout_3.addWidget(self.titleLabel)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.progressBar = QProgressBar(self.frame)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setMinimumSize(QSize(200, 0))
        self.progressBar.setMaximumSize(QSize(300, 16777215))
        font2 = QFont()
        font2.setFamilies([u"Ubuntu Medium"])
        font2.setPointSize(10)
        font2.setBold(True)
        self.progressBar.setFont(font2)
        self.progressBar.setStyleSheet(u"QProgressBar {\n"
"                           background-color: #003126;\n"
"                           color: #7cffe4;\n"
"                           border-radius: 10px;\n"
"                          text-align: center; }\n"
"\n"
"                           QProgressBar::chunk {border-radius: 10px;\n"
"                           background-color: #01c370; }")
        self.progressBar.setValue(24)

        self.horizontalLayout_3.addWidget(self.progressBar)


        self.horizontalLayout_4.addLayout(self.horizontalLayout_3)


        self.verticalLayout.addWidget(self.frame)

        self.frame_2 = QFrame(Form)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(-1, -1, -1, 5)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.frame_3 = QFrame(self.frame_2)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(350, 0))
        self.frame_3.setStyleSheet(u"QFrame{background-color: #1d1e2c;\n"
"border:none;\n"
"border-radius:25px;\n"
"}")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.frame_3)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(5, 5, 5, 5)
        self.label_2 = QLabel(self.frame_3)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMaximumSize(QSize(16777215, 40))
        font3 = QFont()
        font3.setPointSize(11)
        self.label_2.setFont(font3)

        self.verticalLayout_5.addWidget(self.label_2)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.singleBtn = QPushButton(self.frame_3)
        self.singleBtn.setObjectName(u"singleBtn")
        self.singleBtn.setMinimumSize(QSize(0, 50))
        font4 = QFont()
        font4.setPointSize(10)
        font4.setBold(True)
        self.singleBtn.setFont(font4)
        self.singleBtn.setStyleSheet(u"QPushButton{\n"
"background-color: #00575e;\n"
"	color: #fcfdf6;\n"
"border:none;\n"
"border-radius:25px;\n"
"}")
        self.singleBtn.setFlat(False)

        self.horizontalLayout_5.addWidget(self.singleBtn)

        self.folderBtn = QPushButton(self.frame_3)
        self.folderBtn.setObjectName(u"folderBtn")
        self.folderBtn.setMinimumSize(QSize(0, 50))
        self.folderBtn.setFont(font4)
        self.folderBtn.setStyleSheet(u"QPushButton{\n"
"background-color: #00a0ac;\n"
"	color: #fef0f9;\n"
"border:none;\n"
"border-radius:25px;\n"
"}")

        self.horizontalLayout_5.addWidget(self.folderBtn)

        self.multipleBtn = QPushButton(self.frame_3)
        self.multipleBtn.setObjectName(u"multipleBtn")
        self.multipleBtn.setMinimumSize(QSize(0, 50))
        font5 = QFont()
        font5.setPointSize(9)
        font5.setBold(True)
        self.multipleBtn.setFont(font5)
        self.multipleBtn.setStyleSheet(u"QPushButton{\n"
"background-color: #0063f7;\n"
"	color: #fef0f9;\n"
"border:none;\n"
"border-radius:25px;\n"
"}")

        self.horizontalLayout_5.addWidget(self.multipleBtn)


        self.verticalLayout_5.addLayout(self.horizontalLayout_5)

        self.label_3 = QLabel(self.frame_3)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMaximumSize(QSize(16777215, 30))
        self.label_3.setFont(font3)

        self.verticalLayout_5.addWidget(self.label_3)

        self.outputDirBtn = QPushButton(self.frame_3)
        self.outputDirBtn.setObjectName(u"outputDirBtn")
        self.outputDirBtn.setMinimumSize(QSize(0, 45))
        font6 = QFont()
        font6.setFamilies([u"MS Shell Dlg 2"])
        font6.setPointSize(11)
        font6.setBold(True)
        self.outputDirBtn.setFont(font6)
        self.outputDirBtn.setStyleSheet(u"QPushButton{\n"
"background-color: #01c370;\n"
"color: #f6fcf2;\n"
"border:none;\n"
"border-radius:20px;\n"
"}")

        self.verticalLayout_5.addWidget(self.outputDirBtn)

        self.startBtn = QPushButton(self.frame_3)
        self.startBtn.setObjectName(u"startBtn")
        self.startBtn.setEnabled(True)
        self.startBtn.setMinimumSize(QSize(0, 45))
        font7 = QFont()
        font7.setPointSize(12)
        font7.setBold(True)
        self.startBtn.setFont(font7)
        self.startBtn.setAutoFillBackground(False)
        self.startBtn.setStyleSheet(u"QPushButton{\n"
"/*background-color: #ff3838;*/\n"
"background-color: none;\n"
"color: #fffafa;\n"
"border:2px solid white;\n"
"border-radius:20px;\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"\n"
"color: #d8d8d8;\n"
"border:2px solid #d8d8d8;\n"
"}")
        self.startBtn.setIconSize(QSize(70, 70))
        self.startBtn.setCheckable(False)
        self.startBtn.setAutoRepeat(False)
        self.startBtn.setAutoDefault(False)
        self.startBtn.setFlat(False)

        self.verticalLayout_5.addWidget(self.startBtn)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer)

        self.label_7 = QLabel(self.frame_3)
        self.label_7.setObjectName(u"label_7")
        font8 = QFont()
        font8.setPointSize(12)
        self.label_7.setFont(font8)

        self.verticalLayout_5.addWidget(self.label_7)

        self.githubBtn = QPushButton(self.frame_3)
        self.githubBtn.setObjectName(u"githubBtn")
        self.githubBtn.setMinimumSize(QSize(0, 30))
        self.githubBtn.setFont(font7)
        self.githubBtn.setStyleSheet(u"QPushButton{\n"
"\n"
"border:none;\n"
"}")

        self.verticalLayout_5.addWidget(self.githubBtn)

        self.label_6 = QLabel(self.frame_3)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font8)
        self.label_6.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.verticalLayout_5.addWidget(self.label_6)


        self.verticalLayout_6.addLayout(self.verticalLayout_5)


        self.horizontalLayout.addWidget(self.frame_3)

        self.frame_4 = QFrame(self.frame_2)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.frame_4)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(5, 0, 5, 0)
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.frame_5 = QFrame(self.frame_4)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setMinimumSize(QSize(0, 30))
        self.frame_5.setFrameShape(QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_7 = QHBoxLayout(self.frame_5)
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label = QLabel(self.frame_5)
        self.label.setObjectName(u"label")
        font9 = QFont()
        font9.setPointSize(11)
        font9.setBold(True)
        self.label.setFont(font9)

        self.horizontalLayout_6.addWidget(self.label)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_2)

        self.resetItemsBtn = QPushButton(self.frame_5)
        self.resetItemsBtn.setObjectName(u"resetItemsBtn")
        self.resetItemsBtn.setEnabled(True)
        self.resetItemsBtn.setMinimumSize(QSize(59, 24))
        self.resetItemsBtn.setFont(font4)
        self.resetItemsBtn.setStyleSheet(u"QPushButton{\n"
"background-color: #ff3838;\n"
"color: #f6fcf2;\n"
"border:none;\n"
"border-radius:10px;\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"\n"
"background-color: #dd2626;\n"
"color: #d6dcd2;\n"
"}")

        self.horizontalLayout_6.addWidget(self.resetItemsBtn)


        self.horizontalLayout_7.addLayout(self.horizontalLayout_6)


        self.verticalLayout_3.addWidget(self.frame_5)

        self.listQueue = QListView(self.frame_4)
        self.listQueue.setObjectName(u"listQueue")
        self.listQueue.setMinimumSize(QSize(300, 0))
        self.listQueue.setStyleSheet(u"QListView{background-color: #23243a;\n"
"border-radius:25px;\n"
"}\n"
"\n"
" QScrollBar:vertical\n"
"    {\n"
"        background-color: #2A2929;\n"
"        width: 15px;\n"
"        margin: 15px 3px 15px 3px;\n"
"        border: 1px transparent #2A2929;\n"
"        border-radius: 4px;\n"
"    }\n"
"\n"
"    QScrollBar::handle:vertical\n"
"    {\n"
"        background-color: #00d4ea;         /* #605F5F; */\n"
"        min-height: 5px;\n"
"        border-radius: 4px;\n"
"    }\n"
"\n"
"    QScrollBar::sub-line:vertical\n"
"    {\n"
"        margin: 3px 0px 3px 0px;\n"
"        border-image: url(:/qss_icons/rc/up_arrow_disabled.png);\n"
"        height: 10px;\n"
"        width: 10px;\n"
"        subcontrol-position: top;\n"
"        subcontrol-origin: margin;\n"
"    }\n"
"\n"
"    QScrollBar::add-line:vertical\n"
"    {\n"
"        margin: 3px 0px 3px 0px;\n"
"        border-image: url(:/qss_icons/rc/down_arrow_disabled.png);\n"
"        height: 10px;\n"
"        width: 10px;\n"
"        subcontrol-position: bo"
                        "ttom;\n"
"        subcontrol-origin: margin;\n"
"    }\n"
"\n"
"    QScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:vertical:on\n"
"    {\n"
"        border-image: url(:/qss_icons/rc/up_arrow.png);\n"
"        height: 10px;\n"
"        width: 10px;\n"
"        subcontrol-position: top;\n"
"        subcontrol-origin: margin;\n"
"    }\n"
"\n"
"    QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on\n"
"    {\n"
"        border-image: url(:/qss_icons/rc/down_arrow.png);\n"
"        height: 10px;\n"
"        width: 10px;\n"
"        subcontrol-position: bottom;\n"
"        subcontrol-origin: margin;\n"
"    }\n"
"\n"
"    QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical\n"
"    {\n"
"        background: none;\n"
"    }\n"
"\n"
"    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical\n"
"    {\n"
"        background: none;\n"
"    }")
        self.listQueue.setFrameShape(QFrame.NoFrame)
        self.listQueue.setFrameShadow(QFrame.Plain)
        self.listQueue.setLineWidth(3)
        self.listQueue.setViewMode(QListView.ListMode)

        self.verticalLayout_3.addWidget(self.listQueue)

        self.label_5 = QLabel(self.frame_4)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font7)

        self.verticalLayout_3.addWidget(self.label_5)

        self.logBrowser = QTextBrowser(self.frame_4)
        self.logBrowser.setObjectName(u"logBrowser")
        font10 = QFont()
        font10.setPointSize(11)
        font10.setBold(False)
        self.logBrowser.setFont(font10)
        self.logBrowser.setStyleSheet(u"QTextBrowser{background-color: #23243a;border-radius:25px;}\n"
"\n"
"\n"
"    QScrollBar:vertical\n"
"    {\n"
"        background-color: #2A2929;\n"
"        width: 15px;\n"
"        margin: 15px 3px 15px 3px;\n"
"        border: 1px transparent #2A2929;\n"
"        border-radius: 4px;\n"
"    }\n"
"\n"
"    QScrollBar::handle:vertical\n"
"    {\n"
"        background-color: #00d4ea;         /* #605F5F; */\n"
"        min-height: 5px;\n"
"        border-radius: 4px;\n"
"    }\n"
"\n"
"    QScrollBar::sub-line:vertical\n"
"    {\n"
"        margin: 3px 0px 3px 0px;\n"
"        border-image: url(:/qss_icons/rc/up_arrow_disabled.png);\n"
"        height: 10px;\n"
"        width: 10px;\n"
"        subcontrol-position: top;\n"
"        subcontrol-origin: margin;\n"
"    }\n"
"\n"
"    QScrollBar::add-line:vertical\n"
"    {\n"
"        margin: 3px 0px 3px 0px;\n"
"        border-image: url(:/qss_icons/rc/down_arrow_disabled.png);\n"
"        height: 10px;\n"
"        width: 10px;\n"
"        subcontrol-position: b"
                        "ottom;\n"
"        subcontrol-origin: margin;\n"
"    }\n"
"\n"
"    QScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:vertical:on\n"
"    {\n"
"        border-image: url(:/qss_icons/rc/up_arrow.png);\n"
"        height: 10px;\n"
"        width: 10px;\n"
"        subcontrol-position: top;\n"
"        subcontrol-origin: margin;\n"
"    }\n"
"\n"
"    QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on\n"
"    {\n"
"        border-image: url(:/qss_icons/rc/down_arrow.png);\n"
"        height: 10px;\n"
"        width: 10px;\n"
"        subcontrol-position: bottom;\n"
"        subcontrol-origin: margin;\n"
"    }\n"
"\n"
"    QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical\n"
"    {\n"
"        background: none;\n"
"    }\n"
"\n"
"    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical\n"
"    {\n"
"        background: none;\n"
"    }")
        self.logBrowser.setFrameShape(QFrame.NoFrame)
        self.logBrowser.setFrameShadow(QFrame.Plain)
        self.logBrowser.setLineWidth(3)

        self.verticalLayout_3.addWidget(self.logBrowser)


        self.verticalLayout_4.addLayout(self.verticalLayout_3)


        self.horizontalLayout.addWidget(self.frame_4)


        self.horizontalLayout_2.addLayout(self.horizontalLayout)


        self.verticalLayout.addWidget(self.frame_2)


        self.verticalLayout_2.addLayout(self.verticalLayout)


        self.retranslateUi(Form)

        self.startBtn.setDefault(False)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.titleLabel.setText(QCoreApplication.translate("Form", u"Audio2Midi", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Import audio files", None))
        self.singleBtn.setText(QCoreApplication.translate("Form", u"Single file", None))
        self.folderBtn.setText(QCoreApplication.translate("Form", u"Folder", None))
        self.multipleBtn.setText(QCoreApplication.translate("Form", u"Multiple", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"Set output directory where file will be saved", None))
        self.outputDirBtn.setText(QCoreApplication.translate("Form", u"Set Output Directory", None))
        self.startBtn.setText(QCoreApplication.translate("Form", u"Export to MIDI", None))
        self.label_7.setText(QCoreApplication.translate("Form", u"Bug report(or Feature request)", None))
        self.githubBtn.setText(QCoreApplication.translate("Form", u"Github", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"By @iamhemantindia", None))
        self.label.setText(QCoreApplication.translate("Form", u"Queue", None))
        self.resetItemsBtn.setText(QCoreApplication.translate("Form", u"Reset", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"Log", None))
        self.logBrowser.setHtml(QCoreApplication.translate("Form", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
    # retranslateUi

