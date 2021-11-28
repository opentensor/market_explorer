import dash
import os
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px

import pandas as pd

df = pd.read_pickle( os.path.expanduser('~/data.pd') )

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id='graph-with-slider'),
    dcc.Slider(
        id='block-slider',
        min = df.index.min(),
        max = df.index.max(),
        value = df.index.min(),
        marks = { str(block): str(block) for block in list(df.index) },
        step=None
    )
])

@app.callback(
    Output('graph-with-slider', 'figure'),
    Input('block-slider', 'value')
)
def update_figure(selected_block):
    filtered_df = df[ selected_block ]
    fig = px.scatter( filtered_df, x="uid", y="stake", log_y=True )
    fig.update_layout( transition_duration=500 )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)