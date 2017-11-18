import logging
from db.mysql import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def make_json(speech,text,data,event):
    res={
        "speech": speech,
        "displayText": text,
        "data": {"facebook": {
            "text": data
        }},
        #"contextOut": context,
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
        return "Would you like to add this email id to your Friend List?"
    else:
        return "User not found!"


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
        speech="User is not in your friend list"
        return make_json(speech,speech,None,None)
