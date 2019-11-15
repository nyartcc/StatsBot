import mysql.connector, os, functools, operator
from dotenv import load_dotenv
import json, requests
import datetime
import calendar



def convertTuple(tup): 
    str = functools.reduce(operator.add, (tup)) 
    return str

load_dotenv()
db_host = os.getenv('DATABASE_HOST')
db_user = os.getenv('DATABASE_USER')
db_pass = os.getenv('DATABASE_PASSWORD')


mydb = mysql.connector.connect(
    host=db_host,
    user=db_user,
    passwd=db_pass,
    database="nyartcco_nyartcc"
)


for i in range(2018,2020):
    for j in range(1,12):
        days_of_month = calendar.monthrange(i,j)
        start_time = datetime.datetime(i,j,1,0,0).timestamp()
        end_time = datetime.datetime(i,j,days_of_month[1],0,0).timestamp()

        mycursor = mydb.cursor()
        mycursor.execute("SELECT SUM(duration) FROM connections WHERE logon_time > {0} AND login_time < {1};").format(start_time[:-2], end_time[:-2])
        hours = convertTuple(mycursor.fetchone())

        print("{0}-{1}: {2}").format(i,j,hours)
        

        








