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


def verify_nick_name(name,facebook_id):
    logger.info("Entry:Verify Nick Name:")
    user = get_session().query(User).filter_by(facebook_id=facebook_id).first()
    user_frnd_list = Table('user_frnd_list', get_metadata(), autoload=True)
    s = user_frnd_list.select((user_frnd_list.c.nick_name == name) & (user_frnd_list.c.usr_id == user.usr_id))
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
                                      created_date=str(datetime.now()),
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
        print(date)
        day = date.strftime('%a')#.weekday()
        print(day)
        s = user_prefs.select((user_prefs.c.usr_id == id) & (user_prefs.c.pref_day == day))
        rs=s.execute()
        rows= rs.fetchone()
        print(rows)
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
                print("No morning and afternoon")
                return make_json_with_buttons(speech,speech,speech,"preferred_time_period_not_available")
        else:
            print("no id")
            return make_json_with_buttons(None,None,None,"preferred_day_not_available")



def insert_into_schtable(date,facebook_id,duration_amount,application,start_time,email,name):



    new_date = datetime.strptime(date , '%Y-%m-%d')
    print(new_date)
    logger.info("Entry:Insert params:")
    user_frnd_list = get_session().query(UserFrndList)
    event_name = "ChatbotNation"
    description = "Google api call"
    time_zone = 'America/New_York'
    start_date = str(date)+'T'+start_time

    end_date = str(date)+'T'+start_time
    print(end_date)
    new_facebook_id = int(facebook_id.replace(" ", ""))
    user = get_session().query(User).filter_by(facebook_id=new_facebook_id).first()
    email_from = user.email_id

    if user.usr_id is not None :
        user_cln_map = get_session().query(UserClnMap).filter_by(usr_id=user.usr_id).first()
        if email is not '':
            s1 = user.select(user.c.email_id == email)
            rs1 = s1.execute()
            row = rs1.fetchone()
            id = row['usr_id']
        elif name is not '':
            user_frnd_list = Table('user_frnd_list',get_metadata(),autoload=True)
            s1 = user_frnd_list.select(user_frnd_list.c.nick_name == name)
            rs1 = s1.execute()
            row = rs1.fetchone()
            id = row['frnd_usr_id']
        user_sch=UserSch(usr_id = user.usr_id, sch_date = new_date , sch_start_time = start_time, sch_duration = duration_amount,
                         application = application, active_flag = 1 , usr_cln_id = user_cln_map.usr_cln_id , usr_prin_part_id = id, created_date = str(datetime.now()) )
        get_session().add(user_sch)
        get_session().commit()

        if email is not '':
            email_to = email
        else:
            s1 = user_frnd_list.select(user_frnd_list.c.nick_name == name)
            rs1 = s1.execute()
            row = rs1.fetchone()
            id = row['frnd_usr_id']
            user2=get_session().query(User).filter_by(usr_id=id).first()
            email_to = user2.email_id
        insert_event(event_name, description, start_date, end_date, time_zone, email_from, email_to)


        logger.info("Exit:Insert params")
    else:
        return "No entry found in User Table"



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

def get_calendar_file(email):
    logger.info("Entry:Get Calendar Authentication File")
    user_cln_map = Table('user_cln_map', get_metadata(), autoload=True)
    s = user_cln_map.select(user_cln_map.c.cln_email_id == email)
    rs = s.execute()
    row = rs.fetchall()
    return row['calendar_json']


def get_credentials(email):
    logger.info("Entry:get credentials for google calendar")
    home_dir = os.path.dirname(__file__)
    credential_dir = os.path.join(home_dir, 'credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    if email is not None:
        json=get_calendar_file(email)
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






def user_greetings(new_facebook_id):
    #con = engine.connect()
    facebook_id = int(new_facebook_id.replace(" ", ""))
    logger.info("Entry:Greet User:")
    user_new = Table('user',get_metadata(),autoload = True)
    u = select([user_new.c.first_name]).where(user_new.c.facebook_id == facebook_id)
    rw = u.execute()
    print(rw)
    row = rw.fetchall()
    value = row[0][0]
    print(value)
    if len(row) :
        return 'Hi'+ value
    else:
        return "No User"


def insert_into_team(facebook_id,team_name):
    logger.info("Entry:Insert Team table:")
    new_facebook_id = int(facebook_id.replace(" ", ""))
    user = get_session().query(User).filter_by(facebook_id=new_facebook_id).first()
    leader_id = user.usr_id
    if user.usr_id is not None :
         user_team = UserTeam(leader_id = leader_id,team_name = team_name,active_flag = 1)
         get_session().add(user_team)
         get_session().commit()
         logger.info("Exit:Insert Team table")
    else:
        return "Not Inserted into the table"


def insert_into_teammap(facebook_id,email):
    logger.info("Entry:Insert Team_map table:")
    new_facebook_id = int(facebook_id.replace(" ", ""))
    user = get_session().query(User).filter_by(facebook_id=new_facebook_id).first()
    user_id = user.usr_id
    if user.usr_id is not None :
         user_team_map = UserTeamMap(usr_id = user_id,usr_email_id = email,active_flag = 1, created_date = str(datetime.now()) )
         get_session().add(user_team_map)
         get_session().commit()
         logger.info("Exit:Insert Team map table")
    else:
        return "Not Inserted into the table Team map"


def insert_into_schtable(date,facebook_id,duration_amount,application,start_time,email,name):
    new_date = datetime.strptime(date , '%Y-%m-%d')
    print(new_date)
    logger.info("Entry:Insert params:")
    user_frnd_list = get_session().query(UserFrndList)
    event_name = "ChatbotNation"
    description = "Google api call"
    time_zone = 'America/New_York'
    start_date = str(date)+'T'+start_time

    end_date = str(date)+'T'+start_time
    print(end_date)
    new_facebook_id = int(facebook_id.replace(" ", ""))
    user = get_session().query(User).filter_by(facebook_id=new_facebook_id).first()
    frnd = Table('user', get_metadata(), autoload=True)
    email_from = user.email_id

    if user.usr_id is not None :
        user_cln_map = get_session().query(UserClnMap).filter_by(usr_id=user.usr_id).first()
        if email is not '':
            s1 = frnd.select(frnd.c.email_id == email)
            rs1 = s1.execute()
            row = rs1.fetchone()
            id = row['usr_id']
        elif name is not '':
            user_frnd_list = Table('user_frnd_list',get_metadata(),autoload=True)
            s1 = user_frnd_list.select(user_frnd_list.c.nick_name == name)
            rs1 = s1.execute()
            row = rs1.fetchone()
            id = row['frnd_usr_id']
        user_sch=UserSch(usr_id = user.usr_id, sch_date = new_date , sch_start_time = start_time, sch_duration = duration_amount,
                         application = application, active_flag = 1 , usr_cln_id = user_cln_map.usr_cln_id , usr_prin_part_id = id, created_date = str(datetime.now()) )
        get_session().add(user_sch)
        get_session().commit()

        if email is not '':
            email_to = email
        else:
            s1 = user_frnd_list.select(user_frnd_list.c.nick_name == name)
            rs1 = s1.execute()
            row = rs1.fetchone()
            id = row['frnd_usr_id']
            user2=get_session().query(User).filter_by(usr_id=id).first()
            email_to = user2.email_id
        insert_event(event_name, description, start_date, end_date, time_zone, email_from, email_to)


        logger.info("Exit:Insert params")
    else:
        return "No entry found in User Table"