import dash
import pandas as pd
from dash import dcc
from dash import html
import plotly.express as px
import plotly.graph_objects as go

sample_data_df = pd.read_csv("sample_data.csv")

app = dash.Dash()
figure = px.bar(sample_data_df)
figure.update_layout(barmode='group')
app.layout = html.Div([
    html.H1("Hello Dash"),
    html.Div("Dash - A Data product development framework from plotly"),
    dcc.Graph(
        id="sample-graph",
        figure=figure
    )
])


if __name__ == '__main__':
    app.run_server(debug=True)