import numpy as np
from sklearn.neighbors import NearestNeighbors
import matplotlib
import matplotlib.pyplot as plt

def GaussConv(data, k_nearest=5, num_points=120, plot_kernel=False, plot_hist=False, plot_conv=False):
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