from collections import Counter
import glob

from PyQt5.QtCore import QTimer

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas

from widgets.BP_Canvas import BP_Canvas
from widgets.Individual_Canvas import Individual_Canvas
from widgets.Total_Canvas import Total_Canvas

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
        entry = int(self.parent.Preview_Entry_ComboBox.currentText())
        data = self.parent.beh_df[self.parent.beh_df['behavior']==behavior].iloc[entry]
        self.parent.Preview_Start_Frame_LineEdit.setText(data['start_fr'])
        self.parent.Preview_Stop_Frame_LineEdit.setText(data['stop_fr'])
        # update comment
        self.parent.Comment_Label.setText(data['comment'])
    def init_plot(self):
        # append bodypoint
        self.BPcanvas = BP_Canvas()
        self.parent.Preview_Ant_Layout.addWidget(self.BPcanvas)
        self.setup_ant_plot()
        # append total density plot
        self.IndDensityCanvas = Individual_Canvas()
        self.parent.Preview_tSNE_Layout.addWidget(self.IndDensityCanvas)
        self.setup_ind_plot()
    def setup_ant_plot(self):
        # extract UI data
        Preview_Ant_Mode = self.parent.Preview_Ant_ComboBox.currentText()
        behavior = self.parent.Preview_Behavior_ComboBox.currentText()
        entry = int(self.parent.Preview_Entry_ComboBox.currentText())
        start_fr = int(self.parent.Preview_Start_Frame_LineEdit.text())
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
        # extract UI data
        Preview_map_Mode = self.parent.Preview_map_ComboBox.currentText()
        behavior = self.parent.Preview_Behavior_ComboBox.currentText()
        entry = int(self.parent.Preview_Entry_ComboBox.currentText())
        start_fr = int(self.parent.Preview_Start_Frame_LineEdit.text())
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
        stop_fr = int(self.parent.Preview_Stop_Frame_LineEdit.text())
        if error_bp or error_ind or BP_frame >= stop_fr or Ind_frame >= stop_fr:
            self.restart_frame()
        pass
    def restart_frame(self):
        if self.timer is not None:
            self.timer.stop()
            self.timer = None
        start_fr = int(self.parent.Preview_Start_Frame_LineEdit.text())
        # start from new beginning
        self.BPcanvas.update_canvas(frame=start_fr)
        self.IndDensityCanvas.update_canvas(frame=start_fr)
        self.BPcanvas.repaint()
        pass
    def save(self):
        # TODO
        pass













