import numpy as np 
import glob

from PyQt5.QtCore import QTimer
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget

from widgets.BP_Canvas import BP_Canvas
from widgets.tsne_Graph import tsne_Graph
from widgets.Density_Canvas import Density_Canvas
from widgets.Individual_Canvas import Individual_Canvas
from widgets.Total_Canvas import Total_Canvas
from widgets.Ethogram import Ethogram

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas

from tools.DataConv import h5_to_npy, npy_to_h5


class Label_Tab():
    def __init__(self, parent):
        self.parent = parent
        self.cur_folder_key = None
        self.cur_embed_dir = None
        self.cur_ind_density_dir = None
        self.cur_tot_density_dir = None
        self.cur_video_dir = None
        self.cluster_dir = None
        self.timer = None
        self.update_widgets()
        self.setup_connection()
        self.init_plot()
        pass
    def update_widgets(self):
        self.parent.Label_Filename_ComboBox.addItems(self.parent.main_df['folder_key'])
        pass
    def setup_connection(self):
        self.parent.Label_Filename_ComboBox.currentIndexChanged.connect(
            self.filename_combobox_change)
        self.parent.Label_Ant_ComboBox.currentIndexChanged.connect(
            self.setup_ant_plot)
        self.parent.Label_Individual_ComboBox.currentIndexChanged.connect(
            self.update_ind_plot)
        self.parent.Label_Population_ComboBox.currentIndexChanged.connect(
            self.update_tot_plot)
        self.parent.Label_Play_Button.clicked.connect(self.toggle_play)
        pass
    def init_plot(self):
        # append bodypoint
        self.BPcanvas = BP_Canvas()
        self.parent.Label_Ant_Layout.addWidget(self.BPcanvas)
        # append individual density plot
        self.IndDensityCanvas = Individual_Canvas()
        self.parent.Label_Individual_Layout.addWidget(self.IndDensityCanvas)
        # append total density plot
        self.TotDensityCanvas = Total_Canvas()
        self.parent.Label_Population_Layout.addWidget(self.TotDensityCanvas)
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
        tot_density_list = glob.glob(folder_path+"/total*.fig")
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
        if len(ind_density_list)==1:
            self.cur_ind_density_dir = ind_density_list[0]
        if len(tot_density_list)==1:
            self.cur_tot_density_dir = tot_density_list[0]
        if len(video_list)==1:
            self.cur_video_dir = video_list[0]
        if len(Watershed_list)==1:
            self.cur_watershed_dir = Watershed_list[0]
        if len(Cluster_list)==1:
            self.cluster_dir = Cluster_list[0]
        # populate plot
        self.setup_ant_plot()
        self.update_ind_plot()
        self.update_tot_plot()
        self.EthogramCanvas.setup_canvas(self.cluster_dir)
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
        Label_Individual_Mode = self.parent.Label_Individual_ComboBox.currentText()
        if Label_Individual_Mode == "Points (HDBSCAN)":
            self.IndDensityCanvas.setup_canvas(embed=self.cur_embed_dir, cluster=self.cluster_dir, mode="Points (HDBSCAN)")
        else:
            print(":: No Individual Plot Mode")
        pass
    def update_tot_plot(self):
        Label_Population_Mode = self.parent.Label_Population_ComboBox.currentText()
        tot_dir = self.parent.main_df['folder_path'].to_numpy()
        if Label_Population_Mode == "HDBSCAN Cluster":
            self.TotDensityCanvas.setup_canvas(tot_dir, mode="HDBSCAN Cluster")
        elif Label_Population_Mode == "Density":
            self.TotDensityCanvas.setup_canvas(tot_dir, mode="Density")
        else:
            print(":: No Total tSNE Plot Mode")
        pass

    def toggle_play(self):
        if self.timer != None:
            self.timer.stop()
            self.timer = None
        else:
            self.timer = QTimer()
            self.timer.timeout.connect(self.nextFrameSlot)
            self.timer.start(100)
        pass
    def nextFrameSlot(self):
        error_ethogram = self.EthogramCanvas.next_frame()
        error_bp = self.BPcanvas.next_frame()
        error_ind = self.IndDensityCanvas.next_frame()
        if error_ethogram or error_bp or error_ind:
            self.timer.stop()
        pass




















