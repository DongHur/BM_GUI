import numpy as np
import scipy.io as sio
import seaborn as sns
from sklearn.neighbors import NearestNeighbors

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.ticker

class Total_Canvas(FigureCanvas):
    def __init__(self, *args, **kwargs):
        self.fig = Figure()
        super(FigureCanvas, self).__init__(self.fig)
        self.ax = self.fig.add_subplot(111)
        self.embed_data = None
        self.label_data = None
        self.mode = ""
        self.xlim, self.ylim = (-100, 100), (-100, 100)
        self.cluster_colors = None
        self.X_H, self.Y_H, self.GH_conv = None, None, None
    def setup_canvas(self, tot_dir, mode=""):
        self.mode = mode
        # combine all data
        for directory in tot_dir:
            # combine embed data
            data_i= sio.loadmat(directory+"/EMBED.mat")['embed_values_i']
            self.embed_data = np.vstack((self.embed_data, data_i)) if self.embed_data is not None else data_i
            # combine cluster laber data
            label_i = np.load(directory+"/cluster.npy")
            self.label_data = np.hstack((self.label_data, label_i)) if self.label_data is not None else label_i
        # populate proper plot mode
        if mode == "HDBSCAN Cluster":
            # format cluster color
            num_cluster = np.max(self.label_data)+1
            color_palette = sns.color_palette('hls', num_cluster)
            self.cluster_colors = [color_palette[x] if x >= 0 else (0.5, 0.5, 0.5) for x in self.label_data]
        elif mode =="Density":
            # build density plot
            self.GH_conv, self.X_H, self.Y_H = self.gaussian_conv(self.embed_data)
        self.num_frame = self.embed_data.shape[0]
        self.xlim = (-1.1*np.max(self.embed_data), 1.1*np.max(self.embed_data))
        self.ylim = (-1.1*np.max(self.embed_data), 1.1*np.max(self.embed_data))
        self.update_canvas()
        pass
    def update_canvas(self):
        self.ax.clear()
        if self.mode == "HDBSCAN Cluster":
            self.ax.set_xlim(left=self.xlim[0], right=self.xlim[1])
            self.ax.set_ylim(bottom=self.ylim[0], top=self.ylim[1])
            self.ax.scatter(self.embed_data[:,0], self.embed_data[:,1], s=5, c=self.cluster_colors)
            self.ax.grid(True, 'both')
        elif self.mode =="Density":
            self.ax.pcolormesh(self.X_H, self.Y_H, self.GH_conv.T, cmap="jet")
            self.ax.grid(True, 'both')
        self.draw()
        pass

    def gaussian_conv(self, data, k_nearest=5, num_points=120, plot_kernel=False, plot_hist=False, plot_conv=False):
        # data - [num_frames, num_dim]
        # knn computation
        nbrs = NearestNeighbors(n_neighbors=k_nearest+1, algorithm='kd_tree').fit(data)
        K_dist, K_idx = nbrs.kneighbors(data)
        K_matrix_idx = nbrs.kneighbors_graph(data).toarray()
        # gaussian conv computation
        sigma = np.median(K_dist[:,-1])
        print("sigma: ", sigma)
        L_bound = -1.0*abs(data.max())-1
        U_bound = 1.0*abs(data.max())+1
        xx = np.linspace(L_bound, U_bound, num_points)
        yy = np.linspace(L_bound, U_bound, num_points)
        XX, YY = np.meshgrid(xx, yy)
        # gaussian kernel
        G = np.exp(-0.5*(XX**2 + YY**2)/sigma**2)/(2*np.pi*sigma**2);
        if plot_kernel:
            plt.figure("Gaussian Kernel")
            plt.imshow(G, extent=[L_bound, U_bound, L_bound, U_bound])
            plt.title("Gaussian Kernel")
            plt.xlabel("X1")
            plt.ylabel("X2")
        # data histogram
        H, xedges, yedges = np.histogram2d(data[:,0], data[:,1], num_points, [[L_bound,U_bound],[L_bound,U_bound]])
        X_H, Y_H = np.meshgrid(xedges, yedges)
        H = H/H.sum()
        if plot_hist:
            plt.figure("Data Histogram")
            plt.pcolormesh(X_H, Y_H, H.T)
            # plt.imshow(H, extent=[L_bound, U_bound, L_bound, U_bound]) 
            plt.title("Data Histogram")
            plt.xlabel("X1")
            plt.ylabel("X2")
        # fft convolution
        fr = np.fft.fft2(G)
        fr2 = np.fft.fft2(H)
        GH_conv = np.fft.fftshift(np.real(np.fft.ifft2(fr*fr2)))
        GH_conv[GH_conv<0] = 0
        if plot_conv:
            plt.figure("Gaussian Convolution")
            plt.pcolormesh(X_H, Y_H, GH_conv.T)
            # plt.imshow(GH_conv, extent=[L_bound, U_bound, L_bound, U_bound])
            plt.title("Gaussian Kernel Convolution w/ Data Histogram")
            plt.xlabel("X1")
            plt.ylabel("X2")
        return GH_conv, X_H, Y_H