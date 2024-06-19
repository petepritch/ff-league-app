import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
YAHOO_CLIENT_ID = os.getenv('CONSUMER_KEY')
YAHOO_CLIENT_SECRET = os.getenv('CONSUMER_SECRET')