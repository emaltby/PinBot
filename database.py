import sqlite3
import config

def init_db():
    conn = sqlite3.connect(config.DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS seen_listings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            platform TEXT NOT NULL,
            url_hash TEXT NOT NULL UNIQUE,
            title TEXT,
            link TEXT,
            emailed INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

def is_new_listing(platform, url_hash):
    conn = sqlite3.connect(config.DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT 1 FROM seen_listings WHERE url_hash = ?', (url_hash,))
    exists = cursor.fetchone() is None
    conn.close()
    return exists

def add_listing(platform, url_hash, title, link, emailed=False):
    conn = sqlite3.connect(config.DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO seen_listings (platform, url_hash, title, link, emailed) VALUES (?, ?, ?, ?, ?)', 
                       (platform, url_hash, title, link, int(emailed)))
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    conn.close()

def get_all_listings():
    conn = sqlite3.connect(config.DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT title, link, emailed FROM seen_listings ORDER BY id DESC')
    listings = cursor.fetchall()
    conn.close()
    return listings
