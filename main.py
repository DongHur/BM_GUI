import numpy as np
import sqlite3
import sys
import os

from PyQt5.QtCore import QTimer, QDir, QUrl
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QShortcut
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget

from UI.Ui_MainWindow import Ui_MainWindow

from widgets.tsne_Graph import tsne_Graph
from widgets.BP_Graph import BP_Graph
from widgets.density_Graph import density_Graph
from widgets.Behavior_Table import Behavior_Table

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__()
        self.fr = 50
        self.con = None
        self.video_on = False
        self.timer = None
        self.filename = ""
        self.dir_path = ""
        self.fr_start = 0
        self.fr_stop = 0
        self.setupUi(self)
        self.setup_connection()
        self.show()

    def setup_connection(self):
        # Append Behavior Table
        self.behaviorTable = Behavior_Table()
        self.tableLayout.addWidget(self.behaviorTable)
        # Append Media Player
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        videoWidget = QVideoWidget()
        self.horizontalLayout_1.addWidget(videoWidget)
        self.mediaPlayer.setVideoOutput(videoWidget)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.setNotifyInterval(int(1000/self.fr))
        self.mediaPlayer.setPlaybackRate(0.3)
        # Append BP graph
        self.BPGraph = BP_Graph() # large body point graph
        self.BPcanvas = FigureCanvas(self.BPGraph)
        self.BPGraph.init_plot()
        self.horizontalLayout_2.addWidget(self.BPcanvas)
        self.smallBPGraph = BP_Graph() # small body point graph
        self.smallBPcanvas = FigureCanvas(self.smallBPGraph)
        self.smallBPGraph.init_plot()
        self.saveFilenameVideoLayout.addWidget(self.smallBPcanvas)
        # Append tSNE graph
        self.tsneGraph = tsne_Graph()
        self.tsnecanvas = FigureCanvas(self.tsneGraph)
        self.tsneGraph.init_plot()
        self.horizontalLayout_3.addWidget(self.tsnecanvas)
        # Append Density Graph
        self.indDensityGraph = density_Graph() # individual density graph
        self.indDensitycanvas = FigureCanvas(self.indDensityGraph)
        self.indDensityGraph.init_plot(title='Individual Density Plot')
        self.horizontalLayout_4.addWidget(self.indDensitycanvas)
        self.densityGraph = density_Graph() # total density graph
        self.densitycanvas = FigureCanvas(self.densityGraph)
        self.densityGraph.init_plot(title='Total Density Plot')
        self.totalBehaviorLayout.addWidget(self.densitycanvas)

        # Connect LineEdit
        self.addBehaviorLineEdit.returnPressed.connect(self.addBehavior)
        self.editBehaviorStopBox.returnPressed.connect(self.editBehavior)
        # Connect Buttons
        self.playButton.pressed.connect(self.play)
        self.stopButton.clicked.connect(self.pause)
        self.addBehaviorButton.clicked.connect(self.addBehavior)
        self.editBehaviorEnterButton.clicked.connect(self.editBehavior)
        self.saveFilenameButton.clicked.connect(self.save_video)
        self.saveFilenamePlayButton.clicked.connect(self.toggle_video)
        self.changeFrameButton.clicked.connect(self.update_frames)
        # Connect MenuBar Tab
        self.uploadVideoOpen.triggered.connect(self.openFile)
        self.uploadDataOpen.triggered.connect(self.uploadData)
        # Connect Slider
        self.horizontalSlider.sliderMoved.connect(self.setPosition)
        # Connect Shortcut
        self.shortcut = QShortcut(QKeySequence("Alt+J"), self.centralwidget, self.key_left)
        self.shortcut2 = QShortcut(QKeySequence("Alt+K"), self.centralwidget, self.key_right)
        self.shortcut3 = QShortcut(QKeySequence("Alt+Space"), self.centralwidget, self.shorcut_spacebar)
        # Connect Combobox
        self.savedBehaviorComboBox.currentIndexChanged.connect(self.update_entry_list)
        self.entryNoComboBox.currentIndexChanged.connect(self.update_parameter)
        
        
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
            self.update_beh_list()
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
    def shorcut_spacebar(self):
        if self.video_on:
            self.pause()
        else:
            self.play()
    def play(self):
        self.video_on = True
        self.mediaPlayer.play()
    def pause(self):
        self.video_on = False
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
        self.update_beh_list()

    def key_left(self):
        # move back one frame
        self.setPosition(self.mediaPlayer.position()-1000/self.fr)
    def key_right(self):
        # move forward one frame
        self.setPosition(self.mediaPlayer.position()+1000/self.fr)

    ######################
    def update_beh_list(self):
        if self.video_on:
            self.stopSmallBPGraph()
        with self.con:
            cur = self.con.cursor()
            cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
            beh_list = cur.fetchall()
            self.savedBehaviorComboBox.clear()
            for idx, behavior in enumerate(beh_list):
                self.savedBehaviorComboBox.addItem(behavior[0])
            self.savedBehaviorComboBox.setCurrentIndex(0)
    def update_entry_list(self, beh_idx):
        if self.video_on:
            self.stopSmallBPGraph()
        # beh_idx is -1 when new behavior is added
        print("BEH_IDX (TESTING): ", beh_idx)
        if beh_idx >= 0:
            behavior = self.savedBehaviorComboBox.itemText(beh_idx)
            with self.con:
                cur = self.con.cursor()
                print("BEHAVIOR (TESTING): ", behavior)
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
        if self.video_on:
            self.stopSmallBPGraph()
        if entry_idx >= 0:
            behavior = self.savedBehaviorComboBox.currentText()
            print("ENTRY_IDX: ", entry_idx)
            print("BEHAVIOR: ",behavior)
            print("COMMAND: ", "SELECT filename, startFr, stopFr, tsneX, tsneY FROM '{}' WHERE id={}"
                    .format(behavior, entry_idx+1))
            with self.con:
                # fetch data for specific behavior and entry
                cur = self.con.cursor()
                cur.execute("SELECT filename, startFr, stopFr, tsneX, tsneY FROM '{}' WHERE id={}"
                    .format(behavior, entry_idx+1))
                data = cur.fetchone()
                # abstract filepath
                self.filename = data[0].split('/')[-2]
                self.dir_path = os.path.dirname(data[0])
                self.fr_start = data[1]
                self.fr_stop = data[2]
                print("DATA: ", data)
                print()
                # update parameter
                self.saveFilenameBox.setText(self.dir_path+"/"+behavior+"_"+str(entry_idx+1)+".mp4")
                self.saveBehaviorStartBox.setText(str(data[1]))
                self.saveBehaviorStopBox.setText(str(data[2]))
                self.tSNE_XmeanLabel.setText("tSNE X (mean): "+format(data[3],'.4f'))
                self.tSNE_YmeanLabel.setText("tSNE Y (mean): "+format(data[4],'.4f'))
                # update GUI UI
                self.saveFilenameBox.repaint()
                self.saveBehaviorStartBox.repaint()
                self.saveBehaviorStopBox.repaint()
                self.tSNE_XmeanLabel.repaint()
                self.tSNE_YmeanLabel.repaint()
        pass
    def update_frames(self):
        if self.video_on:
            self.stopSmallBPGraph()
        self.fr_start = self.saveBehaviorStartBox.text()
        self.fr_stop = self.saveBehaviorStopBox.text()
        if self.fr_start and self.fr_stop:
            # restart small bp_graph video
            self.fr_start = int(self.fr_start)
            self.fr_stop = int(self.fr_stop)
        pass

    # Play small bp_graph video
    def toggle_video(self):
        if not self.video_on:
            print("IN HERE")
            self.playSmallBPGraph()
        else:
            print("STOP HERE")
            self.stopSmallBPGraph()
    def playSmallBPGraph(self):
        print("path: ", self.dir_path)
        print("filename: ", self.filename)
        if  self.dir_path and self.filename:
            self.saveFilenamePlayButton.setText("Stop")
            self.saveFilenamePlayButton.repaint()
            # get bodypoint data
            self.smallBPGraph.set_newfile(self.dir_path+'/BP_'+self.filename+'.npy')
            # reset and start video
            self.video_on=True
            self.pos_iter = self.fr_start
            # setup timer for video
            self.timer = QTimer()
            self.timer.timeout.connect(self.iter_video)
            self.timer.start(100)
        pass
    def stopSmallBPGraph(self):
            self.timer.stop()
            self.saveFilenamePlayButton.setText("Play")
            self.saveFilenamePlayButton.repaint()
            self.video_on=False

    def iter_video(self):
        self.smallBPGraph.update_graph(position=self.pos_iter, frame_data=True)
        self.smallBPcanvas.draw()
        if self.pos_iter+1 == self.fr_stop:
            self.pos_iter = self.fr_start
        else:
            self.pos_iter += 1
        pass

    # Save small bp_graph functionality
    def save_video(self):
        # parameter for video
        filepath = self.saveFilenameBox.text()
        start = int(self.saveBehaviorStartBox.text())
        stop = int(self.saveBehaviorStopBox.text())
        fig_title = self.savedBehaviorComboBox.currentText() + ": Entry #" + self.entryNoComboBox.currentText()
        self.alpha = 1
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
            frames=np.arange(start, stop), fargs=(plt, self.smallBPGraph.data, self.lines), interval=50, blit=True)
        line_ani.save(filepath, writer=writer)
        pass
    def init_graph(self):
        for line in self.lines:
            line.set_data([],[])
        return self.lines
    def update_graph(self, frame, plt, data, lines):
        # plot ant points for specific time point t; specific to out setup with 30bp ants
        # data format: num_bp x (X_coord, Y_coord) x t
        if False:
            lines[0].set_data(data[0:4,0,frame], data[0:4,1,frame])
            lines[1].set_data(data[4:8,0,frame], data[4:8,1,frame])
            lines[2].set_data(data[8:11,0,frame], data[8:11,1,frame])
            lines[3].set_data(data[11:14,0,frame], data[11:14,1,frame])
            lines[4].set_data(data[14:17,0,frame], data[14:17,1,frame])
            lines[5].set_data(data[17:21,0,frame], data[17:21,1,frame])
            lines[6].set_data(data[21:24,0,frame], data[21:24,1,frame])
            lines[7].set_data(data[24:27,0,frame], data[24:27,1,frame])
            lines[8].set_data(data[27:30,0,frame], data[27:30,1,frame])
        else:
            plt.plot(data[0:4,0,frame], data[0:4,1,frame], '-bo', alpha=self.alpha)
            plt.plot(data[4:8,0,frame], data[4:8,1,frame], '-go', alpha=self.alpha)
            plt.plot(data[8:11,0,frame], data[8:11,1,frame], '-ro', alpha=self.alpha)
            plt.plot(data[11:14,0,frame], data[11:14,1,frame], '-co', alpha=self.alpha)
            plt.plot(data[14:17,0,frame], data[14:17,1,frame], '-mo', alpha=self.alpha)
            plt.plot(data[17:21,0,frame], data[17:21,1,frame], '-yo', alpha=self.alpha)
            plt.plot(data[21:24,0,frame], data[21:24,1,frame], '-ko', alpha=self.alpha)
            plt.plot(data[24:27,0,frame], data[24:27,1,frame], '-go', alpha=self.alpha)
            plt.plot(data[27:30,0,frame], data[27:30,1,frame], '-ro', alpha=self.alpha)
            self.alpha = 0.15
        return lines        




if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    sys.exit(app.exec_())
