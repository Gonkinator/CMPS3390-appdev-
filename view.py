
from tkinter import *
from tkinter import ttk
from control import get_card_info
from PIL import ImageTk, Image
import urllib.request
import io
import json
import os
import sqlite3



name = None
card_type = None
rarity = None
market = None
photo = None
last_card = None
collection = []
COLLECTION_FILE = "collection.json"
filter_field_options = ("Name", "Set", "Rarity")
filter_field_var = None
filter_text_var = None

conn = sqlite3.connect("pokemon_cards_colection.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS cards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    "set" TEXT NOT NULL,
    rarity TEXT NOT NULL,
    market REAL NOT NULL,
    image_url TEXT NOT NULL
)""")
conn.commit()


#=================================================================================================#
# FUNCTIONS ======================================================================================#
def show_start():
    for p in pages:
        p.pack_forget()
    page = pages[0]
    page.pack()

def show_add():
    for p in pages:
        p.pack_forget()
    page = pages[1]
    page.pack()

def update_add_view():
    pokemon_image.config(image=photo) 
    pokemon_name.config(text=f"Card Name: {name}")
    pokemon_type.config(text=f"Card Type: {card_type}")
    pokemon_rarity.config(text=f"Rarity: {rarity}")
    pokemon_market.config(text=f"Market Price: ${market}")

def add_card(event=None):
    query = entry.get()
    if(query):
        card_info = get_card_info(query)
        
        if card_info:
            global name, card_type, rarity, market, photo, last_card
            name = card_info.get("name", "Unknown")
            card_type = card_info.get("cardType")
            rarity = card_info.get("rarity", "Unknown Rarity")
            img_url = card_info.get("imageUrl")
            prices = card_info.get("prices", {})
            if isinstance(prices, dict) and prices:
                market = prices.get("market")

            # Try to load image, but do not fail if network is blocked
            photo = None
            if img_url:
                try:
                    with urllib.request.urlopen(img_url) as u:
                        raw_data = u.read()
                    image = Image.open(io.BytesIO(raw_data))
                    photo = ImageTk.PhotoImage(image)
                except Exception:
                    photo = None

            last_card = card_info
            update_add_view()
        else:
            print("No card found with that name or ID.\n")
    else:
        print("Please enter a card name or ID.")

def record_from_card(card_dict):
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

def save_current_card():
    if not last_card:
        print("Search a card first before saving.")
        return
    rec = record_from_card(last_card)
    collection.append(rec)
    persist_collection()
    refresh_collection_view()
    entry.delete(0, END)
    show_start()

def persist_collection():
    try:
        with open(COLLECTION_FILE, "w") as f:
            json.dump(collection, f, ensure_ascii=False, indent=2)
            cursor.executemany("INSERT INTO cards (name, set, rarity, market, image_url) VALUES (?, ?, ?, ?, ?)", collection)
            conn.commit()
    except Exception as e:
        print(f"Failed to save collection: {e}")

def load_collection():
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

def refresh_collection_view():
    # Clear tree rows
    for row in collection_tree.get_children():
        collection_tree.delete(row)
    # Insert records
    for idx, rec in enumerate(collection):
        price = rec.get("market")
        price_str = f"${price}" if isinstance(price, (int, float)) else (f"${price}" if price else "-")
        tag = "odd" if idx % 2 else "even"
        collection_tree.insert("", "end", iid=str(idx), values=(rec.get("name"), rec.get("set"), rec.get("rarity"), price_str), tags=(tag,))
    # Update total
    total = 0.0
    for rec in collection:
        p = rec.get("market")
        try:
            if p is not None:
                total += float(p)
        except (TypeError, ValueError):
            pass
    total_value_lbl.config(text=f"Total Value: ${total:,.2f}")

def remove_selected():
    selected = collection_tree.selection()
    if not selected:
        return
    # Remove from end to start to maintain indices
    for iid in sorted((int(s) for s in selected), reverse=True):
        if 0 <= iid < len(collection):
            collection.pop(iid)
    persist_collection()
    refresh_collection_view()

def apply_collection_filter(event=None):
    # Stub: future implementation will filter the Treeview rows.
    field = filter_field_var.get()
    text = filter_text_var.get().strip()
    print(f"Filter stub — Field: {field}, Text: '{text}' (not implemented)")

def clear_collection_filter():
    filter_field_var.set("Name")
    filter_text_var.set("")
    refresh_collection_view()
            
#=================================================================================================#
# INITIALIZE WINDOW ==============================================================================#
root = Tk()
root.geometry('1280x720')
root.title("Pokemon Card Manager")

filter_field_var = StringVar(master=root, value="Name")
filter_text_var = StringVar(master=root, value="")

#root frame
main_frame = Frame(root)

#double nested frame start screen
start = Frame(main_frame)

title = Label(start,text="Welcome to the Pokemon Card Manager")
##put it top left aka 0,0 w means left justified, 20 pad top 10 bottom, 12 on sides
title.grid(row=0, column=0, sticky='w', pady=(20, 10), padx=12)

add_button = Button(start,
                    text="ADD CARD",
                    width=12,
                    command=show_add
                   )

add_button.grid(row=0, column=1, sticky='e', padx=12)

filter_frame = Frame(start)
filter_frame.grid(row=1, column=0, columnspan=2, sticky='we', padx=12, pady=(5, 16))

filter_label = Label(filter_frame, text="Filter:")
filter_label.grid(row=0, column=0, padx=(0, 8), sticky='w')

filter_field = ttk.Combobox(filter_frame,
                            values=filter_field_options,
                            textvariable=filter_field_var,
                            state="readonly",
                            width=12,
                            justify="center")
filter_field.grid(row=0, column=1, padx=(0, 8))

filter_entry = Entry(filter_frame,
                     textvariable=filter_text_var,
                     width=24,
                     highlightthickness=0,
                     )
filter_entry.grid(row=0, column=2, padx=(0, 8))
filter_entry.bind("<Return>", apply_collection_filter)

filter_btn = Button(filter_frame,
                    text="FILTER",
                    command=apply_collection_filter)
filter_btn.grid(row=0, column=3, padx=(0, 6))

clear_btn = Button(filter_frame,
                   text="CLEAR",
                   command=clear_collection_filter)
clear_btn.grid(row=0, column=4)


columns = ("Name", "Set", "Rarity", "Market Value")
collection_tree = ttk.Treeview(start, columns=columns, show="headings", height=20)
for col in columns:
    collection_tree.heading(col, text=col)
    collection_tree.column(col, anchor='w', width=140)
collection_tree.grid(row=2, column=0, columnspan=2, padx=(12, 0), sticky='nsew')



total_value_lbl = Label(start,text="Total Value: $0.00")
total_value_lbl.grid(row=3, column=0, sticky='w', padx=12, pady=12)

remove_btn = Button(start,
                    text="REMOVE SELECTED",
                    command=remove_selected)

remove_btn.grid(row=3, column=1, sticky='e', padx=12, pady=12)

add = Frame(main_frame)

entry_lb = Label(add,text="Enter TCGplayer ID or Card Name")
entry_lb.grid(row=1, column=0, padx=5)

entry = Entry(add,
              width=15,
              highlightthickness=0)
entry.grid(row=1, column=1)
entry.bind("<Return>", add_card)

entry_search = Button(add,
                      text="ADD",
                      width=6,
                      command=add_card
                     )

entry_search.grid(row=1, column=2)

back_btn = Button(add,
                  text="BACK",
                  command=show_start)
back_btn.grid(row=0, column=0, sticky='w', padx=10, pady=10)

save_btn = Button(add,
                  text="SAVE TO COLLECTION",
                  command=save_current_card)

save_btn.grid(row=0, column=2, sticky='e', padx=10, pady=10)

pokemon_image = Label(add,
                      image=photo,
                     ) 
pokemon_image.grid(row=2, column=0, columnspan=3)

pokemon_name = Label(add,
                     text=f"",
                    )
pokemon_name.grid(row=3, column=0, columnspan=3)

pokemon_type = Label(add,
                     text=f""
                    )
pokemon_type.grid(row=4, column=0, columnspan=3)

pokemon_rarity = Label(add,
                       text=f""
                      )
pokemon_rarity.grid(row=5, column=0, columnspan=3)

pokemon_market = Label(add,
                       text=f"",
                      )
pokemon_market.grid(row=6, column=0, columnspan=3)

main_frame.pack(fill=BOTH, expand=True)
pages = [start, add]


buttons_frame = Frame(root)
buttons_frame.pack()

load_collection()
show_start()
refresh_collection_view()
root.mainloop()
