from tkinter import *
from tkinter import messagebox
import json
from pprint import pprint


# TODO: implement search function ... and the rest lol

mycardlist = {}

class MyGui:
    def __init__(self, master): # master is the 'main' window in this case, passed in as root
        cardlist_F = Frame(master, bg='red')  # define frame in the main window (normally root, but is now master)
        cardlist_F.grid(row=0, column=0, rowspan=3, sticky=NSEW)
        cardimage_F = Frame(master, bg='blue')
        cardimage_F.grid(row=0, column=1, columnspan=2)
        carddatalabels_F = Frame(master, bg='purple')
        carddatalabels_F.grid(row=1, column=1)
        carddata_F = Frame(master, bg='yellow')
        carddata_F.grid(row=1, column=2)
        carddesc_F = Frame(master, bg='green')
        carddesc_F.grid(row=2, column=1, columnspan=2)

    # Objects for cardframe
        self.deckname_L = Label(cardlist_F, text='Current Deck')
        self.deckname_L.grid(row=0, column=0, columnspan=2)

        self.cardlist_LB = Listbox(cardlist_F)
        self.cardlist_LB.grid(row=1, column=0, columnspan=2, sticky=NSEW)
        self.populatedeck()
        self.cardlist_LB.bind("<<ListboxSelect>>", self.updateselectedcarddata)

        # TODO: add save command
        self.loaddeck_B = Button(cardlist_F, text='Load')
        self.loaddeck_B.grid(row=2, column=0)

        # TODO: add load command
        self.savedeck_B = Button(cardlist_F, text='Save')
        self.savedeck_B.grid(row=2, column=1)

    # Objects for carddetails
        self.cardname_var = StringVar()
        self.cardname_L = Label(cardimage_F, textvariable=self.cardname_var)
        self.cardname_L.grid(row=0, column=0, columnspan=2)


        # TODO: Change this to first item selected
        self.cardpicture_I = PhotoImage(file='images\Molten Giant.png')
        self.cardpicture_L = Label(cardimage_F, image=self.cardpicture_I)
        self.cardpicture_L.grid(row=1, column=0, columnspan=2)

    # Objects for card data labels
        self.cardtype_L = Label(carddatalabels_F, text='Type: ')
        self.cardtype_L.grid(row=0, column=1)

        self.cardclass_L = Label(carddatalabels_F, text='Class: ')
        self.cardclass_L.grid(row=1, column=1)

        self.cardattack_L = Label(carddatalabels_F, text='Attack: ')
        self.cardattack_L.grid(row=2, column=1)

        self.cardhealth_L = Label(carddatalabels_F, text='Health: ')
        self.cardhealth_L.grid(row=3, column=1)

        self.cardcost_L = Label(carddatalabels_F, text='Cost: ')
        self.cardcost_L.grid(row=4, column=1)

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

    # Card description frame
        self.carddescription_var = StringVar()
        self.carddescription_L = Label(carddesc_F, textvariable=self.carddescription_var)
        self.carddescription_L.grid(row=5, column=1, columnspan=2)

    # TODO: populate deck card list
    def populatedeck(self):
        with open('deck1.json') as data_file:
            data = json.loads(data_file.read())
            
        for card in data:
            self.cardlist_LB.insert(END, card)
        
        global mycardlist
        mycardlist = data
        # pprint(data['Aberration']['attack']) '1'
        
        
    def updateselectedcarddata(self, event):
        try:
            currentselection = self.cardlist_LB.get(self.cardlist_LB.curselection())
            print(currentselection)
            self.cardname_var.set(currentselection)
            self.cardtype_var.set(mycardlist[currentselection]['type'])
            self.cardclass_var.set(mycardlist[currentselection]['class'])
            self.cardattack_var.set(mycardlist[currentselection]['attack'])
            self.cardhealth_var.set(mycardlist[currentselection]['health'])
            self.cardcost_var.set(mycardlist[currentselection]['cost'])
            self.carddescription_var.set(mycardlist[currentselection]['description'])
            self.img = PhotoImage(file="images\\"+str(currentselection)+'.png')
            self.cardpicture_L.configure(image = self.img)
            
        except Exception as e:
            print('ERROR: ' + str(e))
            
        
   




'''
    # Make a main menu at the top
        self.menu = Menu(master)
        master.config(menu=self.menu)

    # Define each menu option
        self.subMenu = Menu(self.menu)  # define menu
        self.menu.add_cascade(label='File', menu=self.subMenu) # create dropdown submenu in main menu bar
        self.subMenu.add_command(label='Open')  # add option to dropdown submenu
        self.subMenu.add_separator() # add separator line to drop down menu
        self.subMenu.add_command(label='Exit', command=master.quit) # add option to dropdown submenu

        self.editMenu = Menu(self.menu) # define menu
        self.menu.add_cascade(label='edit', menu=self.editMenu) # create dropdown editmenu in main menu bar
        self.editMenu.add_command(label='yoza') # add option to dropdown edit menu

    # define labels
        self.name_L = Label(frame, text='Username')
        self.name_L.grid(row=0, column=0)
        self.pass_L = Label(frame, text='Password')
        self.pass_L.grid(row=1, column=0)

    # define entries (textbox)
        self.entry_u = Entry(frame)
        self.entry_u.grid(row=0, column=1)
        self.entry_p = Entry(frame)
        self.entry_p.grid(row=1, column=1)

    # define buttons
        self.submit_B = Button(frame, text='Submit', command=self.loginMsg) # command = function to be called when clicked
        self.submit_B.grid(row=2, column=0, sticky=E)   # stick to the East
        self.quit_B = Button(frame, text='Quit', command=frame.quit)
        self.quit_B.grid(row=2, column=1)

    # add content to toolbar
        self.toolbar_B = Button(toolbar, text='Toolbar', command=self.toolbarPrint)
        self.toolbar_B.grid()

    # define status bar at the bottom
        self.status_L = Label(master, text='Preparing for nothing...', bd=1, relief=SUNKEN, anchor=W)    # bd = border size, sunken = sunken into screen, anchor WEST
        self.status_L.grid()

    # define and render a photo
        self.photo = PhotoImage(file='Ok-icon.png')
        self.photo_L = Label(frame, image=self.photo)
        self.photo_L.grid()

    # Listbox
        self.listbox = Listbox(frame)
        self.listbox.grid()

        self.listbox.insert(END, "a list entry")

        for item in ["one", "two", "three", "four"]:
            self.listbox.insert(END, item)

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


    def loginMsg(self):
        print('You have successfully logged in')

    def toolbarPrint(self):
        print('Toolbar :)')
'''
######END OF MYGUI CLASS######


def main():
    root = Tk()
    root.title("PyGuiTest")
    b = MyGui(root)  # create class, passing in root (which is called master in the class)
    root.mainloop()

if __name__ == "__main__":  # allows program to be imported as a module by not automatically running
    main()
