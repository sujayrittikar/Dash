import dash
import pandas as pd
from dash import dcc
from dash import html
from plotly import express as px

app = dash.Dash()
sample_df = pd.read_csv("sample_data.csv")
figure = px.scatter(
    x=sample_df['x'],
    y=sample_df['y'],
    render_mode="marker"
)

app.layout = html.Div([
    html.H1(
        children="A Sample Scatter Chart",
        style={
            "textAlign": "center"
        }
    ),
    dcc.Graph(
        id="scatter_chart",
        figure=figure
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)