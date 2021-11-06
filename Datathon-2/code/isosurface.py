import linecache
import numpy as np
import plotly.graph_objects as go

# %matplotlib inline
data_file = "../input/datav2/multifield.0119.txt"

X = []
Y = []
Z = []
DENS = []
idx = 600*248*37
x = 0
y = 0
z = 37
while idx < 600*248*43:
    X.append(x)
    Y.append(y)
    Z.append(z)
    r = linecache.getline(data_file, idx+1).strip().split(' ')
    if r != '':
        den = np.log(float(r[0]))
        DENS.append(den)
    x += 1
    if x == 600:
        x = 0
        y += 1
    if y == 248:
        y = 0
        z += 1
    idx += 1


MAX_Density = np.nanmax(DENS)
MIN_Density = np.nanmin(DENS)

#Visualising the data
fig= go.Figure(
    data=go.Isosurface(
        x=X,
        y=Y,
        z=Z,
        value=DENS,
        isomin=MIN_Density ,
        isomax=MAX_Density,
        surface_count=5,
        colorbar_title="Density",
        opacity=0.75,
        caps=dict(x_show=False,y_show=False,z_show=False)
    )
    ,
    layout=go.Layout(
        scene = dict(
                    xaxis = dict(title='X'),
                    yaxis = dict(title='Y'),
                    zaxis = dict(title='Z'),
                ),
        title = go.layout.Title(
            text='Particle Density'
        )
    )
)

fig.show()