import numpy as np
import pandas as pd 
import matplotlib
matplotlib.use("Agg")
import matplotlib.animation as anim
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import glob
import linecache
from sklearn.preprocessing import MinMaxScaler

#Defining animation writer to make a video
FFMpegWriter = anim.writers['ffmpeg']
metadata = dict(title='Curl', artist='Neetha',
                comment='Animation')
writer = FFMpegWriter(fps=12, metadata=metadata)

#Input files
data_files = glob.glob("../input/dv-data-1/multifield.*.txt")
data_files.sort()
velo_files = glob.glob("../input/dv-data-1/velocity.*.txt")
velo_files.sort()


scaler = MinMaxScaler()
#function to get data from a given timestamp
def get_frame_q(data_file, velo_file):
    idx = 0
    STARS = dict()
    STARS1 = dict()
    timestamp = velo_file.strip().split('/')[3]
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
    x = 0
    y = 0
    idx = 0
    with open(velo_file,'r') as f:
        while(f):
            r = f.readline()
            if r != '':
                if idx < 600*248*41 and idx >= 600*248*40:
                    data = r.strip().split(' ')
                    r_temp_x = linecache.getline(velo_file, idx+1).strip().split(' ')
                    r_temp_y = linecache.getline(velo_file, idx+600).strip().split(' ')
                    r_temp_z = linecache.getline(velo_file, idx+600*248).strip().split(' ')
                    curl_x = (float(data[1])-float(data[2]) + float(r_temp_y[2]) - float(r_temp_z[1]))/0.01
                    curl_y = (float(data[2])-float(data[0]) + float(r_temp_z[0]) - float(r_temp_x[2]))/0.01
                    if x not in STARS1:
                        STARS1[x] = dict()
                    STARS1[x][y] = [curl_x, curl_y]
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
            
    X1 = []
    Y1 = []       
    for x in STARS1:
        X1.append(x)
        for y in STARS1[x]:
            Y1.append(y)

    X1 = list(set(X1))
    Y1 = list(set(Y1))

    X1.sort()
    Y1.sort()

    # Convert curl and density into grid format
    Dens = np.zeros((len(X),len(Y)),np.float)
    CurlX = np.zeros((len(X1),len(Y1)),np.float)
    CurlY = np.zeros((len(X1),len(Y1)),np.float)

    for i in range(len(X)):
        for j in range(len(Y)):
            Dens[i][j] = STARS[X[i]][Y[j]]
            
    for i in range(len(X1)):
        for j in range(len(Y1)):
            CurlX[i][j] = STARS1[X1[i]][Y1[j]][0]
            CurlY[i][j] = STARS1[X1[i]][Y1[j]][1]

    # Visualize the data
    plt.clf()
    x, y = np.meshgrid(X, Y)
    scaler.fit(Dens.T)
    h = plt.contourf(x,y,scaler.transform(Dens.T),levels=np.linspace(0,1,100),cmap=cm.summer)
    cbar = plt.colorbar()
    q = plt.quiver(x,y, CurlX.T, CurlY.T,width=0.0005, color="white")
    plt.quiverkey(q, 0.1, 1, 0.1, "") 
    plt.title("Log of total particle density at {}".format(timestamp.strip(".txt")))
    return q

# Saving the frames into a video
fig = plt.figure(figsize=(16,8))
with writer.saving(fig, "qc4.mp4", dpi=100):
    for i in range(0, len(data_files)):
        print(i)
        get_frame_q(data_files[i], velo_files[i])
        writer.grab_frame()