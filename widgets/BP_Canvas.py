import numpy as np
import pandas as pd
import cv2
import os

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.image as mpimg

from PyQt5.QtWidgets import QWidget


class BP_Canvas(FigureCanvas):
    def __init__(self, *args, **kwargs):
        self.fig = Figure()
        super(BP_Canvas, self).__init__(self.fig)
        self.ax = self.fig.add_subplot(111)
        self.mode = None
        self.data = None
        self.num_frame, self.num_bp, self.num_dim = 0, 30, 3
        self.perc = 0
        self.cur_frame = 0
    def setup_canvas(self, video_dir, DLC_dir, mode="Skeleton"):
        self.mode = mode
        if mode == "Skeleton":
            # setup DeepLabCut
            store = pd.HDFStore(DLC_dir, mode='r')
            df = store['df_with_missing']
            self.num_bp = len(list(df.columns.levels[1]))
            self.num_dim = len(list(df.columns.levels[2]))
            self.num_frame = len(df)
            self.data = df.T.to_numpy().reshape(self.num_bp, self.num_dim, self.num_frame) # num_bp x num_coord x frame
            store.close()
        elif mode == "Skeleton + Video":
            # setup DeepLabCut
            store = pd.HDFStore(DLC_dir, mode='r')
            df = store['df_with_missing']
            self.num_bp = len(list(df.columns.levels[1]))
            self.num_dim = len(list(df.columns.levels[2]))
            self.num_frame = len(df)
            self.data = df.T.to_numpy().reshape(self.num_bp, self.num_dim, self.num_frame) # num_bp x num_coord x frame
            store.close()
            # setup ant video
            self.cap = cv2.VideoCapture(video_dir)
            self.cap.set(1, 0)
            _, framePic = self.cap.read()
        elif mode == "Video":
            # setup ant video
            self.cap = cv2.VideoCapture(video_dir)
            self.cap.set(1, 0)
            _, framePic = self.cap.read()
        else:
            print(":: Could not recognize mode")
        
        # TODO: setup other mode to take out translational and rotational
        self.update_canvas(frame=self.cur_frame)
        # cap.release()
        pass
    def next_frame(self):
        if self.cur_frame >= self.num_frame-1:
            error=True
        else:
            self.update_canvas(self.cur_frame+1)
            error=False
        return error, self.cur_frame
    def update_canvas(self, frame=0):
        self.ax.clear()
        self.cur_frame = frame
        self.perc = round(np.mean(self.data[:,2,frame])*100, 2)
        if self.mode == "Skeleton":
            # update DeepLabCut
            self.plot_bpgraph(frame)
        elif self.mode == "Skeleton + Video":
            # update DeepLabCut
            self.plot_bpgraph(frame)
            # update ant video
            self.cap.set(1, frame)
            _, framePic = self.cap.read()
            self.ax.imshow(framePic)
        elif self.mode == "Video":
            # update ant video
            self.cap.set(1, frame)
            _, framePic = self.cap.read()
            self.ax.imshow(framePic)
        else:
            print(":: Could not recognize mode")
        self.draw()
        pass
    def plot_bpgraph(self, frame=0):
        # self.fig.clear()
        marker = 'o'
        s=4
        # plot graph
        self.ax.margins(0.8)
        self.ax.get_xaxis().set_visible(False)
        self.ax.get_yaxis().set_visible(False)
        self.ax.plot(self.data[0:4,0,frame], self.data[0:4,1,frame], marker=marker, markersize=s)
        self.ax.plot(self.data[4:8,0,frame], self.data[4:8,1,frame], marker=marker, markersize=s)
        self.ax.plot(self.data[8:11,0,frame], self.data[8:11,1,frame], marker=marker, markersize=s)
        self.ax.plot(self.data[11:14,0,frame], self.data[11:14,1,frame], marker=marker, markersize=s)
        self.ax.plot(self.data[14:17,0,frame], self.data[14:17,1,frame], marker=marker, markersize=s)
        self.ax.plot(self.data[17:21,0,frame], self.data[17:21,1,frame], marker=marker, markersize=s)
        self.ax.plot(self.data[21:24,0,frame], self.data[21:24,1,frame], marker=marker, markersize=s)
        self.ax.plot(self.data[24:27,0,frame], self.data[24:27,1,frame], marker=marker, markersize=s)
        self.ax.plot(self.data[27:30,0,frame], self.data[27:30,1,frame], marker=marker, markersize=s)
        pass











