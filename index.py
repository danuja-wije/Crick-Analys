import time
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from app import app
from app import server

from apps import association, classification

header = html.Div([
    dbc.Row([
        html.Img(src=app.get_asset_url('logo_world.png'), id='logo'),
        dbc.Col([
            dbc.Row([
                html.H1(["Crick Analysis"], id='header_name'),
            ], className='logo_text_1'),
            dbc.Row([
                html.H6("Online player forecast & predictor")
            ])
        ])
    ]),
    html.Div(id='nav_home', children=[])
], className='header_box')

carousel = dbc.Carousel(
    items=[
        {"key": "1", "src": app.get_asset_url('caro-1.jpg')},
        {"key": "2", "src": app.get_asset_url('caro-2.jpg')},
        {"key": "3", "src": app.get_asset_url('caro-3.jpg')},
        {"key": "4", "src": app.get_asset_url('caro-4.jpg')},
        {"key": "5", "src": app.get_asset_url('caro-5.jpg')},
    ],
    controls=False,
    indicators=False,
    interval=3000,
    ride="carousel",
    id='car',
)
bowler = html.B('Bowler')
Striker = html.B('Striker')
Venue = html.B('Venue')
Over = html.B('Over')
Non_Striker = html.B('Non-Striker')
card = html.Div([
    html.Div([
        dbc.Row([
            dbc.Col([
                html.H6("Player Runs Forecast"),

                html.P(
                    'Choose the Striker, Bowler, Non-Striker, Venue and Over to predict, how the Striker will score through out each ball in the over. Use our ML model to forecast the match like a real game changer.'),
                html.Center(dbc.Button("Predict", id='btn-1', href='/apps/classification', value=1))
            ], className='btn-box')
        ])
    ], className='inner-box'),

    html.Div([
        dbc.Row([
            dbc.Col([
                html.H6("Find The Winning Patterns"),
                html.P(
                    "Choose the opposition team to find the patterns of their winnings in different conditions. Use Our Association Rule Mining Model to identify hidden relationship for each team management."),
                html.Center(dbc.Button("Start Find", id='btn-2', href='/apps/association', value=2))
            ], className='btn-box')
        ])
    ], className='inner-box')
], className='button-card')

absolute_content = html.Div(className='absolute_content')

content = html.Div([
    carousel,
], className='content')

footer = html.Footer([
    html.P("Copyright 2021 © Team-13. All Rights Reserved.")
], className='footer')

home_content = html.Div([
    content,
    card,
])

app.layout = html.Div(
    [
        dcc.Location(id='url', refresh=False),
        header,
        dcc.Loading(type='default', id='loading-1', children=[
            html.Div(id='page_content', children=[]),
        ]),
        footer
    ], className='container-fluid'
)
nav = html.Div([
    dbc.Button(
        children=[
            html.Img(src=app.get_asset_url('left_arrow.png'), id='back_arrow_icon'),
            html.Img(src=app.get_asset_url('home.png'), id='home_icon'),
        ],
        href='/',
        style={"margin-top": "20px", "margin-bottom": "15px", "background": 0, "border": 0, "text-align": "center",
               "padding": "5px"}
    )
])


@app.callback([Output(component_id='page_content', component_property='children'),
               Output(component_id='nav_home', component_property='children')],
              Input(component_id='url', component_property='pathname'))
def load_content(pathname):
    if pathname == '/':
        return home_content, None
    elif pathname == '/apps/classification':
        return classification.layout, nav
    elif pathname == '/apps/association':
        return association.layout, nav
    else:
        return ["404 Error"], nav


if __name__ == "__main__":
    app.run_server(debug=True)
