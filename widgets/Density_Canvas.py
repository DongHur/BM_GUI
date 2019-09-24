import numpy as np
import scipy.io as sio

import matplotlib
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.ticker
matplotlib.rc('xtick', labelsize=8) 
matplotlib.rc('ytick', labelsize=8) 

class Density_Canvas(FigureCanvas):
    def __init__(self, *args, **kwargs):
        self.fig = Figure()
        super(Density_Canvas, self).__init__(self.fig)
        self.density_filepath = ''
        self.watershed_filepath = ''
        self.CData = None
        self.ax = self.fig.add_subplot(111)
        self.mode = None
        self.XLim, self.YLim = None, None
        self.title = 'Density Plot'
    def setup_canvas(self, density_filepath, watershed_filepath, mode="Denstiy"):
        self.mode = mode
        self.density_filepath = density_filepath
        self.watershed_filepath = watershed_filepath
        self.ax.clear()
        
        self.ax.grid()
        # read data
        data = sio.loadmat(density_filepath, squeeze_me=True, struct_as_record=False)
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
                break
        print(self.CData)
        # read Watershed Data
        self.WaterData = sio.loadmat(watershed_filepath, squeeze_me=True, struct_as_record=False)['L']
        self.update_canvas()
        pass
    def update_canvas(self, frame=0):
        if self.mode == "Points":
            self.point_plot()
        elif self.mode == "Density":
            self.density_plot()
        elif self.mode == "Points + Density":
            self.point_plot()
            self.density_plot()
        elif self.mode == "Points + Watershed":
            self.point_plot()
            self.watershed_plot()
        elif self.mode == "Points + Density + Watershed":
            self.point_plot()
            self.density_plot()
            self.watershed_plot()
        elif self.mode == "Points + Density":
            self.point_plot()
            self.density_plot()
        elif self.mode == "Density + Watershed":
            self.density_plot()
            self.watershed_plot()

        # set axes
        self.ax.set(xlim=self.XLim, ylim=self.YLim)
        self.ax.set_title(self.title, fontsize=8);
        self.ax.tick_params(axis='both', labelsize=6);
        self.draw()
        pass
    def density_plot(self):
        im = self.ax.imshow(self.CData, cmap='jet', origin='lower', 
            extent=(self.XLim[0]-0.5, self.XLim[1]-0.5, self.YLim[0]-0.5, self.YLim[1]-0.5))
        # set color range
        maxDensity = np.amax(self.CData)
        im.set_clim(vmin=0, vmax=maxDensity*.8)
        # make colorbar
        divider = make_axes_locatable(self.ax)
        cax = divider.append_axes('right', size='5%', pad=0.05)
        cbar = self.fig.colorbar(im, cax, orientation='vertical')
        cbar.ax.tick_params(labelsize=8) 
        cbar.formatter.set_powerlimits((0, 0))
        cbar.update_ticks() 
        pass
    def point_plot(self):

        pass
    def watershed_plot(self):
        print(self.WaterData)
        xx = np.linspace(self.XLim[0], self.XLim[1], self.CData.shape[0])
        yy = np.linspace(self.YLim[0], self.YLim[1], self.CData.shape[1])
        loc = np.where(self.WaterData==0)
        print()
        self.ax.plot(yy[loc[1]], xx[loc[0]], 'k.')
        pass



# self.title = title
# self.clear()
# ax = self.add_subplot(111)
# ax.plot([], '*-')
# ax.set_title(title, fontsize=8);
# ax.tick_params(axis='both', labelsize=8);
# ax.grid()