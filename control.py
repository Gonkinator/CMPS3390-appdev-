# (Note for pokemontcg) *Need to figure how to handle invalid requests*
# Solution 1: Exclusively use requests library
# Solution 2: Use requests as validation, then use pokemontcg for getting data

from pokemontcgsdk import *                         # import all data from pokemontcg library                          
import requests                                     # import requests library
from control import *

base_url = "https://api.pokemontcg.io/v2/cards"     # base url for searching

def get_card_info(poke_card):                            # get card info from name function
    
    url = f"{base_url}/{poke_card}"                      # parce URL
    response = requests.get(url)                    # GET from parced URL

    if response.status_code == 200:                 # If request was OK
        card_info = response.json()                 # card_data = python dict from response
        card_info = card_info["data"]               # parse to object name "data" (why they make it like this ???)
        print_info(card_info)

    else:                                           # Request failed w/ temp terminal response
        print("The card you were trying" \
        " to find does not exist\n")

def print_info(card_info):
    # PRICE CONVERSION ===========================================================================#
    con_price = (requests.get("https://open.er-api.com/v6/latest/EUR")).json() # Get all EUR conversions into json
    
    eur_price = card_info["cardmarket"]["prices"]["averageSellPrice"]
    usd_price = con_price["rates"]["USD"] * eur_price

    usd_price = "{:.2f}".format(usd_price)
    #=============================================================================================#

    # * temp *
    # PRINT INFO =================================================================================#
    print(f"Name: {card_info["name"]}")
    print(f"Supertype: {card_info["supertype"]}")
    print(f"Rarity: {card_info["rarity"]}")
    print(f"Price: USD ${usd_price}")
    #=============================================================================================#