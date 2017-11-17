from flask import Flask
from flask import make_response
from flask import request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
import logging
import json
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://admin:admin123@chatbotnation.ccw2jw89y0nl.us-west-2.rds.amazonaws.com:3306/chatbot_nation"
engine = create_engine('mysql+pymysql://admin:admin123@chatbotnation.ccw2jw89y0nl.us-west-2.rds.amazonaws.com:3306/chatbot_nation', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()
metadata = MetaData(bind=engine)
db = SQLAlchemy()
db.init_app(app)



# app.config['SQLALCHEMY_DATABASE_URI'] =
# db.init_app(app)

@app.route('/', methods=['POST'])
def chatbot_facade():
    req = request.get_json(silent=True, force=True)

    logger.info("Entry:Chatbot Facade")
    #print("Input Json:")
    #print(json.dumps(req, indent=4, sort_keys=True))

    if req.get("result").get("action") == "check_nick_name":
        parameters= req.get("result").get("parameters")
        name=parameters.get("given-name")
        print(name)
        speech=verify_nick_name(name)
        res = {
            "speech": speech,
            "displayText": speech,
            "data": {"facebook": {
                "text": speech
            }},
            # "contextOut": [],
            "source": "Test",
            "followupEvent": { "name": "first_event"

            }
         }
    elif req.get("result").get("action") == "check_email":
        parameters = req.get("result").get("parameters")
        email = parameters.get("email")
        print(email)
        speech = verify_email_id(email)
        res = {
            "speech": speech,
            "displayText": speech,
            "data": {"facebook": {
                "text": speech
            }},
            # "contextOut": [],
            "source": "Test"
        }
    else:
        res={}

    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    logger.info("Exit:Chatbot Facade")
    return r


def verify_nick_name(name):
    logger.info("Entry:Verify Nick Name:")
    user_frnd_list = Table('user_frnd_list',metadata, autoload=True)
    s = user_frnd_list.select(user_frnd_list.c.nick_name==name)
    rs = s.execute()
    row= rs.fetchall()
    logger.info("Exit:Verify Nick Name")
    if len(row):
        return "Yes, User found in our system!"
    else:
        return "User not found!"


def verify_email_id(email):
    logger.info("Entry:Verify Email Id:")
    users = Table('user',metadata, autoload=True)
    s = users.select(users.c.email_id==email)
    rs = s.execute()
    row= rs.fetchall()
    print(row)
    logger.info("Exit:Verify Email Id")
    if len(row):
        return "Would you like to add this email id to your Friend List?"
    else:
        return "User not found!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ['PORT']))
    #app.run()
