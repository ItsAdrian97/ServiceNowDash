import pandas_datareader.data as web
import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html
from serviceNow1_1 import getIncidents
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import plotly
app = dash.Dash()
stock = 'ServiceNow'
start = datetime.datetime(2015, 1, 1)
end = datetime.datetime(2018, 2, 8)
df = getIncidents()
#print(df.Date)

##df = df.drop("Symbol", axis=1)

app.layout = html.Div(children=[
    html.H1(children='ServiceNow'),


    dcc.Graph(id='live-graph'),
        dcc.Interval(
            id='interval-component',
            interval=1*1000, # in milliseconds
            n_intervals=0
        ),
    dcc.Graph(
        id='example-graph2',
        figure={
            'data': [
                {'x': df.Date, 'y': df.closed_at, 'type': 'bar', 'name': 'Incidents Closed'},
            ],
            'layout': {
                'title': stock
            }
        }
    )
])


@app.callback(Output('live-graph', 'figure'),
              [Input('interval-component', 'n_intervals')])
    
def update_graph_scatter(input_data):
    data= getIncidents()
    print(list(data['Date']))
  
    
    return {'data': [
                {'x': [1, 2, 3, 4, 5], 'y': [9, 6, 2, 1, 5], 'type': 'line', 'name': 'Boats'},
                ],
            'layout': {
                'title': 'Basic Dash Example'
            }}
                                           


if __name__ == '__main__':
    app.run_server(debug=True)
