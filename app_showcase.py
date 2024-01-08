'''
Title: Prosody-Gesture Interplay in Counting-out Rhymes
Author: @sarkadava  
Creation Date: January 2024
'''

### PACKAGES

import pandas as pd
# import plotly.express as px  
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import Dash, dcc, html, Input, Output  # pip install dash (version 2.0.0 or higher)

# Print versions of those packages


### INITIATE DASH APP

app = Dash(__name__)

### PREPARE/LOAD THE DATA

# These are our data
df = pd.read_csv('./co_rhymes_testdata/dash_ts.csv')

# Count the velocity from the m_ column
df['v_fing'] = df['m_fing'].diff()
df['v_wrist'] = df['m_wrist'].diff()
df['v_elb'] = df['m_elb'].diff()

acoustics_f = ['env', 'env_att', 'f0']
kinematics_f = ['m_fing', 'a_fing', 'v_fing', 'm_wrist', 'a_wrist', 'v_wrist', 'm_elb', 'a_elb', 'v_elb']

### APP LAYOUT

app.layout = html.Div(
    style={'backgroundColor': '#FFFFFF', 'color': '#0f0f0f'},
    children=[
    # Make some descriptions
    html.H1("Prosody-Gesture Interplay in Counting-out Rhymes", style={'textAlign': 'center'}),
    html.H3("Kadavá Šárka, Aleksandra Ćwiek, Susanne Fuchs, Wim Pouw", style={'textAlign': 'center'}),
    html.H3("This project investigates the coordination of prosody and pointing gestures in Polish counting-out rhymes. The data were acquired by Katarzyna Stoltmann at Leibniz-Center General Linguistics, Berlin. ", style={'textAlign': 'center'}),
    html.H3(
    html.A("contact: kadava@leibniz-zas.de", href="mailto:kadava@leibniz-zas.de", style={'display': 'block', 'textAlign': 'center', 'color': '#0f0f0f'})),
    html.Br(),
    # Add some dropdown menus
    html.Div([
        html.Div([
            html.Label("Speaker:", style={'textAlign': 'center'}),
            dcc.Dropdown(id="speaker",
                        options=[{'label': i, 'value': i} for i in df.speaker.unique()],
                        multi=False,
                        value="1",
                        style={'width': "90%"}
                        ),
        ], style={'width': '10%', 'display': 'inline-block'}),

        html.Div([
            html.Label("Rhyme name:", style={'textAlign': 'center'}),
            dcc.Dropdown(id="rhyme_name",
                        options=[{'label': i, 'value': i} for i in df.rhyme_name.unique()],
                        multi=False,
                        value="ent",
                        style={'width': "90%"}
                        ),
        ], style={'width': '10%', 'display': 'inline-block'}),

        html.Div([
            html.Label("Pointing hand:", style={'textAlign': 'center'}),
            dcc.Dropdown(id="point_hand",
                        options=[{'label': i, 'value': i} for i in df.point_hand.unique()],
                        multi=False,
                        value="_L",
                        style={'width': "90%"}
                        ),
        ], style={'width': '10%', 'display': 'inline-block'}),

        html.Div([
            html.Label("Speech rate:", style={'textAlign': 'center'}),
            dcc.Dropdown(id="speech_rate",
                        options=[{'label': i, 'value': i} for i in df.speech_rate.unique()],
                        multi=False,
                        value="normal",
                        style={'width': "90%"}
                        ),
        ], style={'width': '10%', 'display': 'inline-block'}),

        html.Div([
            html.Label("Select kinematic feature:", style={'textAlign': 'center'}),
            dcc.Dropdown(id="kin_feat",
                        options=[{'label': i, 'value': i} for i in kinematics_f],
                        multi=False,
                        value="m_fing",
                        style={'width': "90%"}
                        ),
        ], style={'width': '15%', 'display': 'inline-block'}),

        html.Div([
            html.Label("Select acoustic feature:", style={'textAlign': 'center'}),
            dcc.Dropdown(id="ac_feat",
                        options=[{'label': i, 'value': i} for i in acoustics_f],
                        multi=False,
                        value="env",
                        style={'width': "90%"}
                        ),
        ], style={'width': '10%', 'display': 'inline-block'}),

    ]),

    html.Br(), # Line break
    # This is our plot of interest
    dcc.Graph(id='time_series', figure={},style={'width': '49%', 'textAlign': 'center','display': 'inline-block'}),
    # This is our video player
    html.Video(controls=True, id='videoplayer', src='', style={'width': '45%', 'textAlign': 'center', 'display': 'inline-block'}, autoPlay=False, muted=True, loop=False),
    html.Br(),
    html.Br(),
    # Add some references
    html.H3("Associated outcomes:", style={'textAlign': 'center'}),
    html.P(
            [
                "Kadavá Šárka, Ćwiek Aleksandra, Stoltmann Katarzyna, Fuchs Susanne, Pouw Wim (2023).",
                " Is gesture-speech physics at work in rhythmic pointing?",
                " Evidence from Polish counting-out rhymes.",
                " In: Radek Skarnitzl & Jan Volín (Eds.), Proceedings of the 20th International Congress of Phonetic Sciences. Guarant International. ",
                html.A("Full paper", href='https://guarant.cz/icphs2023/955.pdf', target="_blank"),
            ],
            style={'textAlign': 'center'}
        ),
])

### UPDATE GRAPH

# Here we specify the inputs and outputs of the app
@app.callback(
    [Output('time_series', 'figure'),
     Output('videoplayer', 'src')],
    [Input('speaker', 'value'),
        Input('rhyme_name', 'value'),
        Input('point_hand', 'value'),
        Input('speech_rate', 'value'),
        Input('kin_feat', 'value'),
        Input('ac_feat', 'value')]
)

# Now we need to update the outputs based on the inputs
def update_graph(speaker, rhyme_name, point_hand, speech_rate, kin_feat, ac_feat):

    ## PLOTTING 
    dff = df.copy()
    dff = dff[(dff.speaker == speaker) & (dff.rhyme_name == rhyme_name) & (dff.point_hand == point_hand) & (dff.speech_rate == speech_rate)]

    if ac_feat == 'f0':
        dff[ac_feat] = dff[ac_feat].replace(0, float('nan'))

    # Create subplots with dual y-axes
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig.add_trace(go.Scatter(x=dff['time_ms'], y=dff[ac_feat], name=ac_feat, mode='lines'))
    fig.add_trace(go.Scatter(x=dff['time_ms'], y=dff[kin_feat], name=kin_feat, mode='lines'), secondary_y=True)

    # Update layout
    fig.update_layout(title='Multimodal timeseries', xaxis=dict(title='time (ms)'))

    # Update y-axis titles
    fig.update_yaxes(title_text=ac_feat, row=1, col=1)
    fig.update_yaxes(title_text=kin_feat, row=1, col=1, secondary_y=True)

    ## VIDEODATA

    # If the point_hand is _L, save hand as Left, otherwise save as Right
    hand = 'Left' if point_hand == '_L' else 'Right'
    # If the speech_rate is normal, save as '', otherwise save as fast
    speech_rate = '_' if speech_rate == 'normal' else '_fast'
    # make speaker a string
    speaker = str(speaker)
    # specify the source of the video
    src = './co_rhymes_assets/' + 'vp' + speaker + '_' + hand + speech_rate + '001.mp4'
    print(src)

    return fig, src

### ---------------------------------- RUN APP ---------------------------------- ###
if __name__ == '__main__':
    app.run_server(debug=True)