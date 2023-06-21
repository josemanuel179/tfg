#!/usr/bin/python3

import dash
import datetime
import pandas as pd
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash.dependencies import Input, Output

# Instanciación del dashboard
app = dash.Dash(external_stylesheets=[dbc.themes.FLATLY])

# Cargar el archivo CSV
df = pd.read_csv('/hermesd/hermes.csv')

# Actualización de formato de la fecha de los datos para incluir en el dashboard
df['Fecha'] = pd.to_datetime(df['Fecha'], format='%Y-%m-%d %H:%M:%S')

# Total de 'ServiciosOK' y 'ServiciosOK' por sistema operativo
servicios_por_so = df.groupby('Maquina').agg({'ServiciosOK': 'sum', 'ServiciosNOK': 'sum'}).reset_index()

# Listado con los tipos de sistema operativo disponibles en los datos
tipos_os = ['Fedora', 'Debian', 'Opensuse']

# Listado con las Fechas únicas, que se encuentran dentro de los datos
dates = df['Fecha'].dt.date.unique()

# Fecha del día actual
today = datetime.date.today()

# -------------------------------------------------

# Div con el diseño del panel de configuración
config_panel = html.Div([
    
   # Nueva fila
    dbc.Row([
        
        # Encabazado para el panel de configuración
        html.H3('Parámetros de configuración',
        style={'margin-top': '16px', 'margin-left': '24px'})
    ],
    style={"height": "5vh"},
    className='bg-primary text-white font-italic'
    ),

    # Nueva fila 
    dbc.Row([

        # Div con el elementos disponibles dentro del panel de configuración
        html.Div([

            # Títutlo del desplegable con los sistemas operativos
            html.H4('Sistemas Operativos',
                style={'margin-top': '8px', 'margin-bottom': '4px'},
                className='font-weight-bold'),

            # Desplegable con los sistemas operativos incluidos en los datos
            dcc.Dropdown(
                id='dropdown-so',

                # Listado de opciones con los sistemas operativos 
                options=tipos_os,
                
                # Listado de opciones con los sistemas operativos inlcuidos al incio de la recarga del dashboard
                value= tipos_os,

                # Habilitada la opción de seleccionar multiples sistemas operativos
                multi=True
            ),

            # Títutlo del selector de fechas
            html.H4('Intervalo de fechas',
                style={'margin-top': '8px', 'margin-bottom': '4px'},
                className='font-weight-bold'),
            
            # Selector de fechas
            dcc.DatePickerRange(
                id='date-range',

                # Fecha mínima permitida del desplegable, que será igual a la fecha mínima de la lista 'dates'
                min_date_allowed= today,

                # Fecha máxima permitida del desplegable, que será igual a la fecha mínima de la lista 'dates'
                max_date_allowed= today + datetime.timedelta(days=365),

                # Fecha mínima del desplegable, que será igual a la fecha mínima de la lista 'dates'
                start_date= today,

                # Fecha máxima del desplegable, que será igual a la fecha mínima de la lista 'dates'
                end_date= today + datetime.timedelta(days=365),

                # Formato de visualización
                display_format='DD/MM/YYYY'
            )
            
            ],
        style={'height': '50vh', 'margin': '8px'}),
    ])
])

# -------------------------------------------------

# Div con el diseño del panel de contenidos
content_panel = html.Div([

    # Nueva fila
    dbc.Row([
        
        # Columna para la gráfica de barras con el histórico de los servicios
        dbc.Col([

            # Títutlo de la gráfica de barras con el histórico de los servicios
            html.H4('Histórico del estado de los servicios',
                className='font-weight-bold')
         ]),

        # Gráfica de barras con el histórico de los servicios
        dcc.Graph(
            id='hitoric-grahp',
        )

    ],
    style={'height': '50vh', 'margin': '8px'}
    ),

    # Nueva fila
    dbc.Row([

        # Columna para la gráfica circular con los porcentages 'servicios ok' vs 'servicios nok'
        dbc.Col([

            # Títutlo de la gráfica circular con los porcentages 'servicios ok' vs 'servicios nok'
            html.H4('Servicios OK vs NOK',
                className='font-weight-bold'),
            
            # Gráfica circular con los porcentages 'servicios ok' vs 'servicios nok'
            dcc.Graph(
                id='round-grahp',    
            )
        ]),

        # Columna para la gráfica de barras con los servicios por 'sistema operativo'
        dbc.Col([

             # Títutlo de la gráfica de barras con los servicios por 'sistema operativo'
            html.H4('Estado de los servicios por Sistema Operativo',
                className='font-weight-bold'),
            
            # Gráfica de barras con los servicios por 'sistema operativo'
            dcc.Graph(
                id='update-grahp')
        ])
        ],
        style={'height': '50vh',
            'margin-top': '16px', 'margin-left': '8px',
            'margin-bottom': '8px', 'margin-right': '8px'})        
])

# -------------------------------------------------

# Definción del diseño del dashboard
app.layout = dbc.Container([

    # Nueva fila
    dbc.Row([

        # Columna con el panel del configuración
        dbc.Col(config_panel, width=3, className='bg-light'),

        # Columna con el panel de contenidos
        dbc.Col(content_panel, width=9)
        ],
        style={"height": "100vh"}
        ),
    ],
    fluid=True
)

# -------------------------------------------------

# Función de callback para actualizar la gráfica de barras con el histórico de los servicios
@app.callback(
    Output('hitoric-grahp', 'figure'),
    Input('dropdown-so', 'value'),
    Input('date-range', 'start_date'),
    Input('date-range', 'end_date')
)
def actualizar_grafica_historico(os_seleccionados, start_date, end_date):
    
    # Filtrado del dataframe en base a los sistemas operativos seleccionados
    data = (df[df['Maquina'].isin(os_seleccionados)])

    # Filtrado del dataframe en base al rago de fechas seleccionadas
    df_filtrado = data[(data['Fecha'] >= pd.to_datetime(start_date + ' 00:00:00', format='%Y-%m-%d %H:%M:%S')) & (data['Fecha'] <= pd.to_datetime(end_date + ' 23:59:59', format='%Y-%m-%d %H:%M:%S'))]

    # Longitud de los datos incluidos en el eje de las x
    numeros_x = list(range(len(df_filtrado['Fecha'])))

    # Listado de str() con las fechas
    fechas_str = [element.strftime("%Y-%m-%d %H:%M:%S") for element in list(df_filtrado['Fecha'])]

    # Creación de la estrucutra de la gráfica de barras
    figure= go.Figure(
        data = [
            
            # Creación de las barras de la gráfica, cada una especificando su nombre y columna del fichero de datos
            go.Bar(x = numeros_x, y = df_filtrado['ServiciosInstalados'], name = 'Servicios Instalados', text = 'Servicios Instalados', marker = dict(color = ['green'] * df_filtrado.shape[0])),
            go.Bar(x = numeros_x, y = df_filtrado['ServiciosOK'], name = 'Servicios OK', text = 'Servicios OK', marker = dict(color = ['blue'] * df_filtrado.shape[0])),
            go.Bar(x = numeros_x, y = df_filtrado['ServiciosNOK'], name = 'Servicios NOK', text = 'Servicios NOK', marker = dict(color= ['red'] * df_filtrado.shape[0])),
            go.Bar(x = numeros_x, y = df_filtrado['ServiciosActualizados'], name = 'Servicios Actualizados', text = 'Servicios Actualizados', marker = dict(color = ['orange'] * df_filtrado.shape[0])),
        ],

        layout=go.Layout(

            # Especificación del tipo de gráfica de barras agrupadas
            barmode='group',
            
            # Especificación de los nombres de los ejes
            xaxis=dict(title='Fecha', tickvals = numeros_x, ticktext = fechas_str, tickangle = 45),
            yaxis=dict(title='Número de Servicios'),

            # Especificación de margenes y colores
            margin=dict(l=40, r=20, t=20, b=20),
            plot_bgcolor = '#f8f9fa',
            paper_bgcolor='#f8f9fa'
        )
    )

    # Se devuelve la gráfica de barras
    return figure

# -------------------------------------------------

# Función de callback para actualizar la gráfica de barras con la comparativa entre 'servicios ok' vs 'servicios nok'
@app.callback(
    Output('round-grahp', 'figure'),
    Input('dropdown-so', 'value'),
    Input('date-range', 'start_date'),
    Input('date-range', 'end_date')
)
def actualizar_grafica_circular(os_seleccionados, start_date, end_date):
    
    # Filtrado del dataframe en base a los sistemas operativos seleccionados
    data = (df[df['Maquina'].isin(os_seleccionados)])

    # Filtrado del dataframe en base al rago de fechas seleccionadas
    df_filtrado = data[(data['Fecha'] >= pd.to_datetime(start_date + ' 00:00:00', format='%Y-%m-%d %H:%M:%S')) & (data['Fecha'] <= pd.to_datetime(end_date + ' 23:59:59', format='%Y-%m-%d %H:%M:%S'))]
    
    # Agrupación de los datos por sistemas operativos y calculo la suma de 'servicios ok' y 'servicios nok'
    servicios_por_so = df_filtrado.groupby('Maquina').agg({'ServiciosOK': 'sum', 'ServiciosNOK': 'sum'}).reset_index()

    # Creación de la estrucutra de la gráfica circular
    figure=go.Figure(
        data=[

            # Creación de la gráfica circular
            go.Pie(

                # Etiquetas de la gráfica
                labels=['Servicios OK', 'Servicios NOK'],

                # Valores para la gáfica
                values=[df_filtrado['ServiciosOK'].sum(), df_filtrado['ServiciosNOK'].sum()],

                # Etiquetas para cada valor de la gráfica
                textinfo='label+percent',

                # Orientación de las etiquetas
                insidetextorientation='radial',

                # Posición de las etiquetas
                textposition='outside',
                
                # Anchura del circulo central
                hole=0.4,

                # Colores para cada etiqueta
                marker=dict(colors=['blue', 'red'])
            )
        ],

        layout=go.Layout(

            # Especificación de colores
            plot_bgcolor = '#f8f9fa', 
            paper_bgcolor='#f8f9fa'
        )
    )

    # Se devuelve la gráfica circular
    return figure

# -------------------------------------------------

# Función de callback para actualizar la gráfica de barras con los servicios por 'sistema operativo'
@app.callback(
    Output('update-grahp', 'figure'),
    Input('dropdown-so', 'value'),
    Input('date-range', 'start_date'),
    Input('date-range', 'end_date')
)
def actualizar_grafica_por_so(os_seleccionados, start_date, end_date):
    
    # Filtrado del dataframe en base a los sistemas operativos seleccionados
    data = (df[df['Maquina'].isin(os_seleccionados)])

    # Filtrado del dataframe en base al rago de fechas seleccionadas
    df_filtrado = data[(data['Fecha'] >= pd.to_datetime(start_date + ' 00:00:00', format='%Y-%m-%d %H:%M:%S')) & (data['Fecha'] <= pd.to_datetime(end_date + ' 23:59:59', format='%Y-%m-%d %H:%M:%S'))]

    # Agrupación de los datos por sistemas operativos y calculo la suma de 'servicios ok' y 'servicios nok'
    servicios_por_so = df_filtrado.groupby('Maquina').agg({'ServiciosActualizados': 'sum', 'ServiciosOK': 'sum', 'ServiciosNOK': 'sum'}).reset_index()

    # Creación de la estrucutra de la gráfica de barras
    figure = go.Figure(
        data=[

            # Creción barra para los 'servicios ok'
            go.Bar(

                # Especificación de los datos por eje
                x = servicios_por_so['Maquina'],
                y = servicios_por_so['ServiciosOK'],

                # Especificación del nombre
                text = 'Servicios OK',
                name = 'Servicios OK',

                # Especificación del color de la barra
                marker = dict(color='blue')
            ),

            # Creción barra para los 'servicios ok'
            go.Bar(

                # Especificación de los datos por eje
                x = servicios_por_so['Maquina'],
                y = servicios_por_so['ServiciosNOK'],

                # Especificación del nombre
                text = 'Servicios NOK',
                name = 'Servicios NOK',

                # Especificación del color de la barra
                marker = dict(color='red')
            ),

            # Creción barra para los 'servicios actualizados'
            go.Bar(

                # Especificación de los datos por eje
                x = servicios_por_so['Maquina'],
                y = servicios_por_so['ServiciosActualizados'],

                # Especificación del nombre
                text = 'Servicios Actualizados',
                name = 'Servicios Actualizados',

                # Especificación del color de la barra
                marker = dict(color='orange')
            )
        ],
        
        layout=go.Layout(

            # Especificación de los nombres de los ejes
            xaxis = dict(title='Sistema Operativo'),
            yaxis = dict(title='Número de Servicios'),
            
            # Especificación de colores
            plot_bgcolor = '#f8f9fa', 
            paper_bgcolor='#f8f9fa'
        )
    )

    # Se devuelve la gráfica de barras
    return figure

# -------------------------------------------------

# Ejecución la aplicación Dash
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug = False, port = 8020)