import dash
import os
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px

import pandas as pd

df = pd.read_pickle( os.path.expanduser('~/data.pd') )

app = dash.Dash(__name__)

app.layout = html.Div(
    [
        dcc.Graph( id='uid_to_incentive') ,
        dcc.Slider(
            id='uid_to_incentive_slider',
            min = df.index.min(),
            max = df.index.max(),
            value = df.index.min(),
            marks = { str(block): str(block) for block in list(df.index) },
            step=None
        ),
        dcc.Dropdown(
            id='uid_dropdown',
            options=[ {'label':str(int(u)), 'value': int(u)} for u in list(df[df.index.max()].uid) ],
            value='value'
        ),
        dcc.Graph(id='stake_over_time'),

    ]
)

@app.callback(
    Output('uid_to_incentive', 'figure'),
    Input('uid_to_incentive_slider', 'value')
)
def update_uid_to_incentive ( selected_block ):
    filtered_df = df[ selected_block ]
    fig = px.scatter( filtered_df, x="uid", y="incentive", template='plotly_dark')
    fig.update_layout( transition_duration=500 )
    return fig

@app.callback(
    Output('stake_over_time', 'figure'),
    Input('uid_dropdown', 'value')
)
def update_stake_over_time ( selected_uid ):
    x = list(df.index)
    y = [ block['stake'][selected_uid] for block in df ]
    xx = [x for x, _ in sorted(zip(x, y))]
    yy = [y for _, y in sorted(zip(x, y))]
    return px.line( x=xx, y=yy, template='plotly_dark')

if __name__ == '__main__':
    app.run_server(host = '0.0.0.0', debug=True)

