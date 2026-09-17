import sys
import time
import random
from datetime import datetime
print("DEBUG: Starting main.py initialization...")
try:
    from apscheduler.schedulers.blocking import BlockingScheduler
except ImportError:
    from unittest.mock import MagicMock
    BlockingScheduler = MagicMock

try:
    from database import init_db, is_new_listing, add_listing
    from scrapers import scrape_facebook
    from notifier import send_email
    import config
    print("DEBUG: Imports successful.")
except Exception as e:
    print(f"DEBUG: Error during imports: {e}")
    sys.exit(1)

def job():
    now = datetime.now()
    # Check time window: 7am - 10pm
    if now.hour < 7 or now.hour >= 22:
        print(f"Outside allowed time window (7am-10pm). Current: {now.strftime('%H:%M')}. Skipping.")
        return

    # Determine frequency based on day of week: 0-4 are weekdays, 5-6 are weekends
    is_weekend = now.weekday() >= 5
    
    if is_weekend:
        # Weekend: 30-60 minutes (30m base + 0-30m delay)
        delay = random.randint(0, 30 * 60)
        base_interval = 30
    else:
        # Weekdays: Slower, e.g., 60-120 minutes (60m base + 0-60m delay)
        delay = random.randint(0, 60 * 60)
        base_interval = 60
        
    print(f"Starting {('Weekend' if is_weekend else 'Weekday')} scraping job after {delay/60:.2f} minute delay...")
    time.sleep(delay)
    
    print("Starting scraping job...")
    sources = [
        ("Facebook", config.FB_MARKETPLACE_URL, scrape_facebook),
    ]

    for name, url, scraper in sources:
        print(f"Scraping {name}...")
        try:
            listings = scraper(url)
            for listing in listings:
                if is_new_listing(name, listing['hash']):
                    send_email(f"New Pinball Listing: {name}", f"{listing['title']}\n{listing['url']}")
                    add_listing(name, listing['hash'])
        except Exception as e:
            print(f"Error scraping {name}: {e}")

if __name__ == '__main__':
    print("DEBUG: Running init_db...")
    init_db()
    print("DEBUG: init_db completed.")
    scheduler = BlockingScheduler()
    # Run every 30 minutes, job handles time/day logic
    scheduler.add_job(job, 'interval', minutes=30)
    print("Scraper service started.")
    job() 
    scheduler.start()
