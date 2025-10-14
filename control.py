# (Note for pokemontcg) *Need to figure how to handle invalid requests*
# Solution 1: Exclusively use requests library
# Solution 2: Use requests as validation, then use pokemontcg for getting data

from pokemontcgsdk import *                         # import all data from pokemontcg library                          
import requests                                     # import requests library

base_url = "https://api.pokemontcg.io/v2/cards"     # base url for searching

def get_card_info(card):                            # get card info from name function
    url = f"{base_url}/{card}"                      # parce URL
    response = requests.get(url)                    # GET from parced URL

    if response.status_code == 200:                 # If request was OK
        card_data = response.json()                 # card_data = python dict from response
        return card_data                            # return data

    else:                                           # Request failed w/ temp terminal response
        print("The card you were trying" \
        " to find does not exist\n")

poke_card = input(str("Input Pokemon Card ID: "))   # temp terminal input (MUST BE ID  |  name search later)
card_info = get_card_info(poke_card)                # execute function with input and output

if card_info:                                       # if got valid response + info
    card_info = card_info["data"]                   # parse to object name "data" (why they make it like this ???)
    
    print(f"{card_info["name"]})")                  # (temp) print some stuff
    print(f"{card_info["supertype"]})")
    print(f"{card_info["subtypes"]})")