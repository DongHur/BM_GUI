import numpy as np
import scipy.io as sio
import os

from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtCore import Qt, QRect, QMetaObject, QCoreApplication, pyqtSignal, QObject, QTimer
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QComboBox, QPushButton, QHBoxLayout)

from widgets.BP_Graph import BP_Graph

import matplotlib 
matplotlib.use("Qt4Agg") 
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.animation as animation
import matplotlib.pyplot as plt

class saveBehaviorWidget(QWidget):
    def __init__(self, con, *args, **kwargs):
        super(saveBehaviorWidget, self).__init__()

        self.con = con
        self.initialize()
        self.retranslateUi()
    def initialize(self):
        self.setObjectName("Form")
        self.resize(1500, 213)

        self.savedBehaviorEntryLabel = QLabel(self)
        self.savedBehaviorEntryLabel.setGeometry(QRect(280, 10, 60, 16))
        self.savedBehaviorEntryLabel.setObjectName("savedBehaviorEntryLabel")

        self.frameLabel2 = QLabel(self)
        self.frameLabel2.setGeometry(QRect(70, 70, 41, 16))
        self.frameLabel2.setObjectName("frameLabel2")

        self.saveBehaviorStartBox = QLineEdit(self)
        self.saveBehaviorStartBox.setEnabled(True)
        self.saveBehaviorStartBox.setGeometry(QRect(130, 70, 61, 21))
        self.saveBehaviorStartBox.setText("")
        self.saveBehaviorStartBox.setObjectName("saveBehaviorStartBox")
        self.saveBehaviorStartBox.setFocusPolicy(Qt.ClickFocus)

        self.savedBehaviorComboBox = QComboBox(self)
        self.savedBehaviorComboBox.setGeometry(QRect(0, 30, 211, 26))
        self.savedBehaviorComboBox.setCursor(QCursor(Qt.PointingHandCursor))
        self.savedBehaviorComboBox.setObjectName("savedBehaviorComboBox")

        self.tSNE_XmeanLabel = QLabel(self)
        self.tSNE_XmeanLabel.setGeometry(QRect(20, 100, 321, 16))
        self.tSNE_XmeanLabel.setObjectName("tSNE_XmeanLabel")

        self.savedBehaviorLabel = QLabel(self)
        self.savedBehaviorLabel.setGeometry(QRect(60, 10, 101, 16))
        self.savedBehaviorLabel.setObjectName("savedBehaviorLabel")

        self.saveBehaviorStopBox = QLineEdit(self)
        self.saveBehaviorStopBox.setGeometry(QRect(220, 70, 61, 21))
        self.saveBehaviorStopBox.setText("")
        self.saveBehaviorStopBox.setObjectName("saveBehaviorStopBox")
        self.saveBehaviorStopBox.setFocusPolicy(Qt.ClickFocus)

        self.saveDashLabel = QLabel(self)
        self.saveDashLabel.setGeometry(QRect(200, 70, 16, 16))
        self.saveDashLabel.setObjectName("saveDashLabel")

        self.saveFilenameBox = QLineEdit(self)
        self.saveFilenameBox.setGeometry(QRect(10, 180, 241, 21))
        self.saveFilenameBox.setObjectName("saveFilenameBox")
        self.saveFilenameBox.setFocusPolicy(Qt.ClickFocus)

        self.saveFilenameButton = QPushButton(self)
        self.saveFilenameButton.setGeometry(QRect(260, 170, 111, 41))
        self.saveFilenameButton.setObjectName("saveFilenameButton")

        self.entryNoComboBox = QComboBox(self)
        self.entryNoComboBox.setGeometry(QRect(250, 30, 121, 26))
        self.entryNoComboBox.setObjectName("entryNoComboBox")

        self.tSNE_YmeanLabel = QLabel(self)
        self.tSNE_YmeanLabel.setGeometry(QRect(20, 120, 321, 16))
        self.tSNE_YmeanLabel.setObjectName("tSNE_YmeanLabel")

        self.saveFilenameLabel = QLabel(self)
        self.saveFilenameLabel.setGeometry(QRect(20, 160, 231, 16))
        self.saveFilenameLabel.setAlignment(Qt.AlignCenter)
        self.saveFilenameLabel.setObjectName("saveFilenameLabel")

        # Create smaller Body Point Graph
        self.horizontalLayoutWidget_6 = QWidget(self)
        self.horizontalLayoutWidget_6.setGeometry(QRect(400, 0, 280, 230))
        self.horizontalLayoutWidget_6.setObjectName("horizontalLayoutWidget_6")

        self.saveFilenameVideoLayout = QHBoxLayout(self.horizontalLayoutWidget_6)
        self.saveFilenameVideoLayout.setContentsMargins(0, 0, 0, 0)
        self.saveFilenameVideoLayout.setObjectName("saveFilenameVideoLayout")
        
        self.smallBPGraph = BP_Graph()
        self.smallBPcanvas = FigureCanvas(self.smallBPGraph)
        self.smallBPGraph.init_plot()
        self.saveFilenameVideoLayout.addWidget(self.smallBPcanvas)

        # connect combobox
        self.savedBehaviorComboBox.currentIndexChanged.connect(self.update_entry_list)
        self.entryNoComboBox.currentIndexChanged.connect(self.update_parameter)

        # connect button
        self.saveFilenameButton.clicked.connect(self.save_video)
        
        QMetaObject.connectSlotsByName(self)
    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "Form"))
        self.savedBehaviorEntryLabel.setText(_translate("Form", "Entry No."))
        self.frameLabel2.setText(_translate("Form", "Frame:"))
        self.tSNE_XmeanLabel.setText(_translate("Form", "tSNE X (mean): NaN"))
        self.savedBehaviorLabel.setText(_translate("Form", "Saved Behavior"))
        self.saveDashLabel.setText(_translate("Form", "-"))
        self.saveFilenameButton.setText(_translate("Form", "Save"))
        self.tSNE_YmeanLabel.setText(_translate("Form", "tSNE Y (mean): NaN"))
        self.saveFilenameLabel.setText(_translate("Form", "Filename"))

    def update_beh_list(self):
        with self.con:
            cur = self.con.cursor()
            cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
            beh_list = cur.fetchall()
            self.savedBehaviorComboBox.clear()
            for idx, behavior in enumerate(beh_list):
                self.savedBehaviorComboBox.addItem(behavior[0])
    def update_entry_list(self, beh_idx):
        behavior = self.savedBehaviorComboBox.itemText(beh_idx)
        with self.con:
            cur = self.con.cursor()
            cur.execute("SELECT COUNT(*) FROM '{}'".format(behavior))
            num_entry = cur.fetchone()
            # clear entry no.
            self.entryNoComboBox.clear()
            print("ENTRY NO: ", num_entry[0])
            for i in range(num_entry[0]):
                self.entryNoComboBox.addItem(str(i+1)) 
            self.entryNoComboBox.setCurrentIndex(0)
        pass
    def update_parameter(self, entry_idx):
        if entry_idx < 0:
            # entry_idx may be -1 if reset combobox
            entry_idx = 0
        behavior = self.savedBehaviorComboBox.currentText()
        print("ENTRY_IDX: ", entry_idx)
        print("BEHAVIOR: ",behavior)
        print("COMMAND: ", "SELECT filename, startFr, stopFr, tsneX, tsneY FROM '{}' WHERE id={}"
                .format(behavior, entry_idx+1))
        with self.con:
            cur = self.con.cursor()
            cur.execute("SELECT filename, startFr, stopFr, tsneX, tsneY FROM '{}' WHERE id={}"
                .format(behavior, entry_idx+1))
            data = cur.fetchone()
            # abstract filepath
            filename = data[0].split('/')[-2]
            dir_path = os.path.dirname(data[0])
            print("DATA: ", data)
            print()
            # update parameter
            self.saveFilenameBox.setText(dir_path+"/"+behavior+"_"+str(entry_idx+1)+".mp4")
            self.saveBehaviorStartBox.setText(str(data[1]))
            self.saveBehaviorStopBox.setText(str(data[2]))
            self.tSNE_XmeanLabel.setText("tSNE X (mean): "+format(data[3],'.4f'))
            self.tSNE_YmeanLabel.setText("tSNE Y (mean): "+format(data[4],'.4f'))
        # update bpgraph
        self.update_video(dir_path, filename, data[1], data[2])
        pass
    def update_video(self, dir_path, filename, fr_start, fr_stop):
        self.smallBPGraph.set_newfile(dir_path+'/BP_'+filename+'.npy')
        # timer to update frame
        self.fr_start = fr_start
        self.fr_stop = fr_stop
        self.pos_iter = fr_start
        if fr_start < fr_stop:
            self.timer = QTimer()
            self.timer.timeout.connect(self.iter_video)
            self.timer.start(100)

        pass
    def iter_video(self):
        self.smallBPGraph.update_graph(position=self.pos_iter, frame_data=True)
        self.smallBPcanvas.draw()
        if self.pos_iter+1 == self.fr_stop:
            self.pos_iter = self.fr_start
        else:
            self.pos_iter += 1
        pass
    def save_video(self):
        # parameter for video
        filepath = self.saveFilenameBox.text()
        start = int(self.saveBehaviorStartBox.text())
        stop = int(self.saveBehaviorStopBox.text())
        fig_title = self.savedBehaviorComboBox.currentText() + ": Entry #" + self.entryNoComboBox.currentText()
        # creates animation writer
        Writer = animation.writers['ffmpeg']
        writer = Writer(fps=15, metadata=dict(arist="Dong Hur"), bitrate=1800)
        # create animation plot
        self.lines = []
        fig = plt.figure()
        ax1 = plt.axes(xlim=(-200,200), ylim=(-200,200))
        line, = ax1.plot([],[],'-o')
        plt.gca().set_aspect('equal', 'box')
        plt.title(fig_title, fontsize=8)
        plt.tick_params(axis='both', labelsize=6)
        for index in range(9):
            lobj = ax1.plot([],[], '-o')[0]
            self.lines.append(lobj)
        # start animating through each iteration
        line_ani = animation.FuncAnimation(fig, self.update_graph,  init_func=self.init_graph,
            frames=np.arange(start, stop), fargs=(self.smallBPGraph.data, self.lines), interval=50, blit=True)
        line_ani.save(filepath, writer=writer)
        pass
    def init_graph(self):
        for line in self.lines:
            line.set_data([],[])
        return self.lines
    def update_graph(self, frame, data, lines):
        # plot ant points for specific time point t; specific to out setup with 30bp ants
        # data format: num_bp x (X_coord, Y_coord) x t
        lines[0].set_data(data[0:4,0,frame], data[0:4,1,frame])
        lines[1].set_data(data[4:8,0,frame], data[4:8,1,frame])
        lines[2].set_data(data[8:11,0,frame], data[8:11,1,frame])
        lines[3].set_data(data[11:14,0,frame], data[11:14,1,frame])
        lines[4].set_data(data[14:17,0,frame], data[14:17,1,frame])
        lines[5].set_data(data[17:21,0,frame], data[17:21,1,frame])
        lines[6].set_data(data[21:24,0,frame], data[21:24,1,frame])
        lines[7].set_data(data[24:27,0,frame], data[24:27,1,frame])
        lines[8].set_data(data[27:30,0,frame], data[27:30,1,frame])
        return lines        

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = saveBehaviorWidget()
    Form.show()
    sys.exit(app.exec_())
