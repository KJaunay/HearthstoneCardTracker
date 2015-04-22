from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import pprint
import tkinter.font as tkfont
import json
import os

# TODO: Implement radio buttons to select/deselect each card :/
# TODO: Create list of 'current' cards
# TODO: Comment code
# TODO: Implement 'save' function
# TODO: Implement feature to detect changes and edits to cardlist
# TODO: Sort imported cards
# TODO: Add feature to build deck

# QTRL+Q (quick documentation)
# CTRL+SHIFT+ALT+N (quick find method)

# TODO: TODAYS OBJECTIVES
# ---------------COMPLETED-----------------------
#       Use PyCharm with Github
#       Debug error when loading deck - Turned out I wasn't clearing the deck in my 'new' open deck method
#       Implement 'Save As' Function
#       Implement 'New Deck' feature
# ---------------CURRENT-----------------------
#

mycardlist = {}

class MyGui:
    def __init__(self, master):  # master is the 'main' window in this case, passed in as root

        # Named Fonts
        # family: The font family name as a string.
        # size: The font height as an integer in points. To get a font n pixels high, use -n.
        # weight: "bold" for boldface, "normal" for regular weight.
        # slant: "italic" for italic, "roman" for unslanted.
        # underline: 1 for underlined text, 0 for normal.
        # overstrike: 1 for overstruck text, 0 for normal.



        self.cardlist_font = tkfont.Font(family='Helvetica', size=11, slant=tkfont.ITALIC, overstrike=1)
        self.datalabels_font = tkfont.Font(family='Courier New', size=8, weight=tkfont.BOLD)
        self.decktitle_font = tkfont.Font(family='MS Sans Serif', size=15, underline=1)
        self.carddesc_font = tkfont.Font(family='Verdana', size=10)

        cardlist_F = Frame(master, bg='red')  # define frame in the main window (normally root, but is now master)
        cardlist_F.grid(row=0, column=0, rowspan=3, sticky=NSEW, ipadx=20, ipady=20)

        cardimage_F = Frame(master, bg='blue')
        cardimage_F.grid(row=0, column=1, columnspan=2, ipadx=20, ipady=20)

        carddatalabels_F = Frame(master, bg='purple')
        carddatalabels_F.grid(row=1, column=1, sticky=NSEW)

        carddata_F = Frame(master, bg='yellow')
        carddata_F.grid(row=1, column=2, sticky=NSEW)

        carddesc_F = Frame(master, bg='green')
        carddesc_F.grid(row=2, column=1, columnspan=2, sticky=EW)

# -------------------------------------------------------------------------------------
    # Objects for main menu
        self.menu = Menu(master)  # Define a new menu item
        master.config(menu=self.menu)  # place new menu in window
    # Objects for file menu
        self.fileMenu = Menu(self.menu)  # Define new window
        self.menu.add_cascade(label='File', menu=self.fileMenu)  # Add new submenu to main menu
        self.fileMenu.add_command(label='New Deck', command=self.newdeck)
        self.fileMenu.add_command(label='Open Deck', command=self.opendeck)  # add options to dropdown menu
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label='Save Deck')
        self.fileMenu.add_command(label='Save Deck As ... ', command=self.savedeckas)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label='Exit', command=master.quit)
    # Objects for edit menu
        self.editMenu = Menu(self.menu)
        self.menu.add_cascade(label='Edit', menu=self.editMenu)
        self.editMenu.add_command(label='Force Update', command=self.notyetimplemented)
        self.editMenu.add_command(label='Clear Current Deck', command=self.clearcurrentdeck)
    # Objects for help menu
        self.helpMenu = Menu(self.menu)
        self.menu.add_cascade(label='Help', menu=self.helpMenu)
        self.helpMenu.add_command(label='How To')
        self.helpMenu.add_separator()
        self.helpMenu.add_command(label='About', command=self.aboutpopup)

# -------------------------------------------------------------------------------------
    # Objects for cardlist frame
        self.deckname_var = StringVar()
        self.deckname_L = Label(cardlist_F, textvariable=self.deckname_var)
        self.deckname_L.grid(row=0, column=0, columnspan=2)
        self.deckname_L.config(font=self.decktitle_font)

        self.searchvar = StringVar()
        self.searchvar.trace("w", lambda name, index, mode: self.searchcards())
        self.searchbox_E = Entry(cardlist_F, textvariable=self.searchvar)
        self.searchbox_E.grid(row=1, column=0, columnspan=2)
        self.searchbox_E.config(width=20)

        self.cardlist_LB = Listbox(cardlist_F)
        self.cardlist_LB.grid(row=2, column=0, columnspan=2, sticky=NSEW)
        self.cardlist_LB.bind("<<ListboxSelect>>", self.updateselectedcarddata)
        self.cardlist_LB.config(height=27, font=self.cardlist_font)

        self.decklist_SB = Scrollbar(cardlist_F, orient=VERTICAL)
        self.decklist_SB.config(command=self.cardlist_LB.yview)
        self.decklist_SB.grid(row=2, column=2, sticky=NS)

        self.cardlist_LB.config(yscrollcommand=self.decklist_SB.set)

        self.loaddeck_B = Button(cardlist_F, text='Load', command=self.opendeck)
        self.loaddeck_B.grid(row=3, column=0)

        # TODO: add save command
        self.savedeck_B = Button(cardlist_F, text='Save')
        self.savedeck_B.grid(row=3, column=1)

# -------------------------------------------------------------------------------------
    # Objects for carddetails
        self.cardname_var = StringVar()
        self.cardname_L = Label(cardimage_F, textvariable=self.cardname_var)
        self.cardname_L.grid(row=0, column=0, columnspan=2)
        self.cardname_L.config(font=self.decktitle_font)

        self.cardpicture_I = PhotoImage(file='')
        self.cardpicture_L = Label(cardimage_F, image=self.cardpicture_I)
        self.cardpicture_L.grid(row=1, column=0, columnspan=2)

# -------------------------------------------------------------------------------------
    # Objects for card data labels
        self.cardtype_L = Label(carddatalabels_F, text='Type: ')
        self.cardtype_L.grid(row=0, column=1)
        self.cardtype_L.config(font=self.datalabels_font)

        self.cardclass_L = Label(carddatalabels_F, text='Class: ')
        self.cardclass_L.grid(row=1, column=1)
        self.cardclass_L.config(font=self.datalabels_font)

        self.cardattack_L = Label(carddatalabels_F, text='Attack: ')
        self.cardattack_L.grid(row=2, column=1)
        self.cardattack_L.config(font=self.datalabels_font)

        self.cardhealth_L = Label(carddatalabels_F, text='Health: ')
        self.cardhealth_L.grid(row=3, column=1)
        self.cardhealth_L.config(font=self.datalabels_font)

        self.cardcost_L = Label(carddatalabels_F, text='Cost: ')
        self.cardcost_L.grid(row=4, column=1)
        self.cardcost_L.config(font=self.datalabels_font)

# -------------------------------------------------------------------------------------
    # Objects for current card data points
        self.cardtype_var = StringVar()
        self.cardtype = Label(carddata_F, textvariable=self.cardtype_var)
        self.cardtype.grid(row=0, column=3)

        self.cardclass_var = StringVar()
        self.cardclass = Label(carddata_F, textvariable=self.cardclass_var)
        self.cardclass.grid(row=1, column=3)

        self.cardattack_var = StringVar()
        self.cardattack = Label(carddata_F, textvariable=self.cardattack_var)
        self.cardattack.grid(row=2, column=3)

        self.cardhealth_var = StringVar()
        self.cardhealth = Label(carddata_F, textvariable=self.cardhealth_var)
        self.cardhealth.grid(row=3, column=3)

        self.cardcost_var = StringVar()
        self.cardcost = Label(carddata_F, textvariable=self.cardcost_var)
        self.cardcost.grid(row=4, column=3)

# -------------------------------------------------------------------------------------
    # Card description frame
        self.carddescription_var = StringVar()
        self.carddescription_L = Label(carddesc_F, textvariable=self.carddescription_var)
        self.carddescription_L.pack()
        self.carddescription_L.config(font=self.carddesc_font, wraplength=340, anchor=CENTER, justify=CENTER)

# -------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------
    def newdeck(self):
        # remove deck title replace with generic "deck%d*"
        self.deckname_var.set("New Deck*")
        # clear current cards in listbox
        self.cardlist_LB.delete(0, END)

    def savedeckas(self):

        savefile = filedialog.asksaveasfile(defaultextension='.JSON', mode='w')
        if savefile is None:  # If operation is 'canceled'
            return

        savefile.write(json.dumps(mycardlist))
        savefile.close()

    def opendeck(self):
        deckname = filedialog.askopenfilename(filetypes=(("JSON files", "*.json"), ("All files", "*.*")))
        selecteddeck = os.path.splitext(os.path.basename(deckname))[0].title()
        self.deckname_var.set(selecteddeck)

        with open(deckname) as data_file:
            data = json.loads(data_file.read())

        self.cardlist_LB.delete(0, END)  # Clear current cardlist

        for card in data:
            self.cardlist_LB.insert(END, card)

        global mycardlist
        mycardlist = data

        # selects first item in list
        self.cardlist_LB.select_set(0)
        self.cardlist_LB.event_generate("<<ListboxSelect>>")

    def clearcurrentdeck(self):
        self.cardlist_LB.delete(0, END)

    def searchcards(self):
        search_term = self.searchvar.get()
        file = open('deck1.json')
        datalist = json.loads(file.read())

        self.cardlist_LB.delete(0, END)  # Clear current cardlist

        for item in datalist:
            if search_term.lower() in item.lower():  # String.lower returns lowercase string
                self.cardlist_LB.insert(END, item)

    def updateselectedcarddata(self, event):
        try:
            currentselection = self.cardlist_LB.get(self.cardlist_LB.curselection())
            self.cardname_var.set(currentselection)
            self.cardtype_var.set(mycardlist[currentselection]['type'])
            self.cardclass_var.set(mycardlist[currentselection]['class'])
            self.cardattack_var.set(mycardlist[currentselection]['attack'])
            self.cardhealth_var.set(mycardlist[currentselection]['health'])
            self.cardcost_var.set(mycardlist[currentselection]['cost'])
            self.carddescription_var.set(mycardlist[currentselection]['description'])
            self.img = PhotoImage(file="images\\" + str(currentselection) + '.png')
            self.cardpicture_L.configure(image=self.img)
            
        except Exception as e:
            print("ERROR: {0}".format(e))

    def aboutpopup(self):
        about_name = '''Developed by Kieran Jaunay'''
        about_contact = '''Please contact k.jaunay@gmail.com with \nany questions or feedback'''
        popup = Tk()
        popup.geometry("300x120")
        popup.wm_title("About")
        name_L = Label(popup, text=about_name)
        name_L.pack(side="top", fill="x", pady=10)
        contact_L = Label(popup, text=about_contact)
        contact_L.pack(fill='x', pady=10)
        B1 = Button(popup, text="Close", command=popup.destroy)
        B1.pack(side="bottom")
        popup.mainloop()

    def notyetimplemented(self):
        questionpopup = messagebox.showinfo('Error', 'Feature not yet implemented')

# -------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------


'''
    # define popup message
        tkinter.messagebox.showinfo('some title', 'some content')

    # define popup with a yes/no question (title, question)
        questionpopup = tkinter.messagebox.askquestion('Question 124', 'Do you like food?')

        if questionpopup == 'yes':
            print('Yes')
        else:
            print('No? Wtf man... ')

    # draw stuff :3
        # define canvas to draw on
        canvas = Canvas(frame, width=200, height=100)
        # as with any other object you need to pack it into the frame
        canvas.grid()
        # define shapes you want to draw (beginning x,y, ending x,y)
        blackLine = canvas.create_line(0,0,200,50)
        redLine = canvas.create_line(0,100,200,50, fill='red')
        # Delete graphic object
        canvas.delete(redLine) #Using (ALL) deletes all objects on the canvas
'''



def main():
    root = Tk()
    root.title("PyGuiTest")
    root.geometry("650x650")
    #root.resizable(width=FALSE, height=FALSE)
    b = MyGui(root)  # create class, passing in root (which is called master in the class)
    root.mainloop()

if __name__ == "__main__":  # allows program to be imported as a module by not automatically running
    main()
