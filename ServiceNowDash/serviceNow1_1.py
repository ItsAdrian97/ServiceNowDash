import pandas as pd
import requests
import json
from datetime import datetime, timedelta, date
from collections import Counter
from functools import reduce

# Set the request parameters
#url = 'https://dev58360.service-now.com/api/now/table/incident?sysparm_query=state=1^sys_created_onONThis month@javascript:gs.beginningOfThisMonth()@javascript:gs.endOfThisMonth()^ORDERBYnumber^ORDERBYDESCcat'
#url= "https://dev58360.service-now.com/api/now/table/incident?sysparm_query=state=1^sys_created_onON2020-05-13@javascript:gs.dateGenerate('2020-05-13','start')@javascript:gs.dateGenerate('2020-05-13','end')"
url1="https://dev58360.service-now.com/api/now/table/incident?sysparm_query=opened_atONThis month@javascript:gs.beginningOfThisMonth()@javascript:gs.endOfThisMonth()"
url2="https://dev58360.service-now.com/api/now/table/incident?sysparm_query=closed_atONThis month@javascript:gs.beginningOfThisMonth()@javascript:gs.endOfThisMonth()"
# Eg. User name="username", Password="password" for this code sample.
user = 'admin'
pwd = 'xgMPwxgQPK00'
openState = 'opened_at'
closedState = 'closed_at'

def getIncidents():
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
    #print(s)
    #print(c)
    return s
    #return c
    
   
DateRange= dateList()
getIncidents()
