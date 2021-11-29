import dash
import os
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import pandas as pd

# Update themes
import plotly.graph_objects as go
import plotly.io as pio

plotly_template = pio.templates["plotly_dark"]
print (plotly_template)

pio.templates["plotly_dark_custom"] = pio.templates["plotly_dark"]

pio.templates["plotly_dark_custom"].update({
    'layout': {
        'paper_bgcolor': '#000000', 
        'plot_bgcolor': '#000000'
    }
})

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
n_neurons_fig.update_layout(template='plotly_dark_custom')
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
    style = {'backgroundColor': '#000000', 'height':'100%', 'width':'100%' },
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
        dcc.Graph( id='values_over_time', style={'width': '100%', 'height': '50%'}),
        dcc.Slider(
            id='uid_to_values_slider',
            min = df.index.min(),
            max = df.index.max(),
            value = df.index.min(),
            marks={
                0: {'label': '0', 'style': {'color': '#77b0b1'}},
                10000: {'label': '10000', 'style': {'color': '#77b0b1'}},
                20000: {'label': '20000', 'style': {'color': '#77b0b1'}},
                30000: {'label': '30000', 'style': {'color': '#77b0b1'}},
                40000: {'label': '40000', 'style': {'color': '#77b0b1'}},
                50000: {'label': '50000', 'style': {'color': '#77b0b1'}},
                60000: {'label': '60000', 'style': {'color': '#77b0b1'}},
                70000: {'label': '70000', 'style': {'color': '#77b0b1'}},
                80000: {'label': '80000', 'style': {'color': '#77b0b1'}},
                90000: {'label': '90000', 'style': {'color': '#77b0b1'}},
                100000: {'label': '100000', 'style': {'color': '#77b0b1'}},
                110000: {'label': '110000', 'style': {'color': '#77b0b1'}},
                120000: {'label': '120000', 'style': {'color': '#77b0b1'}},
                130000: {'label': '130000', 'style': {'color': '#77b0b1'}},
                140000: {'label': '140000',  'style': {'color': '#77b0b1'}},
                150000: {'label': '150000',  'style': {'color': '#77b0b1'}},
                160000: {'label': '160000',  'style': {'color': '#77b0b1'}},
                170000: {'label': '170000',  'style': {'color': '#77b0b1'}},
                180000: {'label': '180000',  'style': {'color': '#77b0b1'}},
                190000: {'label': '190000',  'style': {'color': '#77b0b1'}},
            },
            step = 1000,
            tooltip={"placement": "bottom", "always_visible": True},
        ),
        dcc.Graph( id='uid_to_values', style={'width': '100%', 'height': '50%'}),
        # dcc.Graph( id='block_to_n', figure = n_neurons_fig),
    ]
)


@app.callback(
    Output('values_over_time', 'figure'),
    Input('uid_dropdown', 'value')
)
def update_incentive_over_time ( selected_uid ):
    x = list(df.index)
    incentive = [ block['incentive'][selected_uid] for block in df ]
    stake = [ block['stake'][selected_uid] for block in df ]
    trust = [ block['trust'][selected_uid] for block in df ]
    rank = [ block['rank'][selected_uid] for block in df ]
    dividends = [ block['dividends'][selected_uid] for block in df ]
    # emission = [ block['emission'][selected_uid] for block in df ]
    consensus = [ block['consensus'][selected_uid] for block in df ]

    # Get sorted data.
    blocks = [x for x, _ in sorted(zip(x, incentive))]
    yy_stake = [y for _, y in sorted(zip(x, stake))]
    yy_rank = [y for _, y in sorted(zip(x, rank))]
    yy_trust = [y for _, y in sorted(zip(x, trust))]
    yy_conensus = [y for _, y in sorted(zip(x, consensus))]
    yy_incentive = [y for _, y in sorted(zip(x, incentive))]
    yy_dividends = [y for _, y in sorted(zip(x, dividends))]
    # yy_emission = [y for _, y in sorted(zip(x, emission))]

    fig = make_subplots(rows=3, cols=2)
    fig.add_trace(  go.Scatter ( x = blocks, y = yy_stake, name="stake"), row=1, col=1 )
    fig.add_trace(  go.Scatter ( x = blocks, y = yy_rank, name="rank"), row=1, col=2 )
    fig.add_trace(  go.Scatter ( x = blocks, y = yy_trust, name="trust"), row=2, col=1 )
    fig.add_trace(  go.Scatter ( x = blocks, y = yy_conensus, name="cosensus"), row=2, col=2 )
    fig.add_trace(  go.Scatter ( x = blocks, y = yy_incentive, name="incentive"), row=3, col=1 )
    fig.add_trace(  go.Scatter ( x = blocks, y = yy_dividends, name="dividends"), row=3, col=2 )
    fig.update_layout(template='plotly_dark_custom')
    fig.update_layout( title_text="UID:{}".format(selected_uid) )
    #fig.update_layout( transition_duration=500 )
    return fig

@app.callback(
    Output('uid_to_values', 'figure'),
    Input('uid_to_values_slider', 'value')
)
def update_uid_to_incentive ( selected_block ):
    closest_index = list(df.index)[0]
    for val in list(df.index):
        if val <= selected_block:
            closest_index = val
        else:
            break
    df_filter = df[ closest_index ]

    fig = make_subplots(rows=3, cols=2)
    fig.add_trace( go.Scatter ( x=df_filter["uid"], y=df_filter["stake"], name="stake"),  row=1, col=1  )
    fig.add_trace( go.Scatter ( x=df_filter["uid"], y=df_filter["rank"], name="rank"),  row=1, col=2  )
    fig.add_trace( go.Scatter ( x=df_filter["uid"], y=df_filter["trust"], name="trust" ),  row=2, col=1  )
    fig.add_trace( go.Scatter ( x=df_filter["uid"], y=df_filter["consensus"], name="consensus" ),  row=2, col=2  )
    fig.add_trace( go.Scatter ( x=df_filter["uid"], y=df_filter["incentive"], name="incentive" ),  row=3, col=1  )
    fig.add_trace( go.Scatter ( x=df_filter["uid"], y=df_filter["dividends"], name="dividends" ), row=3, col=2  )
    fig.update_layout(template='plotly_dark_custom')
    fig.update_layout( title_text="Block:{}".format(selected_block) )
    #fig.update_layout( transition_duration=500 )
    return fig

if __name__ == '__main__':
    app.run_server(host = '0.0.0.0', debug=True)

