# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1438, 809)
        MainWindow.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(10, 10, 341, 311))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_1 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_1.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_1.setObjectName("horizontalLayout_1")
        self.horizontalSlider = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSlider.setGeometry(QtCore.QRect(20, 330, 1401, 22))
        self.horizontalSlider.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.playButton = QtWidgets.QPushButton(self.centralwidget)
        self.playButton.setGeometry(QtCore.QRect(10, 360, 113, 32))
        self.playButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.playButton.setObjectName("playButton")
        self.horizontalLayoutWidget_3 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(370, 10, 341, 311))
        self.horizontalLayoutWidget_3.setObjectName("horizontalLayoutWidget_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayoutWidget_4 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_4.setGeometry(QtCore.QRect(730, 10, 341, 311))
        self.horizontalLayoutWidget_4.setObjectName("horizontalLayoutWidget_4")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_4)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayoutWidget_5 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_5.setGeometry(QtCore.QRect(1090, 10, 341, 311))
        self.horizontalLayoutWidget_5.setObjectName("horizontalLayoutWidget_5")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_5)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.stopButton = QtWidgets.QPushButton(self.centralwidget)
        self.stopButton.setGeometry(QtCore.QRect(130, 360, 113, 32))
        self.stopButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.stopButton.setObjectName("stopButton")
        self.divider1 = QtWidgets.QFrame(self.centralwidget)
        self.divider1.setGeometry(QtCore.QRect(10, 390, 1421, 20))
        self.divider1.setFrameShape(QtWidgets.QFrame.HLine)
        self.divider1.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.divider1.setObjectName("divider1")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(30, 420, 370, 71))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.addBehaviorLabel = QtWidgets.QLabel(self.frame)
        self.addBehaviorLabel.setGeometry(QtCore.QRect(10, 30, 60, 16))
        self.addBehaviorLabel.setObjectName("addBehaviorLabel")
        self.addBehaviorLineEdit = QtWidgets.QLineEdit(self.frame)
        self.addBehaviorLineEdit.setGeometry(QtCore.QRect(80, 30, 171, 21))
        self.addBehaviorLineEdit.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.addBehaviorLineEdit.setObjectName("addBehaviorLineEdit")
        self.addBehaviorButton = QtWidgets.QPushButton(self.frame)
        self.addBehaviorButton.setGeometry(QtCore.QRect(250, 20, 113, 41))
        self.addBehaviorButton.setObjectName("addBehaviorButton")
        self.editBehaviorFrame = QtWidgets.QFrame(self.centralwidget)
        self.editBehaviorFrame.setGeometry(QtCore.QRect(450, 420, 531, 71))
        self.editBehaviorFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.editBehaviorFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.editBehaviorFrame.setObjectName("editBehaviorFrame")
        self.editBehaviorLabel = QtWidgets.QLabel(self.editBehaviorFrame)
        self.editBehaviorLabel.setGeometry(QtCore.QRect(70, 10, 69, 16))
        self.editBehaviorLabel.setObjectName("editBehaviorLabel")
        self.editBehaviorFrLabel = QtWidgets.QLabel(self.editBehaviorFrame)
        self.editBehaviorFrLabel.setGeometry(QtCore.QRect(260, 10, 101, 16))
        self.editBehaviorFrLabel.setObjectName("editBehaviorFrLabel")
        self.editBehaviorComboBox = QtWidgets.QComboBox(self.editBehaviorFrame)
        self.editBehaviorComboBox.setGeometry(QtCore.QRect(10, 30, 210, 26))
        self.editBehaviorComboBox.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.editBehaviorComboBox.setObjectName("editBehaviorComboBox")
        self.editBehaviorStartBox = QtWidgets.QLineEdit(self.editBehaviorFrame)
        self.editBehaviorStartBox.setEnabled(True)
        self.editBehaviorStartBox.setGeometry(QtCore.QRect(230, 30, 61, 21))
        self.editBehaviorStartBox.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.editBehaviorStartBox.setText("")
        self.editBehaviorStartBox.setObjectName("editBehaviorStartBox")
        self.editBehaviorStopBox = QtWidgets.QLineEdit(self.editBehaviorFrame)
        self.editBehaviorStopBox.setGeometry(QtCore.QRect(320, 30, 61, 21))
        self.editBehaviorStopBox.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.editBehaviorStopBox.setText("")
        self.editBehaviorStopBox.setObjectName("editBehaviorStopBox")
        self.dashLabel = QtWidgets.QLabel(self.editBehaviorFrame)
        self.dashLabel.setGeometry(QtCore.QRect(300, 30, 16, 16))
        self.dashLabel.setObjectName("dashLabel")
        self.editBehaviorEnterButton = QtWidgets.QPushButton(self.editBehaviorFrame)
        self.editBehaviorEnterButton.setGeometry(QtCore.QRect(400, 20, 113, 41))
        self.editBehaviorEnterButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.editBehaviorEnterButton.setObjectName("editBehaviorEnterButton")
        self.divider2 = QtWidgets.QFrame(self.centralwidget)
        self.divider2.setGeometry(QtCore.QRect(10, 500, 971, 20))
        self.divider2.setFrameShape(QtWidgets.QFrame.HLine)
        self.divider2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.divider2.setObjectName("divider2")
        self.savedBehaviorLabel = QtWidgets.QLabel(self.centralwidget)
        self.savedBehaviorLabel.setGeometry(QtCore.QRect(70, 530, 101, 16))
        self.savedBehaviorLabel.setObjectName("savedBehaviorLabel")
        self.savedBehaviorComboBox = QtWidgets.QComboBox(self.centralwidget)
        self.savedBehaviorComboBox.setGeometry(QtCore.QRect(10, 550, 211, 26))
        self.savedBehaviorComboBox.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.savedBehaviorComboBox.setObjectName("savedBehaviorComboBox")
        self.savedBehaviorEntryLabel = QtWidgets.QLabel(self.centralwidget)
        self.savedBehaviorEntryLabel.setGeometry(QtCore.QRect(290, 530, 60, 16))
        self.savedBehaviorEntryLabel.setObjectName("savedBehaviorEntryLabel")
        self.horizontalLayoutWidget_6 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_6.setGeometry(QtCore.QRect(400, 530, 271, 231))
        self.horizontalLayoutWidget_6.setObjectName("horizontalLayoutWidget_6")
        self.saveFilenameVideoLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_6)
        self.saveFilenameVideoLayout.setContentsMargins(0, 0, 0, 0)
        self.saveFilenameVideoLayout.setObjectName("saveFilenameVideoLayout")
        self.saveFilenameBox = QtWidgets.QLineEdit(self.centralwidget)
        self.saveFilenameBox.setGeometry(QtCore.QRect(20, 700, 241, 21))
        self.saveFilenameBox.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.saveFilenameBox.setObjectName("saveFilenameBox")
        self.saveFilenameLabel = QtWidgets.QLabel(self.centralwidget)
        self.saveFilenameLabel.setGeometry(QtCore.QRect(30, 680, 231, 16))
        self.saveFilenameLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.saveFilenameLabel.setObjectName("saveFilenameLabel")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(990, 410, 431, 351))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.tableLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.tableLayout.setContentsMargins(0, 0, 0, 0)
        self.tableLayout.setObjectName("tableLayout")
        self.FrameLabel = QtWidgets.QLabel(self.centralwidget)
        self.FrameLabel.setGeometry(QtCore.QRect(260, 360, 60, 16))
        self.FrameLabel.setObjectName("FrameLabel")
        self.horizontalLayoutWidget_7 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_7.setGeometry(QtCore.QRect(690, 530, 271, 231))
        self.horizontalLayoutWidget_7.setObjectName("horizontalLayoutWidget_7")
        self.totalBehaviorLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_7)
        self.totalBehaviorLayout.setContentsMargins(0, 0, 0, 0)
        self.totalBehaviorLayout.setObjectName("totalBehaviorLayout")
        self.frameLabel2 = QtWidgets.QLabel(self.centralwidget)
        self.frameLabel2.setGeometry(QtCore.QRect(30, 590, 41, 16))
        self.frameLabel2.setObjectName("frameLabel2")
        self.entryNoComboBox = QtWidgets.QComboBox(self.centralwidget)
        self.entryNoComboBox.setGeometry(QtCore.QRect(260, 550, 121, 26))
        self.entryNoComboBox.setObjectName("entryNoComboBox")
        self.tSNE_XmeanLabel = QtWidgets.QLabel(self.centralwidget)
        self.tSNE_XmeanLabel.setGeometry(QtCore.QRect(30, 620, 241, 16))
        self.tSNE_XmeanLabel.setObjectName("tSNE_XmeanLabel")
        self.tSNE_YmeanLabel = QtWidgets.QLabel(self.centralwidget)
        self.tSNE_YmeanLabel.setGeometry(QtCore.QRect(30, 640, 241, 16))
        self.tSNE_YmeanLabel.setObjectName("tSNE_YmeanLabel")
        self.saveBehaviorStartBox = QtWidgets.QLineEdit(self.centralwidget)
        self.saveBehaviorStartBox.setEnabled(True)
        self.saveBehaviorStartBox.setGeometry(QtCore.QRect(90, 590, 61, 21))
        self.saveBehaviorStartBox.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.saveBehaviorStartBox.setText("")
        self.saveBehaviorStartBox.setObjectName("saveBehaviorStartBox")
        self.saveBehaviorStopBox = QtWidgets.QLineEdit(self.centralwidget)
        self.saveBehaviorStopBox.setGeometry(QtCore.QRect(180, 590, 61, 21))
        self.saveBehaviorStopBox.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.saveBehaviorStopBox.setText("")
        self.saveBehaviorStopBox.setObjectName("saveBehaviorStopBox")
        self.saveDashLabel = QtWidgets.QLabel(self.centralwidget)
        self.saveDashLabel.setGeometry(QtCore.QRect(160, 590, 16, 16))
        self.saveDashLabel.setObjectName("saveDashLabel")
        self.changeFrameButton = QtWidgets.QPushButton(self.centralwidget)
        self.changeFrameButton.setGeometry(QtCore.QRect(270, 580, 131, 32))
        self.changeFrameButton.setObjectName("changeFrameButton")
        self.saveFilenamePlayButton = QtWidgets.QPushButton(self.centralwidget)
        self.saveFilenamePlayButton.setGeometry(QtCore.QRect(280, 620, 113, 32))
        self.saveFilenamePlayButton.setObjectName("saveFilenamePlayButton")
        self.saveFilenameButton = QtWidgets.QPushButton(self.centralwidget)
        self.saveFilenameButton.setGeometry(QtCore.QRect(280, 690, 113, 32))
        self.saveFilenameButton.setObjectName("saveFilenameButton")
        self.FrameNumberLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.FrameNumberLineEdit.setGeometry(QtCore.QRect(310, 360, 113, 21))
        self.FrameNumberLineEdit.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.FrameNumberLineEdit.setObjectName("FrameNumberLineEdit")
        self.frameBackButton = QtWidgets.QPushButton(self.centralwidget)
        self.frameBackButton.setGeometry(QtCore.QRect(430, 360, 51, 32))
        self.frameBackButton.setObjectName("frameBackButton")
        self.frameFrontButton = QtWidgets.QPushButton(self.centralwidget)
        self.frameFrontButton.setGeometry(QtCore.QRect(478, 360, 51, 32))
        self.frameFrontButton.setObjectName("frameFrontButton")
        self.editBehaviorFrame.raise_()
        self.horizontalLayoutWidget_2.raise_()
        self.horizontalSlider.raise_()
        self.playButton.raise_()
        self.horizontalLayoutWidget_3.raise_()
        self.horizontalLayoutWidget_4.raise_()
        self.horizontalLayoutWidget_5.raise_()
        self.stopButton.raise_()
        self.divider1.raise_()
        self.frame.raise_()
        self.divider2.raise_()
        self.savedBehaviorLabel.raise_()
        self.savedBehaviorComboBox.raise_()
        self.savedBehaviorEntryLabel.raise_()
        self.horizontalLayoutWidget_6.raise_()
        self.saveFilenameBox.raise_()
        self.saveFilenameLabel.raise_()
        self.horizontalLayoutWidget.raise_()
        self.FrameLabel.raise_()
        self.horizontalLayoutWidget_7.raise_()
        self.frameLabel2.raise_()
        self.entryNoComboBox.raise_()
        self.tSNE_XmeanLabel.raise_()
        self.tSNE_YmeanLabel.raise_()
        self.saveBehaviorStartBox.raise_()
        self.saveBehaviorStopBox.raise_()
        self.saveDashLabel.raise_()
        self.changeFrameButton.raise_()
        self.saveFilenamePlayButton.raise_()
        self.saveFilenameButton.raise_()
        self.FrameNumberLineEdit.raise_()
        self.frameBackButton.raise_()
        self.frameFrontButton.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1438, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.uploadVideoOpen = QtWidgets.QAction(MainWindow)
        self.uploadVideoOpen.setObjectName("uploadVideoOpen")
        self.uploadDataOpen = QtWidgets.QAction(MainWindow)
        self.uploadDataOpen.setObjectName("uploadDataOpen")
        self.menuFile.addAction(self.uploadVideoOpen)
        self.menuFile.addAction(self.uploadDataOpen)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.playButton.setText(_translate("MainWindow", "Play"))
        self.stopButton.setText(_translate("MainWindow", "Stop"))
        self.addBehaviorLabel.setText(_translate("MainWindow", "Behavior:"))
        self.addBehaviorButton.setText(_translate("MainWindow", "Add"))
        self.editBehaviorLabel.setText(_translate("MainWindow", "Behavior"))
        self.editBehaviorFrLabel.setText(_translate("MainWindow", "Frame Range"))
        self.dashLabel.setText(_translate("MainWindow", "-"))
        self.editBehaviorEnterButton.setText(_translate("MainWindow", "Enter"))
        self.savedBehaviorLabel.setText(_translate("MainWindow", "Saved Behavior"))
        self.savedBehaviorEntryLabel.setText(_translate("MainWindow", "Entry No."))
        self.saveFilenameLabel.setText(_translate("MainWindow", "Filename"))
        self.FrameLabel.setText(_translate("MainWindow", "Frame:"))
        self.frameLabel2.setText(_translate("MainWindow", "Frame:"))
        self.tSNE_XmeanLabel.setText(_translate("MainWindow", "tSNE X (mean): NaN"))
        self.tSNE_YmeanLabel.setText(_translate("MainWindow", "tSNE Y (mean): NaN"))
        self.saveDashLabel.setText(_translate("MainWindow", "-"))
        self.changeFrameButton.setText(_translate("MainWindow", "Update Frames"))
        self.saveFilenamePlayButton.setText(_translate("MainWindow", "Play"))
        self.saveFilenameButton.setText(_translate("MainWindow", "Save"))
        self.frameBackButton.setText(_translate("MainWindow", "<"))
        self.frameFrontButton.setText(_translate("MainWindow", ">"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.uploadVideoOpen.setText(_translate("MainWindow", "Open Video"))
        self.uploadDataOpen.setText(_translate("MainWindow", "Open Data"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
