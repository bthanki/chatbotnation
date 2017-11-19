create table test(ID numeric,name varchar(255));
Insert into test(ID,name) values(123,'Sreekanth');

select * from test;

create table User (Usr_ID mediumint NOT NULL auto_increment,
					Usr_Name varchar(255),
                    First_Name varchar(255),
                    Last_Name varchar(255),
                    Email_ID varchar(320),
                    Phone_Num int,
                    Created_Date datetime,
                    Updated_Date datetime,
                    Conference_Num Int,
                    Skype varchar(255),
                    Google_Hangout varchar(255),
                    Go_to_Meeting varchar(255),
                    Join_Me varchar(255),
                    Web_Ex varchar(255),
                    video_conf varchar(255),
                    PRIMARY KEY(Usr_ID)
                    );

create table user_cln_map (usr_cln_id mediumint NOT NULL auto_increment,
					usr_id mediumint(255),
                    client_name varchar(255),
                    cln_Email_ID varchar(320),
                    cln_str int,
                    PRIMARY KEY(usr_cln_id),
                    FOREIGN KEY (usr_id)
                    REFERENCES user(usr_id)
                    );

create table user_pref(usr_pref_id mediumint NOT NULL auto_increment,
					usr_id mediumint(255),
                    pref_day int(255),
                    pref_start_time time,
                    pref_end_time time,
                    max_time int(3),
                    time_zone varchar(255),
                    active_flag varchar(255),
                    created_date datetime,
                    updated_date datetime,
                    pref_usr_cln_id mediumint,
                    PRIMARY KEY(usr_pref_id),
                    FOREIGN KEY (usr_id)
                    REFERENCES user(usr_id)
                    );	
create table user_sch(usr_sch_id mediumint NOT NULL auto_increment,
					usr_id mediumint(255),
                    sch_date date,
                    sch_start_time time,
                    sch_duration int(3),
                    application varchar(255),
                    location varchar(255),
                    active_flag tinyint,
                    usr_cln_id mediumint,
                    usr_prin_part_id mediumint,
                    created_date datetime default now(),
                    updated_date datetime,
                    usr_sync int,
                    prim_part_sync int,
                    PRIMARY KEY(usr_sch_id),
                    FOREIGN KEY (usr_id)
                    REFERENCES user(usr_id),
                    FOREIGN KEY(usr_cln_id)
                    REFERENCES user_cln_map(usr_cln_id)
                    );	
create table user_gst(usr_gst_id mediumint NOT NULL auto_increment,
					usr_id mediumint(255),
                    email_id varchar(255),
                    active_flag tinyint,
                    usr_sync int,
                    email_sync int,
                    PRIMARY KEY(usr_gst_id),
                    FOREIGN KEY (usr_id)
                    REFERENCES user(usr_id)
                    );	

create table user_team(team_id mediumint NOT NULL auto_increment,
					leader_id mediumint(255),
                    team_name varchar(255),
                    created_date datetime default now(),
                    updated_date datetime,
                    active_flag tinyint,
                    PRIMARY KEY(team_id),
                    FOREIGN KEY (leader_id)
                    REFERENCES user(usr_id)
                    );
create table user_team_map(team_id mediumint NOT NULL auto_increment,
					usr_id mediumint(255),
                    usr_email_id varchar(255),
                    created_date datetime default now(),
                    updated_date datetime,
                    active_flag tinyint,
                    PRIMARY KEY(team_id),
                    FOREIGN KEY (usr_id)
                    REFERENCES user(usr_id)
                    );

create table user_frnd_list(usr_frnd_list_id mediumint NOT NULL auto_increment,
					usr_id mediumint,
                    frnd_usr_id mediumint,
                    created_date datetime default now(),
                    updated_date datetime,
                    active_flag tinyint,
                    PRIMARY KEY(usr_frnd_list_id),
                    FOREIGN KEY (usr_id)
                    REFERENCES user(usr_id),
                    FOREIGN KEY (frnd_usr_id)
                    REFERENCES user(usr_id)
                    );

show fields from user;

show fields from user_chat_rsp;

show fields from user_cln_map;

show fields from user_frnd_list;

show fields from user_gst;

show fields from user_pref;

show fields from user_sch;

show fields from user_team;

show fields from user_team_map;

show fields from user_vip_list;

select * from user;

/* Inserrting into table users*/

INSERT INTO `chatbot_nation`.`user`
(
`usr_name`,
`first_name`,
`last_name`,
`email_id`,
`phone_num`,
`created_date`,
`updated_date`,
`conference_num`,
`skype`,
`google_hangout`,
`go_to_meeting`,
`join_me`,
`web_ex`,
`video_conf`)
VALUES
(
"chatbotnation1",
"Sreekanth",
"cherapati",
"chatbotnation1@gmail.com",
8139986838,
sysdate(),
sysdate(),
123546,
"scherapati",
"scherapati",
"xyz123",
"abcdef1254",
"scherapati1235",
"xyz789");



INSERT INTO `chatbot_nation`.`user`
(
`usr_name`,
`first_name`,
`last_name`,
`email_id`,
`phone_num`,
`created_date`,
`updated_date`,
`conference_num`,
`skype`,
`google_hangout`,
`go_to_meeting`,
`join_me`,
`web_ex`,
`video_conf`)
VALUES
(
"chatbotnation2",
"Bharghav",
"Thanki",
"chatbotnation2@gmail.com",
3125849874,
sysdate(),
sysdate(),
123546,
"bmthanki",
"bmthanki",
"xyz123",
"abcdef1254",
"bmthanki12345",
"xyz789");


INSERT INTO `chatbot_nation`.`user`
(
`usr_name`,
`first_name`,
`last_name`,
`email_id`,
`phone_num`,
`created_date`,
`updated_date`,
`conference_num`,
`skype`,
`google_hangout`,
`go_to_meeting`,
`join_me`,
`web_ex`,
`video_conf`)
VALUES
(
"chatbotnation2",
"Mounika",
"Kancharla",
"chatbotnation3@gmail.com",
3125849874,
sysdate(),
sysdate(),
123546,
"mkancharla",
"mkancharla",
"xyz123",
"abcdef1254",
"mkancharla12345",
"xyz789");


INSERT INTO `chatbot_nation`.`user`
(
`usr_name`,
`first_name`,
`last_name`,
`email_id`,
`phone_num`,
`created_date`,
`updated_date`,
`conference_num`,
`skype`,
`google_hangout`,
`go_to_meeting`,
`join_me`,
`web_ex`,
`video_conf`)
VALUES
(
"chatbotnation4",
"Natasha",
"Gandhi",
"chatbotnation4@gmail.com",
3125849874,
sysdate(),
sysdate(),
123546,
"nsg",
"nsg",
"xyz123",
"abcdef1254",
"nsg124458",
"xyz789");


select * from user;
Delete from user where usr_id=2;
ALTER TABLE user AUTO_INCREMENT = 1;

Update user set usr_name="chatbotnation3" where usr_id=2;

INSERT INTO `chatbot_nation`.`user_cln_map`
(
`usr_id`,
`client_name`,
`cln_Email_ID`,
`active_flag`,
`created_date`,
`updated_date`)
VALUES
(
(Select distinct usr_id from chatbot_nation.user where first_name="Sreekanth"),
"Google_Calender",
(Select distinct email_id from chatbot_nation.user where first_name="Sreekanth"),
"Y",
sysdate(),
sysdate());

INSERT INTO `chatbot_nation`.`user_cln_map`
(
`usr_id`,
`client_name`,
`cln_Email_ID`,
`active_flag`,
`created_date`,
`updated_date`)
VALUES
(
(Select distinct usr_id from chatbot_nation.user where first_name="Bharghav"),
"Google_Calender",
(Select distinct email_id from chatbot_nation.user where first_name="Bharghav"),
"Y",
sysdate(),
sysdate());

INSERT INTO `chatbot_nation`.`user_cln_map`
(
`usr_id`,
`client_name`,
`cln_Email_ID`,
`active_flag`,
`created_date`,
`updated_date`)
VALUES
(
(Select distinct usr_id from chatbot_nation.user where first_name="Mounika"),
"Google_Calender",
(Select distinct email_id from chatbot_nation.user where first_name="Mounika"),
"Y",
sysdate(),
sysdate());

INSERT INTO `chatbot_nation`.`user_cln_map`
(
`usr_id`,
`client_name`,
`cln_Email_ID`,
`active_flag`,
`created_date`,
`updated_date`)
VALUES
(
(Select distinct usr_id from chatbot_nation.user where first_name="Natasha"),
"Google_Calender",
(Select distinct email_id from chatbot_nation.user where first_name="Natasha"),
"Y",
sysdate(),
sysdate());

select * from user_cln_map;

delete from user_cln_map where usr_id=3;

ALTER TABLE user_cln_map AUTO_INCREMENT = 1;

INSERT INTO `chatbot_nation`.`user_frnd_list`
(
`usr_id`,
`frnd_usr_id`,
`created_date`,
`updated_date`,
`active_flag`)
VALUES
(
(Select distinct usr_id from chatbot_nation.user where first_name="Natasha"),
(Select distinct usr_id from chatbot_nation.user where first_name="Mounika"),
sysdate(),
sysdate(),
"Y");

INSERT INTO `chatbot_nation`.`user_frnd_list`
(
`usr_id`,
`frnd_usr_id`,
`created_date`,
`updated_date`,
`active_flag`)
VALUES
(
(Select distinct usr_id from chatbot_nation.user where first_name="Mounika"),
(Select distinct usr_id from chatbot_nation.user where first_name="Sreekanth"),
sysdate(),
sysdate(),
"Y");

INSERT INTO `chatbot_nation`.`user_frnd_list`
(
`usr_id`,
`frnd_usr_id`,
`created_date`,
`updated_date`,
`active_flag`)
VALUES
(
(Select distinct usr_id from chatbot_nation.user where first_name="Sreekanth"),
(Select distinct usr_id from chatbot_nation.user where first_name="Natasha"),
sysdate(),
sysdate(),
"Y");

INSERT INTO `chatbot_nation`.`user_frnd_list`
(
`usr_id`,
`frnd_usr_id`,
`created_date`,
`updated_date`,
`active_flag`)
VALUES
(
(Select distinct usr_id from chatbot_nation.user where first_name="Bharghav"),
(Select distinct usr_id from chatbot_nation.user where first_name="Sreekanth"),
sysdate(),
sysdate(),
"Y");

select * from `chatbot_nation`.`user_frnd_list`;

INSERT INTO `chatbot_nation`.`user_gst`
(
`usr_id`,
`email_id`,
`active_flag`,
`usr_sync`,
`email_sync`)
VALUES
(
(Select distinct usr_id from chatbot_nation.user where first_name="Bharghav"),
(Select distinct email_id from chatbot_nation.user where first_name="Bharghav"),
"Y",
"Y",
"Y");

INSERT INTO `chatbot_nation`.`user_gst`
(
`usr_id`,
`email_id`,
`active_flag`,
`usr_sync`,
`email_sync`)
VALUES
(
(Select distinct usr_id from chatbot_nation.user where first_name="Natasha"),
(Select distinct email_id from chatbot_nation.user where first_name="Natasha"),
"Y",
"Y",
"Y");

INSERT INTO `chatbot_nation`.`user_gst`
(
`usr_id`,
`email_id`,
`active_flag`,
`usr_sync`,
`email_sync`)
VALUES
(
(Select distinct usr_id from chatbot_nation.user where first_name="Mounika"),
(Select distinct email_id from chatbot_nation.user where first_name="Mounika"),
"Y",
"Y",
"Y");

INSERT INTO `chatbot_nation`.`user_gst`
(
`usr_id`,
`email_id`,
`active_flag`,
`usr_sync`,
`email_sync`)
VALUES
(
(Select distinct usr_id from chatbot_nation.user where first_name="Sreekanth"),
(Select distinct email_id from chatbot_nation.user where first_name="Sreekanth"),
"Y",
"Y",
"Y");

select * from `chatbot_nation`.`user_gst`;

delete from `chatbot_nation`.`user_gst` where usr_gst_id=4;

ALTER TABLE user_gst AUTO_INCREMENT = 1;

INSERT INTO `chatbot_nation`.`user_pref`
(
`usr_id`,
`pref_day`,
`pref_start_time`,
`pref_end_time`,
`max_time_in_min`,
`time_zone`,
`active_flag`,
`created_date`,
`updated_date`,
`pref_usr_cln_id`)
VALUES
(
(Select distinct usr_id from chatbot_nation.user where first_name="Sreekanth"),
"TUE",
"13:00:00",
"13:30:00",
30,
"EST",
"Y",
sysdate(),
sysdate(),
(Select distinct usr_cln_id from chatbot_nation.user_cln_map where usr_id=1));


INSERT INTO `chatbot_nation`.`user_pref`
(
`usr_id`,
`pref_day`,
`pref_start_time`,
`pref_end_time`,
`max_time_in_min`,
`time_zone`,
`active_flag`,
`created_date`,
`updated_date`,
`pref_usr_cln_id`)
VALUES
(
(Select distinct usr_id from chatbot_nation.user where first_name="Mounika"),
"TUE",
"13:00:00",
"13:30:00",
30,
"EST",
"Y",
sysdate(),
sysdate(),
(Select distinct usr_cln_id from chatbot_nation.user_cln_map where usr_id=3));

INSERT INTO `chatbot_nation`.`user_pref`
(
`usr_id`,
`pref_day`,
`pref_start_time`,
`pref_end_time`,
`max_time_in_min`,
`time_zone`,
`active_flag`,
`created_date`,
`updated_date`,
`pref_usr_cln_id`)
VALUES
(
(Select distinct usr_id from chatbot_nation.user where first_name="Bharghav"),
"TUE",
"13:00:00",
"13:30:00",
30,
"EST",
"Y",
sysdate(),
sysdate(),
(Select distinct usr_cln_id from chatbot_nation.user_cln_map where usr_id=2));

INSERT INTO `chatbot_nation`.`user_pref`
(
`usr_id`,
`pref_day`,
`pref_start_time`,
`pref_end_time`,
`max_time_in_min`,
`time_zone`,
`active_flag`,
`created_date`,
`updated_date`,
`pref_usr_cln_id`)
VALUES
(
(Select distinct usr_id from chatbot_nation.user where first_name="Natasha"),
"TUE",
"13:00:00",
"13:30:00",
30,
"EST",
"Y",
sysdate(),
sysdate(),
(Select distinct usr_cln_id from chatbot_nation.user_cln_map where usr_id=4));

select * from user_pref;


Truncate table usr_gst;

INSERT INTO `chatbot_nation`.`user_vip_list`
(
`usr_id`,
`vip_id`,
`active_flag`,
`created_date`,
`updated_date`)
VALUES
(
(Select distinct usr_id from chatbot_nation.user where first_name="Sreekanth"),
(Select distinct usr_id from chatbot_nation.user where first_name="Bharghav"),
"Y",
sysdate(),
sysdate());


INSERT INTO `chatbot_nation`.`user_vip_list`
(
`usr_id`,
`vip_id`,
`active_flag`,
`created_date`,
`updated_date`)
VALUES
(
(Select usr_id from chatbot_nation.user where first_name="Natasha"),
(Select usr_id from chatbot_nation.user where first_name="Mounika"),
"Y",
sysdate(),
sysdate());

select * from `chatbot_nation`.`user_vip_list`;

delete from `chatbot_nation`.`user_vip_list` where vip_id=3;

Alter table user_vip_list AUTO_INCREMENT = 1;



	




