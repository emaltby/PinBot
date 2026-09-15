from database import init_db, is_new_listing, add_listing
from scrapers import get_hash

def test_db():
    print("Testing database...")
    init_db()
    url = "http://test.url"
    h = get_hash(url)
    
    assert is_new_listing("Test", h) == True
    add_listing("Test", h)
    assert is_new_listing("Test", h) == False
    print("Database test passed.")

if __name__ == '__main__':
    test_db()
