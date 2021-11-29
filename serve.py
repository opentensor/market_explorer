import dash
import os
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go

import pandas as pd

df = pd.read_pickle( os.path.expanduser('~/data/all_blocks.pd') )
df = df.sort_index()
app = dash.Dash(__name__)

blocks = list(df.index)
n_active_neurons = [ d.active.sum() for d in df ]
n_neurons_fig = go.Figure()
n_neurons_fig.add_trace( 
    go.Scatter ( 
        x = blocks, 
        y = n_active_neurons
    )
)
n_neurons_fig.update_layout(template='plotly_dark')
n_neurons_fig.update_layout(title_text="N/block")
n_neurons_fig.update_layout(
    xaxis=dict (
        rangeslider=dict(
            visible=True
        ),
        type="linear"
    )
)

app.layout = html.Div(
    className = "page",
    style = {'backgroundColor': 'black'},
    children = [
        dcc.Graph( id='block_to_n', figure = n_neurons_fig),
        dcc.Graph( id='uid_to_incentive' ),
        dcc.Slider(
            id='uid_to_incentive_slider',
            min = df.index.min(),
            max = df.index.max(),
            value = df.index.min(),
            step = 1000
        ),

        dcc.Dropdown(
            id = 'uid_dropdown',
            options = [ {'label':str(int(u)), 'value': int(u)} for u in list(df[df.index.max()].uid) ],
            value = 0,
            style = {'backgroundColor': 'black'}
        ),
        dcc.Graph(id='incentive_over_time'),
    ]
)

@app.callback(
    Output('uid_to_incentive', 'figure'),
    Input('uid_to_incentive_slider', 'value')
)
def update_uid_to_incentive ( selected_block ):
    closest_index = list(df.index)[0]
    for val in list(df.index):
        if val <= selected_block:
            closest_index = val
        else:
            break
    filtered_df = df[ closest_index ]
    fig = px.scatter( filtered_df, x="uid", y="incentive", template='plotly_dark', marginal_y="histogram", title="Incentive @ block:{}".format( selected_block ), labels=dict(x="uid", y="incentive") )
    fig.update_layout( transition_duration=500 )
    return fig

@app.callback(
    Output('incentive_over_time', 'figure'),
    Input('uid_dropdown', 'value')
)
def update_incentive_over_time ( selected_uid ):
    x = list(df.index)
    y = [ block['incentive'][selected_uid] for block in df ]
    xx = [x for x, _ in sorted(zip(x, y))]
    yy = [y for _, y in sorted(zip(x, y))]
    return px.line( x=xx, y=yy, template='plotly_dark', markers=True, title="Incentive @ uid: {}".format( selected_uid ), labels=dict(x="block", y="incentive") )

if __name__ == '__main__':
    app.run_server(host = '0.0.0.0', debug=True)

