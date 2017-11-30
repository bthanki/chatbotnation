from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String, Time, text, BIGINT, LargeBinary
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class User(Base):
    __tablename__ = 'user'

    usr_id = Column(Integer, primary_key=True)
    usr_name = Column(String(255))
    first_name = Column(String(255))
    last_name = Column(String(255))
    email_id = Column(String(320))
    phone_num = Column(Integer)
    created_date = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    updated_date = Column(DateTime)
    conference_num = Column(Integer)
    skype = Column(String(255))
    google_hangout = Column(String(255))
    go_to_meeting = Column(String(255))
    join_me = Column(String(255))
    web_ex = Column(String(255))
    video_conf = Column(String(255))
    facebook_id = Column(BIGINT)


class UserChatRsp(Base):
    __tablename__ = 'user_chat_rsp'

    usr_chat_rsp_id = Column(Integer, primary_key=True)
    usr_id = Column(ForeignKey('user.usr_id'), index=True)
    usr_input = Column(String(255), nullable=False)
    usr_output = Column(String(255), nullable=False)
    created_date = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))

    usr = relationship('User')


class UserClnMap(Base):
    __tablename__ = 'user_cln_map'

    usr_cln_id = Column(Integer, primary_key=True)
    usr_id = Column(ForeignKey('user.usr_id'), index=True)
    client_name = Column(String(255))
    cln_email_id = Column(String(320))
    cln_str = Column(Integer)
    active_flag = Column(String(1))
    created_date = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    updated_date = Column(DateTime)
    calendar_json = Column(String(50))
    usr = relationship('User')


class UserFrndList(Base):
    __tablename__ = 'user_frnd_list'

    usr_frnd_list_id = Column(Integer, primary_key=True)
    usr_id = Column(ForeignKey('user.usr_id'), index=True)
    frnd_usr_id = Column(ForeignKey('user.usr_id'), index=True)
    created_date = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    updated_date = Column(DateTime)
    active_flag = Column(Integer)
    nick_name = Column(String(255))
    frnd_usr = relationship('User', primaryjoin='UserFrndList.frnd_usr_id == User.usr_id')
    usr = relationship('User', primaryjoin='UserFrndList.usr_id == User.usr_id')


class UserGst(Base):
    __tablename__ = 'user_gst'

    usr_gst_id = Column(Integer, primary_key=True)
    usr_id = Column(ForeignKey('user.usr_id'), index=True)
    email_id = Column(String(255))
    active_flag = Column(Integer)
    usr_sync = Column(Integer)
    email_sync = Column(Integer)

    usr = relationship('User')


class UserPref(Base):
    __tablename__ = 'user_pref'

    usr_pref_id = Column(Integer, primary_key=True)
    usr_id = Column(ForeignKey('user.usr_id'), index=True)
    pref_day = Column(Integer)
    pref_start_time = Column(Time)
    pref_end_time = Column(Time)
    max_time = Column(Integer)
    time_zone = Column(String(255))
    active_flag = Column(String(255))
    created_date = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    updated_date = Column(DateTime)
    pref_usr_cln_id = Column(Integer)

    usr = relationship('User')


class UserSch(Base):
    __tablename__ = 'user_sch'

    usr_sch_id = Column(Integer, primary_key=True)
    usr_id = Column(ForeignKey('user.usr_id'), index=True)
    sch_date = Column(Date)
    sch_start_time = Column(Time)
    sch_duration = Column(Integer)
    application = Column(String(255))
    location = Column(String(255))
    active_flag = Column(Integer)
    usr_cln_id = Column(ForeignKey('user_cln_map.usr_cln_id'), index=True)
    usr_prin_part_id = Column(Integer)
    created_date = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    updated_date = Column(DateTime)
    usr_sync = Column(Integer)
    prim_part_sync = Column(Integer)

    usr_cln = relationship('UserClnMap')
    usr = relationship('User')


class UserTeam(Base):
    __tablename__ = 'user_team'

    team_id = Column(Integer, primary_key=True)
    leader_id = Column(ForeignKey('user.usr_id'), index=True)
    team_name = Column(String(255))
    created_date = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    updated_date = Column(DateTime)
    active_flag = Column(Integer)

    leader = relationship('User')


class UserTeamMap(Base):
    __tablename__ = 'user_team_map'

    team_id = Column(Integer, primary_key=True)
    usr_id = Column(ForeignKey('user.usr_id'), index=True)
    usr_email_id = Column(String(255))
    created_date = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    updated_date = Column(DateTime)
    active_flag = Column(Integer)

    usr = relationship('User')


class UserVipList(Base):
    __tablename__ = 'user_vip_list'

    usr_vip_list_id = Column(Integer, primary_key=True)
    usr_id = Column(ForeignKey('user.usr_id'), index=True)
    vip_id = Column(ForeignKey('user.usr_id'), index=True)
    active_flag = Column(String(1))
    created_date = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    updated_date = Column(DateTime)

    usr = relationship('User', primaryjoin='UserVipList.usr_id == User.usr_id')
    vip = relationship('User', primaryjoin='UserVipList.vip_id == User.usr_id')