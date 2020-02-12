import numpy as np
import scipy.io as sio
import seaborn as sns

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.ticker

from tools.GaussConv import GaussConv
from tools.gmm import gmm

class Tot_Canvas(FigureCanvas):
    def __init__(self, *args, **kwargs):
        self.fig = Figure()
        super(FigureCanvas, self).__init__(self.fig)
        self.ax = self.fig.add_subplot(111)
        self.label = None
        self.mode = ""
        self.xlim, self.ylim = (-100, 100), (-100, 100)
        self.color = None
        self.X_H, self.Y_H, self.GH_conv = None, None, None
    
    def setup_canvas(self, embed, mode):
        self.mode = mode
        # set canvas size
        self.num_frame = embed.shape[0]
        self.xlim = (-1.1*np.max(embed), 1.1*np.max(embed))
        self.ylim = (-1.1*np.max(embed), 1.1*np.max(embed))
        # update/init canvas
        self.update_canvas(embed)
    
    def update_canvas(self, embed):
        self.ax.clear()
        if self.mode=="HDBSCAN Cluster":
            # copute clustering 
            self.label, self.prob = gmm(embed)
            # format cluster color
            num_cluster = np.max(self.label)+1
            color_palette = sns.color_palette('hls', num_cluster)
            self.color = [color_palette[x] if x >= 0 else (0.5, 0.5, 0.5) for x in self.label]
            # create graph
            self.ax.set_xlim(left=self.xlim[0], right=self.xlim[1])
            self.ax.set_ylim(bottom=self.ylim[0], top=self.ylim[1])
            self.ax.scatter(embed[:,0], embed[:,1], s=5, c=self.color)
            self.ax.grid(True, 'both')
        elif self.mode=="Density":
            # compute Gaussin Conv
            self.GH_conv, self.X_H, self.Y_H = GaussConv(data=embed)
            # create graph
            self.ax.pcolormesh(self.X_H, self.Y_H, self.GH_conv.T, cmap="jet")
            self.ax.grid(True, 'both')
        self.draw()

    