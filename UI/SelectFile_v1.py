# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'BehaviorGUI.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!
import numpy as np
import os
import glob

from PyQt5 import QtCore, QtGui, QtWidgets
import pyqtgraph as pg

from widgets.Graph1_Widget import Graph1_Widget
from widgets.Graph2_Widget import Graph2_Widget

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(976, 670)
        self.FilesList = QtWidgets.QListWidget(Form)
        self.FilesList.setGeometry(QtCore.QRect(20, 360, 171, 301))
        self.FilesList.setObjectName("FilesList")
        self.FilesList.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.NumFilesLabel = QtWidgets.QLabel(Form)
        self.NumFilesLabel.setGeometry(QtCore.QRect(220, 520, 251, 16))
        self.NumFilesLabel.setObjectName("NumFilesLabel")
        self.NumFramesLabel = QtWidgets.QLabel(Form)
        self.NumFramesLabel.setGeometry(QtCore.QRect(220, 540, 251, 16))
        self.NumFramesLabel.setObjectName("NumFramesLabel")
        self.TitleLabel = QtWidgets.QLabel(Form)
        self.TitleLabel.setGeometry(QtCore.QRect(430, 10, 151, 16))
        self.TitleLabel.setObjectName("TitleLabel")
        self.UploadButton = QtWidgets.QPushButton(Form)
        self.UploadButton.setGeometry(QtCore.QRect(210, 360, 113, 32))
        self.UploadButton.setObjectName("UploadButton")
        self.IndFileDrop = QtWidgets.QComboBox(Form)
        self.IndFileDrop.setGeometry(QtCore.QRect(650, 360, 221, 26))
        self.IndFileDrop.setObjectName("IndFileDrop")
        self.FrameLabel = QtWidgets.QLabel(Form)
        self.FrameLabel.setGeometry(QtCore.QRect(570, 470, 60, 16))
        self.FrameLabel.setObjectName("FrameLabel")
        self.IndNumFrameLabel = QtWidgets.QLabel(Form)
        self.IndNumFrameLabel.setGeometry(QtCore.QRect(580, 400, 351, 16))
        self.IndNumFrameLabel.setObjectName("IndNumFrameLabel")
        self.IndBehaviorLabel = QtWidgets.QLabel(Form)
        self.IndBehaviorLabel.setGeometry(QtCore.QRect(580, 420, 351, 16))
        self.IndBehaviorLabel.setObjectName("IndBehaviorLabel")
        self.IndCommentLabel = QtWidgets.QLabel(Form)
        self.IndCommentLabel.setGeometry(QtCore.QRect(580, 440, 301, 16))
        self.IndCommentLabel.setObjectName("IndCommentLabel")
        self.FrameLineEdit = QtWidgets.QLineEdit(Form)
        self.FrameLineEdit.setGeometry(QtCore.QRect(630, 470, 111, 21))
        self.FrameLineEdit.setObjectName("FrameLineEdit")
        self.PlayButton = QtWidgets.QPushButton(Form)
        self.PlayButton.setGeometry(QtCore.QRect(760, 470, 91, 32))
        self.PlayButton.setAutoFillBackground(False)
        self.PlayButton.setObjectName("PlayButton")
        self.StopButton = QtWidgets.QPushButton(Form)
        self.StopButton.setGeometry(QtCore.QRect(860, 470, 91, 32))
        self.StopButton.setObjectName("StopButton")
        self.CommentFrame = QtWidgets.QFrame(Form)
        self.CommentFrame.setGeometry(QtCore.QRect(570, 510, 391, 141))
        self.CommentFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.CommentFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.CommentFrame.setObjectName("CommentFrame")
        self.FrameCommentLabel = QtWidgets.QLabel(self.CommentFrame)
        self.FrameCommentLabel.setGeometry(QtCore.QRect(20, 10, 60, 16))
        self.FrameCommentLabel.setObjectName("FrameCommentLabel")
        self.BehaviorCommentLabel = QtWidgets.QLabel(self.CommentFrame)
        self.BehaviorCommentLabel.setGeometry(QtCore.QRect(20, 40, 60, 16))
        self.BehaviorCommentLabel.setObjectName("BehaviorCommentLabel")
        self.CommentLabel = QtWidgets.QLabel(self.CommentFrame)
        self.CommentLabel.setGeometry(QtCore.QRect(20, 70, 71, 16))
        self.CommentLabel.setObjectName("CommentLabel")
        self.DashLabel = QtWidgets.QLabel(self.CommentFrame)
        self.DashLabel.setGeometry(QtCore.QRect(200, 10, 16, 16))
        self.DashLabel.setObjectName("DashLabel")
        self.FrameStopLineEdit = QtWidgets.QLineEdit(self.CommentFrame)
        self.FrameStopLineEdit.setGeometry(QtCore.QRect(220, 10, 91, 21))
        self.FrameStopLineEdit.setObjectName("FrameStopLineEdit")
        self.FrameStartLineEdit = QtWidgets.QLineEdit(self.CommentFrame)
        self.FrameStartLineEdit.setGeometry(QtCore.QRect(90, 10, 91, 21))
        self.FrameStartLineEdit.setObjectName("FrameStartLineEdit")
        self.BehaviorLineEdit = QtWidgets.QLineEdit(self.CommentFrame)
        self.BehaviorLineEdit.setGeometry(QtCore.QRect(90, 40, 281, 21))
        self.BehaviorLineEdit.setObjectName("BehaviorLineEdit")
        self.CommentTextEdit = QtWidgets.QPlainTextEdit(self.CommentFrame)
        self.CommentTextEdit.setGeometry(QtCore.QRect(90, 70, 281, 61))
        self.CommentTextEdit.setObjectName("CommentTextEdit")
        self.CheckAllButton = QtWidgets.QPushButton(Form)
        self.CheckAllButton.setGeometry(QtCore.QRect(210, 450, 113, 32))
        self.CheckAllButton.setObjectName("CheckAllButton")
        self.UncheckAllButton = QtWidgets.QPushButton(Form)
        self.UncheckAllButton.setGeometry(QtCore.QRect(210, 480, 113, 32))
        self.UncheckAllButton.setObjectName("UncheckAllButton")
        self.horizontalLayoutWidget = QtWidgets.QWidget(Form)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 40, 461, 311))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.Graph1Layout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.Graph1Layout.setContentsMargins(0, 0, 0, 0)
        self.Graph1Layout.setObjectName("Graph1Layout")
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(Form)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(500, 40, 461, 311))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.Graph2Layout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.Graph2Layout.setContentsMargins(0, 0, 0, 0)
        self.Graph2Layout.setObjectName("Graph2Layout")
        self.DeleteButton = QtWidgets.QPushButton(Form)
        self.DeleteButton.setGeometry(QtCore.QRect(210, 420, 113, 32))
        self.DeleteButton.setObjectName("Delete_Button")
        self.UploadFolderButton = QtWidgets.QPushButton(Form)
        self.UploadFolderButton.setGeometry(QtCore.QRect(210, 390, 113, 32))
        self.UploadFolderButton.setObjectName("UploadFolderButton")
        self.NumFramesSelectedLabel = QtWidgets.QLabel(Form)
        self.NumFramesSelectedLabel.setGeometry(QtCore.QRect(220, 580, 251, 16))
        self.NumFramesSelectedLabel.setObjectName("NumFramesSelectedLabel")
        self.NumFilesSelectedLabel = QtWidgets.QLabel(Form)
        self.NumFilesSelectedLabel.setGeometry(QtCore.QRect(220, 560, 251, 16))
        self.NumFilesSelectedLabel.setObjectName("NumFilesSelectedLabel")

        # append graph
        self.Graph1 = Graph1_Widget()
        self.Graph2 = Graph2_Widget()
        self.Graph1Layout.addWidget(self.Graph1)
        self.Graph2Layout.addWidget(self.Graph2)
        self.Graph1.init_plot()
        self.Graph2.init_plot()
        # append text
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        # connect button
        self.UploadButton.clicked.connect(self.upload_file)
        self.UploadFolderButton.clicked.connect(self.upload_folder)
        self.DeleteButton.clicked.connect(self.delete_files)
        self.CheckAllButton.clicked.connect(self.checkall_files)
        self.UncheckAllButton.clicked.connect(self.uncheckall_files)
        self.FilesList.itemClicked.connect(self.check_file)
        self.FilesList.itemChanged.connect(self.changed_file)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.NumFilesLabel.setText(_translate("Form", "# Files: "))
        self.NumFramesLabel.setText(_translate("Form", "# Frames:"))
        self.TitleLabel.setText(_translate("Form", "Behavioral Mapping"))
        self.UploadButton.setText(_translate("Form", "Upload File"))
        self.FrameLabel.setText(_translate("Form", "Frame:"))
        self.IndNumFrameLabel.setText(_translate("Form", "Number of Frames:"))
        self.IndBehaviorLabel.setText(_translate("Form", "Behavior:"))
        self.IndCommentLabel.setText(_translate("Form", "Comment: "))
        self.PlayButton.setText(_translate("Form", "Play"))
        self.StopButton.setText(_translate("Form", "Stop"))
        self.FrameCommentLabel.setText(_translate("Form", "Frames: "))
        self.BehaviorCommentLabel.setText(_translate("Form", "Behavior: "))
        self.CommentLabel.setText(_translate("Form", "Comment:"))
        self.DashLabel.setText(_translate("Form", "-"))
        self.CheckAllButton.setText(_translate("Form", "Check All"))
        self.UncheckAllButton.setText(_translate("Form", "Uncheck All"))
        self.DeleteButton.setText(_translate("Form", "Delete"))
        self.UploadFolderButton.setText(_translate("Form", "Upload Folder"))
        self.NumFramesSelectedLabel.setText(_translate("Form", "# Frames Selected:"))
        self.NumFilesSelectedLabel.setText(_translate("Form", "# Files Selected:"))

    def upload_file(self):
        filename,_  = QtWidgets.QFileDialog.getOpenFileName(None, "Select EMBED.mat", "", "MAT files (EMBED.mat)")        # add to file list widget
        if filename:
            item = QtWidgets.QListWidgetItem(filename)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            item.setCheckState(QtCore.Qt.Unchecked)
            self.FilesList.addItem(item)
            # update graph 1 plot
            self.Graph1.add_dir(filename)
            self.update_file_info()
        pass
    def upload_folder(self):
        folder = QtWidgets.QFileDialog.getExistingDirectory(None, "Select Directory")
        if folder:
            files_path = glob.glob(folder+"/**/EMBED.mat", recursive=True)
            for filename in files_path:
                # add to file list widget
                item = QtWidgets.QListWidgetItem(filename)
                item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
                item.setCheckState(QtCore.Qt.Unchecked)
                self.FilesList.addItem(item)
                # update graph 1 plot
                self.Graph1.add_dir(filename)
            self.update_file_info()
        pass
    def delete_files(self):
        list_items=self.FilesList.selectedItems()
        if list_items:        
            for item in list_items:
                self.FilesList.takeItem(self.FilesList.row(item))
                self.Graph1.delete_dir(item.text())
        # UPDATE CHECK LIST IN GRAPH1
        self.Graph1.update_graph()
        self.update_file_info()
        pass
    def checkall_files(self):
        for index in range(self.FilesList.count()):
            item = self.FilesList.item(index);
            item.setCheckState(QtCore.Qt.Checked)
            self.Graph1.update_checked(item.text(), isChecked=True)
        # UPDATE CHECK LIST IN GRAPH1
        self.Graph1.update_graph()
        self.update_file_info()
        pass
    def uncheckall_files(self):
        for index in range(self.FilesList.count()):
            item = self.FilesList.item(index);
            item.setCheckState(QtCore.Qt.Unchecked)
            self.Graph1.update_checked(item.text(), isChecked=False)
        # UPDATE CHECK LIST IN GRAPH1
        self.Graph1.update_graph()
        self.update_file_info()
        pass
    def check_file(self, item):
        if item.checkState() == QtCore.Qt.Checked:
            self.Graph1.update_checked(item.text(), isChecked=True)
        elif item.checkState() == QtCore.Qt.Unchecked:
            self.Graph1.update_checked(item.text(), isChecked=False)
        pass
        self.Graph1.update_graph()
        self.update_file_info()
    def changed_file(self):
        print('here')
        pass
    def update_file_info(self):
        app.processEvents() 
        # split text w/ respect to :
        NumFiles_base = self.NumFilesLabel.text().split(':')[0]
        NumFrames_base = self.NumFramesLabel.text().split(':')[0]
        NumFramesSelected_base = self.NumFramesSelectedLabel.text().split(':')[0]
        NumFilesSelected_base = self.NumFilesSelectedLabel.text().split(':')[0]
        # update file info
        self.NumFilesLabel.setText(NumFiles_base+": "+str(self.Graph1.data_info['num_files']))
        self.NumFramesLabel.setText(NumFrames_base+": "+str(self.Graph1.data_info['num_frames']))
        self.NumFramesSelectedLabel.setText(NumFramesSelected_base+": "+str(self.Graph1.data_info['num_selected_frames']))
        self.NumFilesSelectedLabel.setText(NumFilesSelected_base+": "+str(self.Graph1.data_info['num_selected_files']))
        pass
    
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
