import glob
import pandas as pd
from collections import Counter
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.animation as animation
import matplotlib.pyplot as plt

#import pyqt tools
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QFileDialog

# import graph modules
from widgets.BP_Canvas import BP_Canvas
from widgets.Ind_Canvas import Ind_Canvas

class Preview_Tab():
    def __init__(self, parent):
        self.parent = parent
        self.update_widgets()
        self.setup_connection()
        self.init_plot()
        self.timer = None
    def update_widgets(self):
        behavior_list = self.parent.beh_df['behavior'].to_numpy()
        behavior = list(Counter(behavior_list).keys())
        # set dropdown box
        self.parent.Preview_Behavior_ComboBox.addItems(behavior)
        self.update_entry_dropdown()
        # set lineEdit
        self.update_frame_lineEdit()
        pass
    def setup_connection(self):
        # connect dropdown
        self.parent.Preview_Ant_ComboBox.activated.connect(self.setup_ant_plot)
        self.parent.Preview_map_ComboBox.activated.connect(self.setup_ind_plot)
        self.parent.Preview_Behavior_ComboBox.activated.connect(self.behavior_change)
        self.parent.Preview_Entry_ComboBox.activated.connect(self.entry_change)
        # connect buttons 
        self.parent.Preview_Play_Button.clicked.connect(self.toggle_play)
        self.parent.Preview_Save_Button.clicked.connect(self.save)
        pass
    def update_entry_dropdown(self):
        behavior = self.parent.Preview_Behavior_ComboBox.currentText()
        num_entry = len(self.parent.beh_df[self.parent.beh_df['behavior']==behavior])
        entry = [str(ele) for ele in range(num_entry)]
        self.parent.Preview_Entry_ComboBox.clear()
        self.parent.Preview_Entry_ComboBox.addItems(entry)
        pass
    def update_frame_lineEdit(self):
        # update frame limits
        behavior = self.parent.Preview_Behavior_ComboBox.currentText()
        entry = self.parent.Preview_Entry_ComboBox.currentText()
        if behavior and entry:
            entry = int(entry)
            data = self.parent.beh_df[self.parent.beh_df['behavior']==behavior].iloc[entry]
            self.parent.Preview_Start_Frame_LineEdit.setValue(int(data['start_fr']))
            self.parent.Preview_Stop_Frame_LineEdit.setValue(int(data['stop_fr']))
            # update comment
            self.parent.Comment_Label.setText(data['comment'])
    def init_plot(self):
        # append bodypoint
        self.BPcanvas = BP_Canvas()
        self.parent.Preview_Ant_Layout.addWidget(self.BPcanvas)
        self.setup_ant_plot()
        # append total density plot
        self.IndDensityCanvas = Ind_Canvas()
        self.parent.Preview_tSNE_Layout.addWidget(self.IndDensityCanvas)
        self.setup_ind_plot()
    def setup_ant_plot(self):
        behavior = self.parent.Preview_Behavior_ComboBox.currentText()
        entry = self.parent.Preview_Entry_ComboBox.currentText()
        if behavior and entry:
            # extract UI data
            Preview_Ant_Mode = self.parent.Preview_Ant_ComboBox.currentText()
            entry = int(entry)
            start_fr = int(self.parent.Preview_Start_Frame_LineEdit.value())
            # find corresponding file based on above parameter
            label_entry = self.parent.beh_df[self.parent.beh_df['behavior']==behavior].iloc[entry]
            label_key = label_entry['folder_key']
            main_data = self.parent.main_df[self.parent.main_df["folder_key"]==label_key]
            label_dir = main_data['folder_path'].iloc[0] 
            # find video file in dir
            cur_video_dir = glob.glob(label_dir + "/*.avi")[0]
            # find DLC file in dir
            cur_DLC_dir = glob.glob(label_dir + "/*.h5")[0]
            # populate proper canvas
            if Preview_Ant_Mode == "Skeleton":
                self.BPcanvas.setup_canvas(cur_video_dir, cur_DLC_dir, mode="Skeleton")
                self.BPcanvas.update_canvas(frame=start_fr)
            elif Preview_Ant_Mode == "Skeleton + Video":
                self.BPcanvas.setup_canvas(cur_video_dir, cur_DLC_dir, mode="Skeleton + Video")
                self.BPcanvas.update_canvas(frame=start_fr)
            elif Preview_Ant_Mode == "Video":
                self.BPcanvas.setup_canvas(cur_video_dir, cur_DLC_dir, mode="Video")
                self.BPcanvas.update_canvas(frame=start_fr)
            else:
                print(":: No Ant Plot Mode")
        pass
    def setup_ind_plot(self):
        behavior = self.parent.Preview_Behavior_ComboBox.currentText()
        entry = self.parent.Preview_Entry_ComboBox.currentText()
        if behavior and entry:
            # extract UI data
            Preview_map_Mode = self.parent.Preview_map_ComboBox.currentText()
            entry = int(entry)
            start_fr = int(self.parent.Preview_Start_Frame_LineEdit.value())
            # find corresponding file based on above parameter
            label_entry = self.parent.beh_df[self.parent.beh_df['behavior']==behavior].iloc[entry]
            label_key = label_entry['folder_key']
            main_data = self.parent.main_df[self.parent.main_df["folder_key"]==label_key]
            label_dir = main_data['folder_path'].iloc[0] 
            # find embed file in dir
            cur_embed_dir = glob.glob(label_dir + "/EMBED.mat")[0]
            # find cluster file in dir
            cluster_dir = glob.glob(label_dir + "/cluster.npy")[0]
            # populate proper figure
            if Preview_map_Mode == "Points (HDBSCAN)":
                self.IndDensityCanvas.setup_canvas(
                    embed = cur_embed_dir, 
                    cluster = cluster_dir, 
                    mode = "Points (HDBSCAN)")
                self.IndDensityCanvas.update_canvas(frame=start_fr)
            else:
                print(":: No Individual Plot Mode")
        pass
    def behavior_change(self):
        self.update_entry_dropdown()
        self.update_frame_lineEdit()
        self.setup_ant_plot()
        self.setup_ind_plot()
        self.restart_frame()
        pass
    def entry_change(self):
        self.update_frame_lineEdit()
        self.setup_ant_plot()
        self.setup_ind_plot()
        self.restart_frame()
        pass
    def toggle_play(self):
        print(self.timer)
        if self.timer != None:
            self.timer.stop()
            self.timer = None
        else:
            self.restart_frame()
            self.timer = QTimer()
            self.timer.timeout.connect(self.nextFrameSlot)
            self.timer.start(100)
        pass
    def nextFrameSlot(self):
        error_bp, BP_frame = self.BPcanvas.next_frame()
        error_ind, Ind_frame = self.IndDensityCanvas.next_frame()
        stop_fr = int(self.parent.Preview_Stop_Frame_LineEdit.value())
        if error_bp or error_ind or BP_frame >= stop_fr or Ind_frame >= stop_fr:
            self.restart_frame()
        pass
    def restart_frame(self):
        if self.timer is not None:
            self.timer.stop()
            self.timer = None
        start_fr = int(self.parent.Preview_Start_Frame_LineEdit.value())
        # start from new beginning
        self.BPcanvas.update_canvas(frame=start_fr)
        self.IndDensityCanvas.update_canvas(frame=start_fr)
        self.BPcanvas.repaint()
        pass
    def save(self):
        # extract UI data
        Preview_map_Mode = self.parent.Preview_map_ComboBox.currentText()
        behavior = self.parent.Preview_Behavior_ComboBox.currentText()
        entry = int(self.parent.Preview_Entry_ComboBox.currentText())
        start_fr = int(self.parent.Preview_Start_Frame_LineEdit.value())
        stop_fr = int(self.parent.Preview_Stop_Frame_LineEdit.value())
        # find corresponding file based on above parameter
        label_entry = self.parent.beh_df[self.parent.beh_df['behavior']==behavior].iloc[entry]
        label_key = label_entry['folder_key']
        main_data = self.parent.main_df[self.parent.main_df["folder_key"]==label_key]
        label_dir = main_data['folder_path'].iloc[0] 
        # save file dialog at label_dir
        dir_suggestion = "{}/{}_{}_{}_fr{}-{}.mp4".format(label_dir,label_key,behavior,entry, start_fr, stop_fr)
        fig_title = "{} {} entry {}, frames={}-{}".format(label_key,behavior,entry, start_fr, stop_fr)
        filepath = QFileDialog.getSaveFileName(self.parent, "Save Video Image",  dir_suggestion,"MP4 Video (*.mp4)")[0]
        print(filepath)
        if filepath != "":
            # find bp file in dir
            DLC_dir = glob.glob(label_dir + "/*.h5")[0]
            store = pd.HDFStore(DLC_dir, mode='r')
            df = store['df_with_missing']
            num_bp, num_dim = len(list(df.columns.levels[1])), len(list(df.columns.levels[2]))
            num_frame = len(df)
            bp_data = df.T.to_numpy().reshape(num_bp, num_dim, num_frame)
            bp_data_trans, _ = self._translational(bp_data, origin_bp=2)
            print(bp_data_trans.shape)
            store.close()
            # creates animation writer
            writer = animation.FFMpegWriter(fps=15, metadata=dict(arist="Dong Hur"), bitrate=1800)
            # setup animation plot
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
            self.alpha = 1
            line_ani = animation.FuncAnimation(fig, self._update_graph,  init_func=self._init_graph,
                frames=list(range(start_fr, stop_fr)), fargs=(plt, bp_data_trans, self.lines), interval=50, blit=True)
            # save animation to proper file
            line_ani.save(filepath, writer=writer)
        pass
    def _init_graph(self):
            for line in self.lines:
                line.set_data([],[])
            return self.lines
    def _update_graph(self, frame, plt, data, lines, mode="ant_bp"):
        # plot ant points for specific time point t; specific to out setup with 30bp ants
        # data format: num_bp x (X_coord, Y_coord) x t
        if mode=="ant_bp":
            lines[0].set_data(data[0:4,0,frame], data[0:4,1,frame])
            lines[1].set_data(data[4:8,0,frame], data[4:8,1,frame])
            lines[2].set_data(data[8:11,0,frame], data[8:11,1,frame])
            lines[3].set_data(data[11:14,0,frame], data[11:14,1,frame])
            lines[4].set_data(data[14:17,0,frame], data[14:17,1,frame])
            lines[5].set_data(data[17:21,0,frame], data[17:21,1,frame])
            lines[6].set_data(data[21:24,0,frame], data[21:24,1,frame])
            lines[7].set_data(data[24:27,0,frame], data[24:27,1,frame])
            lines[8].set_data(data[27:30,0,frame], data[27:30,1,frame])
        elif mode=="overlay_ant_bp":
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
    def _translational(data, origin_bp):
        # data format: num_bp x num_coord x t
        # origin_bp - specifies which body point to make the origin
        return np.copy(data - data[origin_bp,:,:]), np.copy(data[origin_bp,:,:])












