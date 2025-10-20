import json
import os
import sqlite3

COLLECTION_FILE = "collection.json"
DB_FILE = "pokemon_cards_collection.db"

# Global collection data
collection = []
conn = None
cursor = None


def init_database():
    """Initialize the database connection and create table."""
    global conn, cursor
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            "set" TEXT NOT NULL,
            rarity TEXT NOT NULL,
            market REAL NOT NULL,
            image_url TEXT NOT NULL
        )
    """)
    conn.commit()


def record_from_card(card_dict):
    """Convert a card dict from API to a collection record."""
    set_info = card_dict.get("set") or {}
    prices = card_dict.get("prices") or {}
    return {
        "name": card_dict.get("name", "Unknown"),
        "set": set_info.get("name", "Unknown Set"),
        "rarity": card_dict.get("rarity", "Unknown Rarity"),
        "market": prices.get("market"),
        "tcgPlayerId": card_dict.get("tcgPlayerId"),
        "imageUrl": card_dict.get("imageUrl"),
    }


def persist_collection():
    """Save collection to JSON file and database."""
    try:
        with open(COLLECTION_FILE, "w", encoding="utf-8") as f:
            json.dump(collection, f, ensure_ascii=False, indent=2)
        
        # Note: This will insert duplicates each time. Consider using DELETE first
        # or switching to a proper upsert pattern in future improvements
        cursor.executemany(
            "INSERT INTO cards (name, set, rarity, market, image_url) VALUES (?, ?, ?, ?, ?)",
            [(c.get("name"), c.get("set"), c.get("rarity"), c.get("market"), c.get("imageUrl")) 
             for c in collection]
        )
        conn.commit()
    except Exception as e:
        print(f"Failed to save collection: {e}")


def load_collection():
    """Load collection from JSON file."""
    global collection
    if not os.path.exists(COLLECTION_FILE):
        return
    try:
        with open(COLLECTION_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                collection.clear()
                collection.extend(data)
    except Exception as e:
        print(f"Failed to load collection: {e}")


def close_database():
    """Close the database connection."""
    if conn:
        conn.close()