import pandas as pd
import requests
import json
from datetime import datetime, timedelta, date
from collections import Counter

# Set the request parameters
#url = 'https://dev58360.service-now.com/api/now/table/incident?sysparm_query=state=1^sys_created_onONThis month@javascript:gs.beginningOfThisMonth()@javascript:gs.endOfThisMonth()^ORDERBYnumber^ORDERBYDESCcat'
#url= "https://dev58360.service-now.com/api/now/table/incident?sysparm_query=state=1^sys_created_onON2020-05-13@javascript:gs.dateGenerate('2020-05-13','start')@javascript:gs.dateGenerate('2020-05-13','end')"
url="https://dev58360.service-now.com/api/now/table/incident?sysparm_query=state=1^opened_atONThis month@javascript:gs.beginningOfThisMonth()@javascript:gs.endOfThisMonth()"
# Eg. User name="username", Password="password" for this code sample.
user = 'admin'
pwd = 'xgMPwxgQPK00'


def getIncidents():
    # Set proper headers
    headers = {"Accept":"application/json"}

    # Do the HTTP request
    response = requests.get(url, auth=(user, pwd), headers=headers)

    # Check for HTTP codes other than 200
    print(response.status_code)
    if response.status_code != 200: 
        print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:', response.content)
        return response.status_code
        exit()

    # Decode the XML response into a dictionary and use the data
    #print(response.json())
    data = response.json()
    s= cleanData(data)
    return s
def daterange(date1, date2):
    for n in range(int ((date2 - date1).days)+1):
        yield date1 + timedelta(n)

def dateList():
    start_dt = date(2015, 12, 20)
    end_dt = datetime.today().date()
    
    for dt in daterange(start_dt, end_dt):
        print(dt.strftime('%d/%m/%Y')) 
    
def cleanData(data):
    total= len(data['result'])
    lstCreated=[]
    for i in range(total):
        createdDate =  data['result'][i]['opened_at']
        dateObject = datetime.strptime(createdDate,'%Y-%m-%d %H:%M:%S')
        dateObject2 = dateObject.strftime('%d/%m/%Y')
        lstCreated.append(dateObject2)
    c= Counter(lstCreated)
    s= pd.DataFrame(c.items(),columns = ['Date','Count'])
    s.reset_index()
    
    return s
    
   
#dateList() 
getIncidents()
