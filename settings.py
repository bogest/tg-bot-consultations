from dotenv import load_dotenv
import os

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_CHAT = os.getenv('ADMIN_CHAT')
ADMIN_ID = int(os.getenv('ADMIN_ID'))