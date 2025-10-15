import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# OpenAI Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Google Calendar Configuration
GOOGLE_CREDENTIALS_FILE = os.getenv('GOOGLE_CREDENTIALS_FILE', 'credentials.json')
GOOGLE_TOKEN_FILE = os.getenv('GOOGLE_TOKEN_FILE', 'token.json')
CALENDAR_ID = os.getenv('CALENDAR_ID', 'primary')

# Application Configuration
TIMEZONE = 'Asia/Seoul'
DEFAULT_WORKING_HOURS = {
    'start': '09:00',
    'end': '18:00'
}
DEFAULT_BREAK_TIME = 30  # minutes between appointments