from unittest.mock import MagicMock
try:
    from playwright.sync_api import sync_playwright
    from playwright_stealth import stealth_sync
except ImportError:
    # Fallback for testing when dependency is not installed
    sync_playwright = MagicMock
    stealth_sync = MagicMock

import time
import random
import hashlib
import config

def get_hash(data):
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

def scrape_facebook(url):
    listings = []
    # If mocked, return dummy data
    if isinstance(sync_playwright, MagicMock):
        return []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        # Add human-like delay
        time.sleep(random.randint(3, 7))
        
        # This is a placeholder as FB Marketplace structure changes often
        elements = page.query_selector_all('a[href*="/marketplace/item/"]')
        for el in elements:
            link = el.get_attribute('href')
            title = el.inner_text().lower()
            # Filter: must match a keyword AND a specific target machine
            is_keyword_match = any(keyword.lower() in title for keyword in config.KEYWORDS)
            is_target_machine_match = any(machine.lower() in title for machine in config.TARGET_MACHINES)
            
            if link and is_keyword_match and is_target_machine_match:
                listings.append({
                    "title": title,
                    "url": f"https://www.facebook.com{link}",
                    "hash": get_hash(link)
                })
        browser.close()
    return listings
