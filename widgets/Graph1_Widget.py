import numpy as np
import pyqtgraph as pg
import scipy.io as sio
# pg.setConfigOption('background', 'w') # FIX THIS SO YOU CAN MODIIFY PER GRAPH

class Graph1_Widget(pg.PlotWidget):
    def __init__(self, *args, **kwargs):
        super(Graph1_Widget, self).__init__()
        self.embed_dir = np.array([]) # update this list and then update the graph for any change in the data
        self.plt = None
        self.data = {}
        self.data_info = {
            "num_files": 0,
            "num_frames": 0,
            "num_selected_files": 0,
            "num_selected_frames": 0
        }
    def init_plot(self):
        self.plt = self.plot(y=[], title="All tSNE Points", pen=None, symbol='o') # MAKE THE SYMBOL POINTS SMALLER
        self.update_data_info()
        pass
    def add_dir(self, dir):
        self.embed_dir = np.append(self.embed_dir, dir)
        # load data
        self.data[dir] = {
            'embed_values': sio.loadmat(dir)['embed_values_i'],
            'isChecked': False
        }
        # update graph
        self.update_data_info()
        pass
    def delete_dir(self, dir):
        if dir in self.data:
            del self.data[dir]
        # update graph
        self.update_data_info()
        pass
    def update_graph(self):
        (x,y,_) = self.get_all_data()
        # update plot
        self.plt.setData(x=x, y=y)
        pass
    def update_checked(self, dir, isChecked):
        self.data[dir]['isChecked'] = isChecked
        self.update_data_info()
        pass
    def update_data_info(self):
        self.data_info['num_files'] = len(self.data)
        self.data_info['num_frames'] = 0
        self.data_info['num_selected_files'] = 0
        self.data_info['num_selected_frames'] = 0

        for attr, value in self.data.items():
            num_frames =  value['embed_values'].shape[0]
            self.data_info['num_frames'] += num_frames 
            if value['isChecked'] == True:
                self.data_info['num_selected_files'] += 1
                self.data_info['num_selected_frames'] += num_frames
    def get_all_data(self, exclude=[]): # CREATE A FUNCTIONALITY THAT ALLOWS YOU TO EXCLUDE CERTAIN FILES
        data_all = np.array([]).reshape(0,2)
        for attr, value in self.data.items():
            if value['isChecked'] == True:
                data_all = np.concatenate((data_all,value['embed_values']), axis=0)
        return data_all[:,0], data_all[:,1], data_all

