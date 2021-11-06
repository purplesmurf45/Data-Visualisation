import glob
import linecache
import matplotlib
matplotlib.use("Agg")
import matplotlib.animation as anim
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd 
import plotly.figure_factory as ff
import plotly.graph_objects as go

# %matplotlib inline


FFMpegWriter = anim.writers['ffmpeg']
metadata = dict(title='Streamlines', artist='Neetha',
                comment='Animation')
writer = FFMpegWriter(fps=12, metadata=metadata)
data_files = glob.glob("../input/dv-data-1/velocity.*.txt")
data_files.sort()
def get_frame(data_file):
    idx = 0
    STARS = dict()
    timestamp = data_file.strip().split('/')[3]
    x = 0
    y = 0
    with open(data_file,'r') as f:
        while(f):
            r = f.readline()
            if r != '':
                if idx < 600*248*41 and idx >= 600*248*40:
                    data = r.strip().split(' ')
                    r_temp_x = linecache.getline(data_file, idx+1).strip().split(' ')
                    r_temp_y = linecache.getline(data_file, idx+600).strip().split(' ')
                    r_temp_z = linecache.getline(data_file, idx+600*248).strip().split(' ')
                    curl_x = (float(data[1])-float(data[2]) + float(r_temp_y[2]) - float(r_temp_z[1]))/0.01
                    curl_y = (float(data[2])-float(data[0]) + float(r_temp_z[0]) - float(r_temp_x[2]))/0.01
                    if x not in STARS:
                        STARS[x] = dict()
                    STARS[x][y] = [curl_x, curl_y]
                    x += 1
            else:
                break
            if x == 600:
                x = 0
                y += 1
            idx += 1


    X = []
    Y = []

    for x in STARS:
        X.append(x)
        for y in STARS[x]:
            Y.append(y)

    X = list(set(X))
    Y = list(set(Y))

    X.sort()
    Y.sort()

    # Convert curl into grid format
    CurlX = np.zeros((len(X),len(Y)),np.float)
    CurlY = np.zeros((len(X),len(Y)),np.float)

    for i in range(len(X)):
        for j in range(len(Y)):
            CurlX[i][j] = STARS[X[i]][Y[j]][0]
            CurlY[i][j] = STARS[X[i]][Y[j]][1]

    # Visualize the data
    plt.clf()
    x, y = np.meshgrid(X, Y)
    s = plt.streamplot(x, y, CurlX.T, CurlY.T)
    plt.title("Streamlines at {}".format(timestamp.strip(".txt")))
#     plt.show()
    return s


fig = plt.figure(figsize=(16,8))

with writer.saving(fig, "stream3.mp4", dpi=100):
    for f in data_files:
        print(f)
        get_frame(f)
        writer.grab_frame()