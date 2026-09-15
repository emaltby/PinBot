import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set these via environment variables for security
DB_PATH = "listings.db"
EMAIL_SENDER = os.getenv("EMAIL_SENDER", "your_email@gmail.com")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "your_app_password")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER", "receiver@gmail.com")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))

# Configure your search URLs here
PINBALL_INFO_RSS_URL = "https://pinside.com/pinball/forum/topic/marketplace-for-sale/feed"
EBAY_SEARCH_URL = "https://www.ebay.com/sch/i.html?_nkw=pinball+machine"
FB_MARKETPLACE_URL = "https://www.facebook.com/marketplace/search/?query=pinball+machine"
