# INITIALIZATIONS ================================================================================#
from tkinter import *                               # import all files/code from tkinter library
from control import *                               # link with control.py file
root = Tk()                                         # instantiate Tkinter -> root
#=================================================================================================#

# FUNCTIONS ======================================================================================#
def users_clicked():                                # CHANGE TO USERS PAGE
    print("Users clicked")                          # temp print

def market_clicked():                               # CHANGE TO MARKET PAGE
    print("Market clicked")                         # temp print

def search():                                       # (unfinished function) NEED ENTER KEY BINDING
    user_input = search_entry.get()                 # get text from textbox
    if(user_input):                                 # has text
        get_card_info(user_input)                   # input textfield into control.py function
#=================================================================================================#

# MAIN ===========================================================================================#
root.title("Pokemon Cards Inventory Manager")       # sets window title
#root.iconbitmap('temp.ico')                        # sets window icon (temporary)
root.geometry('500x500')                            # sets window size

frame = Frame(root)                                 # sets a frame (scenes)
frame.grid(row=0, column=0)                         # position of frame

# Following Lines is just to create a GUI  |  Organizing/Styling later
app_title = Label(frame, text="Pokemon Cards Inventory Manager", font=(25))         # create label
app_title.grid(row=0, column=0)                                                     # grid location 

users_button = Button(frame, text="USERS", command=users_clicked, font=(15))        # create button
users_button.grid(row=1, column=0)                                                  # grid location

market_button = Button(frame, text="MARKET", command=market_clicked,  font=(15))    # create button
market_button.grid(row=1, column=1)                                                 # grid location

search_entry = Entry(frame)                                                         # create textbox
search_entry.grid(row=1, column=2)                                                  # grid location
#=================================================================================================#

root.mainloop()                                     # keep Tkinter running