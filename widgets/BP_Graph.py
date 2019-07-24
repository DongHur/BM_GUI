import numpy as np

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

class BP_Graph(Figure):
    def __init__(self, *args, **kwargs):
        super(BP_Graph, self).__init__()
        self.bp_filepath = ''
        self.num_frame = 0
        self.duration = 1
        self.data = None
    def init_plot(self):
        self.clear()
        ax = self.add_subplot(111)
        ax.plot([], 'o-')
        ax.set_title('Ant Body Point Graph', fontsize=8);
        ax.tick_params(axis='both', labelsize=6);
        pass
    def set_newfile(self, filepath):
        self.bp_filepath = filepath
        self.data = np.load(filepath) # (30,2,5901)
        self.num_frame = self.data.shape[2]
        pass
    def set_duration(self, duration):
        self.duration = duration
        pass
    def update_graph(self, position, frame_data=False):
        if frame_data:
            frame = position # frame as data point
        else:
            frame = int(self.num_frame*position/self.duration)-1 # index is one less; millisecond as data
        self.clear()
        ax = self.add_subplot(111)
        # plot ant points for specific time point t; specific to out setup with 30bp ants
        # data format: num_bp x (X_coord, Y_coord) x t
        # ax.scatter(self.data[:,0,frame], self.data[:,1,frame])
        # graph parameters
        marker = 'o'
        s=4
        # plot graph
        ax.plot(self.data[0:4,0,frame], self.data[0:4,1,frame], marker=marker, markersize=s)
        ax.plot(self.data[4:8,0,frame], self.data[4:8,1,frame], marker=marker, markersize=s)
        ax.plot(self.data[8:11,0,frame], self.data[8:11,1,frame], marker=marker, markersize=s)
        ax.plot(self.data[11:14,0,frame], self.data[11:14,1,frame], marker=marker, markersize=s)
        ax.plot(self.data[14:17,0,frame], self.data[14:17,1,frame], marker=marker, markersize=s)
        ax.plot(self.data[17:21,0,frame], self.data[17:21,1,frame], marker=marker, markersize=s)
        ax.plot(self.data[21:24,0,frame], self.data[21:24,1,frame], marker=marker, markersize=s)
        ax.plot(self.data[24:27,0,frame], self.data[24:27,1,frame], marker=marker, markersize=s)
        ax.plot(self.data[27:30,0,frame], self.data[27:30,1,frame], marker=marker, markersize=s)
        ax.set_xlim(left=-200, right=200)
        ax.set_ylim(bottom=-200, top=200)
        ax.set_aspect('equal', 'box')
        ax.set_title('Ant Body Point Graph', fontsize=8);
        ax.tick_params(axis='both', labelsize=6);
        pass







