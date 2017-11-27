# -*- coding: utf-8 -*-
"""
Created on Sat Nov 18 16:11:36 2017

@author: cherp
"""

from __future__ import print_function
import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

import datetime

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'
CALENDARID='cherpatisreekanth@gmail.com'
service=None

def get_credentials():
    """Gets valid user credentials from storage.
    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.
    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, 'calendar-python-quickstart.json')

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

def read_calendar():
    CAL=service.calendarList().get(calendarId=CALENDARID).execute()
    print("Calendar Summary & Role:",CAL['summary'],CAL['accessRole'])


def insert_event():

    event = {
      'summary': 'Test Insert Event',
      'location': 'Home',
      'description': 'Automagic for the people',
      'start': {
        'dateTime': '2017-12-29T14:00:00-07:00',
        'timeZone': 'America/Los_Angeles',
      },
      'end': {
        'dateTime': '2017-12-29T15:00:00-07:00',
        'timeZone': 'America/Los_Angeles',
      },
      'attendees':[
            {'email':'chatbotnation1@mail.usf.edu'}
            ],
      'reminders': {
        'useDefault': True,
      },
    }

    event = service.events().insert(calendarId=CALENDARID, body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))

def main():
    global service
    """Shows basic usage of the Google Calendar API.
    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    eventsResult = service.events().list(
        calendarId=CALENDARID, timeMin=now, maxResults=10, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))

        print(start,end,'Summary Redacted')
        print("----------\n")

    read_calendar()
    insert_event()


if __name__ == '__main__':
    main()