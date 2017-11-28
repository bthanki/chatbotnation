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
                    slot = str(start.strftime('%H:%M')) + "-" + str((start + duration_time).strftime('%H:%M'))
                    slots.append(slot)
                    start+= duration_time
                speech="Please Choose from the available slots"
                return make_json_with_buttons(speech, speech, slots, None)

            elif period=="Afternoon" and start > a1 and end <= a2 :
                #nslots = (end - start) / duration_time
                while start + duration_time <= end:
                    slot = str(start.strftime('%H:%M')) + "-" + str((start + duration_time).strftime('%H:%M'))
                    print(slot)
                    slots.append(slot)
                    start += duration_time
                speech = "Please Choose from the available slots"
                return make_json_with_buttons(speech, speech, slots, None)

            else:
                #slots=[]
                speech="Please Choose different time period"
                return make_json_with_buttons(speech,speech,speech,"preferred_time_period_not_available")
        else:
            return make_json_with_buttons(None,None,None,"preferred_day_not_available")




def insert_event(event_name,description,start_date,end_date,time_zone,email_from,email_to):
    logger.info("Entry:insert event in google calendar")
    credentials = get_credentials(email_from)
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
    event=event_json_creation(event_name,description,start_date,end_date,time_zone,email_from,email_to)
    event = service.events().insert(calendarId=email_from, body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))

def event_json_creation(event_name,description,start_date,end_date,time_zone,email_from,email_to):
    logger.info("Entry:event json creation for google calendar")
    event = {
        'summary': event_name,
        'location': 'Office',
        'description': description,
        'start': {
            'dateTime': start_date,
            'timeZone': time_zone,
        },
        'end': {
            'dateTime': end_date,
            'timeZone': time_zone,
        },
        'attendees': [
            {'email': email_to}
        ],
        'reminders': {
            'useDefault': True,
        },
    }
    return event

def get_credentials(email):
    logger.info("Entry:get credentials for google calendar")
    home_dir = os.path.dirname(__file__)
    credential_dir = os.path.join(home_dir, 'credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    if(email=='chatbotnation1@gmail.com'):
        json='chatbotnation1.json'
    elif (email=='chatbotnation2@gmail.com'):
        json = 'chatbotnation2.json'
    elif (email=='chatbotnation3@gmail.com'):
        json = 'chatbotnation3.json'
    elif (email=='chatbotnation4@gmail.com'):
        json = 'chatbotnation4.json'
    credential_path = os.path.join(credential_dir, json)

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


def insert_into_schtable(date,facebook_id,duration_amount,team_name,application,start_time):
    logger.info("Entry:insert schedule in local")
    new_date = datetime.datetime.strptime(date , '%Y-%m-%d')
    new_facebook_id = int(facebook_id.replace(" ",""))
    logger.info("Entry:Insert params:")
    user_new = Table('user',metadata,autoload = True)
    s = user_new.select(user_new.c.facebook_id == new_facebook_id)
    rs = s.execute()
    rsx = rs.fetchall()

    if len(rsx) :
        con = engine.connect()
        u = select([user_new.c.usr_id]).where(user_new.c.facebook_id == new_facebook_id)
        rw = con.execute(u)
        row = rw.fetchall()
        user_schedule = Table('user_sch',metadata, autoload=True)
        user_team_new = Table('user_team', metadata, autoload=True)
        con = engine.connect()
        rs = con.execute(user_schedule.insert().values(sch_date=new_date, usr_id=row[0][0], sch_duration=duration_amount, application = application,sch_start_time = start_time))
        wk = con.execute(user_team_new.insert().values(leader_id = row[0][0],team_name = team_name ))
        logger.info("Exit:Insert params")
        if rs :
             return "Awesome you meeting has been scheduled!"
        else:
             return "Not Inserted!"
    else :
        return "No entry found in User Table"



def user_greetings(new_facebook_id):
    con = engine.connect()
    facebook_id = int(new_facebook_id.replace(" ", ""))
    logger.info("Entry:Greet User:")
    user_new = Table('user',metadata,autoload = True)
    u = select([user_new.c.first_name]).where(user_new.c.facebook_id == facebook_id)
    rw = con.execute(u)
    print(rw)
    row = rw.fetchall()
    value = row[0][0]
    print(value)
    if len(row) :
        return 'Hi'+ value
    else:
        return "No User"

