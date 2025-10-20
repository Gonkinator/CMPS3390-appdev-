# INITIALIZATIONS ================================================================================#
import requests

BASE_URL = "https://www.pokemonpricetracker.com/api/v2/cards"
API_KEY = "pokeprice_free_96f09a56bcdb4e2a5a5c5ae8a9830c4a119022b1dafd675b"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}
HTTP_TIMEOUT = 10
#=================================================================================================#


# FUNCTIONS ======================================================================================#
def _extract_first_card(obj):
    """
    Return the first card dict from ANY reasonable payload shape, or None.
    Handles:
      - {"data": [ ... ]}
      - {"data": {"cards": [ ... ]}}
      - {"cards": [ ... ]}
      - {"results": [ ... ]}
      - {"data": {...single card...}}
      - {...single card...}
    """
    if obj is None:
        return None

    # If list, return first element (if present)
    if isinstance(obj, list):
        return obj[0] if obj else None

    # If dict, try common keys or treat as single-card
    if isinstance(obj, dict):
        # If it already looks like a card
        if any(k in obj for k in ("name", "rarity", "set", "prices")):
            return obj

        # Common container keys
        for key in ("data", "cards", "results", "items"):
            if key in obj:
                return _extract_first_card(obj[key])

    # Unknown shape
    return None


def _request_one(params, label):
    """Make request, handle errors, and extract the first card without [] indexing bugs."""
    try:
        r = requests.get(BASE_URL, headers=HEADERS, params=params, timeout=HTTP_TIMEOUT)
    except requests.RequestException as e:
        print(f"[{label}] Network error: {e}\n")
        return None

    if r.status_code != 200:
        print(f"[{label}] Error: {r.status_code} - {r.text[:200]}\n")
        return None

    try:
        payload = r.json()
    except ValueError:
        print(f"[{label}] Invalid JSON response.\n")
        return None

    card = _extract_first_card(payload)
    return card


def get_card_info(query):
    """
    Combined search:
      - If the query is all digits, try tcgPlayerId first, then name.
      - Otherwise try name first, then tcgPlayerId.
    Returns the first matching card dict, or None.
    """
    q = (query or "").strip()
    looks_like_id = q.isdigit()

    if looks_like_id:
        # Try ID, then name
        hit = _request_one({"tcgPlayerId": q, "includeHistory": "false", "limit": 1}, "byID")
        return hit or _request_one({"search": q, "includeHistory": "false", "limit": 1}, "byName")
    else:
        hit = _request_one({"search": q, "includeHistory": "false", "limit": 1}, "byName")
        return hit or _request_one({"tcgPlayerId": q, "includeHistory": "false", "limit": 1}, "byID")
#=================================================================================================#


# syntax for view
if __name__ == "__main__":
    poke_card = input("Enter Pokémon card name or TCGplayer ID: ").strip()
    card_info = get_card_info(poke_card)

    if card_info:
        name = card_info.get("name", "Unknown")
        set_info = (card_info.get("set") or {}).get("name", "Unknown Set")
        rarity = card_info.get("rarity", "Unknown Rarity")
        print(f"\n{name} — {set_info}")
        print(f"Rarity: {rarity}")

        prices = card_info.get("prices", {})
        if isinstance(prices, dict) and prices:
            market = prices.get("market")
            low = prices.get("low")
            high = prices.get("high")
        
            print("\n--- Current Prices (USD) ---")
            if market is not None: print(f"Market Price: ${market}")
            if low is not None: print(f"Lowest Price: ${low}")
            if high is not None: print(f"Highest Price: ${high}")
        else:
            print("No price data available.")
    else:
        print("No card found with that name or ID.\n")