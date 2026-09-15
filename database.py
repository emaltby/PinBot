import sqlite3
from config import DB_PATH

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS seen_listings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            platform TEXT NOT NULL,
            url_hash TEXT NOT NULL UNIQUE
        )
    ''')
    conn.commit()
    conn.close()

def is_new_listing(platform, url_hash):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT 1 FROM seen_listings WHERE url_hash = ?', (url_hash,))
    exists = cursor.fetchone() is None
    conn.close()
    return exists

def add_listing(platform, url_hash):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO seen_listings (platform, url_hash) VALUES (?, ?)', (platform, url_hash))
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    conn.close()
