import sys
import time
import random
import os
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
    from matcher import is_machine_match
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
    if not os.getenv("TESTING"):
        time.sleep(delay)
    
    print("Starting scraping job...")
    
    # Reload config dynamically from json
    from dynamic_config import load_dynamic_config
    dynamic_conf = load_dynamic_config()
    
    urls = getattr(config, 'FB_MARKETPLACE_URLS', None) or [config.FB_MARKETPLACE_URL]
    sources = [
        (f"Facebook (Query {i+1})", url, scrape_facebook) for i, url in enumerate(urls)
    ]

    for name, url, scraper in sources:
        print(f"Scraping {name}...")
        try:
            listings = scraper(url, keywords=dynamic_conf['KEYWORDS'], target_machines=dynamic_conf['TARGET_MACHINES'])
            # Polite delay between multiple query URLs to avoid bot detection
            if not os.getenv("TESTING"):
                time.sleep(random.randint(5, 12))
            for listing in listings:
                if is_new_listing(name, listing['hash']):
                    # Filter logic for email
                    is_keyword_match = any(keyword.lower() in listing['title'].lower() for keyword in dynamic_conf.get('KEYWORDS', []))
                    is_target_machine_match = any(is_machine_match(machine, listing['title']) for machine in dynamic_conf.get('TARGET_MACHINES', []))
                    is_excluded = any(ex.lower() in listing['title'].lower() for ex in dynamic_conf.get('EXCLUDE_KEYWORDS', []))
                    price_valid = listing['price'] >= 40
                    
                    if is_keyword_match and is_target_machine_match and price_valid and not is_excluded:
                        print(f"Logging and emailing listing: {listing['title']}")
                        send_email(f"New Pinball Listing: {name}", listing['title'], link=listing['url'], price=listing['price'])
                        add_listing(name, listing['hash'], listing['title'], listing['url'], emailed=True)
                    else:
                        print(f"Logging listing (not emailed): {listing['title']}")
                        add_listing(name, listing['hash'], listing['title'], listing['url'], emailed=False)
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
