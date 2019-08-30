import numpy as np 
import glob

from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget

from widgets.BP_Canvas import BP_Canvas
from widgets.tsne_Graph import tsne_Graph
from widgets.Density_Canvas import Density_Canvas

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas

from tools.DataConv import h5_to_npy, npy_to_h5


class Label_Tab():
    def __init__(self, parent):
        self.parent = parent
        self.cur_folder_key = None
        self.cur_tsne_dir = None
        self.cur_ind_density_dir = None
        self.cur_tot_density_dir = None
        self.cur_video_dir = None
        self.setup_connection()
    def setup(self):
        self.init_plot()
        self.update_widgets()

        pass
    def update_widgets(self):
        self.parent.Label_Filename_ComboBox.addItems(self.parent.main_df['folder_key'])
        pass
    def setup_connection(self):
        self.parent.Label_Filename_ComboBox.currentIndexChanged.connect(
            self.filename_combobox_change)
        self.parent.Label_Ant_ComboBox.currentIndexChanged.connect(
            self.update_ant_plot)
        self.parent.Label_Individual_ComboBox.currentIndexChanged.connect(
            self.update_ind_tSNE_plot)
        self.parent.Label_Population_ComboBox.currentIndexChanged.connect(
            self.update_tot_tSNE_plot)
        
        pass
    def filename_combobox_change(self, i):
        self.cur_folder_key = self.parent.Label_Filename_ComboBox.currentText()
        row = self.parent.main_df.loc[self.parent.main_df['folder_key']==self.cur_folder_key]
        folder_path = row["folder_path"].values.item()
        # finds individual files in folder key
        DLC_list = glob.glob(folder_path+"/"+self.cur_folder_key+"*.h5")
        BP_list = glob.glob(folder_path+"/BP*.npy")
        tsne_list = glob.glob(folder_path+"/EMBED.mat")
        ind_density_list = glob.glob(folder_path+"/indiv*.fig")
        tot_density_list = glob.glob(folder_path+"/total*.fig")
        video_list = glob.glob(folder_path+"/"+self.cur_folder_key+"*.avi")
        Watershed_list = glob.glob(folder_path+"/Watershed.mat")
        # check and assign directory
        if len(DLC_list)==1:
            self.cur_DLC_dir = DLC_list[0]
        if len(BP_list)==1:
            self.cur_bp_dir = BP_list[0]
        if len(tsne_list)==1:
            self.cur_tsne_dir = tsne_list[0]
        if len(ind_density_list)==1:
            self.cur_ind_density_dir = ind_density_list[0]
        if len(tot_density_list)==1:
            self.cur_tot_density_dir = tot_density_list[0]
        if len(video_list)==1:
            self.cur_video_dir = video_list[0]
        if len(Watershed_list)==1:
            self.cur_watershed_dir = Watershed_list[0]
        # print(self.cur_DLC_dir, self.cur_bp_dir, self.cur_tsne_dir, 
        #     self.cur_ind_density_dir, self.cur_tot_density_dir, self.cur_video_dir)
        self.update_ant_plot()
        self.update_ind_tSNE_plot()
        self.update_tot_tSNE_plot()
        pass
    def init_plot(self):
        # append bodypoint
        self.BPcanvas = BP_Canvas()
        self.parent.Label_Ant_Layout.addWidget(self.BPcanvas)
        # append tsne plot
        # self.tsneGraph = tsne_Graph()
        # self.tsnecanvas = FigureCanvas(self.tsneGraph)
        # self.tsneGraph.init_plot()
        # self.parent.Label_Individual_Layout.addWidget(self.tsnecanvas)
        # append individual density plot
        self.IndDensityCanvas = Density_Canvas() # individual density graph
        self.parent.Label_Individual_Layout.addWidget(self.IndDensityCanvas)
        # append total density plot
        self.TotDensityCanvas = Density_Canvas() # individual density graph
        self.parent.Label_Population_Layout.addWidget(self.TotDensityCanvas)
    def update_ant_plot(self):
        Label_Ant_Mode = self.parent.Label_Ant_ComboBox.currentText()
        if Label_Ant_Mode == "Skeleton":
            self.BPcanvas.setup_canvas(self.cur_video_dir, self.cur_DLC_dir, mode="Skeleton")
            self.BPcanvas.update_canvas(frame=1000)
        elif Label_Ant_Mode == "Skeleton + Video":
            self.BPcanvas.setup_canvas(self.cur_video_dir, self.cur_DLC_dir, mode="Skeleton + Video")
            self.BPcanvas.update_canvas(frame=1000)
        elif Label_Ant_Mode == "Video":
            self.BPcanvas.setup_canvas(self.cur_video_dir, self.cur_DLC_dir, mode="Video")
            self.BPcanvas.update_canvas(frame=1000)
        # elif Label_Ant_Mode == "Video":
            # Append MediaPlayer Graph
            # self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
            # videoWidget = QVideoWidget()
            # self.Label_Ant_Layout.addWidget(videoWidget)
            # self.mediaPlayer.setVideoOutput(videoWidget)
            # self.mediaPlayer.positionChanged.connect(self.positionChanged)
            # self.mediaPlayer.durationChanged.connect(self.durationChanged)
            # self.mediaPlayer.setNotifyInterval(int(1000/self.fr))
            # self.mediaPlayer.setPlaybackRate(0.3)
        else:
            print(":: No Ant Plot Mode")
        pass
    def update_ind_tSNE_plot(self):
        # Label_Individual_Mode = self.parent.Label_Individual_ComboBox.currentText()
        # if Label_Individual_Mode == "Points":
        #     # Append tSNE graph
            
        # elif Label_Individual_Mode == "Points + Density":
        #     # Append tSNE graph
        #     # Append Density Graph
        # elif Label_Individual_Mode == "Points + Watershed":
        #     # Append tSNE graph
        # elif Label_Individual_Mode == "Points + Density + Watershed":
        #     # Append tSNE graph
        #     # Append Density Graph
            
        # else:
        #     print(":: No Individual Plot Mode")
        pass
    def update_tot_tSNE_plot(self):
        Label_Population_Mode = self.parent.Label_Population_ComboBox.currentText()
        print("YOOOOOOOOOOOOO")
        if Label_Population_Mode == "Density":
            self.TotDensityCanvas.setup_canvas(self.cur_tot_density_dir, self.cur_watershed_dir, 
                mode="Density")
            self.TotDensityCanvas.update_canvas()
        elif Label_Population_Mode == "Density + Watershed":
            self.TotDensityCanvas.setup_canvas(self.cur_tot_density_dir, self.cur_watershed_dir, 
                mode="Density + Watershed")
        else:
            print(":: No Total tSNE Plot Mode")
        pass























