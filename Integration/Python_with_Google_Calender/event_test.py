# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 17:42:45 2017

@author: cherp
"""

from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None
    
SCOPES = 'https://www.googleapis.com/auth/calendar'
store=file.Storage('storage.json')
creds=store.get()
if not creds or creds.invalid:
    flow=client.flow_from_clientsecrets('client_secret_1.json',SCOPES)
    creds=tools.run_flow(flow, store, flags) \
        if flags else tools.run(flow,store)
service = build('calendar','v3',http=creds.authorize(Http()))

EVENT= {
    'summary': 'Test Insert Event',
    'start': {
        'dateTime': '2017-12-31T16:00:00-07:00',
        'timeZone': 'America/Los_Angeles',
      },
      'end': {
        'dateTime': '2017-12-31T17:00:00-07:00',
        'timeZone': 'America/Los_Angeles',
      },
    'attendees':[
            {'email':'cherpatisreekanth@gmail.com'},
            {'email':'chatbotnation3@gmail.com'},
            {'email':'bmthanki@mail.usf.edu'}
            ],
        }

e= service.events().insert(calendarId='chatbotnation1@gmail.com',
              sendNotifications=True, body=EVENT).execute()

print(''' **** %r Event added:
        Start: %s
        End: %s ''' % (e['summary'].encode('utf-8'),
            e['start']['dateTime'],e['end']['dateTime']))