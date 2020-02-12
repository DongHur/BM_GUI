import numpy as np 
import glob
import os
import pandas as pd
import scipy.io as sio

#import pyqt tools
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QShortcut, QMessageBox, QFileDialog

# import graph modules
from widgets.BP_Canvas import BP_Canvas
from widgets.Ind_Canvas import Ind_Canvas
from widgets.Ethogram_Canvas import Ethogram_Canvas
from widgets.Tot_Canvas import Tot_Canvas

# from tools.hdbscan import hdbscan
from tools.gmm import gmm
from tools.Helper import findVideoDir, findEmbedDir

class Label_Tab():
    def __init__(self, parent):
        self.parent = parent
        self.cur_folder_key = None
        self.cur_DLC_dir, self.cur_embed_dir, self.cur_video_dir = None, None, None
        self.timer, self.speed = None, 1
        self.setup_widgets()
        self.setup_connection()
        self.init_plot()

# ***** exec function *****
    def setup_widgets(self):
        self.parent.Label_Filename_ComboBox.addItems(self.parent.main_df['folder_key'])
        self.parent.Label_Behavior_ComboBox.addItems(self.parent.beh_key_df['behavior'])
    def setup_connection(self):
        # dropdown
        self.parent.Label_Filename_ComboBox.activated.connect(self.update_filename_change)
        self.parent.Label_Ant_ComboBox.activated.connect(self.update_bp_plot)
        self.parent.Label_Individual_ComboBox.activated.connect(self.update_ind_plot)
        # button
        self.parent.Label_Play_Button.clicked.connect(self.toggle_play)
        self.parent.Label_Add_Button.clicked.connect(self.add_behavior_key)
        self.parent.Label_Enter_Button.clicked.connect(self.add_behavior)
        self.parent.Label_Left_Button.clicked.connect(self.left_button_clicked)
        self.parent.Label_Right_Button.clicked.connect(self.right_button_clicked)
        self.parent.Export_Ethogram_Button.clicked.connect(self.export_ethogram)
        self.parent.LabelLoadTotPlot.clicked.connect(self.update_tot_plot)
        # slider
        self.parent.Label_HSlider.sliderMoved.connect(self.setFrame)
        self.parent.speed_spinbox.valueChanged.connect(self.setSpeed)
        # shortcut
        QShortcut(QKeySequence("Alt+Space"), self.parent.centralwidget, self.toggle_play)
    def init_plot(self):
        # append bodypoint
        self.BPcanvas = BP_Canvas()
        self.parent.Label_Ant_Layout.addWidget(self.BPcanvas)
        # append individual plot
        self.IndDensityCanvas = Ind_Canvas()
        self.parent.Label_Individual_Layout.addWidget(self.IndDensityCanvas)
        # append ethogram plot
        self.EthogramCanvas = Ethogram_Canvas()
        self.parent.Ethogram_VerticalLayout.addWidget(self.EthogramCanvas)
        # append total plot
        self.TotDensityCanvas = Tot_Canvas()
        self.parent.Label_Population_Layout.addWidget(self.TotDensityCanvas)
    
# ***** event listener function *****
    def update_filename_change(self, index):
        # search selected folder path
        self.cur_folder_key = self.parent.Label_Filename_ComboBox.currentText()
        row = self.parent.main_df.loc[ self.parent.main_df['folder_key']==self.cur_folder_key ]
        folder_path = row["folder_path"].values.item()
        # finds individual files in folder key
        DLC_list = glob.glob(folder_path+"/"+self.cur_folder_key+"*.h5")
        embed_list, file_type = findEmbedDir(folder = folder_path)
        video_list = findVideoDir(folder = folder_path)
        # check and assign directory
        if len(DLC_list)==1: self.cur_DLC_dir = DLC_list[0]
        if len(embed_list)==1: self.cur_embed_dir = embed_list[0]
        if len(video_list)==1: self.cur_video_dir = video_list[0]
        # compute cluster
        if file_type == "npy":
            embed_data = np.load(self.cur_embed_dir)
        elif file_type == "mat":
            embed_data = sio.loadmat(self.cur_embed_dir)['embed_values_i']
        else:
            embed_data = []
        label_data, label_prob = gmm(embed_data)
        # update individual canvas
        self.update_bp_plot()
        self.update_ind_plot(embed_data, label_data, label_prob)
        self.update_ethogram_plot(label_data, label_prob)
        self._update_display() 
    def update_tot_plot(self):
        mode = self.parent.Label_Population_ComboBox.currentText()
        tot_dir = self.parent.main_df['folder_path'].to_numpy()
        embed = None
        # combine all data
        for directory in tot_dir:
            embed_list, file_type = findEmbedDir(folder = directory)
            if file_type == "npy":
                data_i = np.load(embed_list[0])
            elif file_type == "mat":
                data_i = sio.loadmat(embed_list[0])['embed_values_i']
            else:
                data_i = []
            embed = np.vstack((embed, data_i)) if embed is not None else data_i

        if len(tot_dir)!=0:
            self.TotDensityCanvas.setup_canvas(embed=embed, mode=mode)
            self.parent.repaint()
        else:
            QMessageBox.warning(None,"warning", "cannot get all total data")
# update individual canvas
    def update_bp_plot(self):
        Label_Ant_Mode = self.parent.Label_Ant_ComboBox.currentText()
        if Label_Ant_Mode == "Skeleton":
            self.BPcanvas.setup_canvas(self.cur_video_dir, self.cur_DLC_dir, mode="Skeleton")
        elif Label_Ant_Mode == "Skeleton + Video":
            self.BPcanvas.setup_canvas(self.cur_video_dir, self.cur_DLC_dir, mode="Skeleton + Video")
        elif Label_Ant_Mode == "Video":
            self.BPcanvas.setup_canvas(self.cur_video_dir, self.cur_DLC_dir, mode="Video")
    def update_ind_plot(self, embed_data, label_data, label_prob):
        Label_Individual_Mode = self.parent.Label_Individual_ComboBox.currentText()
        if Label_Individual_Mode == "Points (HDBSCAN)":
            self.IndDensityCanvas.setup_canvas(
                embed=embed_data, 
                label=label_data,
                prob=label_prob,
                mode="Points (HDBSCAN)")
    def update_ethogram_plot(self, label_data, label_prob):
        cluster_id = self.EthogramCanvas.setup_canvas(label_data, label_prob)
        self.parent.Cluster_idx_value.setText(str(cluster_id))

# add behavior functionality
    def add_behavior_key(self):
        behavior = self.parent.Label_Add_Behavior_LineEdit.text()
        # update widgets with new behavior
        self.parent.Label_Add_Behavior_LineEdit.setText("")
        self.parent.Label_Behavior_ComboBox.addItem(behavior)
        self.parent.Label_Add_Behavior_LineEdit.repaint()
        # store in dataframe
        self.parent.beh_key_df=self.parent.beh_key_df.append({'behavior': behavior}, ignore_index=True)
    def add_behavior(self):
        folder_key = self.parent.Label_Filename_ComboBox.currentText()
        behavior = self.parent.Label_Behavior_ComboBox.currentText()
        if behavior != "" and folder_key != "":
            # get ui info
            cluster_id = self.parent.Cluster_idx_value.text()
            start_fr = self.parent.Label_Start_Frame.value()
            stop_fr = self.parent.Label_Stop_Frame.value()
            comment = self.parent.Label_Comment_TextEdit.toPlainText()
            # reset input box
            self.parent.Label_Start_Frame.setValue(0)
            self.parent.Label_Stop_Frame.setValue(0)
            self.parent.Label_Comment_TextEdit.setPlainText("")
            self.parent.Label_Comment_TextEdit.repaint()
            # store in dataframe
            self.parent.beh_df = self.parent.beh_df.append({
                'folder_key': folder_key,
                'cluster_id': int(cluster_id),
                'behavior': behavior, 
                'start_fr': start_fr, 
                'stop_fr': stop_fr, 
                'comment': comment
                }, ignore_index=True)
            # update other Tabs
            self.parent.BehaviorsTab.setup_table()
            self.parent.PreviewTab.setup_widgets()
        else:
            QMessageBox.warning(None,"warning", "input a folder_key and/or behavior")
# export data
    def export_ethogram(self):
        dir_csv = os.getcwd()+"/ethogram.csv"
        filepath = QFileDialog.getSaveFileName(self.parent, "Export Ethogram Data", dir_csv ,"CSV(*.csv)")[0]
        if filepath != "":
            (num_bp, num_dim, num_fr) = self.BPcanvas.data.shape
            # get ethogram data
            df_etho = pd.DataFrame(self.EthogramCanvas.label)
            df_etho.columns = ["ethogram"]
            # get bodypoint data
            df_bp = pd.DataFrame(self.BPcanvas.data.reshape(num_bp*num_dim, num_fr).T)
            bp_header = []
            for bp in range(num_bp):
                bp_header.extend(["bp "+str(bp)+" x", "bp "+str(bp)+" y", "bp "+str(bp)+" prob"])
            df_bp.columns = bp_header
            # combine and save data
            df_comb = pd.concat([df_etho, df_bp], axis=1)
            df_comb.to_csv(filepath, index=False)
    
# ***** helper function *****  
    def _update_display(self):
        # update slider
        self.parent.Label_HSlider.setMinimum(0)
        self.parent.Label_HSlider.setMaximum(self.EthogramCanvas.num_frame-1)
        self.parent.Label_HSlider.setValue(0)
        # update frame label
        self.parent.Label_Frame_Number_Label.setText("{}/{}".format(0,self.EthogramCanvas.num_frame-1))
    
# ***** animation listener function *****
    def toggle_play(self):
        if self.cur_folder_key:
            if self.timer != None:
                self.timer.stop()
                self.timer = None
            else:
                self.timer = QTimer()
                self.timer.timeout.connect(self.nextFrameSlot)
                self.timer.start(100/self.speed)
        else:
            QMessageBox.warning(None,"warning", "Click a file you want to see")
    def left_button_clicked(self):
        if self.cur_folder_key is None:
            choice = QMessageBox.warning(None,"warning", "Select a file you would like to use")
        else:
            self.previousFrameSlot()
            self.parent.repaint()
    def right_button_clicked(self):
        if self.cur_folder_key is None:
            choice = QMessageBox.warning(None,"warning", "Select a file you would like to use")
        else:
            self.nextFrameSlot()
            self.parent.repaint()
    def previousFrameSlot(self):
        error_ethogram, frame, cluster_id = self.EthogramCanvas.previous_frame()
        error_bp, _ = self.BPcanvas.previous_frame()
        error_ind, _ = self.IndDensityCanvas.previous_frame()
        self.parent.Label_Frame_Number_Label.setText("{}/{}".format(frame,self.EthogramCanvas.num_frame-1))
        self.parent.Label_HSlider.setValue(frame)
        self.parent.Cluster_idx_value.setText(str(cluster_id))
        if self.timer!=None and (error_ethogram or error_bp or error_ind):
            self.timer.stop()
            self.timer = None
        pass
    def nextFrameSlot(self):
        # update GUI with next frame
        error_ethogram, frame, cluster_id  = self.EthogramCanvas.next_frame()
        error_bp, _ = self.BPcanvas.next_frame()
        error_ind, _ = self.IndDensityCanvas.next_frame()
        self.parent.Label_Frame_Number_Label.setText("{}/{}".format(frame,self.EthogramCanvas.num_frame-1))
        self.parent.Label_HSlider.setValue(frame)
        self.parent.Cluster_idx_value.setText(str(cluster_id))
        if self.timer!=None and (error_ethogram or error_bp or error_ind):
            self.timer.stop()
            self.timer = None
        pass
    def setFrame(self, frame):
        print(frame)
        if self.cur_folder_key is None:
            choice = QMessageBox.warning(None,"warning", "Select a file you would like to use")
        else:
            # stop timer for movie
            if self.timer != None:
                self.timer.stop()
                self.timer = None
            error_eth, _, cluster_id = self.EthogramCanvas.set_frame(frame)
            error_bp, _ = self.BPcanvas.set_frame(frame)
            error_ind, _ = self.IndDensityCanvas.set_frame(frame)
            self.parent.Label_Frame_Number_Label.setText("{}/{}".format(frame,self.EthogramCanvas.num_frame-1))
            self.parent.Cluster_idx_value.setText(str(cluster_id))
        pass
    def setSpeed(self, speed):
        if self.timer != None:
            self.timer.stop()
            self.timer = None
        self.speed=speed
        pass














