from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

app = Dash(__name__)

data = pd.read_csv('hermes.csv')

def generate_table(dataframe, max_rows=50):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

# os = px.bar(data, x="Sistema Operativo", y="Servicios", color="City", barmode="group")
# services = px.bar(data, x="Fruit", y="Amount", color="City", barmode="group")

app.layout = html.Div(classname="content", children=[
   ''' 
   html.H1(children='Servicio Hermes'),

    html.H4(children='Datos Hermes'),
    generate_table(data),

    html.Div(children=[
        dcc.Graph(id='os-graph', figure=os, style={'display': 'inline-block'}),
        dcc.Graph(id='services-graph', figure=services, style={'display': 'inline-block'})
    ])
    '''

    html.Div(
    className="right_content",
    children=[
        html.Div(
            className="top_metrics",
            children=[
            'This is top metrics'
            ]
        ),
        html.Div(
            'This down top metrics'
        ),
    ]
    ),

])

def create_dash():
    app.run_server(debug=True)
