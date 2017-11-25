import logging
from db.mysql import *
from datetime import datetime, timedelta, time


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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


def verify_email_id(email):
    logger.info("Entry:Verify Email Id:")
    users = Table('user',get_metadata(), autoload=True)
    s = users.select(users.c.email_id==email)
    rs = s.execute()
    row= rs.fetchall()
    print(row)
    logger.info("Exit:Verify Email Id")
    if len(row):
        speech = "Would you like to add this email id to your Friend List?"
        return make_json(speech, speech, speech, None)
    else:
        speech="User not found!"
        return make_json(speech,speech,speech,None)


def verify_nick_name(name):
    logger.info("Entry:Verify Nick Name:")
    user_frnd_list = Table('user_frnd_list', get_metadata(), autoload=True)
    s = user_frnd_list.select(user_frnd_list.c.nick_name == name)
    rs = s.execute()
    row = rs.fetchall()
    logger.info("Exit:Verify Nick Name")
    if len(row):
        return make_json(None,None,None,"day_event")
    else:
        speech="User is not in your friend list. Please give his registered email id."
        return make_json(speech,speech,speech,None)


def save_friend(email):
    logger.info("Entry:Save Friend")
    users = Table('user', get_metadata(), autoload=True)
    s = users.select(users.c.email_id == email)
    rs = s.execute()
    row = rs.fetchall()
    logger.info("Exit:Save Friend")
    if len(row):
        return make_json(None,None,None,"day_event")
    else:
        speech="User is not in your friend list. Please use his registered email id."
        return make_json(speech,speech,speech,None)


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
            return make_json(speech,speech,slots,None)
        else:
            return make_json(None,None,None,"preferred_day_not_available")
