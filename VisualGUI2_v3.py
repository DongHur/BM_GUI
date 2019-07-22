from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia, QtMultimediaWidgets

from PyQt5.QtCore import QRect, Qt, QMetaObject, QTimer, QDir, QUrl
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QSlider, QPushButton, QLabel, QLCDNumber, 
QFrame, QLineEdit, QComboBox, QMenuBar, QStatusBar, QAction, QFileDialog, QMenu)
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget

from widgets.tsne_Graph import tsne_Graph
from widgets.BP_Graph import BP_Graph
from widgets.density_Graph import density_Graph
from widgets.behaviorTableWidget import behaviorTableWidget

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

class Ui_MainWindow(object):
    def __init__(self, *args, **kwargs):
        super(Ui_MainWindow, self).__init__()
        self.filepath = ''
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
        self.FrameLabel.setGeometry(QRect(260, 370, 60, 16))
        self.FrameLabel.setObjectName("FrameLabel")

        self.FramelcdNumber = QLCDNumber(self.centralwidget)
        self.FramelcdNumber.setGeometry(QRect(310, 362, 91, 31))
        self.FramelcdNumber.setObjectName("FramelcdNumber")

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

        self.editBehaviorLabel = QLabel(self.centralwidget)
        self.editBehaviorLabel.setGeometry(QRect(540, 430, 69, 16))
        self.editBehaviorLabel.setObjectName("editBehaviorLabel")

        self.editBehaviorFrLabel = QLabel(self.centralwidget)
        self.editBehaviorFrLabel.setGeometry(QRect(720, 430, 101, 16))
        self.editBehaviorFrLabel.setObjectName("editBehaviorFrLabel")

        self.divider1 = QFrame(self.centralwidget)
        self.divider1.setGeometry(QRect(10, 390, 1421, 20))
        self.divider1.setFrameShape(QFrame.HLine)
        self.divider1.setFrameShadow(QFrame.Sunken)
        self.divider1.setObjectName("divider1")

        self.dashLabel = QLabel(self.centralwidget)
        self.dashLabel.setGeometry(QRect(750, 450, 16, 16))
        self.dashLabel.setObjectName("dashLabel")

        self.editBehaviorStartBox = QLineEdit(self.centralwidget)
        self.editBehaviorStartBox.setGeometry(QRect(680, 450, 61, 21))
        self.editBehaviorStartBox.setText("")
        self.editBehaviorStartBox.setObjectName("editBehaviorStartBox")
        self.editBehaviorStartBox.setFocusPolicy(Qt.ClickFocus)

        self.editBehaviorStopBox = QLineEdit(self.centralwidget)
        self.editBehaviorStopBox.setGeometry(QRect(770, 450, 61, 21))
        self.editBehaviorStopBox.setText("")
        self.editBehaviorStopBox.setObjectName("editBehaviorStopBox")
        self.editBehaviorStopBox.setFocusPolicy(Qt.ClickFocus)

        self.editBehaviorEnterButton = QPushButton(self.centralwidget)
        self.editBehaviorEnterButton.setGeometry(QRect(850, 440, 113, 41))
        self.editBehaviorEnterButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.editBehaviorEnterButton.setObjectName("editBehaviorEnterButton")

        self.editBehaviorComboBox = QComboBox(self.centralwidget)
        self.editBehaviorComboBox.setGeometry(QRect(460, 450, 210, 26))
        self.editBehaviorComboBox.setCursor(QCursor(Qt.PointingHandCursor))
        self.editBehaviorComboBox.setObjectName("editBehaviorComboBox")

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

        self.editBehaviorFrame = QFrame(self.centralwidget)
        self.editBehaviorFrame.setGeometry(QRect(450, 420, 531, 71))
        self.editBehaviorFrame.setFrameShape(QFrame.StyledPanel)
        self.editBehaviorFrame.setFrameShadow(QFrame.Raised)
        self.editBehaviorFrame.setObjectName("editBehaviorFrame")

        self.divider2 = QFrame(self.centralwidget)
        self.divider2.setGeometry(QRect(10, 500, 971, 20))
        self.divider2.setFrameShape(QFrame.HLine)
        self.divider2.setFrameShadow(QFrame.Sunken)
        self.divider2.setObjectName("divider2")

        self.savedBehaviorLabel = QLabel(self.centralwidget)
        self.savedBehaviorLabel.setGeometry(QRect(70, 530, 101, 16))
        self.savedBehaviorLabel.setObjectName("savedBehaviorLabel")

        self.savedBehaviorComboBox = QComboBox(self.centralwidget)
        self.savedBehaviorComboBox.setGeometry(QRect(10, 550, 211, 26))
        self.savedBehaviorComboBox.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.savedBehaviorComboBox.setObjectName("savedBehaviorComboBox")

        self.savedBehaviorEntryLabel = QLabel(self.centralwidget)
        self.savedBehaviorEntryLabel.setGeometry(QRect(290, 530, 60, 16))
        self.savedBehaviorEntryLabel.setObjectName("savedBehaviorEntryLabel")

        self.horizontalLayoutWidget_6 = QWidget(self.centralwidget)
        self.horizontalLayoutWidget_6.setGeometry(QRect(400, 530, 271, 231))
        self.horizontalLayoutWidget_6.setObjectName("horizontalLayoutWidget_6")

        self.saveFilenameVideoLayout = QHBoxLayout(self.horizontalLayoutWidget_6)
        self.saveFilenameVideoLayout.setContentsMargins(0, 0, 0, 0)
        self.saveFilenameVideoLayout.setObjectName("saveFilenameVideoLayout")

        self.saveFilenameButton = QPushButton(self.centralwidget)
        self.saveFilenameButton.setGeometry(QRect(260, 690, 111, 41))
        self.saveFilenameButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.saveFilenameButton.setObjectName("saveFilenameButton")

        self.saveFilenameBox = QLineEdit(self.centralwidget)
        self.saveFilenameBox.setGeometry(QRect(10, 700, 241, 21))
        self.saveFilenameBox.setObjectName("saveFilenameBox")
        self.saveFilenameBox.setFocusPolicy(Qt.ClickFocus)

        self.saveFilenameLabel = QLabel(self.centralwidget)
        self.saveFilenameLabel.setGeometry(QRect(20, 680, 231, 16))
        self.saveFilenameLabel.setAlignment(Qt.AlignCenter)
        self.saveFilenameLabel.setObjectName("saveFilenameLabel")

        self.horizontalLayoutWidget = QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QRect(990, 420, 431, 341))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")

        self.FrameLabel = QLabel(self.centralwidget)
        self.FrameLabel.setGeometry(QRect(260, 370, 60, 16))
        self.FrameLabel.setObjectName("FrameLabel")

        self.FramelcdNumber = QLCDNumber(self.centralwidget)
        self.FramelcdNumber.setGeometry(QRect(310, 362, 91, 31))
        self.FramelcdNumber.setObjectName("FramelcdNumber")

        self.horizontalLayoutWidget_7 = QWidget(self.centralwidget)
        self.horizontalLayoutWidget_7.setGeometry(QRect(690, 530, 271, 231))
        self.horizontalLayoutWidget_7.setObjectName("horizontalLayoutWidget_7")

        self.totalBehaviorLayout = QHBoxLayout(self.horizontalLayoutWidget_7)
        self.totalBehaviorLayout.setContentsMargins(0, 0, 0, 0)
        self.totalBehaviorLayout.setObjectName("totalBehaviorLayout")

        self.frameLabel2 = QLabel(self.centralwidget)
        self.frameLabel2.setGeometry(QRect(80, 590, 41, 16))
        self.frameLabel2.setObjectName("frameLabel2")

        self.entryNoComboBox = QComboBox(self.centralwidget)
        self.entryNoComboBox.setGeometry(QRect(260, 550, 121, 26))
        self.entryNoComboBox.setObjectName("entryNoComboBox")

        self.tSNE_XmeanLabel = QLabel(self.centralwidget)
        self.tSNE_XmeanLabel.setGeometry(QRect(30, 620, 321, 16))
        self.tSNE_XmeanLabel.setObjectName("tSNE_XmeanLabel")
        self.tSNE_YmeanLabel = QLabel(self.centralwidget)
        self.tSNE_YmeanLabel.setGeometry(QRect(30, 640, 321, 16))
        self.tSNE_YmeanLabel.setObjectName("tSNE_YmeanLabel")

        self.saveBehaviorStartBox = QLineEdit(self.centralwidget)
        self.saveBehaviorStartBox.setEnabled(True)
        self.saveBehaviorStartBox.setGeometry(QRect(140, 590, 61, 21))
        self.saveBehaviorStartBox.setText("")
        self.saveBehaviorStartBox.setObjectName("saveBehaviorStartBox")
        self.saveBehaviorStartBox.setFocusPolicy(Qt.ClickFocus)
        self.saveBehaviorStopBox = QLineEdit(self.centralwidget)
        self.saveBehaviorStopBox.setGeometry(QRect(230, 590, 61, 21))
        self.saveBehaviorStopBox.setText("")
        self.saveBehaviorStopBox.setObjectName("saveBehaviorStopBox")
        self.saveBehaviorStopBox.setFocusPolicy(Qt.ClickFocus)

        self.saveDashLabel = QLabel(self.centralwidget)
        self.saveDashLabel.setGeometry(QRect(210, 590, 16, 16))
        self.saveDashLabel.setObjectName("saveDashLabel")

        self.horizontalLayoutWidget = QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QRect(990, 420, 431, 341))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.tableLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.tableLayout.setContentsMargins(0, 0, 0, 0)
        self.tableLayout.setObjectName("tableLayout")

        self.behaviorTable = behaviorTableWidget(self.horizontalLayoutWidget)
        self.tableLayout.addWidget(self.behaviorTable)

        self.behaviorTable.raise_()
        self.editBehaviorFrame.raise_()
        self.horizontalLayoutWidget_2.raise_()
        self.horizontalSlider.raise_()
        self.playButton.raise_()
        self.horizontalLayoutWidget_3.raise_()
        self.horizontalLayoutWidget_4.raise_()
        self.horizontalLayoutWidget_5.raise_()
        self.stopButton.raise_()
        self.editBehaviorLabel.raise_()
        self.editBehaviorFrLabel.raise_()
        self.divider1.raise_()
        self.dashLabel.raise_()
        self.editBehaviorStartBox.raise_()
        self.editBehaviorStopBox.raise_()
        self.editBehaviorEnterButton.raise_()
        self.editBehaviorComboBox.raise_()
        self.frame.raise_()
        self.divider2.raise_()
        self.savedBehaviorLabel.raise_()
        self.savedBehaviorComboBox.raise_()
        self.savedBehaviorEntryLabel.raise_()
        self.horizontalLayoutWidget_6.raise_()
        self.saveFilenameButton.raise_()
        self.saveFilenameBox.raise_()
        self.saveFilenameLabel.raise_()
        self.horizontalLayoutWidget.raise_()
        self.FrameLabel.raise_()
        self.FramelcdNumber.raise_()
        self.horizontalLayoutWidget_7.raise_()
        self.frameLabel2.raise_()
        self.entryNoComboBox.raise_()
        self.tSNE_XmeanLabel.raise_()
        self.tSNE_YmeanLabel.raise_()
        self.saveBehaviorStartBox.raise_()
        self.saveBehaviorStopBox.raise_()
        self.saveDashLabel.raise_()
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
        self.actionOpen = QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.menuFile.addAction(self.actionOpen)
        self.menubar.addAction(self.menuFile.menuAction())
        self.actionOpen.triggered.connect(self.openFile)

        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

        # Create Media Player
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        videoWidget = QVideoWidget()
        self.horizontalLayout_1.addWidget(videoWidget)
        self.mediaPlayer.setVideoOutput(videoWidget)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.setNotifyInterval(1)
        self.mediaPlayer.setPlaybackRate(0.1)

        # Append BP graph
        self.BPGraph = BP_Graph()
        self.BPcanvas = FigureCanvas(self.BPGraph)
        self.BPGraph.init_plot()
        self.horizontalLayout_2.addWidget(self.BPcanvas)

        # Create smaller Media Player
        self.smallBPGraph = BP_Graph()
        self.smallBPcanvas = FigureCanvas(self.smallBPGraph)
        self.smallBPGraph.init_plot()
        self.saveFilenameVideoLayout.addWidget(self.smallBPcanvas)

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
        # connect button
        self.playButton.clicked.connect(self.play)
        self.stopButton.clicked.connect(self.stop)
        self.addBehaviorButton.clicked.connect(self.addBehavior)
        self.editBehaviorEnterButton.clicked.connect(self.editBehavior)
        # connect slider
        self.horizontalSlider.sliderMoved.connect(self.setPosition)
        self.horizontalSlider.sliderMoved.connect(self.FramelcdNumber.display)
        # connect keys
        self.shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Alt+Left"), self.centralwidget, self.key_left)
        self.shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Alt+Right"), self.centralwidget, self.key_right)



        # timer to update frame
        self.timer = QTimer(self.FramelcdNumber)
        self.timer.timeout.connect(self.updateLcdNumberContent)
        self.timer.start(1)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.playButton.setText(_translate("MainWindow", "Play"))
        self.stopButton.setText(_translate("MainWindow", "Stop"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        # Part 2
        self.editBehaviorLabel.setText(_translate("MainWindow", "Behavior"))
        self.editBehaviorFrLabel.setText(_translate("MainWindow", "Frame Range"))
        self.dashLabel.setText(_translate("MainWindow", "-"))
        self.editBehaviorEnterButton.setText(_translate("MainWindow", "Enter"))
        self.addBehaviorLabel.setText(_translate("MainWindow", "Behavior:"))
        self.addBehaviorButton.setText(_translate("MainWindow", "Add"))
        self.savedBehaviorLabel.setText(_translate("MainWindow", "Saved Behavior"))
        self.savedBehaviorEntryLabel.setText(_translate("MainWindow", "Entry No."))
        self.saveFilenameButton.setText(_translate("MainWindow", "Save"))
        self.saveFilenameLabel.setText(_translate("MainWindow", "Filename"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.FrameLabel.setText(_translate("MainWindow", "Frame: "))
        self.frameLabel2.setText(_translate("MainWindow", "Frame:"))
        self.tSNE_XmeanLabel.setText(_translate("MainWindow", "tSNE X (mean): NaN"))
        self.tSNE_YmeanLabel.setText(_translate("MainWindow", "tSNE Y (mean): NaN"))
        self.saveDashLabel.setText(_translate("MainWindow", "-"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))


    def openFile(self):
        folder = QFileDialog.getExistingDirectory(
            None, "Select Directory", QDir.homePath() )
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
    # Part 1
    def play(self):
        self.mediaPlayer.play()
    def stop(self):
        self.mediaPlayer.pause()
    def positionChanged(self, position):
        self.horizontalSlider.setValue(position)
        self.BPGraph.update_graph(position)
        self.BPcanvas.draw()
        self.tsneGraph.update_graph(position)
        self.tsnecanvas.draw()
    def updateLcdNumberContent(self):
        duration = self.mediaPlayer.duration()
        position = self.mediaPlayer.position()
        if duration != 0 and self.BPGraph.num_frame != 0:
            self.FramelcdNumber.display(int(1.0*self.BPGraph.num_frame*position/duration))
        else:
            self.FramelcdNumber.display(0)
        pass
        
    def durationChanged(self, duration):
        self.horizontalSlider.setRange(0, duration)
        self.BPGraph.set_duration(duration)
        self.tsneGraph.set_duration(duration)
    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)
        self.BPGraph.update_graph(position)
        self.BPcanvas.draw()
        self.tsneGraph.update_graph(position)
        self.tsnecanvas.draw()
    # Part 2
    def addBehavior(self):
        newBehText = self.addBehaviorLineEdit.text()
        if newBehText: 
            self.addBehaviorLineEdit.clear()
            self.editBehaviorComboBox.addItem(newBehText)

    def editBehavior(self):
        behavior = self.editBehaviorComboBox.currentText()
        startFr = self.editBehaviorStartBox.text()
        stopFr = self.editBehaviorStopBox.text()
        self.editBehaviorStartBox.clear()
        self.editBehaviorStopBox.clear()
        if behavior and startFr and stopFr:
            self.behaviorTable.add_row(behavior, startFr, stopFr)
        pass
    def key_left(self):
        self.setPosition(self.mediaPlayer.position()-1)
    def key_right(self):
        self.setPosition(self.mediaPlayer.position()+1)



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
