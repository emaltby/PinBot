import feedparser
import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import time
import random
import hashlib

def get_hash(data):
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

def scrape_pinball_info(url):
    listings = []
    feed = feedparser.parse(url)
    for entry in feed.entries:
        listings.append({
            "title": entry.title,
            "url": entry.link,
            "hash": get_hash(entry.link)
        })
    return listings

def scrape_ebay(url):
    listings = []
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(response.content, 'html.parser')
    # Simplified extraction, will need adjustment based on site structure
    for item in soup.select('.s-item__link'):
        link = item.get('href')
        if link:
            listings.append({
                "title": item.get_text(),
                "url": link,
                "hash": get_hash(link)
            })
    return listings

def scrape_facebook(url):
    listings = []
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
            if link:
                listings.append({
                    "title": "Facebook Marketplace Item",
                    "url": f"https://www.facebook.com{link}",
                    "hash": get_hash(link)
                })
        browser.close()
    return listings
