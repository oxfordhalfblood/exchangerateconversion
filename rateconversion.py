
import requests
import json
import pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
import configparser
# import sqlalchemy as db

filelist = []                                 # this is our queue
filelist.append('msg1.json')
filelist.append('msg2.json')

def connection():
    config = configparser.RawConfigParser()
    config.read('config.ini')
    return MySQLdb.connect(host=config.get('mysqlDB', 'host'),   # your host, usually localhost
                        user=config.get('mysqlDB', 'user'),         # your username
                        passwd=config.get('mysqlDB', 'passwd'),  # your password
                        db=config.get('mysqlDB', 'db'),          # name of the data base
                        port=int(config.get('mysqlDB', 'port'))
                        ) 

def insertintotable(in_base, in_action, created_at, in_date, in_rates): 
    #  must create a Cursor object. It will let execute all the queries 
    con = connection()
    cur = con.cursor()
    #  all in query has to be string           
    mySql_insert_query = """INSERT INTO message (action, base, createdat, date) VALUES (%s, %s, %s, %s) """ 
    recordTuple1 = (in_action, in_base, created_at, in_date)
    
    cur.execute(mySql_insert_query, recordTuple1)
    msg_id = con.insert_id()                  # get the foreign key (msgid)
    print("Record inserted successfully into message table")
    # print(msg_id)

    for currency in in_rates:
        # print(currency)                        # get keys:  HKD, CAD, CZK, NOK
        rate = in_rates[currency]              # get values of the keys like- 5.0525983456
        mySql_insert_query2 = """INSERT INTO conversion (msgid, currency, rate) VALUES (%s, %s, %s) """ 
        recordTuple2 = (msg_id, currency, rate)
        cur.execute(mySql_insert_query2, recordTuple2)

    con.commit()
    print("Record inserted successfully into conversion table")

    cur.execute("SELECT * FROM message")
    # print all the first cell of all the rows
    print("Message Table: ")
    for row in cur.fetchall():
        print(row)
    
    cur.execute("SELECT * FROM conversion")
    # print all the first cell of all the rows
    print("Conversion Table: ")

    for row in cur.fetchall():
        print(row)

    con.close()


def apiextract(defaulturl, msg):

    if 'base' in msg['context']:
        defaulturl += '?base='
        defaulturl += msg['context']['base']
        # print(defaulturl)

    if 'symbols' in msg['context'] and (msg['context']['symbols']!=''):
        symbol = msg['context']['symbols']

        if symbol != None:
            defaulturl += '&symbols='
            gettype = type(symbol)

            if gettype == type([]):
                count = 0

                for i in symbol:
                    defaulturl += i

                    if count != len(symbol)-1:
                        defaulturl += ','

                    count += 1

            elif gettype == type(" "):
                defaulturl += symbol
                # print(defaulturl)

    
    if requests.get(defaulturl).status_code == 200:
        response = requests.get(defaulturl).json()
    else:
        print('Web site does not exist')
        return 0

    print("Api response: ",response)  # dict type
    out_base = response['base']
    out_rates = response['rates']
    out_date = response['date']
    # print(out_base)
    
    if 'created_at' not in msg:
        msg['created_at']= None

    if 'base' not in msg:
        msg['base']= None

    insertintotable(msg['action'], msg['context']['base'], msg['created_at'], out_date, out_rates)
    print("Next Message Loading.....")
    return 1

def main():
    for file in filelist:
        with open(file, 'r') as f:
            msg_dict = json.load(f)

            for msg in msg_dict:
                print("Input given: ",msg)
                action = msg['action'].lower()

                # if action not in ["current", "historic"]:
                #     print("invalid ")
            
                if "current" in action:
                    defaulturl = "https://api.ratesapi.io/api/latest"
                    val = "curr"
                    # print(val)
                    apiextract(defaulturl,msg)

                elif "historic" in action:
                    val = "hist"
                    # print(val)
                    defaulturl = "https://api.ratesapi.io/api/"

                    if val == "hist":
                        if 'date' in msg['context']:
                            defaulturl += msg['context']['date']
                            apiextract(defaulturl,msg)
                        else:
                            print("date not found")
                            exit

                else:
                    print("invalid action. please insert valid action in message")

if __name__== "__main__":
  main()