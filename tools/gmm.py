import numpy as np
import seaborn as sns
from sklearn.mixture import GaussianMixture, BayesianGaussianMixture

def gmm(data, n_components=40, plot=False):
    gmm = GaussianMixture(n_components)
    gmm.fit(data)
    label = gmm.predict(data)
    prob = np.max(gmm.predict_proba(data), axis=1)
    # print(gmm.score(data))
    if plot:
        # format cluster color
        color_palette = sns.color_palette('hls', n_components)
        cluster_colors = [color_palette[x] for x in label]
        cluster_member_colors = np.array([(x[0],x[1],x[2],p*0.1) for x, p in zip(cluster_colors, )])
        # plot
        plt.figure("GMM Clustering")
        plt.title("GMM Clustering")
        plt.xlabel("X1")
        plt.ylabel("X2")
        plt.scatter(data[:,0],data[:,1], s=1.5, c=cluster_member_colors)
    return label, prob