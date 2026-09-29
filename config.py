import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Set these via environment variables for security
DB_PATH = os.getenv("DB_PATH", "listings.db")
EMAIL_SENDER = os.getenv("EMAIL_SENDER", "your_email@gmail.com")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "your_app_password")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER", "receiver@gmail.com")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))

# Configure your search URLs here (Multiple URLs cast a wider net to maximize discovery)
FB_MARKETPLACE_URL = "https://www.facebook.com/marketplace/sheffield/search?query=pinball%20machine&radius_in_km=250&locale=en_GB"

FB_MARKETPLACE_URLS = [
    "https://www.facebook.com/marketplace/sheffield/search?query=pinball&radius_in_km=250&locale=en_GB",
    "https://www.facebook.com/marketplace/sheffield/search?query=pinball%20machine&radius_in_km=250&locale=en_GB",
    "https://www.facebook.com/marketplace/sheffield/search?query=stern%20pinball&radius_in_km=250&locale=en_GB",
    "https://www.facebook.com/marketplace/sheffield/search?query=williams%20pinball&radius_in_km=250&locale=en_GB",
]
