import pandas_datareader.data as web
import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import requests
import serviceNow1_1 as sn
from datetime import datetime, timedelta, date

##print(x)
app = dash.Dash()
url1= "https://dev58360.service-now.com/api/now/table/incident?sysparm_query=opened_atONThis month@javascript:gs.beginningOfThisMonth()@javascript:gs.endOfThisMonth()"
url2="https://dev58360.service-now.com/api/now/table/incident?sysparm_query=closed_atONThis month@javascript:gs.beginningOfThisMonth()@javascript:gs.endOfThisMonth()"
user = 'admin'
pwd = 'xgMPwxgQPK00'
openState = 'opened_at'
closedState = 'closed_at'
app.layout = html.Div(children=[
    html.Div(children='''
        Symbol to graph:
    '''),
##    dcc.Input(id='input', value='', type='text'),
    dcc.Interval(
            id='interval-component',
            interval=1*1000, # in milliseconds
            n_intervals=0),
    html.Div(id='output-graph'),
])

##@app.callback(
##    Output(component_id='output-graph', component_property='children'),
##    [Input(component_id='input', component_property='value')]
##)
##def update_value(input_data):
##    start = datetime.datetime(2015, 1, 1)
##    end = datetime.datetime.now()
##    x=getIncidents()
##    df = web.DataReader(input_data, 'yahoo', start, end)
##    df.reset_index(inplace=True)
##    print(x.Date)
##    df.set_index("Date", inplace=True)
##    #df = df.drop("Symbol", axis=1)
##
##    return dcc.Graph(
##        id='example-graph',
##        figure={
##            'data': [
##                {'x': x.Date, 'y': x.opened_at, 'type': 'line', 'name': input_data},
##            ],
##            'layout': {
##                'title': input_data
##            }
##        }
##    )


def getIncidents():
    url1= "https://dev58360.service-now.com/api/now/table/incident?sysparm_query=opened_atONThis month@javascript:gs.beginningOfThisMonth()@javascript:gs.endOfThisMonth()"
    url2="https://dev58360.service-now.com/api/now/table/incident?sysparm_query=closed_atONThis month@javascript:gs.beginningOfThisMonth()@javascript:gs.endOfThisMonth()"
    openDF= getRecords(url1,openState)
    closeDF= getRecords(url2,closedState)

    final = pd.DataFrame({
        'Date':DateRange},
        columns=[ 'Date']
        )
    data_frames = [openDF, closeDF,final]
    #df_merged = pd.merge(data_frames,on='Date',how='outer')
    df_merged = reduce(lambda  left,right: pd.merge(left,right,on=['Date'],
                                            how='outer'), data_frames).fillna(0)
    df_merged = df_merged.sort_values('Date')
    #print(df_merged)
    return df_merged
def getRecords(url,column):
    # Set proper headers
    print(url)
    headers = {"Accept":"application/json"}

    # Do the HTTP request
    response = requests.get(url, auth=(user, pwd), headers=headers)

    # Check for HTTP codes other than 200
    #print(response.status_code)
    if response.status_code != 200: 
        #print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.content)
        return response.status_code
        exit()

    # Decode the XML response into a dictionary and use the data
    #print(response.json())
    data = response.json()
    s= cleanData(data,column)
    return s
def daterange(date1, date2):
    for n in range(int ((date2 - date1).days)+1):
        yield date1 + timedelta(n)

def dateList():
    DateRange=[]
    start_dt = date(2020, 5, 1)
    end_dt = datetime.today().date()
    
    for dt in daterange(start_dt, end_dt):
        DateRange.append(dt.strftime('%d/%m/%Y'))
    return DateRange
    
def cleanData(data, column):
    total= len(data['result'])
    lstRecords=[]
    for i in range(total):
        record =  data['result'][i][column]
        dateObject = datetime.strptime(record,'%Y-%m-%d %H:%M:%S')
        dateObject2 = dateObject.strftime('%d/%m/%Y')
        lstRecords.append(dateObject2)
    c= Counter(lstRecords)
    s= pd.DataFrame(c.items(),columns = ['Date',column])
    s.reset_index()
    return s
    
@app.callback(Output('output-graph', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_graph(n):
    headers = {"Accept":"application/json"}
    response = requests.get(url, auth=(user, pwd), headers=headers)
    data = response.json()
    x = getIncidents()
    #print(x)
    #y = sn.getIncidents()
    return dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': x.Date, 'y': x.opened_at, 'type': 'line', 'name': n},
            ],
            'layout': {
                'title': n
            }
        }
    )
x=sn.getIncidents()
DateRange= dateList()
if __name__ == '__main__':
    
    app.run_server(debug=True)
