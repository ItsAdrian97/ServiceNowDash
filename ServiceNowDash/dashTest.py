import pandas_datareader.data as web
import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html
from serviceNow1_1 import getIncidents
import pandas as pd

app = dash.Dash()
stock = 'ServiceNow'
start = datetime.datetime(2015, 1, 1)
end = datetime.datetime(2018, 2, 8)
df = getIncidents()
print(df.info())

##df = df.drop("Symbol", axis=1)

app.layout = html.Div(children=[
    html.H1(children='Whoa, a graph!'),

    html.Div(children='''
        Making a stock graph!.
    '''),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': df.Date, 'y': df.opened_at, 'type': 'line', 'name': 'Incidents Opened'},
            ],
            'layout': {
                'title': stock
            }
        }
    ),
    dcc.Graph(
        id='example-graph2',
        figure={
            'data': [
                {'x': df.Date, 'y': df.closed_at, 'type': 'line', 'name': 'Incidents Closed'},
            ],
            'layout': {
                'title': stock
            }
        }
    )
    
])

if __name__ == '__main__':
    app.run_server(debug=True)
