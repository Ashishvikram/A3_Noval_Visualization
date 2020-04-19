import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd
import numpy as np

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv("diamonds.csv")

available_color = df['color'].unique()
available_cut = df['cut'].unique()
available_clarity = df['clarity'].unique()
available_measures = ['carat', 'depth', 'table', 'price']
available_dimensions = ['color','clarity','cut']


clarity_score = {'I1':0.125,'SI2':0.25, 'SI1':0.375, 'VS1':0.5, 'VS2':0.625, 'VVS2':0.75, 'VVS1':0.875, 'IF':1}

df['clarity_value'] = df['clarity'].map(clarity_score)

# fig = px.scatter_3d(df, x='x', y='y', z='z',
#                color='color',symbol='cut', size='clarity_value')


app.layout = html.Div([

        html.Div([
            html.Label('Color'),
            dcc.Checklist(
                id='available_color',
                options=[{'label': i, 'value': i} for i in available_color],
                value=['D','J'],
                labelStyle={'display': 'inline-block'}

            ),html.Label('Cut'),
            dcc.Checklist(
                id='available_cut',
                options=[{'label': i, 'value': i} for i in available_cut],
                value=['Ideal','Premium','Fair'],
                labelStyle={'display': 'inline-block'}
            ),html.Label('Clarity'),
            dcc.Checklist(
                id='available_clarity',
                options=[{'label': i, 'value': i} for i in available_clarity],
                value=['I1','IF'],
                labelStyle={'display': 'inline-block'}
            ),html.Label('Measures'),
            dcc.RadioItems(
                id='available_measures',
                options=[{'label': i, 'value': i} for i in available_measures],
                value='carat',
                labelStyle={'display': 'inline-block'}
            )
        ],style={'width': '49%', 'display': 'inline-block','margin-bottom':'5px'}),
        html.Div([html.Div([
        html.H3('Dimension Complexity'),
            dcc.Graph(
                id='final_output',
                # figure= fig,
            )
        ], className="six columns"),
        html.Div([
        html.H3('Measures Complexity'),
            dcc.Graph(
                id='final_output_2',
                # figure= fig,
            )
        ], className="six columns"),
],className="row")
])


@app.callback(
    dash.dependencies.Output('final_output','figure'),
    [dash.dependencies.Input('available_color', 'value'), dash.dependencies.Input('available_cut', 'value'),
     dash.dependencies.Input('available_clarity', 'value')])

def update_graph(col,cut,clar):
    dff = df[df.color.isin(col) & df.clarity.isin(clar) & df.cut.isin(cut)]
    trace_1 = px.scatter_3d(dff, x='x', y='y', z='z',
               color='color',symbol='cut', size='clarity_value')

    fig = go.Figure(data = trace_1)

    return fig

@app.callback(
    dash.dependencies.Output('final_output_2','figure'),
    [dash.dependencies.Input('available_color', 'value'), dash.dependencies.Input('available_cut', 'value'),
     dash.dependencies.Input('available_clarity', 'value'),dash.dependencies.Input('available_measures', 'value')])

def update_graph(col,cut,clar,msr):
    dff = df[df.color.isin(col) & df.clarity.isin(clar) & df.cut.isin(cut)]
    trace_1 = px.scatter_3d(dff, x='x', y='y', z='z',
               color=msr)
    fig = go.Figure(data = trace_1)
    return fig



if __name__ == '__main__':
    app.run_server(debug=True)