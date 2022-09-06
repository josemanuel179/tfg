#!/usr/bin/python3

from dash import Dash, html, dcc, dash_table
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output

app = Dash(__name__)

df = pd.read_csv("/hermesd/hermes.csv")

colors = {"background": "#011833", "text": "#7FDBFF"}

app.layout = html.Div(
    [
        html.H1(
            "Hermes - Herramienta de gestión de servicioss Linux",
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Label("Sistema Operativo"),
                        dcc.Dropdown(
                            id="operative-system",
                            options=[
                                {"label": s, "value": s} for s in df.Maquina.unique()
                            ],
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    [
                        html.Label("Fechas Ejecuciones"),
                        dcc.Dropdown(
                            id="execution-dates",
                            options=[
                                {"label": s, "value": s} for s in df.Fecha.unique()
                            ],
                            className="dropdown",
                        ),
                    ]
                ),
            ],
            className="row",
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Label("Servicios instalados por Sistema Operativo"),
                        dcc.Graph(
                            id='install-graph',
                        ),
                    ]
                ),
                html.Div(
                    [
                        html.Label("Servicios actualizados por Sistema Operativo"),
                        dcc.Graph(
                            id='ok-graph',
                        ),
                    ]
                ),
                html.Div(
                    [
                        html.Label("Servicios desactualizados por Sistema Operativo"),
                        dcc.Graph(
                            id='nok-graph',
                        ),
                    ]
                ),
            ],
        ),
        html.Div(
            dash_table.DataTable(
                df.to_dict('records'),
                [{"name": i, "id": i} for i in df.columns])
        ),

    ],
    className="container",
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
