'''
This is a template for creating a Dash app.
'''

### PACKAGES

import pandas as pd
import plotly.express as px # pip install plotly
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import Dash, dcc, html, Input, Output  # pip install dash 

# Load other packages if needed

### INITIATE DASH APP

app = Dash(__name__)

### PREPARE/LOAD THE DATA

# These are our data
df = pd.read_csv('./path_to_data/file.csv')

# Familiarize yourself - print the columns of the data
print(df.columns)

### APP LAYOUT

app.layout = html.Div(
    style={'backgroundColor': '#FFFFFF', 'color': '#0f0f0f'}, 
    children=[
    # Make some descriptions
    html.H1("Title", style={'textAlign': 'center'}),
    html.H3("Some description", style={'textAlign': 'center'}),
    html.Br(), # Line breaker

    # Add some dropdown menus 
    html.Div([
        html.Div([
            html.Label("Name 1:", style={'textAlign': 'center'}),
            dcc.Dropdown(id="name1",
                        options=[{'label': i, 'value': i} for i in df.name1.unique()], # Create the options
                        multi=False,
                        value="default",
                        style={'width': "90%"}
                        ),
        ], style={'width': '10%', 'display': 'inline-block'}),

        html.Div([
            html.Label("Name 2:", style={'textAlign': 'center'}),
            dcc.Dropdown(id="name2",
                        options=[{'label': i, 'value': i} for i in df.name2.unique()], # Create the options
                        multi=False,
                        value="default",
                        style={'width': "90%"}
                        ),
        ], style={'width': '10%', 'display': 'inline-block'}),
    ]),

    # You can add any other component - check https://dash.plotly.com/dash-core-components

    html.Br(),
    # This is the plot of interest - more at https://dash.plotly.com/dash-core-components/graph
    dcc.Graph(id='graph_name', figure={},style={'width': '49%', 'textAlign': 'center','display': 'inline-block'}),
    # This is the video player - more at https://dash.plotly.com/dash-html-components/video
    html.Video(controls=True, id='videoplayer', src='', style={'width': '45%', 'textAlign': 'center', 'display': 'inline-block'}, autoPlay=False, muted=True, loop=False),
    html.Br(),
    html.Br(),
    
])

### UPDATE GRAPH

# Here we specify the inputs and outputs of the app
@app.callback(
    [Output('graph_name', 'figure'),
     Output('videoplayer', 'src')],
    [Input('name1', 'value'),
        Input('name2', 'value')]
)

# Now we need to update the outputs based on the inputs
def update_graph(name1, name2):

    # Filter the data based on the inputs
    dff = df.copy()
    dff = dff[(dff.name1 == name1) & (dff.name2 == name2)]

    ## PLOTTING 

    # Multimodal timeseries
    # Create subplots with dual y-axes
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig.add_trace(go.Scatter(x=dff['time'], y=dff[name1], name=name1, mode='lines'))
    fig.add_trace(go.Scatter(x=dff['time'], y=dff[name2], name=name2, mode='lines'), secondary_y=True)

    # Update layout
    fig.update_layout(title='Multimodal timeseries', xaxis=dict(title='time'))

    # Update y-axis titles
    fig.update_yaxes(title_text=name1, row=1, col=1)
    fig.update_yaxes(title_text=name2, row=1, col=1, secondary_y=True)

    # Scatter plot
    # fig = px.scatter(dff, x="name1", y="name2", color="color", size="size", hover_data=['hover_data'])

    ## VIDEODATA

    # Specify the source of the video
    src = './assets/' + 'video_name.mp4'
    print(src)

    return fig, src

### ---------------------------------- RUN APP ---------------------------------- ###
if __name__ == '__main__':
    app.run_server(debug=True)