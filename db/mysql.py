from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *

metadata=None

session=None

def dbconnect():
    engine = create_engine('mysql+pymysql://admin:admin123@chatbotnation.ccw2jw89y0nl.us-west-2.rds.amazonaws.com:3306/chatbot_nation', convert_unicode=True)
    db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
    Base = declarative_base()
    Base.query = db_session.query_property()
    global metadata
    metadata= MetaData(bind=engine)
    Session = sessionmaker(bind=engine)
    Session = sessionmaker()
    Session.configure(bind=engine)
    global session
    session=Session()

def get_metadata():
    return metadata

def get_session():
    return session

