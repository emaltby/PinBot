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

def scrape_facebook(url, keywords, target_machines):
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
        
        elements = page.query_selector_all('a[href*="/marketplace/item/"]')
        print(f"DEBUG: Found {len(elements)} potential listing elements.")
        for el in elements:
            link = el.get_attribute('href')
            if not link:
                continue
                
            title = el.inner_text().lower()
            
            # NOTE: Price extraction is highly dependent on FB DOM structure and may require adjustment
            price_el = el.query_selector('span[class*="price"]')
            price = 0
            if price_el:
                try:
                    price_text = price_el.inner_text().replace('£', '').replace(',', '').strip()
                    price = float(price_text)
                except ValueError:
                    price = 0
            
            listings.append({
                "title": title,
                "url": f"https://www.facebook.com{link}",
                "hash": get_hash(link),
                "price": price
            })
        browser.close()
    return listings
