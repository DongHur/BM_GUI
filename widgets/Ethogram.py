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


class Ethogram(FigureCanvas):
    def __init__(self, *args, **kwargs):
        self.fig = plt.figure()
        super(FigureCanvas, self).__init__(self.fig)
        self.ax = self.fig.add_subplot(111)
        self.ax.get_yaxis().set_visible(False)
        plt.tight_layout(pad=-1)
        self.label_data = None # num_cluster (n)
        self.frame = 0
        self.vmin, self.vmax = 0,0
        self.num_frame = None
    def setup_canvas(self, cluster_dir):
        self.label_data = np.load(cluster_dir)
        self.num_frame = self.label_data.shape[0]
        self.vmin, self.vmax = np.min(self.label_data), np.max(self.label_data)
        # format cluster color
        num_cluster = np.max(self.label_data)+1
        color_palette = sns.color_palette('hls', num_cluster)
        cluster_colors = [color_palette[x] if x >= 0 else (0.5, 0.5, 0.5) for x in self.label_data]
        self.color_palette = np.insert(color_palette, 0, (0.5, 0.5, 0.5), axis=0)
        self.cmap = ListedColormap(self.color_palette)
        self.update_canvas()
        pass
    def update_canvas(self, frame=0):
        self.frame = frame
        self.ax.clear()
        xlim_min, xlim_max = frame-40, frame+40
        start = xlim_min if xlim_min >= 0 else 0
        stop = xlim_max if xlim_max <= self.num_frame else self.num_frame 
        self.ax.imshow([self.label_data[start:stop]], cmap=self.cmap, vmin=self.vmin, vmax=self.vmax, extent=(start, stop, 0, 1))
        self.ax.axvline(x=frame, color='r', linewidth=4)
        self.ax.set_xlim(left=xlim_min, right=xlim_max)
        self.ax.get_yaxis().set_visible(False)
        self.draw()
        pass
    def next_frame(self):
        if self.frame >= self.num_frame:
            error=True
        else:
            self.update_canvas(self.frame+1)
            error=False
        return error






