import dates_manager as dtm
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = [
    "https://www.googleapis.com/auth/calendar.readonly",
    "https://www.googleapis.com/auth/calendar.events.readonly",
    "https://www.googleapis.com/auth/calendar.events.owned",
    "https://www.googleapis.com/auth/calendar.events",
]

creds = Credentials.from_authorized_user_file("token.json", SCOPES)

service = build("calendar", "v3", credentials=creds)

matches = dtm.schedule_return()
for match in matches:
    team1, team2, year, month, day, hour, minute, checker = match
    event_name = team1 + " vs " + team2
    date = "-".join([year, month, day]) + "T"
    start_time = date + ":".join([hour, minute, "00"])
    timeZone = "Etc/UTC"
    hour = str(int(hour) + 1).zfill(2) if hour != "24" else "00"
    end_time = date + ":".join([hour, minute, "00"])

    print(event_name, start_time, end_time)
    event = {
        "summary": event_name,
        "description": "Match at lolesports.com/schedule",
        "start": {
            "dateTime": start_time,
            "timeZone": timeZone,
        },
        "end": {
            "dateTime": end_time,
            "timeZone": timeZone,
        },
    }
    event = (
        service.events()
        .insert(
            calendarId="ilv5csjir2espe1t64i5l5f0mc@group.calendar.google.com",
            body=event,
        )
        .execute()
    )
    break
