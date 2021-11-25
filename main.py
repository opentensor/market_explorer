import dash
import bittensor
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import plotly.figure_factory as ff


app = dash.Dash(__name__)


graph = bittensor.metagraph( subtensor = bittensor.subtensor( network='local' ) ).load()

df = pd.DataFrame(columns=['uid', 'active', 'stake','rank','trust', 'consensus', 'incentive', 'dividends', 'emission'], index=graph.uids.tolist())
for uid in graph.uids.tolist():
    df.loc[uid] = pd.Series({'uid':uid, 'active': graph.active[uid].item(), 'stake':graph.S[uid].item(), 'rank':graph.R[uid].item(), 'trust':graph.T[uid].item(), 'consensus':graph.C[uid].item(), 'incentive':graph.I[uid].item(), 'dividends':graph.D[uid].item(), 'emission':graph.E[uid].item()})

print (df)

fig7 = go.Figure(data=[go.Table(
    header=dict(values=list(df.columns),
                fill_color='paleturquoise',
                align='left'),
    cells=dict(values=df.transpose().values.tolist(),
               fill_color='lavender',
               align='left'))
])

fig1 = px.scatter(df, x="uid", y="stake", color="active")
fig2 = px.scatter(df, x="uid", y="rank", color="active" )
fig3 = px.scatter(df, x="uid", y="trust", color="active" )
fig4 = px.scatter(df, x="uid", y="consensus", color="active" )
fig5 = px.scatter(df, x="uid", y="incentive", color="active" )
fig6 = px.scatter(df, x="uid", y="dividends", color="active" )

WT = go.Figure(data=go.Heatmap( z=(graph.W > 0).int().tolist() ))
BT = go.Figure(data=go.Heatmap( z=(graph.B > 0).int().tolist() ))

WT.update_layout(autosize=False, width=2000,  height=2000)
BT.update_layout(autosize=False, width=2000,  height=2000)

markdown_text = '''
### Nakamoto network explorer
'''

app.layout = html.Div(children=[
    html.H1(children='Bittensor'),
    dcc.Markdown(children=markdown_text),
    dcc.Graph(id='stake', figure=fig1),
    dcc.Graph(id='ranks', figure=fig2),
    dcc.Graph(id='trust', figure=fig3),
    dcc.Graph(id='consensus', figure=fig4),
    dcc.Graph(id='incentive', figure=fig5),
    dcc.Graph(id='dividends', figure=fig6),
    dcc.Graph(id='weights', figure=WT),
    dcc.Graph(id='bonds', figure=BT),
    dcc.Graph(id='metagraph', figure=fig7),
])

if __name__ == '__main__':
    app.run_server(debug=False)