import logging
from db.mysql import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

response = '''{{
"speech": {0},
"displayText": {1},
"data": {{"facebook": {{
                "text": {2}
            }}}},
"contextOut": {3},
"followupEvent": {{"name": {4}}}
}}'''


def response_string(speech,text,data,context,event):
    return response.format(speech,text,data,context,event)


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
        return response_string("{}","{}","{}","{}","\"day_event\"").replace("\n", "")
    else:
        speech="\"User is not in your friend list\""
        return response_string(speech,speech,speech,{},{}).replace("\n", "")
