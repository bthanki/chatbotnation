import logging
import datetime
from db.mysql import *
from models.models import *

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
    if len(row):
        return make_json(None,None,None,"day_event")
    else:
        speech="User is not in your friend list. Please give his registered email id."
        return make_json(speech,speech,speech,None)


def save_friend(facebook_id,email,name):
    logger.info("Entry:Save Friend")
    user = get_session().query(User).filter_by(facebook_id=facebook_id).first()
    friend = get_session().query(User).filter_by(email_id=email).first()
    #users = Table('user', get_metadata(), autoload=True)
    #user = users.select(users.c.facebook_id == facebook_id)
    #rs = user.execute()
    #user = rs.fetchall()
    #friend = users.select(users.c.email_id == email)
    #rs = friend.execute()
    #friend = rs.fetchall()
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
        speech="There was some problem to add your friend"
        return make_json(speech,speech,speech,None)
