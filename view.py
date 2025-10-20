# INITIALIZATIONS ================================================================================#
from tkinter import *
from control import get_card_info
from PIL import ImageTk, Image
import urllib.request
import io

name = None
card_type = None
rarity = None
market = None
photo = None
#=================================================================================================#
# FUNCTIONS ======================================================================================#
def switch_menu():
    for p in pages:
        p.pack_forget()
    page = pages[0]
    page.pack()

def switch_users():
    for p in pages:
        p.pack_forget()
    page = pages[1]
    page.pack()

def switch_search():
    for p in pages:
        p.pack_forget()
    page = pages[2]
    page.pack()

def update_search():
    pokemon_image.config(image=photo) 
    pokemon_name.config(text=f"Card Name: {name}")
    pokemon_type.config(text=f"Card Type: {card_type}")
    pokemon_rarity.config(text=f"Rarity: {rarity}")
    pokemon_market.config(text=f"Market Price: ${market}")

def searchPokemon(event=None):
    query = entry.get()
    if(query):
        card_info = get_card_info(query)
        
        if card_info:
            global name, card_type, rarity, market, photo
            name = card_info.get("name", "Unknown")
            card_type = card_info.get("cardType")
            rarity = card_info.get("rarity", "Unknown Rarity")
            img_url = card_info.get("imageUrl")
            prices = card_info.get("prices", {})
            if isinstance(prices, dict) and prices:
                market = prices.get("market")

            with urllib.request.urlopen(img_url) as u:
                raw_data = u.read()
            image = Image.open(io.BytesIO(raw_data))
            photo = ImageTk.PhotoImage(image)

            update_search()
        else:
            print("No card found with that name or ID.\n")
            
#=================================================================================================#
# INITIALIZE WINDOW ==============================================================================#
root = Tk()
root.geometry('600x800')
root.title("Pokemon Card Manager")
main_frame = Frame(root, bg="#ffffff")
#=================================================================================================#
# MENU PAGE ======================================================================================#
menu = Frame(main_frame, bg="#ffffff")

title = Label(menu,
              bg='#ffffff',
              text="Welcome to the Pokemon Card Manager",
              font=("fixedsys", 20)
             )
title.grid(row=1, column=0, columnspan=3)

search_button = Button(menu,
                      bg="#888888",
                      fg='#ffffff',
                      text="SEARCH",
                      font=("fixedsys", 20),
                      width=10,
                      command=switch_search
                     )
search_button.grid(row=3, column=0)

users_button = Button(menu,
                      bg='#888888',
                      fg='#ffffff',
                      text="USERS",
                      font=("fixedsys", 20),
                      width=10,
                      command=switch_users
                     )
users_button.grid(row=3, column=2)

search_hint = Label(menu,
                    bg='#ffffff',
                    text="Opens a search page\nfor Pokemon Cards",
                    font=("fixedsys", 12)
                   )
search_hint.grid(row=4, column=0)

users_hint = Label(menu,
                   bg='#ffffff',
                   text="Shows a list of users",
                   font=("fixedsys", 12),
                  )
users_hint.grid(row=4, column=2)

menu.pack(pady=20)
#=================================================================================================#
# USERS PAGE =====================================================================================#
users = Frame(main_frame)
users_lb = Label(users, text="Users", font=("fixedsys", 20)).pack()
#=================================================================================================#
# SEARCH PAGE ====================================================================================#
search = Frame(main_frame, bg="#ffffff")

entry_lb = Label(search,
                 bg='#ffffff',
                 text="Search by TCG Player ID\nor by Card Name",
                 font=("fixedsys", 12)
                )
entry_lb.grid(row=1, column=0, padx=5)

entry = Entry(search,
              bg='#ffffff',
              font=("fixedsys", 20),
              width=15
             )
entry.grid(row=1, column=1)
entry.bind("<Return>", searchPokemon)

entry_search = Button(search,
                      bg='#888888',
                      fg='#ffffff',
                      text="SEARCH",
                      font=("fixedsys", 20),
                      width=6,
                      command=searchPokemon
                     )
entry_search.grid(row=1, column=2)

pokemon_image = Label(search,
                      bg='#ffffff',
                      image=photo,
                     ) 
pokemon_image.grid(row=2, column=0, columnspan=3)

pokemon_name = Label(search,
                     bg='#ffffff',
                     text=f"",
                     font=("fixedsys", 20)
                    )
pokemon_name.grid(row=3, column=0, columnspan=3)

pokemon_type = Label(search,
                     bg='#ffffff',
                     text=f"",
                     font=("fixedsys", 20)
                    )
pokemon_type.grid(row=4, column=0, columnspan=3)

pokemon_rarity = Label(search,
                       bg='#ffffff',
                       text=f"",
                       font=("fixedsys", 20)
                      )
pokemon_rarity.grid(row=5, column=0, columnspan=3)

pokemon_market = Label(search,
                       bg='#ffffff',
                       text=f"",
                       font=("fixedsys", 20)
                      )
pokemon_market.grid(row=6, column=0, columnspan=3)
#=================================================================================================#
# MAIN FRAME PACK ================================================================================#
main_frame.pack(fill=BOTH, expand=True)
pages = [menu, users, search]
#=================================================================================================#

buttons_frame = Frame(root)
buttons_frame.pack()

root.mainloop()