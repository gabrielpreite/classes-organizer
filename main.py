from __future__ import print_function
import datetime
import secrets
import pickle
import os.path
import json
import hashlib
import bencode
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def addCalendars(calSum, service):
    calId = ""
    with open("ids.json") as f2:
        ids = json.loads(f2.read())
        for item in ids["calendars"]:
            if item["summary"] == calSum:
                calId = item["id"]
    try:
        resCalendar = service.calendars().get(calendarId=calId).execute()
        print("Found existing calendar for "+calSum)
    except:
        newCal = {
            "summary": calSum,
            "timezone": "Europe/Rome",
        }
        res = service.calendars().insert(body=newCal).execute()
        ids["calendars"].append({"summary": calSum, "id": res["id"]})
        with open("ids.json", "w") as f2:
            json.dump(ids, f2)
        print("Added calendar for "+calSum)
    #print(resCalendar)

def main():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('calendar', 'v3', credentials=creds)

    with open("primo1.json") as f:
        cal = json.loads(f.read())
    for item in cal:
        calSum = item["title"].split(" ",1)[0]
        addCalendars(calSum, service)

if __name__ == '__main__':
    main()