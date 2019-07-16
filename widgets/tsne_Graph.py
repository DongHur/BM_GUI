import numpy as np
import scipy.io as sio

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

class tsne_Graph(Figure):
    def __init__(self, *args, **kwargs):
        super(tsne_Graph, self).__init__()
        self.tsne_filepath = ''
        self.num_frame = 0
        self.duration = 1
        self.data = None
        self.XLim = (-100,100)
        self.YLim = (-100,100)
    def init_plot(self):
        self.clear()
        ax = self.add_subplot(111)
        ax.plot([], '*-')
        ax.set_title('tSNE Projection', fontsize=8);
        ax.tick_params(axis='both', labelsize=6);
        pass
    def set_newfile(self, filepath):
        self.tsne_filepath = filepath
        self.data = sio.loadmat(filepath)['embed_values_i'] # (frame x 2)
        self.num_frame = self.data.shape[0]
        pass
    def set_duration(self, duration):
        self.duration = duration
        pass
    def set_dim(self, xlim, ylim):
        self.XLim = xlim
        self.YLim = ylim
        pass
    def update_graph(self, position):
        # self.plt.setData(x=self.data[:,0], y=self.data[:,1])
        frame = int(self.num_frame*position/self.duration)-1 # index is one less
        self.clear()
        ax = self.add_subplot(111)
        if frame>0:
            ax.scatter(self.data[:frame-1, 0], self.data[:frame-1, 1], c='b', alpha=0.07)
        ax.scatter(self.data[frame, 0], self.data[frame, 1], c='r')
        ax.set_xlim(left=self.XLim[0], right=self.XLim[1])
        ax.set_ylim(bottom=self.YLim[0], top=self.YLim[1])
        ax.set_aspect('equal', 'datalim')
        ax.set_title('tSNE Projection', fontsize=8);
        ax.tick_params(axis='both', labelsize=6);
        pass

