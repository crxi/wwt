import numpy as np
import plotly.graph_objs as go
import streamsync as ss

# we only need to create these once
x = np.linspace(-3, 4, 141)
y = np.linspace(-3, 4, 141)
X, Y = np.meshgrid(x, y)

def get(state, *key): return (state[k] for k in key)

def plot_line(state):
    w0, w1, theta = get(state, 'w0', 'w1', 'theta')
    Z = w0 * X + w1 * Y    
    
    if 'contours' in state['options']:    
        labels = dict(start=-10, end=10, size=0.5, showlabels = True,
                      labelfont = dict(size = 14, color = 'black'))
    else:
        labels = dict(start=theta, end=theta, size=0.5)
    if 'heatmap' in state['options']:
        colorscale = [(0,'#0000ff'), (0.5,'#9999ff'), (0.5,'#ff9999'),(1.0,'#ff0000')]
    else:
        colorscale = [(0.0, '#ffffff'), (1.0, '#ffffff')]
    templ = (f'w0 &times; x0 + w1 &times; x1'
             f'<br>  = {w0:.2f}' + " &times; %{x:.1f} + " f'{w1:.2f}' " &times; %{y:.1f}"
              "<br>  = %{z:.3f}<extra></extra>")
    zabs = 2 # max(abs(theta - np.min(Z)), (np.max(Z) - theta))/4
    contour = go.Contour(
        x=x, y=y, z=Z, 
        colorscale=colorscale, zmin=theta-zabs, zmax=theta+zabs,
        contours=dict(coloring='heatmap', **labels),
        opacity=0.6, showscale=False, hovertemplate=templ,
    )
    data = [contour]
    layout = go.Layout(
        title=f'{w0:.3f} x0 + {w1:.3f} x1 >= {theta}',
        width=700,height=700,
        xaxis=dict(title='x0', range=[-1.1, 2.1], fixedrange=True,
          constrain="domain", scaleanchor="y", scaleratio=1,
          dtick=1,tick0=0),
        yaxis=dict(title='x1', range=[-1.1, 2.1], fixedrange=True,
          constrain="domain", dtick=1,tick0=0),
        paper_bgcolor='#EEEEEE',
        margin=dict(l=30, r=30, t=30, b=30),
    )
    fig = go.Figure(data=data, layout=layout)

    truth = state['truth']
    for i in [0,1]:
        for j in [0,1]:
            add_circle(fig, i, j, truth[i,j], state)
    state['graph'] = fig

def add_circle(fig, x, y, truth, state):
    w0, w1 = get(state, 'w0', 'w1')
    value = w0 * x + w1 * y
    templ = (f'w0 &times; x0 + w1 &times; x1'
            f'<br>  = {w0:.2f}' + " &times; %{x:.1f} + " f'{w1:.2f}' " &times; %{y:.1f}"
            f"<br>  = {value:.3f}<extra></extra>")
    # Determine color based on truth
    circle_color = 'black' if truth == 0 else 'red'
    text_color = 'pink' if truth == 0 else 'white'
    # Add a scatter plot for the circle
    fig.add_trace(go.Scatter(x=[x], y=[y], mode='markers', showlegend=False,
                             marker=dict(color=circle_color, size=28),
                             hoverinfo='none', hovertemplate=templ))
    
    # Add annotation (label) inside the circle
    fig.add_annotation(x=x, y=y, text=str(truth), showarrow=False,
                       font=dict(color=text_color, size=16),
                       xanchor='center', yanchor='middle')
    return fig
    

def reset(state):
    state['w0'] = 1
    state['w1'] = 1
    state['theta'] = 1
    state['truth'] = np.zeros(shape=(2,2), dtype='int32')
    plot_line(state)

def click(state, payload):
    c = payload[0]
    if 1 <= c['curveNumber'] <= 4:
        x, y = c['x'], c['y']
        v = state['truth'][x,y]
        state['truth'][x,y] = 0 if v else 1
        plot_line(state)

def options_changed(state, payload):
    state['options'] = payload
    plot_line(state)

initial_state = ss.init_state({
    "title": "w0w1theta Demo",
    "w0": 1,
    "w1": 1,
    "theta": 1,
    "truth": np.zeros(shape=(2,2), dtype='int32'),
    "graph" : None,
    "options": [],
})

plot_line(initial_state)