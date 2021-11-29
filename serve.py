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
n_neurons_fig.update_layout(title_text="Active/block")
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
    style = {'backgroundColor': '#000000' },
    children = [
        html.Div(
            html.Img(src=app.get_asset_url('tau.png'), style={'height':'3%', 'width':'3%'}),
        ),
        dcc.Dropdown(
            id = 'uid_dropdown',
            options = [ {'label':str(int(u)), 'value': int(u)} for u in list(df[df.index.max()].uid) ],
            value = 0,
            style = {'backgroundColor': '#000000' }
        ),
        dcc.Graph( id='stake_over_time' ),
        dcc.Graph( id='rank_over_time' ),
        dcc.Graph( id='trust_over_time' ),
        dcc.Graph( id='consensus_over_time' ),
        dcc.Graph( id='incentive_over_time' ),
        dcc.Graph( id='dividends_over_time' ),
        dcc.Graph( id='emission_over_time' ),
        dcc.Graph( id='uid_to_incentive' ),
        dcc.Slider(
            id='uid_to_incentive_slider',
            min = df.index.min(),
            max = df.index.max(),
            value = df.index.min(),
            step = 1000
        ),
        dcc.Graph( id='block_to_n', figure = n_neurons_fig),
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
    fig = px.scatter( filtered_df, x="uid", y="incentive", template='plotly_dark', title="Incentive @ block:{}".format( selected_block ), labels=dict(x="uid", y="incentive") )
    fig.update_layout( transition_duration=500 )
    return fig

@app.callback(
    [ 
        Output('stake_over_time', 'figure'),
        Output('rank_over_time', 'figure'), 
        Output('trust_over_time', 'figure'), 
        Output('consensus_over_time', 'figure'), 
        Output('incentive_over_time', 'figure'), 
        Output('dividends_over_time', 'figure'), 
        Output('emission_over_time', 'figure'), 
    ],
    Input('uid_dropdown', 'value')
)
def update_incentive_over_time ( selected_uid ):
    x = list(df.index)
    incentive = [ block['incentive'][selected_uid] for block in df ]
    stake = [ block['stake'][selected_uid] for block in df ]
    trust = [ block['trust'][selected_uid] for block in df ]
    rank = [ block['rank'][selected_uid] for block in df ]
    dividends = [ block['dividends'][selected_uid] for block in df ]
    emission = [ block['emission'][selected_uid] for block in df ]
    consensus = [ block['consensus'][selected_uid] for block in df ]

    # Get sorted data.
    xx = [x for x, _ in sorted(zip(x, incentive))]
    yy_stake = [y for _, y in sorted(zip(x, stake))]
    yy_rank = [y for _, y in sorted(zip(x, stake))]
    yy_trust = [y for _, y in sorted(zip(x, trust))]
    yy_conensus = [y for _, y in sorted(zip(x, consensus))]
    yy_incentive = [y for _, y in sorted(zip(x, incentive))]
    yy_dividends = [y for _, y in sorted(zip(x, dividends))]
    yy_emission = [y for _, y in sorted(zip(x, emission))]

    # Build scatters.
    stake_over_time = px.line( x=xx, y=yy_stake, template='plotly_dark', markers=True, title="Stake @ uid: {}".format( selected_uid ), labels=dict(x="block", y="stake") )
    rank_over_time = px.line( x=xx, y=yy_rank, template='plotly_dark', markers=True, title="Rank @ uid: {}".format( selected_uid ), labels=dict(x="block", y="rank") )
    trust_over_time = px.line( x=xx, y=yy_trust, template='plotly_dark', markers=True, title="Trust @ uid: {}".format( selected_uid ), labels=dict(x="block", y="trust") )
    consensus_over_time = px.line( x=xx, y=yy_conensus, template='plotly_dark', markers=True, title="Consensus @ uid: {}".format( selected_uid ), labels=dict(x="block", y="consensus") )
    incentive_over_time = px.line( x=xx, y=yy_incentive, template='plotly_dark', markers=True, title="Incentive @ uid: {}".format( selected_uid ), labels=dict(x="block", y="incentive") )
    dividends_over_time = px.line( x=xx, y=yy_dividends, template='plotly_dark', markers=True, title="Dividends @ uid: {}".format( selected_uid ), labels=dict(x="block", y="dividends") )
    emission_over_time = px.line( x=xx, y=yy_emission, template='plotly_dark', markers=True, title="Emission @ uid: {}".format( selected_uid ), labels=dict(x="block", y="emission") )

    return stake_over_time, rank_over_time, trust_over_time, consensus_over_time, incentive_over_time, dividends_over_time, emission_over_time

if __name__ == '__main__':
    app.run_server(host = '0.0.0.0', debug=True)

