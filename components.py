import dash
from dash import dcc
from dash import html

app = dash.Dash()
app.layout = html.Div([
    html.H1("Hello Dash"),
    html.Div("Dash - A Data product development framework from plotly"),
    dcc.Dropdown(options=["1", "2", "5"]),
    dcc.LogoutButton()
])


if __name__ == '__main__':
    app.run_server(debug=True)