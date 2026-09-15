from apscheduler.schedulers.blocking import BlockingScheduler
from database import init_db, is_new_listing, add_listing
from scrapers import scrape_pinball_info, scrape_ebay, scrape_facebook
from notifier import send_email
import config

def job():
    print("Starting scraping job...")
    sources = [
        ("PinballInfo", config.PINBALL_INFO_RSS_URL, scrape_pinball_info),
        ("eBay", config.EBAY_SEARCH_URL, scrape_ebay),
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
    init_db()
    scheduler = BlockingScheduler()
    scheduler.add_job(job, 'interval', minutes=60)
    print("Scraper service started.")
    job() # Run immediately once
    scheduler.start()
