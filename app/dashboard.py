#!/usr/bin/python3

from dash import Dash, html, dcc, dash_table
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

app = Dash(external_stylesheets=[dbc.themes.LUX])

df = pd.read_csv("/hermesd/hermes.csv")

controls = dbc.Card(
    [
        html.Div(
            [
                dbc.Label("Sistema Operativo Derivado"),
                dcc.Dropdown(
                    id="operative-system",
                    options=[
                        {"label": col, "value": col} for col in df.Maquina.unique()
                    ],
                    value="sepal length (cm)",
                ),
            ]
        ),
        html.Div(
            [
                dbc.Label("Fechas Ejecuciones"),
                dcc.Dropdown(
                    id="execution-dates",
                    options=[
                        {"label": col, "value": col} for col in df.Fecha.unique()
                    ],
                ),
            ]
        ),
    ],
    body=True,
)

app.layout = dbc.Container(
    [
        html.H1("Hermes - Herramienta de gestión de servicios Linux"),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(controls, md=4),
                dbc.Col(dcc.Graph(id="install-graph"), md=8),
                dbc.Col(dcc.Graph(id="ok-graph"), md=8),
                dbc.Col(dcc.Graph(id="nok-graph"), md=8),
                dbc.Col(dcc.Table(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns])),
            ],
            align="center",
        ),
    ],
    fluid=True,
)


@app.callback(
    Output("install-graph", "figure"),
    Output("ok-graph", "figure"),
    Output("nok-graph", "figure"),
    Input("operative-system", "value"),
    Input("execution-dates", "value"),
)
def update_figures(selected_year, operative_system):
    
    if selected_year:
        df = df[(df.Fecha == selected_year)]

    if operative_system:
        df = df[df.Maquina <= operative_system]

    install_fig = px.bar(
        df, 
        x="Maquina", 
        y="ServiciosInstalados", 
        color="continent", 
        barmode="group"
    )

    ok_fig = px.bar(
        df, 
        x="Maquina", 
        y="ServiciosInstalados", 
        color="continent", 
        barmode="group"
    )

    nok_fig = px.bar(
        df, 
        x="Maquina", 
        y="ServiciosInstalados", 
        color="continent", 
        barmode="group"
    )

    install_fig.update_layout(
        plot_bgcolor=colors["background"],
        paper_bgcolor=colors["background"],
        font_color=colors["text"],
    )

    return install_fig, ok_fig, nok_fig

if __name__ == "__main__":
    app.run_server(debug=True, host='0.0.0.0', port = 8050)
