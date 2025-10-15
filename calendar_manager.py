import os
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import pytz
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import config

# Google Calendar API scopes
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

class CalendarManager:
    def __init__(self):
        self.service = None
        self.timezone = pytz.timezone(config.TIMEZONE)
        
    def authenticate(self):
        """Google Calendar API authentication"""
        creds = None
        
        # Check if token file exists
        if os.path.exists(config.GOOGLE_TOKEN_FILE):
            creds = Credentials.from_authorized_user_file(config.GOOGLE_TOKEN_FILE, SCOPES)
        
        # If there are no valid credentials, run the OAuth flow
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if os.path.exists(config.GOOGLE_CREDENTIALS_FILE):
                    flow = InstalledAppFlow.from_client_secrets_file(
                        config.GOOGLE_CREDENTIALS_FILE, SCOPES)
                    creds = flow.run_local_server(port=0)
                else:
                    print("Google credentials file not found. Using mock data for demo.")
                    return False
            
            # Save credentials for next run
            with open(config.GOOGLE_TOKEN_FILE, 'w') as token:
                token.write(creds.to_json())
        
        try:
            self.service = build('calendar', 'v3', credentials=creds)
            return True
        except Exception as e:
            print(f"Error building calendar service: {e}")
            return False
    
    def get_events(self, start_date: datetime, end_date: datetime) -> List[Dict]:
        """Retrieve calendar events for specified period"""
        if not self.service:
            return self._get_mock_events(start_date, end_date)
        
        try:
            events_result = self.service.events().list(
                calendarId=config.CALENDAR_ID,
                timeMin=start_date.isoformat() + 'Z',
                timeMax=end_date.isoformat() + 'Z',
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            return self._format_events(events)
            
        except HttpError as error:
            print(f"Error fetching events: {error}")
            return self._get_mock_events(start_date, end_date)
    
    def _format_events(self, events: List[Dict]) -> List[Dict]:
        """Format event data"""
        formatted_events = []
        
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))
            
            # Parse datetime
            if 'T' in start:
                start_dt = datetime.fromisoformat(start.replace('Z', '+00:00'))
                end_dt = datetime.fromisoformat(end.replace('Z', '+00:00'))
            else:
                start_dt = datetime.fromisoformat(start)
                end_dt = datetime.fromisoformat(end)
            
            formatted_events.append({
                'id': event.get('id', ''),
                'title': event.get('summary', 'No Title'),
                'start': start_dt,
                'end': end_dt,
                'description': event.get('description', ''),
                'location': event.get('location', ''),
                'all_day': 'date' in event['start']
            })
        
        return formatted_events
    
    def _get_mock_events(self, start_date: datetime, end_date: datetime) -> List[Dict]:
        """Generate mock calendar events for demo"""
        mock_events = []
        current_date = start_date.date()
        end_date_only = end_date.date()
        
        # Weekly recurring events
        while current_date <= end_date_only:
            # Monday
            if current_date.weekday() == 0:
                mock_events.extend([
                    {
                        'id': f'mock_meeting_{current_date}_1',
                        'title': 'Team Meeting',
                        'start': datetime.combine(current_date, datetime.min.time().replace(hour=9, minute=0)),
                        'end': datetime.combine(current_date, datetime.min.time().replace(hour=10, minute=0)),
                        'description': 'Weekly team meeting',
                        'location': 'Conference Room A',
                        'all_day': False
                    },
                    {
                        'id': f'mock_lunch_{current_date}',
                        'title': 'Lunch Appointment',
                        'start': datetime.combine(current_date, datetime.min.time().replace(hour=12, minute=0)),
                        'end': datetime.combine(current_date, datetime.min.time().replace(hour=13, minute=0)),
                        'description': 'Lunch meeting with client',
                        'location': 'Restaurant',
                        'all_day': False
                    }
                ])
            
            # Tuesday
            elif current_date.weekday() == 1:
                mock_events.extend([
                    {
                        'id': f'mock_presentation_{current_date}',
                        'title': 'Presentation',
                        'start': datetime.combine(current_date, datetime.min.time().replace(hour=14, minute=0)),
                        'end': datetime.combine(current_date, datetime.min.time().replace(hour=15, minute=30)),
                        'description': 'Quarterly report presentation',
                        'location': 'Main Conference Room',
                        'all_day': False
                    }
                ])
            
            # Wednesday
            elif current_date.weekday() == 2:
                mock_events.extend([
                    {
                        'id': f'mock_doctor_{current_date}',
                        'title': 'Regular Checkup',
                        'start': datetime.combine(current_date, datetime.min.time().replace(hour=10, minute=30)),
                        'end': datetime.combine(current_date, datetime.min.time().replace(hour=11, minute=30)),
                        'description': 'Annual health checkup',
                        'location': 'Hospital',
                        'all_day': False
                    }
                ])
            
            # Thursday
            elif current_date.weekday() == 3:
                mock_events.extend([
                    {
                        'id': f'mock_workout_{current_date}',
                        'title': 'Gym',
                        'start': datetime.combine(current_date, datetime.min.time().replace(hour=18, minute=0)),
                        'end': datetime.combine(current_date, datetime.min.time().replace(hour=19, minute=30)),
                        'description': 'Weekly workout',
                        'location': 'Fitness Center',
                        'all_day': False
                    }
                ])
            
            # Friday
            elif current_date.weekday() == 4:
                mock_events.extend([
                    {
                        'id': f'mock_review_{current_date}',
                        'title': 'Weekly Review',
                        'start': datetime.combine(current_date, datetime.min.time().replace(hour=16, minute=0)),
                        'end': datetime.combine(current_date, datetime.min.time().replace(hour=17, minute=0)),
                        'description': 'Weekly work review',
                        'location': 'Office',
                        'all_day': False
                    }
                ])
            
            current_date += timedelta(days=1)
        
        return mock_events
    
    def get_free_time_slots(self, start_date: datetime, end_date: datetime, 
                           duration_minutes: int = 60) -> List[Dict]:
        """Find available time slots within specified period"""
        events = self.get_events(start_date, end_date)
        
        # Group by day
        daily_events = {}
        for event in events:
            date_key = event['start'].date()
            if date_key not in daily_events:
                daily_events[date_key] = []
            daily_events[date_key].append(event)
        
        free_slots = []
        current_date = start_date.date()
        end_date_only = end_date.date()
        
        while current_date <= end_date_only:
            if current_date.weekday() < 5:  # Weekdays only
                day_events = daily_events.get(current_date, [])
                day_slots = self._find_free_slots_for_day(
                    current_date, day_events, duration_minutes
                )
                free_slots.extend(day_slots)
            
            current_date += timedelta(days=1)
        
        return free_slots
    
    def _find_free_slots_for_day(self, date, events: List[Dict], 
                                duration_minutes: int) -> List[Dict]:
        """Find free time slots for specific date"""
        # Set working hours
        work_start = datetime.combine(date, datetime.min.time().replace(hour=9, minute=0))
        work_end = datetime.combine(date, datetime.min.time().replace(hour=18, minute=0))
        
        # Sort events by time
        sorted_events = sorted(events, key=lambda x: x['start'])
        
        free_slots = []
        current_time = work_start
        
        for event in sorted_events:
            event_start = event['start']
            event_end = event['end']
            
            # Check if there is sufficient time between current time and event start time
            if (event_start - current_time).total_seconds() >= duration_minutes * 60:
                free_slots.append({
                    'start': current_time,
                    'end': event_start,
                    'duration_minutes': int((event_start - current_time).total_seconds() / 60),
                    'date': date
                })
            
            # Update current time to event end time (including buffer time)
            current_time = event_end + timedelta(minutes=config.DEFAULT_BREAK_TIME)
        
        # Check free time after last event
        if (work_end - current_time).total_seconds() >= duration_minutes * 60:
            free_slots.append({
                'start': current_time,
                'end': work_end,
                'duration_minutes': int((work_end - current_time).total_seconds() / 60),
                'date': date
            })
        
        return free_slots