import glob

def findVideoDir(folder):
    avi_list = glob.glob(folder+"/*.avi")
    mp4_list = glob.glob(folder+"/*.mp4")
    if len(avi_list)>=1: video = avi_list
    elif len(mp4_list)>=1: video = mp4_list
    else: video = []
    return video

def findEmbedDir(folder):
    npy_list = glob.glob(folder+"/EMBED.npy")
    mat_list = glob.glob(folder+"/EMBED.mat")
    if len(npy_list)>=1: 
        embed = npy_list
        fileType = "npy"
    elif len(mat_list)>=1: 
        embed = mat_list
        fileType = "mat"
    else: 
        embed = []
        fileType = None
    return embed, fileType

def findClusterDir(folder):
    npy_list = glob.glob(folder+"/CLUSTER.npy")
    if len(npy_list)>=1: 
        cluster = npy_list
    else: 
        cluster = []
    return cluster