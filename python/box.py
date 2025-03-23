import plotly.graph_objects as go
import numpy as np

fig = go.Figure()

x_wall0 = np.zeros((2, 2))
y_wall0 = np.array([[0, 0], [10, 10]])
z_wall0 = np.array([[0, 10], [0, 10]])
fig.add_trace(go.Surface(
    x=x_wall0, y=y_wall0, z=z_wall0,
    colorscale='tropic', opacity=1, showscale=False
))

x_wall1 = np.ones((2, 2))
y_wall1 = np.array([[0, 0], [10, 10]])
z_wall1 = np.array([[0, 10], [0, 10]])
fig.add_trace(go.Surface(
    x=x_wall1, y=y_wall1, z=z_wall1,
    colorscale='purp', opacity=0.5, showscale=False
))

x_wall2 = np.array([[0, 10], [0, 10]])
y_wall2 = np.array([[0, 0], [10, 10]])
z_wall2 = np.zeros((2, 2))
fig.add_trace(go.Surface(
    x=x_wall2, y=y_wall2, z=z_wall2,
    colorscale='edge', opacity=1, showscale=False
))

x_wall3 = np.array([[0, 10], [0, 10]])
y_wall3 = np.array([[0, 0], [10, 10]])
z_wall3 = np.ones((2, 2)) * 10
fig.add_trace(go.Surface(
    x=x_wall3, y=y_wall3, z=z_wall3,
    colorscale='jet', opacity=0.5, showscale=False
))

x_wall4 = np.array([[0, 10], [0, 10]])
y_wall4 = np.zeros((2, 2))
z_wall4 = np.array([[0, 10], [0, 10]])
fig.add_trace(go.Surface(
    x=x_wall4, y=y_wall4, z=z_wall4,
    colorscale='inferno', opacity=1, showscale=False
))

x_wall5 = np.array([[0, 10], [0, 10]])
y_wall5 = np.ones((2, 2))
z_wall5 = np.ones((2, 2)) * 10
fig.add_trace(go.Surface(
    x=x_wall5, y=y_wall5, z=z_wall5,
    colorscale='hot', opacity=0.5, showscale=False
))

def cubes(size, pos_x, pos_y, pos_z, color):
    # create points
    x, y, z = np.meshgrid(
        np.linspace(pos_x-size/2, pos_x+size/2, 2), 
        np.linspace(pos_y-size/2, pos_y+size/2, 2), 
        np.linspace(pos_z-size/2, pos_z+size/2, 2),
    )
    x = x.flatten()
    y = y.flatten()
    z = z.flatten()
    
    return go.Mesh3d(x=x, y=y, z=z, alphahull=1, flatshading=True, color=color, lighting={'diffuse': 0.1, 'specular': 2.0, 'roughness': 0.5})
size = 5
outer_size_x = 20
outer_size_y = 20
outer_size_z = 20
inner_size=1
fig.add_trace(cubes(inner_size, 2, 2, 2, 'rgba(100,0,100,0.1)'))


fig.update_layout(
    scene=dict(
        xaxis_title='X Axis',
        yaxis_title='Y Axis',
        zaxis_title='Z Axis',
        xaxis=dict(range=[1, 10]),
        yaxis=dict(range=[1, 10]),
        zaxis=dict(range=[1, 10]),
    ),dragmode = 'turntable',
     scene_camera=dict(
        eye=dict(x=1.25, y=1.25, z=1.25),
        up=dict(x=0, y=0, z=1)
    )
)

fig.show(config={'displayModeBar': False})

