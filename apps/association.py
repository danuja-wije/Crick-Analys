import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_extensions as de
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from app import app
import pandas as pd
import ARMModel

data = pd.read_csv("ODI(ARM).csv")
winning_teams = ['Australia','India','New Zealand','England','Sri Lanka','South Africa','Pakistan','West Indies']


anim = html.Div([
    html.Img(src=app.get_asset_url('team_celeb.gif'),id='arm-main-gif')
])
cardForm = html.Div([
    dbc.Label("Choose Your Team", html_for="team_drop"),
    dcc.Dropdown(
        id='team_drop',
        options=[{'label': i, 'value': i} for i in winning_teams],
        style={'color': 'black'},
    ),
    html.Br(),
    html.Div(id='arm-form-alert', children=[]),
    html.Center(dbc.Button("Submit", id='arm-button-submit', n_clicks=0, className='btn btn-primary btn-lg')),
    html.Br(),
    html.Div([
        html.Fieldset([
            html.Legend('Input - Output Explanation'),
            html.H6('Sample Input:'),
            html.P('Sri Lanka'),
            html.H6('Input Explanation:'),
            html.P('Selected winning Team is Sri Lanka'),
            html.H6('Sample Output:'),
            html.P('Sri Lanka->First Inning | Sri Lanka->Foreign Country'),
            html.H6('Output Explanation:'),
            html.P(
                'When Sri Lanka won matches most of the time they played in a foreign cricket ground and the inning they played was the 1st inning'),
        ])
    ],className='example-box')
], className='cardFrom')

cardDisplay = html.Div([
    html.Div(id='arm-answer', children=[])
], className='cardDisplay')

content = html.Div([
    cardForm,
    cardDisplay
], className='classify-content')

layout = html.Div(
    [
        content
    ], className='layout'
)


@app.callback(Output('arm-answer', 'children'),Output('arm-form-alert', 'children'), Input('arm-button-submit', 'n_clicks'), State('team_drop', 'value'))

def find_rules(n_clicks, value):

    if n_clicks > 0:
        if value == None:
            alert = dbc.Alert('Please Fill The Input Field And Try Again !', className='alert alert-danger')
            cover = html.Div([
                html.Img(src=app.get_asset_url('arm-cover-1.png'), id='arm-cover-1'),
                html.Div([html.H1('Please Select Your Team')], id='arm-message-box'),
                # html.Img(src=app.get_asset_url('arm-cover-2.jpg'), id='arm-cover-2')
            ], className='arm-cover')
            return cover,alert
        else:
            result = ARMModel.arm_rule(value)
            h_frequant = []
            frequant = []
            for i in result:
                if len(i)>2:
                    names = ''
                    for j in range(len(i)):
                        if j == len(i) -1:
                            names += '{}'.format(i[j])
                        else:
                            names += '{}    |   '.format(i[j])
                    h_frequant.append(names)
                else:
                    names = ''
                    for j in range(len(i)):
                        if j == len(i) - 1:
                            names += '{}'.format(i[j])
                        else:
                            names += '{}    |   '.format(i[j])
                    frequant.append(names)
            w1 = ['{}'.format(value)]*len(h_frequant)
            w2 = ['{}'.format(value)]*len(frequant)
            h_table_data = pd.DataFrame(
                {
                    "Consequents":h_frequant,
                    "Winner":w1
                }
            )
            l_table_data = pd.DataFrame(
                {
                    "Consequents": frequant,
                    "Winner": w2
                }
            )

            low_table = dbc.Table.from_dataframe(l_table_data,striped=True, bordered=True, hover=True)
            high_table = dbc.Table.from_dataframe(h_table_data,striped=True, bordered=True, hover=True)

            head = None

            if value in winning_teams:
                head = html.Div([html.Img(src=app.get_asset_url('{}_flag.png'.format(value)),id='arm-img-1'), html.H1('Team {}'.format(value)), html.Img(src=app.get_asset_url('{}_flag.png'.format(value)),id='arm-img-2')],id='arm-main-header')

            container = html.Div([
                head,
                anim,
                html.H3('Frequent Item Sets', id='arm-header-1'),
                html.Div([low_table], className='table-1'),
                html.H3('Most Frequent Item Sets', id='arm-header-2'),
                html.Div([high_table], className='table-2'),
            ],className='arm-out-box')
            return container,None
    else:
        cover = html.Div([
            html.Img(src=app.get_asset_url('arm-cover-1.png'),id='arm-cover-1'),
            html.Div(['Please Select Your Team To View'],id='arm-message-box'),
            html.Img(src=app.get_asset_url('arm-cover-2.jpg'),id='arm-cover-2')
        ],className='arm-cover')
        return cover,None
