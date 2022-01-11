import calender_manager as calm
import dates_manager as dtm
from pprint import pprint
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

matches = dtm.schedule_return()[:8]
creds = calm.check_creds()
service = build('calendar', 'v3', credentials=creds)

for match in matches:
    event = {
            'summary': match[0]+' vs '+match[1],
            'location': None,
            'description': 'Match at lolesports.com/schedule',
            'start': {
                'dateTime': match[-2],
                'timeZone': 'Asia/Kathmandu',
            },
            'end': {
                'dateTime': match[-2][:-2]+"60",
                'timeZone': 'Asia/Kathmandu',
            },
            'recurrence': [
                'RRULE:FREQ=DAILY;COUNT=1'
            ],
            'attendees': [
                None
            ],
            'reminders': {
                'useDefault': True,
            },
            }
    try :
        event = service.events().insert(calendarId='primary', body=event).execute()
    except HttpError as error:
        print('An error occurred: %s' % error)
    print(event)
    print(match)
    break

#======== templates
event = {
  'summary': 'Google I/O 2015',
  'location': '800 Howard St., San Francisco, CA 94103',
  'description': 'A chance to hear more about Google\'s developer products.',
  'start': {
    'dateTime': '2015-05-28T09:00:00-07:00',
    'timeZone': 'America/Los_Angeles',
  },
  'end': {
    'dateTime': '2015-05-28T17:00:00-07:00',
    'timeZone': 'America/Los_Angeles',
  },
  'recurrence': [
    'RRULE:FREQ=DAILY;COUNT=1'
  ],
  'attendees': [
    {'email': 'lpage@example.com'},
    {'email': 'sbrin@example.com'},
  ],
  'reminders': {
    'useDefault': False,
    'overrides': [
      {'method': 'email', 'minutes': 24 * 60},
      {'method': 'popup', 'minutes': 10},
    ],
  },
}

# event = service.events().insert(calendarId='primary', body=event).execute()
# print 'Event created: %s' % (event.get('htmlLink'))
