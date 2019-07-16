import numpy as np
import pyqtgraph as pg
import scipy.io as sio

class Graph2_Widget(pg.PlotWidget):
    def __init__(self, *args, **kwargs):
        super(Graph2_Widget, self).__init__()
        self.embed_dir = np.array([])
    def init_plot(self):
        self.plt = self.plot(y=[2,3,4,5,1,6], title="Individual tSNE Points", pen=None, symbol='o') # MAKE THE SYMBOL POINTS SMALLER
        pass