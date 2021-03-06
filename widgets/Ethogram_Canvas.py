import numpy as np
import pandas as pd
import os
import seaborn as sns

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle
from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt

from PyQt5.QtWidgets import QWidget


class Ethogram_Canvas(FigureCanvas):
    def __init__(self, *args, **kwargs):
        self.fig = plt.figure()
        super(FigureCanvas, self).__init__(self.fig)
        self.ax = self.fig.add_subplot(111)
        self.ax.get_yaxis().set_visible(False)
        plt.tight_layout(pad=-1)
        self.label = None # num_cluster (n)
        self.frame = 0
        self.num_frame = None
        self.start_idx = 0
    def setup_canvas(self, label, prob):
        self.label, self.prob = label, prob
        self.num_frame = self.label.shape[0]
        self.start_idx = 0
        # format cluster color
        num_cluster = np.max(self.label)+1
        color_palette = sns.color_palette('hls', num_cluster)
        cluster_colors = [color_palette[x] if x >= 0 else (0.5, 0.5, 0.5) for x in self.label]
        self.color_palette = np.insert(color_palette, 0, (0.5, 0.5, 0.5), axis=0)
        self.cmap = ListedColormap(self.color_palette)
        # update/init ethogram canvas
        self.update_canvas()
        return self.label[0]
    def update_canvas(self, frame=0):
        self.frame = frame
        self.ax.clear()
        xlim_min, xlim_max = frame-40, frame+40
        start = xlim_min if xlim_min >= 0 else 0
        stop = xlim_max if xlim_max <= self.num_frame else self.num_frame 
        self.ax.imshow([self.label[start:stop]], 
            cmap=self.cmap, 
            vmin=np.min(self.label), 
            vmax=np.max(self.label), 
            extent=(start, stop, 0, 1))
        self.ax.axvline(x=frame+0.5, color='r', linewidth=4)
        self.ax.set_xlim(left=xlim_min, right=xlim_max)
        self.ax.get_yaxis().set_visible(False)
        self.ax.tick_params(axis="x", which="minor", width=10)
        self.draw()
        pass
    def next_frame(self):
        # check if next frame exist
        if self.frame+1 >= self.num_frame:
            error=True
            cluster_id = self.label[self.frame]
            return error, self.frame, cluster_id
        else:
            error=False
            cluster_id = self.label[self.frame+1]
            self.update_canvas(self.frame+1)
            return error, self.frame, cluster_id
    def previous_frame(self):
        if self.frame-1 < 0:
            error=True
            cluster_id = self.label[self.frame]
            return error, self.frame, cluster_id
        else:
            cluster_id = self.label[self.frame-1]
            self.update_canvas(self.frame-1)
            error=False
            return error, self.frame, cluster_id
    def set_frame(self, frame):
        if frame >= self.num_frame:
            error=True
        else:
            self.update_canvas(frame)
            error=False
        return error, self.frame, self.label[frame]






