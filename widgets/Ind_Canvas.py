import numpy as np
import scipy.io as sio
import seaborn as sns

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.ticker

class Ind_Canvas(FigureCanvas):
    def __init__(self, *args, **kwargs):
        self.fig = Figure()
        super(FigureCanvas, self).__init__(self.fig)
        self.ax = self.fig.add_subplot(111)
        self.data = None
        self.frame = 0
        self.num_frame = None
        self.mode = ""
        self.xlim, self.ylim = (-100, 100), (-100, 100)
        self.cluster_colors = None
    def setup_canvas(self, embed, cluster, mode=""):
        self.mode = mode
        if mode == "Points (HDBSCAN)":
            self.embed_data = sio.loadmat(embed)['embed_values_i']
            self.label_data = np.load(cluster)
            # format cluster color
            num_cluster = np.max(self.label_data)+1
            color_palette = sns.color_palette('hls', num_cluster)
            self.cluster_colors = [color_palette[x] if x >= 0 else (0.5, 0.5, 0.5) for x in self.label_data]
            # self.cluster_member_colors = np.array([sns.desaturate(x, p) for x, p in zip(cluster_colors, clusterer.probabilities_)])
        self.num_frame = self.embed_data.shape[0]
        self.xlim = (-1.1*np.max(self.embed_data), 1.1*np.max(self.embed_data))
        self.ylim = (-1.1*np.max(self.embed_data), 1.1*np.max(self.embed_data))
        self.update_canvas()
        pass
    def update_canvas(self, frame=0):
        self.frame = frame
        self.ax.clear()
        self.ax.set_xlim(left=self.xlim[0], right=self.xlim[1])
        self.ax.set_ylim(bottom=self.ylim[0], top=self.ylim[1])
        self.ax.grid(True, 'both')
        if self.mode == "Points (HDBSCAN)":
            self.ax.scatter(self.embed_data[:frame,0], self.embed_data[:frame,1], s=5, c=self.cluster_colors[:frame])
            self.ax.scatter(self.embed_data[frame,0], self.embed_data[frame,1], s=10, c='r')
        self.draw()
        pass
    def next_frame(self):
        if self.frame+1 >= self.num_frame:
            error=True
        else:
            self.update_canvas(self.frame+1)
            error=False
        return error, self.frame
    def previous_frame(self):
        if self.frame-1 < 0:
            error=True
        else:
            self.update_canvas(self.frame-1)
            error=False
        return error, self.frame
    def set_frame(self, frame):
        if frame >= self.num_frame:
            error=True
        else:
            self.update_canvas(frame)
            error=False
        return error, self.frame






