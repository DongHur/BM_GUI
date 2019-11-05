import hdbscan
import matplotlib
import matplotlib.pyplot as plt

def hdbscan(data, min_cluster_size=10, min_samples=65, plot_cluster=False, plot_cluster_noiseless=False, 
    plot_span_tree=False, plot_linkage_tree=False, plot_condense_tree=False):
    # data - [num_frames, num_dim]
    if min_samples is None:
        clusterer = hdbscan.HDBSCAN(
            min_cluster_size=min_cluster_size,
            allow_single_cluster=False,
            gen_min_span_tree=True)
    else:
        clusterer = hdbscan.HDBSCAN(
            min_cluster_size=min_cluster_size,
            min_samples=min_samples, 
            allow_single_cluster=False,
            gen_min_span_tree=True)
    clusterer.fit(data)
    # plot figures
    if plot_span_tree:
        plt.figure("Minnimum Spanning Tree")
        clusterer.minimum_spanning_tree_.plot(edge_cmap='viridis', edge_alpha=0.6, node_size=80, edge_linewidth=2)
        # plt.savefig(FIG_PATH+"Minnimum Spanning Tree")
    if plot_linkage_tree:
        plt.figure("Linkage Tree")
        clusterer.single_linkage_tree_.plot(cmap='viridis', colorbar=True)
        # plt.savefig(FIG_PATH+"Linkage Tree")
    if plot_condense_tree:
        plt.figure("Condense Tree")
        clusterer.condensed_tree_.plot()
        # plt.savefig(FIG_PATH+"Condense Tree")
    # control density of color based on probability
    num_cluster = int(clusterer.labels_.max()+1)
    print("Number of Clusters: ", num_cluster)
    print("Points Classified: {}%".format(round(len(np.where(clusterer.labels_!=-1)[0])/len(clusterer.labels_)*100,2)))
    # format cluster color
    color_palette = sns.color_palette('hls', num_cluster)
    cluster_colors = [color_palette[x] if x >= 0 else (0.5, 0.5, 0.5) for x in clusterer.labels_]
    cluster_member_colors = np.array([sns.desaturate(x, p) for x, p in zip(cluster_colors, clusterer.probabilities_)])
    # plot figures
    if plot_cluster:
        plt.figure("Labelled Scatter Plot")
        plt.title("Labelled Scatter Plot")
        plt.xlabel("X1")
        plt.ylabel("X2")
        plt.scatter(data[:,0], data[:,1], s=1.5, c=cluster_member_colors)
    if plot_cluster_noiseless:
        plt.figure("Noiseless Labelled Scatter Plot")
        plt.title("Labelled Scatter Plot w/o Noise")
        plt.xlabel("X1")
        plt.ylabel("X2")
        idx = clusterer.labels_ != -1
        plt.scatter(data[idx,0], data[idx,1], s=1.5, c=cluster_member_colors[idx])

        # fig = go.Figure(data=go.Scatter(x=data[idx,0], y=data[idx,1], 
        #     mode='markers', text=clusterer.labels_[idx], marker=dict(color=clusterer.labels_[idx], opacity=0.2)))
        # fig.show()
    # plt.savefig(FIG_PATH+"Labelled Scatter Plot")
    return clusterer.labels_, clusterer.probabilities_ 
