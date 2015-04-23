from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import pprint
import tkinter.font as tkfont
import json
import os

# TODO: Implement functionality to keep track of number of each card
# TODO: Add visual of total num cards
# TODO: Create list of 'current' cards
# TODO: Comment code
# TODO: Implement 'save' function
# TODO: Implement feature to detect changes and edits to cardlist
# TODO: Sort imported cards
# TODO: Add functionality to shift buttons

# QTRL+Q (quick documentation)
# CTRL+SHIFT+ALT+N (quick find method)

# TODO: TODAYS OBJECTIVES
# ---------------COMPLETED-----------------------
#       Add feature to build deck
#           - Add two new frames to contain shift buttons and the ListBox - DONE
#           - Add new ListBox to act as new deck - DONE
#           - Add the four buttons to shift cards to and from new deck - DONE
#           - Change ListboxSelect event handler to detect which - DONE
#           - Created and called method to fill allcardlist and display it
# ---------------CURRENT-----------------------
#       Add Scrollbar to allcardlist


usercardlist = {}
allcardlist = {}


class MyGui:
    def __init__(self, master):  # master is the 'main' window in this case, passed in as root
        # Objects for main menu
        self.menu = Menu(master)  # Define a new menu item
        master.config(menu=self.menu)  # place new menu in window

        # Objects for file menu
        self.fileMenu = Menu(self.menu)  # Define new window
        self.menu.add_cascade(label='File', menu=self.fileMenu)  # Add new submenu to main menu
        self.fileMenu.add_command(label='New Deck', command=self.newdeck)
        self.fileMenu.add_command(label='Open Deck', command=self.loaddeck)  # add options to dropdown menu
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
        # Named Fonts
        # family: The font family name as a string.
        # size: The font height as an integer in points. To get a font n pixels high, use -n.
        # weight: "bold" for boldface, "normal" for regular weight.
        # slant: "italic" for italic, "roman" for unslanted.
        # underline: 1 for underlined text, 0 for normal.
        # overstrike: 1 for overstruck text, 0 for normal.
        self.cardlist_font = tkfont.Font(family='Helvetica', size=11, slant=tkfont.ITALIC)
        self.datalabels_font = tkfont.Font(family='Courier New', size=8, weight=tkfont.BOLD)
        self.decktitle_font = tkfont.Font(family='MS Sans Serif', size=15, underline=1)
        self.carddesc_font = tkfont.Font(family='Verdana', size=10)

# -------------------------------------------------------------------------------------
        completecardlist_F = Frame(master, bg='yellow')
        completecardlist_F.grid(row=0, column=0, padx=10, pady=10)

        # Search function entry
        self.searchvar = StringVar()
        self.searchvar.trace("w", lambda name, index, mode: self.searchcards())
        self.searchbox_E = Entry(completecardlist_F, textvariable=self.searchvar)
        self.searchbox_E.grid(row=0, column=0)
        self.searchbox_E.config(width=25)

        # All cards listbox
        self.allcards_LB = Listbox(completecardlist_F)
        self.allcards_LB.grid(row=5, column=0)
        self.allcards_LB.config(height=30, font=self.cardlist_font)
        self.allcards_LB.bind("<<ListboxSelect>>", lambda event, self=self, obj="allcards": self.updateselectedcarddata(event, obj))

        self.allcards_SB = Scrollbar(completecardlist_F, orient=VERTICAL)
        self.allcards_SB.grid(row=5, column=10, sticky=NS)
        self.allcards_SB.config(command=self.allcards_LB.yview)
        self.allcards_LB.config(yscrollcommand=self.allcards_SB.set)

# -------------------------------------------------------------------------------------
        shiftbuttons_F = Frame(master, bg='cyan')
        shiftbuttons_F.grid(row=0, column=5, padx=10, pady=10)

        # single right shift button
        self.shiftsingleright_B = Button(shiftbuttons_F, text='>')
        self.shiftsingleright_B.grid(row=0, column=0, sticky=EW, padx=5, pady=5)
        
        # single left shift button
        self.shiftsingleleft_B = Button(shiftbuttons_F, text='<')
        self.shiftsingleleft_B.grid(row=5, column=0, sticky=EW, padx=5, pady=5)

        # shift all right button
        self.shiftallright_B = Button(shiftbuttons_F, text='>>')
        self.shiftallright_B.grid(row=10, column=0, padx=5, pady=5)

        # shift all left button
        self.shiftallleft_B = Button(shiftbuttons_F, text='<<')
        self.shiftallleft_B.grid(row=15, column=0, padx=5, pady=5)

# -------------------------------------------------------------------------------------
        usercardlist_F = Frame(master, bg='blue')
        usercardlist_F.grid(row=0, column=10, padx=10, pady=10)

        # User deck title label
        self.userdeckname_var = StringVar()
        self.userdeckname_L = Label(usercardlist_F, textvariable=self.userdeckname_var)
        self.userdeckname_L.grid(row=0, column=0, columnspan=10)
        self.userdeckname_L.config(font=self.decktitle_font)

        # User deck card list listbox
        self.usercardlist_LB = Listbox(usercardlist_F)
        self.usercardlist_LB.grid(row=5, column=0, columnspan=10, sticky=NSEW)
        self.usercardlist_LB.config(height=30, font=self.cardlist_font)
        self.usercardlist_LB.bind("<<ListboxSelect>>", lambda event, self=self, obj=self.usercardlist_LB: self.updateselectedcarddata(event, obj))
        

        # User card list scrollbar
        self.usercardlist_SB = Scrollbar(usercardlist_F, orient=VERTICAL)
        self.usercardlist_SB.config(command=self.usercardlist_LB.yview)
        self.usercardlist_SB.grid(row=5, column=10, sticky=NS)
        self.usercardlist_LB.config(yscrollcommand=self.usercardlist_SB.set)

        # 'Load Deck' button
        self.loaduserdeck_B = Button(usercardlist_F, text='Load', command=self.loaddeck)
        self.loaduserdeck_B.grid(row=10, column=0, sticky=E, padx=30)

        # 'Save Deck' button
        self.saveuserdeck_B = Button(usercardlist_F, text='Save', command=self.loaddeck)
        self.saveuserdeck_B.grid(row=10, column=5, sticky=E)
        

# -------------------------------------------------------------------------------------
        carddetail_F = Frame(master, bg='red')
        carddetail_F.grid(row=0, column=15, padx=10, pady=10)

        # Card title label
        self.cardname_var = StringVar()
        self.cardname_L = Label(carddetail_F, textvariable=self.cardname_var)
        self.cardname_L.grid(row=0, column=0, columnspan=10)
        self.cardname_L.config(font=self.decktitle_font)

        # Card image label
        self.cardpicture_I = PhotoImage(file='')
        self.cardpicture_L = Label(carddetail_F, image=self.cardpicture_I)
        self.cardpicture_L.grid(row=5, column=0, columnspan=10)

        # Card type labels
        self.cardtype_L = Label(carddetail_F, text='Type: ')
        self.cardtype_L.grid(row=15, column=0)
        self.cardtype_L.config(font=self.datalabels_font)

        self.cardtype_var = StringVar()
        self.cardtype = Label(carddetail_F, textvariable=self.cardtype_var)
        self.cardtype.grid(row=15, column=5)

        # Card class labels
        self.cardclass_L = Label(carddetail_F, text='Class: ')
        self.cardclass_L.grid(row=20, column=0)
        self.cardclass_L.config(font=self.datalabels_font)

        self.cardclass_var = StringVar()
        self.cardclass = Label(carddetail_F, textvariable=self.cardclass_var)
        self.cardclass.grid(row=20, column=5)

        # Card attack labels
        self.cardattack_L = Label(carddetail_F, text='Attack: ')
        self.cardattack_L.grid(row=25, column=0)
        self.cardattack_L.config(font=self.datalabels_font)

        self.cardattack_var = StringVar()
        self.cardattack = Label(carddetail_F, textvariable=self.cardattack_var)
        self.cardattack.grid(row=25, column=5)

        # Card health labels
        self.cardhealth_L = Label(carddetail_F, text='Health: ')
        self.cardhealth_L.grid(row=30, column=0)
        self.cardhealth_L.config(font=self.datalabels_font)

        self.cardhealth_var = StringVar()
        self.cardhealth = Label(carddetail_F, textvariable=self.cardhealth_var)
        self.cardhealth.grid(row=30, column=5)

        # Card cost labels
        self.cardcost_L = Label(carddetail_F, text='Cost: ')
        self.cardcost_L.grid(row=35, column=0)
        self.cardcost_L.config(font=self.datalabels_font)

        self.cardcost_var = StringVar()
        self.cardcost = Label(carddetail_F, textvariable=self.cardcost_var)
        self.cardcost.grid(row=35, column=5)

        # Card description label
        self.carddescription_var = StringVar()
        self.carddescription_L = Label(carddetail_F, textvariable=self.carddescription_var)
        self.carddescription_L.grid(row=40, column=0, columnspan=10)
        self.carddescription_L.config(font=self.carddesc_font, wraplength=340, anchor=CENTER, justify=CENTER)

        self.fillcardlist()

# -------------------------------------------------------------------------------------
    def fillcardlist(self):
        file = open("cardlist.json", "r")
        filedump = json.loads(file.read())

        global allcardlist
        allcardlist = filedump

        self.allcards_LB.delete(0, END)

        for card in filedump:
            self.allcards_LB.insert(END, card)

        # selects first item in list
        self.allcards_LB.select_set(0)
        self.allcards_LB.event_generate("<<ListboxSelect>>")

    def newdeck(self):
        # remove deck title replace with generic "deck%d*"
        self.userdeckname_var.set("New Deck*")
        # clear current cards in listbox
        self.usercardlist_LB.delete(0, END)

    def savedeckas(self):

        savefile = filedialog.asksaveasfile(defaultextension='.JSON', mode='w')
        if savefile is None:  # If operation is 'canceled'
            return

        savefile.write(json.dumps(usercardlist))
        savefile.close()

    def loaddeck(self):
        deckname = filedialog.askopenfilename(filetypes=(("JSON files", "*.json"), ("All files", "*.*")))
        selecteddeck = os.path.splitext(os.path.basename(deckname))[0].title()
        self.userdeckname_var.set(selecteddeck)

        with open(deckname) as data_file:
            data = json.loads(data_file.read())

        self.usercardlist_LB.delete(0, END)  # Clear current cardlist

        for card in data:
            self.usercardlist_LB.insert(END, card)

        global usercardlist
        usercardlist = data

        # selects first item in list
        self.usercardlist_LB.select_set(0)
        self.usercardlist_LB.event_generate("<<ListboxSelect>>")

    def clearcurrentdeck(self):
        self.usercardlist_LB.delete(0, END)

    def searchcards(self):
        search_term = self.searchvar.get()
        file = open('cardlist.json')
        datalist = json.loads(file.read())

        self.allcards_LB.delete(0, END)  # Clear current cardlist

        for item in datalist:
            if search_term.lower() in item.lower():  # String.lower returns lowercase string
                self.allcards_LB.insert(END, item)

    def updateselectedcarddata(self, event, obj):
        # userlist allcards
        global allcardlist
        global usercardlist

        if obj == "allcards":
            listbox = self.allcards_LB
            listvar = allcardlist
        else:
            listbox = self.usercardlist_LB
            listvar = usercardlist

        try:
            currentselection = listbox.get(listbox.curselection())
            self.cardname_var.set(currentselection)
            self.img = PhotoImage(file="images\\" + str(currentselection) + '.png')
            self.cardpicture_L.configure(image=self.img)
            self.cardtype_var.set(listvar[currentselection]['type'])
            self.cardclass_var.set(listvar[currentselection]['class'])
            self.cardattack_var.set(listvar[currentselection]['attack'])
            self.cardhealth_var.set(listvar[currentselection]['health'])
            self.cardcost_var.set(listvar[currentselection]['cost'])
            self.carddescription_var.set(listvar[currentselection]['description'])
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
    root.geometry("800x650")
    #root.resizable(width=FALSE, height=FALSE)
    b = MyGui(root)  # create class, passing in root (which is called master in the class)
    root.mainloop()

if __name__ == "__main__":  # allows program to be imported as a module by not automatically running
    main()
