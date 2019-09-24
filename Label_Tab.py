import numpy as np 
import glob

from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import QTimer
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QShortcut, QMessageBox


from widgets.BP_Canvas import BP_Canvas
from widgets.tsne_Graph import tsne_Graph
from widgets.Density_Canvas import Density_Canvas
from widgets.Individual_Canvas import Individual_Canvas
from widgets.Ethogram import Ethogram

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas

class Label_Tab():
    def __init__(self, parent):
        self.parent = parent
        self.cur_folder_key = None
        self.cur_embed_dir = None
        self.cur_ind_density_dir = None
        self.cur_video_dir = None
        self.cluster_dir = None
        self.timer = None
        self.speed = 1
        self.update_widgets()
        self.setup_connection()
        self.init_plot()
        self.setup_shortcut()
        pass
    def update_widgets(self):
        self.parent.Label_Filename_ComboBox.addItems(self.parent.main_df['folder_key'])
        self.parent.Label_Behavior_ComboBox.addItems(self.parent.beh_key_df['behavior'])
        pass
    def setup_connection(self):
        # setup dropdown
        self.parent.Label_Filename_ComboBox.activated.connect(
            self.filename_combobox_change)
        self.parent.Label_Ant_ComboBox.activated.connect(
            self.setup_ant_plot)
        self.parent.Label_Individual_ComboBox.activated.connect(
            self.update_ind_plot)
        # setup button
        self.parent.Label_Play_Button.clicked.connect(self.toggle_play)
        self.parent.Label_Add_Button.clicked.connect(self.add_behavior_key)
        self.parent.Label_Enter_Button.clicked.connect(self.add_behavior)
        self.parent.Label_Left_Button.clicked.connect(self.left_button_clicked)
        self.parent.Label_Right_Button.clicked.connect(self.right_button_clicked)
        # setup slider
        self.parent.Label_HSlider.sliderMoved.connect(self.setFrame)
        self.parent.speed_spinbox.valueChanged.connect(self.setSpeed)
        pass
    def setup_shortcut(self):
        QShortcut(QKeySequence("Alt+Space"), self.parent.centralwidget, self.toggle_play)
        pass
    def init_plot(self):
        # append bodypoint
        self.BPcanvas = BP_Canvas()
        self.parent.Label_Ant_Layout.addWidget(self.BPcanvas)
        # append individual density plot
        self.IndDensityCanvas = Individual_Canvas()
        self.parent.Label_Individual_Layout.addWidget(self.IndDensityCanvas)
        # append ethogram plot
        self.EthogramCanvas = Ethogram()
        self.parent.Ethogram_VerticalLayout.addWidget(self.EthogramCanvas)
    
    def filename_combobox_change(self, index):
        self.cur_folder_key = self.parent.Label_Filename_ComboBox.currentText()
        row = self.parent.main_df.loc[self.parent.main_df['folder_key']==self.cur_folder_key]
        folder_path = row["folder_path"].values.item()
        # finds individual files in folder key
        DLC_list = glob.glob(folder_path+"/"+self.cur_folder_key+"*.h5")
        BP_list = glob.glob(folder_path+"/BP*.npy")
        embed_list = glob.glob(folder_path+"/EMBED.mat")
        ind_density_list = glob.glob(folder_path+"/indiv*.fig")
        video_list = glob.glob(folder_path+"/"+self.cur_folder_key+"*.avi")
        Watershed_list = glob.glob(folder_path+"/Watershed.mat")
        Cluster_list = glob.glob(folder_path+"/cluster.npy")
        # check and assign directory
        if len(DLC_list)==1:
            self.cur_DLC_dir = DLC_list[0]
        if len(BP_list)==1:
            self.cur_bp_dir = BP_list[0]
        if len(embed_list)==1:
            self.cur_embed_dir = embed_list[0]
        if len(video_list)==1:
            self.cur_video_dir = video_list[0]
        if len(Cluster_list)==1:
            self.cluster_dir = Cluster_list[0]
        # populate plot
        self.setup_ant_plot()
        self.update_ind_plot()
        self.EthogramCanvas.setup_canvas(self.cluster_dir)
        # update slider
        self.parent.Label_HSlider.setMinimum(0)
        self.parent.Label_HSlider.setMaximum(self.EthogramCanvas.num_frame-1)
        self.parent.Label_HSlider.setValue(0)
        # update frame label
        self.parent.Label_Frame_Number_Label.setText("{}/{}".format(0,self.EthogramCanvas.num_frame-1))
        pass
        
    def setup_ant_plot(self):
        Label_Ant_Mode = self.parent.Label_Ant_ComboBox.currentText()
        if Label_Ant_Mode == "Skeleton":
            self.BPcanvas.setup_canvas(self.cur_video_dir, self.cur_DLC_dir, mode="Skeleton")
        elif Label_Ant_Mode == "Skeleton + Video":
            self.BPcanvas.setup_canvas(self.cur_video_dir, self.cur_DLC_dir, mode="Skeleton + Video")
        elif Label_Ant_Mode == "Video":
            self.BPcanvas.setup_canvas(self.cur_video_dir, self.cur_DLC_dir, mode="Video")
        else:
            print(":: No Ant Plot Mode")
        pass
    def update_ind_plot(self):
        # extract parameter based on ui
        Label_Individual_Mode = self.parent.Label_Individual_ComboBox.currentText()
        # populate proper figure
        if Label_Individual_Mode == "Points (HDBSCAN)":
            self.IndDensityCanvas.setup_canvas(
                embed = self.cur_embed_dir, 
                cluster = self.cluster_dir, 
                mode = "Points (HDBSCAN)")
        else:
            print(":: No Individual Plot Mode")
        pass

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
            # verify if user wants to delete
            choice = QMessageBox.warning(None,"warning", "Click a file you want to see")
        pass
    def left_button_clicked(self):
        if self.cur_folder_key is None:
            choice = QMessageBox.warning(None,"warning", "Select a file you would like to use")
        else:
            self.previousFrameSlot()
            self.parent.repaint()
        pass
    def right_button_clicked(self):
        if self.cur_folder_key is None:
            choice = QMessageBox.warning(None,"warning", "Select a file you would like to use")
        else:
            self.nextFrameSlot()
            self.parent.repaint()
        pass
    def previousFrameSlot(self):
        error_ethogram, frame = self.EthogramCanvas.previous_frame()
        error_bp, _ = self.BPcanvas.previous_frame()
        error_ind, _ = self.IndDensityCanvas.previous_frame()
        self.parent.Label_Frame_Number_Label.setText("{}/{}".format(frame,self.EthogramCanvas.num_frame-1))
        self.parent.Label_HSlider.setValue(frame)
        if error_ethogram or error_bp or error_ind:
            self.timer.stop()
            self.timer = None
        pass
    def nextFrameSlot(self):
        error_ethogram, frame = self.EthogramCanvas.next_frame()
        error_bp, _ = self.BPcanvas.next_frame()
        error_ind, _ = self.IndDensityCanvas.next_frame()
        self.parent.Label_Frame_Number_Label.setText("{}/{}".format(frame,self.EthogramCanvas.num_frame-1))
        self.parent.Label_HSlider.setValue(frame)
        if error_ethogram or error_bp or error_ind:
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
            error_eth, _ = self.EthogramCanvas.set_frame(frame)
            error_bp, _ = self.BPcanvas.set_frame(frame)
            error_ind, _ = self.IndDensityCanvas.set_frame(frame)
            self.parent.Label_Frame_Number_Label.setText("{}/{}".format(frame,self.EthogramCanvas.num_frame-1))
        pass
    def setSpeed(self, speed):
        if self.timer != None:
            self.timer.stop()
            self.timer = None
        self.speed=speed
        pass
    # Add behavior
    def add_behavior_key(self):
        behavior = self.parent.Label_Add_Behavior_LineEdit.text()
        self.parent.Label_Add_Behavior_LineEdit.setText("")
        self.parent.Label_Add_Behavior_LineEdit.repaint()
        # add to other widgets
        self.parent.Label_Behavior_ComboBox.addItem(behavior)
        # store in dataframe
        self.parent.beh_key_df=self.parent.beh_key_df.append({'behavior': behavior}, ignore_index=True)
        print(behavior)
        pass
    def add_behavior(self):
        folder_key = self.parent.Label_Filename_ComboBox.currentText()
        behavior = self.parent.Label_Behavior_ComboBox.currentText()
        if behavior == "":
            choice = QMessageBox.warning(None,"warning", "Input a behavior")
        if self.cur_folder_key is None or folder_key == "":
            choice = QMessageBox.warning(None,"warning", "Select a file you would like to use")
        else:
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
                'behavior': behavior, 
                'start_fr': start_fr, 
                'stop_fr': stop_fr, 
                'comment': comment
                }, ignore_index=True)
            # update other tabs
            self.parent.update_behavior_tabs()
        pass

















