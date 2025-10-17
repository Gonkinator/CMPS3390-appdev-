import requests

API_KEY = "pokeprice_free_3782ad58a346398eef2292808e87a8e7811b19e227ebf856"
BASE_URL = "https://www.pokemonpricetracker.com/api/v2/cards"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}"
}


def get_card_info(query):
    """
    Search for a Pokémon card using the Pokémon Price Tracker API.
    You can use the card name (e.g., 'Charizard') or an ID.
    """
    params = {
        "search": query,      # Search term (name, set, or ID)
        #"tcgPlayerId": query,
        "includeHistory": "false",
        "limit": 1            # Only return the top result
    }

    response = requests.get(BASE_URL, headers=HEADERS, params=params)

    if response.status_code == 200:
        data = response.json()
        if data.get("data"):
            return data["data"][0]  # Return the first match
        else:
            print("No card found with that name or ID.\n")
            return None
    else:
        print(f"Error: {response.status_code} - {response.text}\n")
        return None

poke_card = input("Enter Pokémon card name or ID: ").strip()
card_info = get_card_info(poke_card)

if card_info:
    name = card_info.get("name", "Unknown")
    set_info = card_info.get("set", {}).get("name", "Unknown Set")
    rarity = card_info.get("rarity", "Unknown Rarity")

    print(f"\n{name} — {set_info}")
    print(f"Rarity: {rarity}")

    prices = card_info.get("prices", {})
    if prices:
        market = prices.get("market")
        low = prices.get("low")
        high = prices.get("high")

        print("\n--- Current Prices (USD) ---")
        if market: print(f"Market Price: ${market}")
        if low: print(f"Lowest Price: ${low}")
        if high: print(f"Highest Price: ${high}")
    else:
        print("No price data available.")

