from tkinter import *                               # import all files/code from tkinter library
root = Tk()                                         # instantiate Tkinter -> root
#=================================================================================================#

root.title("Pokemon Cards Inventory Manager")       # sets window title
#root.iconbitmap('temp.ico')                        # sets window icon (temporary)
root.geometry('500x500')                            # sets window size

# Following Lines is just to create a GUI  |  Organizing/Styling later
app_title = Label(root, text="Pokemon Cards Inventory Manager", font=(25))  # create label
app_title.pack(pady=20)                             # packs (place from top) label onto window

users_button = Button(root, text="USERS", font=(15))                        # create button
users_button.pack(pady=10)                          # packs (place from top) button onto window

#=================================================================================================#
root.mainloop()                                     # keep Tkinter running