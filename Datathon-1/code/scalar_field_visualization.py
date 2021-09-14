import numpy as np
import pandas as pd 
import matplotlib
matplotlib.use("Agg")
import matplotlib.animation as anim
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from sklearn.preprocessing import MinMaxScaler
import glob

#Defining animation writer to make a video
FFMpegWriter = anim.writers['ffmpeg']
metadata = dict(title='Gas temperature', artist='Neetha',
                comment='Animation')
writer = FFMpegWriter(fps=12, metadata=metadata)

#Input files
data_files = glob.glob("../input/dv-data-1/multifield.*.txt")
data_files.sort()


scaler = MinMaxScaler()
#function to get data from a given timestamp
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
                    gas = float(data[0])
                    if x not in STARS:
                        STARS[x] = dict()
                    STARS[x][y] = gas
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

    # Convert Density into grid format
    Dens = np.zeros((len(X),len(Y)),np.float)

    for i in range(len(X)):
        for j in range(len(Y)):
            Dens[i][j] = STARS[X[i]][Y[j]]

    # Visualize the data
    plt.clf()
    x, y = np.meshgrid(X, Y)
    scaler.fit(Dens.T)
    h = plt.contourf(x,y,scaler.transform(Dens.T),levels=np.linspace(72,25000,100),cmap=cm.YlOrRd)
    cbar = plt.colorbar()
    cbar.set_label("Relative density")
    plt.title("Log of total particle density at {}".format(timestamp.strip(".txt")))
    # plt.show()
    return h
 
 #Saving the frames into a video
fig = plt.figure(figsize=(16,8))
with writer.saving(fig, "gas_hot.mp4", dpi=100):
    for f in data_files:
        get_frame(f)
        writer.grab_frame()
 