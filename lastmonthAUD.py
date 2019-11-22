import datetime, calendar
import rateconversion
import requests
import json

now = datetime.datetime.now()
year = now.year
month = int(now.month-1)
# print(month)
num_days = calendar.monthrange(year, month)[1]
#print(num_days)
days = [datetime.date(year, month, day).strftime("%Y-%m-%d") for day in range(1, num_days+1)]
# print(days)

con = rateconversion.connection()
cur = con.cursor()
base = "AUD"

for day in days:
    lastmonthurl = "https://api.ratesapi.io/api/"
    lastmonthurl += day
    lastmonthurl += '?base='
    lastmonthurl += base
    print(lastmonthurl)
    response = requests.get(lastmonthurl).json()
    print(response)
    json_rates = json.dumps(response['rates'])
    mySql_insert_query = """INSERT INTO lastmonthfill (date, rates) VALUES (%s, %s) """ 
    # print(response['date'])
    recordTuple = (response['date'], json_rates)
    cur.execute(mySql_insert_query, recordTuple) 
    con.commit()
    print("Record inserted successfully into lastmonthfill table")

# print("Record inserted successfully into message table")

# days = [("%Y-%m-%d", year-month-day) for day in range(1, num_days+1)]


