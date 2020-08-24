
# IMPORT MODULES
import pandas as pd
from datetime import datetime as dt

# Function returns a connection
# def preprocess_data(data,resampleFreq='30S'):
#     df = pd.DataFrame.from_dict(data).set_index('record_id')
# 
#     #Next round of improvements will store these values in the db
#     # with the correct type, rendering the following 2 lines of code unnecessary:
#     df['when_day_time']= pd.to_datetime(df['when_day_time'])
#     df[['tempF','humidity']] = df[['tempF','humidity']].astype('float64')
# 
#     # Filter 
#     whichYr=2020
#     whichMonth=7
#     whichDay=27
#     newDf = df[(df.when_day_time.dt.year>=whichYr) & (df.when_day_time.dt.month==whichMonth)& (df.when_day_time.dt.day>=whichDay)]
# 
#     #Pivot & Resample 
#     return(newDf.pivot(index='when_day_time',columns='sensor_id',values=['tempF','humidity']).resample(resampleFreq).mean())
    
# --------------------------------
# WHILE LOCAL: 
# 1- READ DATA FROM MySQL DATABASE:
#data = returnData(dbname='temp_project')

# 2- CONVERT DATA from dictCursor to dataFrame:
#df = preprocess_data(data)

# ONCE DEPLOYED TO HEROKU
# 1- Import saved csv to dataframe:
df = pd.read_csv("./data/interim/Temperature_data.csv", index_col=0, header=[0,1], parse_dates=True)

# --------------------------------
# DEFINE COLORS & LABELS FOR GRAPHING SENSOR DATA
sensors = {'dht02': {'color': '#F44DDB', 'label': "Upstairs: Alex's old room"},
            'dht04': {'color': '#CF1214', 'label': "Upstairs: Master bedroom"},
            'dht01': {'color': '#0E3DEC', 'label': "Downstairs: Barb office"},
            'dht03': {'color': '#25E4F0', 'label': "Downstairs: Dining area"}}
                            
# IMPORT MORE MODULES
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Try to make interactive slider
import plotly.graph_objs as go
from plotly.offline import init_notebook_mode, iplot
# init_notebook_mode(connected=True)
import chart_studio.plotly as py
import plotly

# INITIALIZE DASH APP
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

top_markdown_text = '''
*v1.1
Early version of dashboard to display realtime(ish) temp sensor readings.*
'''
last_updated_text = "**Last updated:"+df.index.max().strftime("%m/%d/%Y, %H:%M:%S")+"**"

# APP.LAYOUT
app.layout = html.Div([

    html.Div([html.H1("Home Monitoring Dashboard")],
            style={'textAlign': "center", "padding-bottom": "5"}),

    # HEADER

    # DROPDOWN w Metric-to-display
    dcc.Markdown(children=top_markdown_text),

    html.Div([html.Span("Metric to display : ", className="six columns",
            style={"text-align": "right", "width": "40%", "padding-top": 10}),

    dcc.Dropdown(id="value-selected", value='tempF',
            options=[{'label': "Temperature ", 'value': 'tempF'},
                    {'label': "Humidity ", 'value': 'humidity'}],
            style={"display": "block", "margin-left": "auto", "margin-right": "auto",
                                                     "width": "70%"},
            className="six columns")], className="row"),

    # -FIGURE- LINE GRAPH
    dcc.Graph(id='line_graph_1'),
    # dcc.Graph(id='line_graph_1',

    html.Div([
        dcc.Markdown(children=last_updated_text)],
            style={"textAlign": "left", "width": "100%"}),
    html.Hr(),	
    ],
)

@app.callback(
    Output("line_graph_1", "figure"),
    [Input("value-selected", "value")]
)
def update_line_graph(selected):
    def title(text):
        if text == "tempF":
            return "Temperature"
        elif text == "humidity":
            return "Humidity"

    dfRaw = df.xs(key=selected, axis=1, level=0) #show temp readings from all sensors 
    dfSmooth = dfRaw.rolling(window=4).mean()#.rename(columns={'dht01':'dht01_avg','dht02':'dht02_avg','dht03':'dht03_avg','dht04':'dht04_avg'})
 
    data = list()
    for s_id in list(sensors.keys()):
        data.append(
            go.Scatter(x=dfSmooth.index, y=dfSmooth[s_id], name = sensors[s_id]['label'], 
                line = dict(color = sensors[s_id]['color'], width = 4), opacity = 0.8))
    layout = dict(
        title=title(selected)+" Readings \n(try interactive slider)",
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,label='1hr',step='hour',stepmode='backward'),
                    dict(count=6,label='6hr',step='hour',stepmode='backward'),
                    dict(step='all')
                ])
            ),
            rangeslider=dict(
                visible = True
            ),
        type='date'
        )
    )
    figure = dict(data=data, layout=layout)
    return figure

if __name__ == '__main__':
	app.run_server(debug=True)
