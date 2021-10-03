import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_extensions as de
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from app import app
import pandas as pd
import numpy as np
from scipy import stats
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from imblearn.over_sampling import SMOTE
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff


#################################################

def predictModel(input_bowler, input_venue, input_batsmen, input_non_stricker, over):
    data = pd.read_csv("ODI(Classification).csv")

    data = data.drop(
        ['inning', 'match_id', 'date', 'batting_team', 'bowling_team', 'winner', 'partnership', 'strike_rate'],
        axis=1)

    venue_key = data['venue'].unique()
    bowler_key = data['bowler'].unique()
    ball_count_key = data['ball_count'].unique()
    non_striker_key = data['non_striker'].unique()
    batsman_key = data['batsman'].unique()

    le = LabelEncoder()
    data["bowler"] = le.fit_transform(data["bowler"])
    data["venue"] = le.fit_transform(data["venue"])
    data["batsman"] = le.fit_transform(data["batsman"])
    data["non_striker"] = le.fit_transform(data["non_striker"])
    data["ball_count"] = le.fit_transform(data["ball_count"])

    venue_label = data['venue'].unique()
    bowler_label = data['bowler'].unique()
    ball_count_label = data['ball_count'].unique()
    non_striker_label = data['non_striker'].unique()
    batsman_label = data['batsman'].unique()

    z = np.abs(stats.zscore(data))
    data = data[(z < 3).all(axis=1)]

    x = data.iloc[:, :5].values
    y = data.iloc[:, 5].values

    over_fit = SMOTE()
    x, y = over_fit.fit_resample(x, y)

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.1, random_state=5)

    knn = KNeighborsClassifier()
    knn.fit(x_train, y_train)
    y_pred = knn.predict(x_test)
    print(accuracy_score(y_test, y_pred))

    venue_dict = {}
    bowler_dict = {}
    ball_count_dict = {}
    non_striker_dict = {}
    batsman_dict = {}

    for a in range(0, len(venue_label)):
        venue_dict[venue_key[a]] = venue_label[a]

    for b in range(0, len(bowler_label)):
        bowler_dict[bowler_key[b]] = bowler_label[b]

    for c in range(0, len(ball_count_label)):
        ball_count_dict[ball_count_key[c]] = ball_count_label[c]

    for d in range(0, len(non_striker_label)):
        non_striker_dict[non_striker_key[d]] = non_striker_label[d]

    for e in range(0, len(batsman_label)):
        batsman_dict[batsman_key[e]] = batsman_label[e]

    venue = input_venue
    bowler = input_bowler
    non_striker = input_non_stricker
    batsman = input_batsmen

    answer = []
    for b in range(1, 7):
        ball = (float(over) + (b * 0.1))
        test_values = [venue_dict[venue], bowler_dict[bowler], ball_count_dict[ball],
                       non_striker_dict[non_striker],
                       batsman_dict[batsman]]
        test = pd.DataFrame(test_values)
        test = test.transpose()
        y_pred = knn.predict(test)
        answer.append(y_pred[0])
        #print(ball, batsman, non_striker, bowler, venue, ' = ', y_pred)
    return answer


#################################################
data = pd.read_csv("ODI(Classification).csv")
batting_teams = data["batting_team"].unique()
bowling_teams = data["bowling_team"].unique()
venues = data["venue"].unique()

cardForm = html.Div([
    dbc.Label("Select Batting Team", html_for="batting_team_drop"),
    dcc.Dropdown(
        id='batting_team_drop',
        options=[{'label': i, 'value': i} for i in batting_teams],
        style={'color': 'black'},
        value=None,
    ),
    dbc.Label("Select Bowling Team", html_for="bowling_team_drop"),
    dcc.Dropdown(
        id='bowling_team_drop',
        options=[{'label': i, 'value': i} for i in bowling_teams],
        style={'color': 'black'},
        value=None,

    ),
    dbc.Label("Select Striker ", html_for="batsman_drop"),
    dcc.Dropdown(
        id='batsman_drop',
        style={'color': 'black'},
        options=[],
        value=None,

    ),

    dbc.Label("Select Non-Strike ", html_for="non-stricker"),
    dcc.Dropdown(
        id='non-stricker',
        style={'color': 'black'},
        options=[],
        value=None,

    ),

    dbc.Label("Select Bowler", html_for="bowler"),
    dcc.Dropdown(
        id='bowler_drop',
        style={'color': 'black'},
        options=[],
        value=None,

    ),

    dbc.Label("Select Venue", html_for="venue"),
    dcc.Dropdown(
        id='venues',
        style={'color': 'black'},
        options=[{'label': i, 'value': i} for i in venues],
        value=None,

    ),

    html.Br(),
    html.Div(id='form-alert', children=[]),
    html.Div([dbc.Label("Select Expected Overs", html_for="range-slider"),dbc.Input(type='text',disabled=True, id='slider-value', value=0)],className='range-flex'),
    dcc.Slider(id="over-range", min=0, max=49, value=0, marks={i: '{}'.format(i) for i in range(0, 50, 5)},
               included=False),

    html.Br(),
    html.Center(dbc.Button("Submit", id='button-submit', n_clicks=0, className='btn btn-primary btn-lg')),
], className='cardFrom')

cardDisplay = html.Div([
    html.Div(id='heading-fig',children=[]),
    html.Div(id='over-summary-graph',children=[]),
    html.Div(id='no-data',children=[]),
    html.Center([html.Div(id='animation-result',children=[]),html.H1(id='answer')]),
    html.Div(id='stat', children=[])
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


@app.callback(Output('slider-value', 'value'), Input('over-range', 'value'))
def update_over(over):
    return '{}'.format(over)


# filter batsmens according to Selected Team
@app.callback([Output(component_id='batsman_drop', component_property='options'),
               Output(component_id='non-stricker', component_property='options')],
              Input(component_id='batting_team_drop', component_property='value'))
def filter_Batsments(team):
    is_country = data["batting_team"] == team
    data_filtered = data[is_country]
    options = [{'label': i, 'value': i} for i in data_filtered["batsman"].unique()]
    return options, options


@app.callback(Output(component_id='bowler_drop', component_property='options'),
              Input(component_id='bowling_team_drop', component_property='value'))
def filter_bowlers(team):
    is_country = data["bowling_team"] == team
    data_filtered = data[is_country]
    options = [{'label': i, 'value': i} for i in data_filtered["bowler"].unique()]
    return options


@app.callback(
    [Output('animation-result', 'children'), Output('heading-fig', 'children'), Output('answer', 'children'),
     Output('over-summary-graph', 'children'), Output('stat', 'children'), Output('no-data', 'children'),
     Output('form-alert', 'children')],
    [Input('button-submit', 'n_clicks')],
    [
        State('batting_team_drop', 'value'),
        State('bowling_team_drop', 'value'),
        State('batsman_drop', 'value'),
        State('non-stricker', 'value'),
        State('venues', 'value'),
        State('bowler_drop', 'value'),
        State('over-range', 'value'),
    ]
)
def update_answer(n_click, batting_team, bowling_team, batsman, non_stricker, venue, bowler, overs):
    if n_click > 0:
        if batsman is None or batting_team is None or batsman is None or non_stricker is None or venue is None or bowler is None or overs is None:
            alert = dbc.Alert('Please Fill The Input Field And Try Again !', className='alert alert-danger')
            fig = None
            graph = html.H4('No Data Found', id='no-data-found')
            vs = None
            card = None
            heading_title = None
            url = "https://assets10.lottiefiles.com/packages/lf20_rc6CDU.json"
            options = dict(loop=True, autoplay=True, rendererSettings=dict(preserveAspectRatio='xMidYMid slice'))
            no_Data = html.Div([
                html.Script(src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"),
                html.Div(de.Lottie(options=options, width="50%", height="50%", url=url))
            ])
            Data_logo = None
            return Data_logo,heading_title,vs, graph, card,no_Data,alert
        else:
            # predictModel(bowler, venue, batsman, non_stricker, overs)
            answer = predictModel(bowler, venue, batsman, non_stricker, overs)
            cordinates = []
            for i in range(1, 7):
                cordinates.append([i, answer[i - 1]])
            data_f = pd.DataFrame(cordinates, columns=['Ball', 'Score'])
            print(data_f)
            tot = sum(answer)
            avg = tot /6
            fig = px.bar(data_f, x='Ball', y='Score',range_y=[0,6], height=500)
            fig.update_layout(
                transition={
                    'duration': 1000,
                    'easing': 'cubic-in-out'
                },
                hovermode='closest',
                yaxis={'title': 'Score'},
                title={'x':0.5,'xanchor':'center'},
            )
            conf = dict({'staticPlot':True})
            BA = 'Batsman -{}'.format(batsman)
            BO = 'Bowler -{}'.format(bowler)
            AV = 'Avg - {}'.format(round(avg,2))
            TO = 'Total - {}'.format(tot)
            heading_title = html.Div([
                html.Div([
                    html.Div([html.Img(src=app.get_asset_url('ball.png'),className='ball-icon'),html.P(BA)],className='inner-row'),
                    html.Div([html.Img(src=app.get_asset_url('ball.png'),className='ball-icon'),html.P(TO)],className='inner-row'),
                ],className='first-row-title'),
                html.Div([
                    html.Div([html.Img(src=app.get_asset_url('ball.png'),className='ball-icon'),html.P(BO)],className='inner-row'),
                    html.Div([html.Img(src=app.get_asset_url('ball.png'),className='ball-icon'),html.P(AV)],className='inner-row'),
                ],className='second-row-title'),
            ],className='head-card')
            vs = '{} VS {}'.format(batting_team, bowling_team)
            graph = dcc.Graph(figure=fig,responsive=True,config=conf)
            count = 0
            for i in answer:
                if i == 6:
                    count += 1
            six = count
            count = 0
            for i in answer:
                if i == 4:
                    count += 1
            four = count
            count = 0
            for i in answer:
                if 1 <= i <= 3:
                    count += 1
            single = count
            count = 0
            for i in answer:
                if i == 0:
                    count += 1
            dots = count
            label = ['Sixes', 'Fours', 'Singles', 'Dots']
            val = [six, four, single, dots]
            table_data = [['Score Type', 'Count'],
                        ['Sixe', six],
                        ['Four', four],
                        ['Single', single],
                        ['Dots', dots], ]
            table_fig = ff.create_table(table_data)

            card = html.Div(
                [
                    html.Center(html.H3('Batsman - {}'.format(batsman))),
                    html.Div([
                        html.Div([
                            dcc.Graph(figure=table_fig,responsive=True,id='stat-table',config=conf)
                        ], className='stat-detail-col'),
                        html.Div([
                            dcc.Graph(id='pie-graph', figure=go.Figure(data=[go.Pie(labels=label, values=val)]))
                        ],className='pie-chart')
                    ],className='stat-outer-box')
                ]
            )
            no_Data = None
            url = "https://assets7.lottiefiles.com/packages/lf20_3rqwsqnj.json"
            options = dict(loop=True, autoplay=True, rendererSettings=dict(preserveAspectRatio='xMidYMid slice'))
            Data_logo = html.Div([
                html.Script(src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"),
                html.Div(de.Lottie(options=options, width="50%", height="50%", url=url))
            ])
            return Data_logo,heading_title,vs, graph, card,no_Data,None
            
    else:
        fig = None
        graph = html.H4('No Data Found',id='no-data-found')
        vs = None
        card = None
        heading_title = None
        url = "https://assets10.lottiefiles.com/packages/lf20_rc6CDU.json"
        options = dict(loop=True, autoplay=True, rendererSettings=dict(preserveAspectRatio='xMidYMid slice'))
        no_Data = html.Div([
            html.Script(src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"),
            html.Div(de.Lottie(options=options, width="50%", height="50%", url=url))
        ])
        Data_logo= None
        return Data_logo,heading_title,vs, graph, card,no_Data,None
