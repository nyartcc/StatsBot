import mysql.connector
import os
import functools
import operator
from dotenv import load_dotenv
import json
import requests
import datetime
from tools import convertTuple

# Load the database variables from the .env file.
load_dotenv()
db_host = os.getenv('DATABASE_HOST')
db_user = os.getenv('DATABASE_USER')
db_pass = os.getenv('DATABASE_PASSWORD')

# Get some date information that will be needed later.
current_date = datetime.datetime.today()
weeknumber = current_date.strftime("%U")




# Establish a connection to the MySQL Database using the .env variables.
mydb = mysql.connector.connect(
    host=db_host,
    user=db_user,
    passwd=db_pass,
    database="nyartcco_nyartcc"
)

# Create a MySQL Connection
mycursor = mydb.cursor()

# Get a bunch of data about the different users. Count number of controllers, visitors, members on LOA etc.
# Members
mycursor.execute("SELECT COUNT(cid) FROM controllers WHERE status = 1;")
members = convertTuple(mycursor.fetchone())

# Visitors
mycursor.execute("SELECT COUNT(cid) FROM controllers WHERE status = 2;")
visitors = convertTuple(mycursor.fetchone())

# LOA
mycursor.execute(
    "SELECT COUNT(cid) FROM controllers WHERE status < 3 AND loa=1;")
loa = convertTuple(mycursor.fetchone())

# Staff
mycursor.execute(
    "SELECT COUNT(cid) FROM controllers WHERE status < 3 AND staff > 0 AND staff <= 6 AND cid!=7;")
staff = convertTuple(mycursor.fetchone())

# Instructors
mycursor.execute(
    "SELECT COUNT(cid) FROM controllers WHERE status < 3 AND instructor = 2;")
instructor = convertTuple(mycursor.fetchone())

# Mentors
mycursor.execute(
    "SELECT COUNT(cid) FROM controllers WHERE status < 3 AND instructor = 1;")
mentor = convertTuple(mycursor.fetchone())

# Send the data to Slack
webhook_url = os.getenv('SLACK_WEBHOOK_GENERAL')
message_data = {
    "blocks": [
        {
            "type": "section",
            "text": {
                    "type": "mrkdwn",
                    "text": "ZNY Statistics: Week #{0}".format(weeknumber)
            }
        },
        {
            "type": "section",
            "block_id": "section567",
            "text": {
                "type": "mrkdwn",
                "text": "*Members: *\n:male-scientist: {0}\tMembers \n :female-scientist: {1}  \tVisitors. \n :man-woman-boy-boy: {2}  \tMembers are marked as LOA.".format(members, visitors, loa)
            },
            "accessory": {
                "type": "image",
                "image_url": "https://image.prntscr.com/image/xkd5HTpdS7GEroH48mgyzA.png",
                "alt_text": "Statistics Icon"
            }
        },
        {
            "type": "section",
            "block_id": "section789",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": "*Staff: *\n :guardsman: {0}  \tSenior Staff \n :male_mage: {1}  \tInstructors \n :male-teacher: {2}\tMentors".format(staff, instructor, mentor)
                }
            ]
        }
    ]
}

response = requests.post(
    webhook_url, data=json.dumps(message_data),
    headers={'Content-type': 'application/json'}
)
if response.status_code != 200:
    raise ValueError(
        'Request to Slack returned an error %s, the response is:\n%s'
        % (reponse.status_code, response.text)
    )
