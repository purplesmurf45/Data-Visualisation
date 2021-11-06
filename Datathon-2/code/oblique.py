import imageio
import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go
plt.cm

# %matplotlib inline

data_type = {
    'total particle density': np.float64,
    'gas temperature (degrees Kelvin)': np.float64,
    'H mass abundance': np.float64,
    'H+ mass abundance': np.float64,
    'He mass abundance': np.float64,
    'He+ mass abundance': np.float64,
    'He++ mass abundance': np.float64,
    'H- mass abundance': np.float64,
    'H_2 mass abundance': np.float64,
    'H_2+ mass abundance': np.float64,
    'X': np.float64,
    'Y': np.float64,
    'Z': np.float64,
}

scalar_list = ['total particle density','gas temperature (degrees Kelvin)','H mass abundance','H+ mass abundance','He mass abundance','He+ mass abundance','He++ mass abundance','H- mass abundance','H_2 mass abundance','H_2+ mass abundance']

data_file = pd.read_csv("/content/drive/MyDrive/multifield.0119.txt", sep=" ", header=None, names=scalar_list, dtype=data_type)

densities = []
for k in range(248*248*600):
    densities.append(data_file["total particle density"].values[k])

# Equation of a plane is ax + by + cz + d = 0
# x = (d - cz - by)/a

#Input constants to plane equation
a = 1
b = -1
c = -2

fig = go.Figure()
#Changing the values of the constant d in the plane equation
for d in range(-100, 100, 2):
    ArrX = []
    ArrY = []
    ArrZ = []
    ArrDENSITY = []
    for j in range(0, 248, 3):
        for k in range(0, 248, 3):
            x = (d - b*j- c*k)/a
            flo = math.floor(x)
            cei = math.ceil(x)
            if 0 <= x and x < 600:
                if flo == cei:
                    x_dens = densities[flo + 600*j + 600*248*k]
                else:
                    x_dens = ((x - flo) * densities[ flo + 600*j + 600*248*k ]) + ((cei - x) * densities[ cei + 600*j + 600*248*k ]) #ceil part
            else:
                x_dens = 0

            ArrX.append(x)
            ArrY.append(j)
            ArrZ.append(k)
            ArrDENSITY.append(x_dens)

    ArrX = np.array(ArrX).reshape(83, 83)
    ArrY = np.array(ArrY).reshape(83, 83)
    ArrZ = np.array(ArrZ).reshape(83, 83)
    ArrDENSITY = np.array(ArrDENSITY).reshape(83, 83)
    
    fig.add_trace( go.Surface(x = ArrX,
                              y = ArrY,
                              z = ArrZ,
                              surfacecolor = ArrDENSITY
        )
    )

fig.data[5].visible = True

steps = []
for i in range(len(fig.data)):
    step = dict(
        method="update",
        args=[{"visible": [False] * len(fig.data)}],
    )
    step["args"][0]["visible"][i] = True
    steps.append(step)

sliders = [dict(
    active=50,
    currentvalue={"prefix": "Current Step: "},
    pad={"t": 50},
    steps=steps
)]

fig.update_layout(
    sliders=sliders
)

fig.write_html(file='slice.html')

