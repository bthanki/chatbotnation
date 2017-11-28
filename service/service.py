import logging
import datetime
from db.mysql import *
from datetime import datetime, timedelta, time
from models.models import *
import os
from apiclient import discovery
import httplib2
import oauth2client
from oauth2client import client
from oauth2client import tools

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'
CALENDARID='cherpatisreekanth@gmail.com'

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

def make_json(speech,text,data,event):
    res={
        "speech": speech,
        "displayText": text,
        "data": {"facebook": {
            "text": data
        }},
        "followupEvent": {"name": event}
    }
    return res


def make_json_with_buttons(speech,text,data,event):
    print(data)
    res={
        "speech": speech,
        "displayText": text,
        "messages": [
            {
                "platform": "facebook",
                "replies": data,
                "title": "Slots Available:",
                "type": 2
            }
        ],
        "followupEvent": {"name": event}
    }

    print(res)

    return res


def verify_email_id(email):
    logger.info("Entry:Verify Email Id:")
    users = Table('user',get_metadata(), autoload=True)
    s = users.select(users.c.email_id==email)
    rs = s.execute()
    row= rs.fetchall()
    print(row)
    if len(row):
        speech = "Would you like to add this email id to your Friend List?"
        return make_json(speech, speech, speech, None)
    else:
        speech="User not found! Please give his registered email id."
        return make_json(speech,speech,speech,None)


def verify_nick_name(name):
    logger.info("Entry:Verify Nick Name:")
    user_frnd_list = Table('user_frnd_list', get_metadata(), autoload=True)
    s = user_frnd_list.select(user_frnd_list.c.nick_name == name)
    rs = s.execute()
    row = rs.fetchall()
    if len(row):
        return make_json(None,None,None,"day_event")
    else:
        speech="User is not in your friend list. Please give his registered email id."
        return make_json(speech,speech,speech,None)


def save_friend(facebook_id,email,name):
    logger.info("Entry:Save Friend")
    user = get_session().query(User).filter_by(facebook_id=facebook_id).first()
    friend = get_session().query(User).filter_by(email_id=email).first()
    if name is None:
        name=friend.first_name
    if user.usr_id is not None and friend.usr_id is not None:
        user_frnd_list = UserFrndList(usr_id=user.usr_id,frnd_usr_id=friend.usr_id,
                                      created_date=str(datetime.datetime.now()),
                                      active_flag="A",nick_name=name)
        get_session().add(user_frnd_list)
        get_session().commit()
        return make_json(None,None,None,"day_event")
    if user.usr_id is not None or friend.usr_id is not None:
        speech = "Either you or your friend is not in the system."
        return make_json(speech, speech, speech, None)
    else:
        speech = "There was some problem to add your friend"
        return make_json(speech, speech, speech, None)


def get_schedule_details(email,name,date,period,duration):
    logger.info("Entry:get Schedule Details")
    users = Table('user', get_metadata(), autoload=True)
    user_frnd_list = Table('user_frnd_list', get_metadata(), autoload=True)
    user_prefs= Table('user_pref', get_metadata(), autoload=True)

    if email is not '':
        s1 = users.select(users.c.email_id == email)
        rs1 = s1.execute()
        row = rs1.fetchone()
        id = row['usr_id']
    elif name is not '':
        s1 = user_frnd_list.select(user_frnd_list.c.nick_name == name)
        rs1 = s1.execute()
        row = rs1.fetchone()
        id = row['frnd_usr_id']

    print(id)
    if id is not None:
        date=datetime.strptime(date,'%Y-%m-%d')
        #print(date)
        day = date.strftime('%a')#.weekday()
        #print(day)
        s = user_prefs.select((user_prefs.c.usr_id == id) & (user_prefs.c.pref_day == day))
        rs=s.execute()
        rows= rs.fetchone()
        #print(rows)
        if rows is not None and len(rows):
            slots = []
            duration_time=timedelta(minutes=duration)
            start=str(rows['pref_start_time'])
            start=datetime.strptime(start,'%H:%M:%S')
            end=str(rows['pref_end_time'])
            end=datetime.strptime(end, '%H:%M:%S')

            m1=datetime.strptime("7:00:00",'%H:%M:%S')
            m2=datetime.strptime("12:00:00",'%H:%M:%S')
            a1=datetime.strptime("12:00:00",'%H:%M:%S')
            a2=datetime.strptime("18:00:00",'%H:%M:%S')

            if period=="Morning" and start >= m1 and end <= m2 :
                #nslots= (end - start)/ duration_time
                while start + duration_time <= end:
                    slot = str(start.strftime('%H:%M:%S')) + "-" + str((start + duration_time).strftime('%H:%M:%S'))
                    slots.append(slot)
                    start+= duration_time
                speech="Please Choose from the available slots"

            elif period=="Afternoon" and start > a1 and end <= a2 :
                #nslots = (end - start) / duration_time
                while start + duration_time <= end:
                    slot = str(start.strftime('%H:%M:%S')) + "-" + str((start + duration_time).strftime('%H:%M:%S'))
                    print(slot)
                    slots.append(slot)
                    start += duration_time
                speech = "Please Choose from the available slots"

            else:
                slots=[]
                speech="Please Choose different time period"
            return make_json_with_buttons(speech,speech,slots,None)
        else:
            return make_json_with_buttons(None,None,None,"preferred_day_not_available")


def get_calendar_json(email):
    logger.info("Entry:get calendar json")
    if email is not None:
        user_cln_map = Table('user_cln_map', get_metadata(), autoload=True)
        s1 = user_cln_map.select(user_cln_map.c.cln_email_id == email)
        rs1 = s1.execute()
        row = rs1.fetchone()
        id = row['calendar_json']
        return id

def insert_event():

    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
    event = {
      'summary': 'Test Insert Event',
      'location': 'Home',
      'description': 'Automagic for the people',
      'start': {
        'dateTime': '2017-12-30T14:00:00-07:00',
        'timeZone': 'America/Los_Angeles',
      },
      'end': {
        'dateTime': '2017-12-30T15:00:00-07:00',
        'timeZone': 'America/Los_Angeles',
      },
      'attendees':[
            {'email':'chatbotnation1@gmail.com'}
            ],
      'reminders': {
        'useDefault': True,
      },
    }

    event = service.events().insert(calendarId=CALENDARID, body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))

def get_credentials():
    home_dir = os.path.dirname(__file__)
    credential_dir = os.path.join(home_dir, 'credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, 'calendar-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


