import psycopg2
import dash
from dash import dcc, html
import pandas.io.sql as psql
import plotly.graph_objects as go

# Establecer la conexión a la base de datos
connection = psycopg2.connect(
    host='localhost',
    user='postgres',
    password='123456789',
    database='BD_final'
)

# Consultar el tipo de vialidad y el tipo de accidente
query_vialidad_accidente = """
    SELECT v.tipo AS tipo_vialidad, a.tipo AS tipo_accidente, COUNT(*) AS count
    FROM vialidad v
    INNER JOIN accidente a ON v.latitud = a.latitud_vialidad AND v.longitud = a.longitud_vialidad
    GROUP BY v.tipo, a.tipo
"""

df_vialidad_accidente = psql.read_sql_query(query_vialidad_accidente, connection)

# Consultar la hora del accidente y el tipo de accidente
query_hora_accidente = """
    SELECT hora, tipo, COUNT(*) AS count
    FROM accidente
    GROUP BY hora, tipo
"""

df_hora_accidente = psql.read_sql_query(query_hora_accidente, connection)

# Consultar la vialidad y los accidentes
query_vialidad = "SELECT latitud, longitud FROM vialidad"
df_vialidad = psql.read_sql_query(query_vialidad, connection)

query_accidente = """
    SELECT a.latitud_vialidad, a.longitud_vialidad, v.nombre_asentamiento
    FROM accidente AS a
    INNER JOIN vialidad AS v ON a.latitud_vialidad = v.latitud AND a.longitud_vialidad = v.longitud
"""
df_accidente = psql.read_sql_query(query_accidente, connection)

# Consultar la cantidad de accidentes por asentamiento
query_accidentes_asentamiento = """
    SELECT nombre_asentamiento, COUNT(*) AS count
    FROM vialidad AS v
    INNER JOIN accidente AS a ON v.latitud = a.latitud_vialidad AND v.longitud = a.longitud_vialidad
    INNER JOIN asentamiento AS s ON v.nombre_asentamiento = s.nombre
    GROUP BY nombre_asentamiento
"""

df_accidentes_asentamiento = psql.read_sql_query(query_accidentes_asentamiento, connection)


query_accidente_resolucion = """
    SELECT tipo, estado, COUNT(*) AS count
    FROM accidente AS a
    INNER JOIN resolucion AS r ON a.folio_resolucion = r.folio
    GROUP BY tipo, estado
"""

df_accidente_resolucion = psql.read_sql_query(query_accidente_resolucion, connection)

color_map = {
    "PENDIENTE": "red",
    "EN PROCESO": "orange",
    "SOLUCIONADO": "green",
}

# Crear la aplicación Dash
app = dash.Dash(__name__)

# Estilos CSS personalizados
external_stylesheets = ['https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css']

# Diseño de la aplicación Dash
app.layout = html.Div(
    children=[
        html.H1("Análisis de Accidentes"),
        html.Div(
            children=[
                dcc.Graph(
                    id="tipo-vialidad-accidente-graph",
                    figure={
                        "data": [
                            go.Bar(
                                x=df_vialidad_accidente[df_vialidad_accidente["tipo_vialidad"] == tipo_vialidad]["tipo_accidente"],
                                y=df_vialidad_accidente[df_vialidad_accidente["tipo_vialidad"] == tipo_vialidad]["count"],
                                name=tipo_vialidad,
                                hovertemplate="<b>Tipo de Accidente</b>: %{x}<br><b>Cantidad</b>: %{y}",
                                text=df_vialidad_accidente[df_vialidad_accidente["tipo_vialidad"] == tipo_vialidad]["count"],
                                textposition="auto",
                                marker={"line": {"color": "rgb(8,48,107)", "width": 1.5}},
                            )
                            for tipo_vialidad in df_vialidad_accidente["tipo_vialidad"].unique()
                        ],
                        "layout": {
                            "xaxis": {"title": "Tipo de Accidente", "showticklabels": True},
                            "yaxis": {"title": "Cantidad", "showgrid": True},
                            "barmode": "stack",
                            "title": "Relación entre Tipo de Vialidad y Tipo de Accidente",
                            "plot_bgcolor": "white",
                            "paper_bgcolor": "white",
                            "font": {"color": "black"},
                        },
                    },
                    className="graph",
                ),
            ],
            style={"width": "50%", "display": "inline-block", "vertical-align": "top"},
            className="graph-container",
        ),
        html.Div(
            children=[
                dcc.Graph(
                    id="hora-accidente-graph",
                    figure={
                        "data": [
                            go.Bar(
                                x=df_hora_accidente[df_hora_accidente["tipo"] == tipo_accidente]["hora"],
                                y=df_hora_accidente[df_hora_accidente["tipo"] == tipo_accidente]["count"],
                                name=tipo_accidente,
                                hovertemplate="<b>Hora</b>: %{x}<br><b>Cantidad</b>: %{y}",
                                text=df_hora_accidente[df_hora_accidente["tipo"] == tipo_accidente]["count"],
                                textposition="auto",
                                marker={"line": {"color": "rgb(214,39,40)", "width": 1.5}},
                            )
                            for tipo_accidente in df_hora_accidente["tipo"].unique()
                        ],
                        "layout": {
                            "xaxis": {"title": "Hora del Accidente", "showticklabels": True},
                            "yaxis": {"title": "Cantidad", "showgrid": True},
                            "title": "Relación entre Hora del Accidente y Tipo de Accidente",
                            "plot_bgcolor": "white",
                            "paper_bgcolor": "white",
                            "font": {"color": "black"},
                        },
                    },
                    className="graph",
                ),
            ],
            style={"width": "50%", "display": "inline-block", "vertical-align": "top"},
            className="graph-container",
        ),
        html.Div(
            children=[
                dcc.Graph(
                    id="accidentes-asentamiento-graph",
                    figure={
                        "data": [
                            go.Bar(
                                x=df_accidentes_asentamiento["nombre_asentamiento"],
                                y=df_accidentes_asentamiento["count"],
                                name="Accidentes",
                                hovertemplate="<b>Asentamiento</b>: %{x}<br><b>Cantidad de Accidentes</b>: %{y}",
                                marker={"color": "orange"},
                            )
                        ],
                        "layout": {
                            "xaxis": {"title": "Asentamiento", "tickangle": 45, "showticklabels": True},
                            "yaxis": {"title": "Cantidad de Accidentes"},
                            "title": "Cantidad de Accidentes por Asentamiento",
                            "autosize": True,
                            "margin": {"l": 40, "r": 40, "t": 40, "b": 40},
                            "scrollZoom": True,
                        },
                    },
                    className="graph",
                ),
            ],
            className="graph-container"
        ),
        html.Div(
            children=[
                dcc.Graph(
                    id="accidente-resolucion-graph",
                    figure={
                        "data": [
                            go.Bar(
                                x=df_accidente_resolucion["tipo"],
                                y=df_accidente_resolucion["count"],
                                name="Cantidad de Accidentes",
                                hovertemplate="<b>Tipo de Accidente</b>: %{x}<br><b>Estado de Resolución</b>: %{marker.color}<br><b>Cantidad de Accidentes</b>: %{y}",
                                marker=dict(
                                    color=[color_map.get(estado, "gray") for estado in df_accidente_resolucion["estado"]],
                                ),
                            )
                        ],
                        "layout": {
                            "xaxis": {"title": "Tipo de Accidente"},
                            "yaxis": {"title": "Cantidad de Accidentes"},
                            "title": "Cantidad de Accidentes según Tipo de Accidente y Estado de Resolución",
                            "autosize": True,
                            "margin": {"l": 50, "r": 50, "t": 50, "b": 50},
                        },
                    },
                    className="graph",
                ),
            ],
            className="graph-container"
        ),
    ],
    className="main-container"
)


if __name__ == "__main__":
    app.run_server(debug=True)

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)