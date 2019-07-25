import numpy as np
import scipy.io as sio

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.ticker

class density_Graph(Figure):
    def __init__(self, *args, **kwargs):
        super(density_Graph, self).__init__()
        self.density_filepath = ''
        self.CData = None
        self.XLim = None
        self.YLim = None
        self.title = ''
    def init_plot(self, title):
        self.title = title
        self.clear()
        ax = self.add_subplot(111)
        ax.plot([], '*-')
        ax.set_title(title, fontsize=8);
        ax.tick_params(axis='both', labelsize=8);
        ax.grid()
        pass
    def set_newfile(self, filepath):
        self.density_filepath = filepath
        self.clear()
        ax = self.add_subplot(111)
        ax.grid()
        # read data
        data = sio.loadmat(filepath,squeeze_me=True, struct_as_record=False)
        matfig = data['hgS_070000']
        childs = matfig.children
        # find axes for graph
        try:
            ax1 = [c for c in childs if c.type == 'axes'][0]
        except:
            ax1 = childs
        self.XLim = ax1.properties.XLim
        self.YLim = ax1.properties.YLim
        # get data and plot it
        for line in ax1.children:
            if line.type == 'image':
                self.CData = line.properties.CData
                print("CData: ", self.CData.shape)
                im = ax.imshow(self.CData, cmap='jet', origin='lower', 
                    extent=(self.XLim[0]-0.5, self.XLim[1]-0.5, self.YLim[0]-0.5, self.YLim[1]-0.5))
                maxDensity = np.amax(self.CData)
                # set color range
                im.set_clim(vmin=0, vmax=maxDensity*.8)
                # make colorbar
                divider = make_axes_locatable(ax)
                cax = divider.append_axes('right', size='5%', pad=0.05)
                cbar = self.colorbar(im, cax, orientation='vertical')
                cbar.ax.tick_params(labelsize=8) 
                cbar.formatter.set_powerlimits((0, 0))
                cbar.update_ticks() 
                break
        # set axes
        ax.set(xlim=self.XLim, ylim=self.YLim)
        ax.set_title(self.title, fontsize=8);
        ax.tick_params(axis='both', labelsize=6);
        pass