import numpy as np
import plotly.graph_objs as go
import streamsync as ss

def plot_line(state):
    w0, w1, theta = [state[i] for i in ['w0', 'w1', 'theta']]

    x = np.linspace(-3, 4, 2)
    y, anno = None, []

    if not np.isclose(w1, 0):
        y = (-w0 / w1) * x + (theta / w1)
    else:
        if not np.isclose(w0, 0):
            y = np.linspace(-4, 4, 400)
            x = np.full_like(y, theta / w0)
        else:
            anno.append(dict(
                x=0, y=0, text="Both w0 and w1 are too close to zero",
                xref="x", yref="y", showarrow=False, yshift=10))

    data = []
    if y is not None:
        data.append(go.Scatter(x=x, y=y, mode='lines', name='line'))

    layout = go.Layout(
        width=700,height=700,
        xaxis=dict(title='x0', range=[-1.1, 2.1], fixedrange=True,
          constrain="domain", scaleanchor="y", scaleratio=1,
          dtick=1,tick0=0),
        yaxis=dict(title='x1', range=[-1.1, 2.1], fixedrange=True,
          constrain="domain", dtick=1,tick0=0),
        paper_bgcolor='#EEEEEE',
        margin=dict(l=30, r=30, t=30, b=30),
        annotations=anno,
    )
    fig = go.Figure(data=data, layout=layout)
    state['graph'] = fig


def plot_line(state):
    w0, w1, theta = [state[i] for i in ['w0', 'w1', 'theta']]
    # Define the range for x and y
    x = np.linspace(-3, 4, 2)
    y = np.linspace(-3, 4, 2)
    X, Y = np.meshgrid(x, y)

    # Calculate w0*x + w1*y
    Z = w0 * X + w1 * Y

    # Create a custom color scale with green for values > theta and red for values < theta
    colorscale = [
        [0.0, '#ffaaaa'], # Start with red
        [0.5, '#ff0000'], # Threshold value (theta) is red
        [0.5, '#0000bb'], # Threshold value (theta) is blue
        [1.0, '#aaaabb']  # End with blue
    ]

    # Create the contour plot
    contour = go.Contour(
        x=x, y=y, z=Z, 
        colorscale=colorscale, 
        contours=dict(
            start=theta, 
            end=theta, 
            size=0.5, 
            coloring='heatmap'
        ),
        opacity=0.6,
        showscale=False,
        hoverinfo='none'
    )
    data = [contour]
    anno = []
    layout = go.Layout(
        width=700,height=700,
        xaxis=dict(title='x0', range=[-1.1, 2.1], fixedrange=True,
          constrain="domain", scaleanchor="y", scaleratio=1,
          dtick=1,tick0=0),
        yaxis=dict(title='x1', range=[-1.1, 2.1], fixedrange=True,
          constrain="domain", dtick=1,tick0=0),
        paper_bgcolor='#EEEEEE',
        margin=dict(l=30, r=30, t=30, b=30),
        annotations=anno,
        title=f'Map of {w0}x0 + {w1}x0 >= {theta} (θ)',
    )
    fig = go.Figure(data=data, layout=layout)
    state['graph'] = fig

def reset(state):
    state['w0'] = 1
    state['w1'] = 1
    state['theta'] = 1
    plot_line(state)


initial_state = ss.init_state({
    "title": "w0w1theta Demo",
    "w0": 1,
    "w1": 1,
    "theta": 1,
    "graph" : None,
})

plot_line(initial_state)