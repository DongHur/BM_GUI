import numpy as np
import sqlite3
import sys

from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia, QtMultimediaWidgets

from PyQt5.QtCore import QRect, Qt, QMetaObject, QTimer, QDir, QUrl, QCoreApplication, QObject, pyqtSignal, QThread, pyqtSlot
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QSlider, QPushButton, QLabel, 
QFrame, QLineEdit, QComboBox, QMenuBar, QStatusBar, QAction, QFileDialog, QMenu)
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaMetaData
from PyQt5.QtMultimediaWidgets import QVideoWidget

from widgets.tsne_Graph import tsne_Graph
from widgets.BP_Graph import BP_Graph
from widgets.density_Graph import density_Graph
from widgets.behaviorTableWidget import behaviorTableWidget
from widgets.saveBehaviorWidget import saveBehaviorWidget

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

class Worker(QObject):
    play = pyqtSignal()
    pause = pyqtSignal()
    def __init__(self,*args, **kwargs):
        super(Worker, self).__init__()

    @pyqtSlot()
    def worker_play(self):
        self.play.emit()
    @pyqtSlot()
    def worker_pause(self):
        self.pause.emit()

class Ui_MainWindow(object):
    def __init__(self, *args, **kwargs):
        super(Ui_MainWindow, self).__init__()
        self.fr = 50
        self.con = None

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1438, 811)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.horizontalLayoutWidget_2 = QWidget(self.centralwidget)
        self.horizontalLayoutWidget_2.setGeometry(QRect(10, 10, 341, 311))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")

        self.horizontalLayout_1 = QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_1.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_1.setObjectName("horizontalLayout_1")

        self.horizontalSlider = QSlider(self.centralwidget)
        self.horizontalSlider.setGeometry(QRect(20, 330, 1401, 22))
        self.horizontalSlider.setOrientation(Qt.Horizontal)
        self.horizontalSlider.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.horizontalSlider.setObjectName("horizontalSlider")

        self.playButton = QPushButton(self.centralwidget)
        self.playButton.setGeometry(QRect(10, 360, 113, 32))
        self.playButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.playButton.setObjectName("playButton")

        self.FrameLabel = QLabel(self.centralwidget)
        self.FrameLabel.setGeometry(QRect(260, 365, 60, 16))
        self.FrameLabel.setObjectName("FrameLabel")

        self.FrameNumberLineEdit = QLineEdit(self.centralwidget)
        self.FrameNumberLineEdit.setGeometry(QRect(310, 365, 91, 21))
        self.FrameNumberLineEdit.setObjectName("FrameNumberLineEdit")
        self.FrameNumberLineEdit.setFocusPolicy(Qt.ClickFocus)

        self.frameBackButton = QPushButton(self.centralwidget)
        self.frameBackButton.setGeometry(QRect(410, 360, 50, 32))
        self.frameBackButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.frameBackButton.setObjectName("frameBackButton")
        self.frameFrontButton = QPushButton(self.centralwidget)
        self.frameFrontButton.setGeometry(QRect(460, 360, 50, 32))
        self.frameFrontButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.frameFrontButton.setObjectName("frameFrontButton")
        self.frameFrontButton.clicked.connect(self.key_right)
        self.frameBackButton.clicked.connect(self.key_left)

        self.horizontalLayoutWidget_3 = QWidget(self.centralwidget)
        self.horizontalLayoutWidget_3.setGeometry(QRect(370, 10, 341, 311))
        self.horizontalLayoutWidget_3.setObjectName("horizontalLayoutWidget_3")

        self.horizontalLayout_2 = QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayoutWidget_4 = QWidget(self.centralwidget)
        self.horizontalLayoutWidget_4.setGeometry(QRect(730, 10, 341, 311))
        self.horizontalLayoutWidget_4.setObjectName("horizontalLayoutWidget_4")
        self.horizontalLayout_3 = QHBoxLayout(self.horizontalLayoutWidget_4)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayoutWidget_5 = QWidget(self.centralwidget)
        self.horizontalLayoutWidget_5.setGeometry(QRect(1090, 10, 341, 311))
        self.horizontalLayoutWidget_5.setObjectName("horizontalLayoutWidget_5")
        self.horizontalLayout_4 = QHBoxLayout(self.horizontalLayoutWidget_5)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")

        self.stopButton = QPushButton(self.centralwidget)
        self.stopButton.setGeometry(QRect(130, 360, 113, 32))
        self.stopButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.stopButton.setObjectName("stopButton")

        ########################
        self.frame = QFrame(self.centralwidget)
        self.frame.setGeometry(QRect(30, 420, 370, 71))
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.frame.setObjectName("frame")

        self.addBehaviorLabel = QLabel(self.frame)
        self.addBehaviorLabel.setGeometry(QRect(10, 30, 60, 16))
        self.addBehaviorLabel.setObjectName("addBehaviorLabel")

        self.addBehaviorLineEdit = QLineEdit(self.frame)
        self.addBehaviorLineEdit.setGeometry(QRect(80, 30, 171, 21))
        self.addBehaviorLineEdit.setObjectName("addBehaviorLineEdit")
        self.addBehaviorLineEdit.setFocusPolicy(Qt.ClickFocus)

        self.addBehaviorButton = QPushButton(self.frame)
        self.addBehaviorButton.setGeometry(QRect(250, 20, 113, 41))
        self.addBehaviorButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.addBehaviorButton.setObjectName("addBehaviorButton")
        
        ##########################
        self.editBehaviorFrame = QFrame(self.centralwidget)
        self.editBehaviorFrame.setGeometry(QRect(450, 420, 531, 71))
        self.editBehaviorFrame.setFrameShape(QFrame.StyledPanel)
        self.editBehaviorFrame.setFrameShadow(QFrame.Raised)
        self.editBehaviorFrame.setObjectName("editBehaviorFrame")

        self.editBehaviorLabel = QLabel(self.editBehaviorFrame)
        self.editBehaviorLabel.setGeometry(QtCore.QRect(70, 10, 69, 16))
        self.editBehaviorLabel.setObjectName("editBehaviorLabel")

        self.editBehaviorFrLabel = QLabel(self.editBehaviorFrame)
        self.editBehaviorFrLabel.setGeometry(QtCore.QRect(260, 10, 101, 16))
        self.editBehaviorFrLabel.setObjectName("editBehaviorFrLabel")

        self.dashLabel = QLabel(self.editBehaviorFrame)
        self.dashLabel.setGeometry(QtCore.QRect(300, 30, 16, 16))
        self.dashLabel.setObjectName("dashLabel")

        self.editBehaviorStartBox = QLineEdit(self.editBehaviorFrame)
        self.editBehaviorStartBox.setGeometry(QtCore.QRect(230, 30, 61, 21))
        self.editBehaviorStartBox.setText("")
        self.editBehaviorStartBox.setObjectName("editBehaviorStartBox")
        self.editBehaviorStartBox.setFocusPolicy(Qt.ClickFocus)

        self.editBehaviorStopBox = QLineEdit(self.editBehaviorFrame)
        self.editBehaviorStopBox.setGeometry(QtCore.QRect(320, 30, 61, 21))
        self.editBehaviorStopBox.setText("")
        self.editBehaviorStopBox.setObjectName("editBehaviorStopBox")
        self.editBehaviorStopBox.setFocusPolicy(Qt.ClickFocus)

        self.editBehaviorEnterButton = QPushButton(self.editBehaviorFrame)
        self.editBehaviorEnterButton.setGeometry(QtCore.QRect(400, 20, 113, 41))
        self.editBehaviorEnterButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.editBehaviorEnterButton.setObjectName("editBehaviorEnterButton")

        self.editBehaviorComboBox = QComboBox(self.editBehaviorFrame)
        self.editBehaviorComboBox.setGeometry(QtCore.QRect(10, 30, 210, 26))
        self.editBehaviorComboBox.setCursor(QCursor(Qt.PointingHandCursor))
        self.editBehaviorComboBox.setObjectName("editBehaviorComboBox")

        ##########
        self.divider1 = QFrame(self.centralwidget)
        self.divider1.setGeometry(QRect(10, 390, 1421, 20))
        self.divider1.setFrameShape(QFrame.HLine)
        self.divider1.setFrameShadow(QFrame.Sunken)
        self.divider1.setObjectName("divider1")

        self.divider2 = QFrame(self.centralwidget)
        self.divider2.setGeometry(QRect(10, 500, 971, 20))
        self.divider2.setFrameShape(QFrame.HLine)
        self.divider2.setFrameShadow(QFrame.Sunken)
        self.divider2.setObjectName("divider2")

        #********  Save Widget  **********
        self.saveLayoutWidget = QWidget(self.centralwidget)
        self.saveLayoutWidget.setGeometry(QRect(5, 530, 1000, 400))
        self.saveLayoutWidget.setObjectName("saveLayoutWidget")
        self.saveHorizWidget = QHBoxLayout(self.saveLayoutWidget)
        self.saveHorizWidget.setContentsMargins(0, 0, 0, 0)
        self.saveHorizWidget.setObjectName("saveHorizWidget")
        self.saveBehaviorWidget = saveBehaviorWidget()
        self.saveHorizWidget.addWidget(self.saveBehaviorWidget)
        #******************

        self.horizontalLayoutWidget = QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QRect(990, 420, 431, 341))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")

        self.horizontalLayoutWidget_7 = QWidget(self.centralwidget)
        self.horizontalLayoutWidget_7.setGeometry(QRect(690, 530, 280, 230))
        self.horizontalLayoutWidget_7.setObjectName("horizontalLayoutWidget_7")

        self.totalBehaviorLayout = QHBoxLayout(self.horizontalLayoutWidget_7)
        self.totalBehaviorLayout.setContentsMargins(0, 0, 0, 0)
        self.totalBehaviorLayout.setObjectName("totalBehaviorLayout")
        
        self.horizontalLayoutWidget = QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QRect(990, 420, 431, 341))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.tableLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.tableLayout.setContentsMargins(0, 0, 0, 0)
        self.tableLayout.setObjectName("tableLayout")

        self.behaviorTable = behaviorTableWidget()
        self.tableLayout.addWidget(self.behaviorTable)

        # Menu Bar
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setGeometry(QRect(0, 0, 1438, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        # Upload Data
        self.uploadDataOpen = QAction(MainWindow)
        self.uploadDataOpen.setObjectName("uploadDataOpen")
        self.menuFile.addAction(self.uploadDataOpen)
        self.uploadDataOpen.triggered.connect(self.uploadData)
        # Open Tab
        self.actionOpen = QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.menuFile.addAction(self.actionOpen)
        self.actionOpen.triggered.connect(self.openFile)
        # Append Action
        self.menubar.addAction(self.menuFile.menuAction())

        # Create Media Player
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        videoWidget = QVideoWidget()
        self.horizontalLayout_1.addWidget(videoWidget)
        self.mediaPlayer.setVideoOutput(videoWidget)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.setNotifyInterval(int(1000/self.fr))
        self.mediaPlayer.setPlaybackRate(0.3)

        # Append BP graph
        self.BPGraph = BP_Graph()
        self.BPcanvas = FigureCanvas(self.BPGraph)
        self.BPGraph.init_plot()
        self.horizontalLayout_2.addWidget(self.BPcanvas)

        # Append tSNE graph
        self.tsneGraph = tsne_Graph()
        self.tsnecanvas = FigureCanvas(self.tsneGraph)
        self.tsneGraph.init_plot()
        self.horizontalLayout_3.addWidget(self.tsnecanvas)

        # Append individual density graph
        self.indDensityGraph = density_Graph()
        self.indDensitycanvas = FigureCanvas(self.indDensityGraph)
        self.indDensityGraph.init_plot(title='Individual Density Plot')
        self.horizontalLayout_4.addWidget(self.indDensitycanvas)

        # Append total density graph
        self.densityGraph = density_Graph()
        self.densitycanvas = FigureCanvas(self.densityGraph)
        self.densityGraph.init_plot(title='Total Density Plot')
        self.totalBehaviorLayout.addWidget(self.densitycanvas)

        # connect lineedit
        self.addBehaviorLineEdit.returnPressed.connect(self.addBehavior)
        self.editBehaviorStopBox.returnPressed.connect(self.editBehavior)

        # create worker
        self.worker = Worker()
        self.thread = QThread()
        self.thread.start()
        self.worker.moveToThread(self.thread)
        self.worker.play.connect(self.play)
        self.worker.pause.connect(self.pause)
        # connect button
        self.playButton.pressed.connect(self.worker.worker_play)
        self.stopButton.clicked.connect(self.worker.worker_pause)
        self.addBehaviorButton.clicked.connect(self.addBehavior)
        self.editBehaviorEnterButton.clicked.connect(self.editBehavior)

        # connect slider
        self.horizontalSlider.sliderMoved.connect(self.setPosition)

        # connect keys
        self.shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Alt+Left"), self.centralwidget, self.key_left)
        self.shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Alt+Right"), self.centralwidget, self.key_right)

        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.playButton.setText(_translate("MainWindow", "Play"))
        self.stopButton.setText(_translate("MainWindow", "Stop"))
        self.frameBackButton.setText(_translate("MainWindow", "<"))
        self.frameFrontButton.setText(_translate("MainWindow", ">"))
        self.editBehaviorLabel.setText(_translate("MainWindow", "Behavior"))
        self.editBehaviorFrLabel.setText(_translate("MainWindow", "Frame Range"))
        self.dashLabel.setText(_translate("MainWindow", "-"))
        self.editBehaviorEnterButton.setText(_translate("MainWindow", "Enter"))
        self.addBehaviorLabel.setText(_translate("MainWindow", "Behavior:"))
        self.addBehaviorButton.setText(_translate("MainWindow", "Add"))
        self.FrameLabel.setText(_translate("MainWindow", "Frame: "))
        # menubar text
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionOpen.setText(_translate("MainWindow", "Open Video"))
        self.uploadDataOpen.setText(_translate("MainWindow", "Upload Data"))
        
    def uploadData(self):
        filepath, _ = QFileDialog.getOpenFileName(None, "Upload Data", 
            QDir.homePath(), "SQL Data (*.db)")
        print(filepath)
        if filepath:
            self.con = sqlite3.connect(filepath)
            cur = self.con.cursor()
            cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
            beh_list = np.array(cur.fetchall()).flatten()
            print("BEHAVIORS: ", beh_list)
            # Populate editBehavior Dropdown
            self.editBehaviorComboBox.clear()
            self.editBehaviorComboBox.addItems(beh_list)
            # Populate behavior table
            self.behaviorTable.connect_data(self.con)
            self.behaviorTable.update_all_table()
            # Populate behavior widget
            self.saveBehaviorWidget.connect_data(self.con)
            self.saveBehaviorWidget.update_beh_list()
        else:
            print('FILE DOES NOT EXIST')
        pass
    def openFile(self):
        folder = QFileDialog.getExistingDirectory(
            None, "Select Directory", QDir.homePath())
        if folder != '':
            filename = folder.split('/')[-1]
            # total density plot
            self.densityGraph.set_newfile(folder+'/total_map.fig')
            self.densitycanvas.draw()
            # individual density plot
            self.indDensityGraph.set_newfile(folder+'/indiv_mat.fig')
            self.indDensitycanvas.draw()
            # set the dimension of tsne based on density plot
            self.tsneGraph.set_dim(xlim=self.indDensityGraph.XLim, ylim=self.indDensityGraph.YLim)
            # body point graph
            self.BPGraph.set_newfile(folder+'/BP_'+filename+'.npy')
            self.BPGraph.update_graph(position=1)
            self.BPcanvas.draw()
            # tsne graph
            self.tsneGraph.set_newfile(folder+'/EMBED.mat')
            self.tsneGraph.update_graph(position=1)
            self.tsnecanvas.draw()
            # media player
            self.mediaPlayer.setMedia(QMediaContent(
                QUrl.fromLocalFile(folder+'/'+filename+'.avi')))
            # behavior table
            self.behaviorTable.set_newfile(folder+'/EMBED.mat')

    def play(self):
        self.mediaPlayer.play()
    def pause(self):
        self.mediaPlayer.pause()
        frame = int(1.0*self.mediaPlayer.position()*self.fr/1000)
        self.FrameNumberLineEdit.setText(str(frame))
        self.FrameNumberLineEdit.repaint()
    def positionChanged(self, position):
        self.horizontalSlider.setValue(position)
        self.BPGraph.update_graph(position)
        self.BPcanvas.draw()
        self.tsneGraph.update_graph(position)
        self.tsnecanvas.draw()
    def durationChanged(self, duration):
        self.horizontalSlider.setRange(0, duration)
        self.BPGraph.set_duration(duration)
        self.tsneGraph.set_duration(duration)
    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)
        self.FrameNumberLineEdit.setText(str(int(1.0*position*self.fr/1000)))
        self.FrameNumberLineEdit.repaint()
    def addBehavior(self):
        newBehText = self.addBehaviorLineEdit.text()
        if newBehText: 
            self.addBehaviorLineEdit.clear()
            self.editBehaviorComboBox.addItem(newBehText)
            self.addBehaviorLineEdit.repaint()

    def editBehavior(self):
        behavior = self.editBehaviorComboBox.currentText()
        startFr = self.editBehaviorStartBox.text()
        stopFr = self.editBehaviorStopBox.text()
        self.editBehaviorStartBox.clear()
        self.editBehaviorStopBox.clear()
        self.editBehaviorStartBox.repaint()
        self.editBehaviorStopBox.repaint()
        if behavior and startFr and stopFr:
            self.behaviorTable.add_row(behavior, startFr, stopFr)
        # update save behavior widget
        self.saveBehaviorWidget.update_beh_list()

    def key_left(self):
        # move back one frame
        self.setPosition(self.mediaPlayer.position()-1000/self.fr)
    def key_right(self):
        # move forward one frame
        self.setPosition(self.mediaPlayer.position()+1000/self.fr)




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
