from tkinter import *
from random import *
from datetime import *
import pickle
dtoday = datetime.today()
today = date(dtoday.year, dtoday.month, dtoday.day)

class HouseKeeper:
    def __init__(self, name, prevWorkDate, priority):
        self.name = name
        self.prevWorkDate = prevWorkDate
        self.priority = priority
class AllHouseKeepers:
    def __init__(self, housekeepers):
        self.housekeepers = housekeepers
    def addHouseKeeper(self, name):
        housekeeper = HouseKeeper(name, "00/00/00", 0)
        self.housekeepers.append(housekeeper)



class TitleBanner(Label):
    def __init__(self, master):
        Label.__init__(self, master, text = "Housekeeping Assigner",
                       font = ("times", 45, "italic"), anchor = W,
                       bg = "brown3", fg = "goldenrod1", relief = GROOVE)

class HousekeeperList(Frame):
    def __init__(self, master, alpha):
        Frame.__init__(self, master, bg = "brown3")
        self.alpha = alpha
        self.activeHousekeepers = self.alpha.allHouseKeepers
        self.list = self.generateList()
        self.generateButtons()
        
    def remove(self):
        name = self.nameEntry.get()
        for hk in self.list:
            if hk["text"] == name:
                self.list.remove(hk)
                for h in self.activeHousekeepers:
                    if h.name == name:
                        self.activeHousekeepers.remove(h)
                        break
                hk.destroy()
                break
        self.redraw()
        
    def add(self):
        name = self.nameEntry.get()
        newHK = HouseKeeper(name, today, 0)
        self.list.append(Button(self, command = self.moveToActive(newHK),
                                    text = name, width = 20, height = 3))
        self.activeHousekeepers.append(newHK)
        self.redraw()

    def generateList(self):
        HKButtons = []
        for hk in self.activeHousekeepers:
            txt = hk.name
            HKButtons.append(Button(self, command = self.moveToActive(hk),
                                    text = txt, width = 20, height = 3))
        r = 0
        for button in HKButtons:
            button.grid(row = r, column = 0, sticky = E+W, columnspan = 2, pady = 3)
            r += 1
        return HKButtons

    def redraw(self):
        for button in self.list:
            button.grid_forget()
        r = 0
        for button in self.list:
            button.grid(row = r, column = 0, sticky = E+W, columnspan = 2, pady = 3)
            r += 1

        self.nameEntry.grid_forget()
        self.addButton.grid_forget()
        self.remButton.grid_forget()
        r = len(self.list)
        self.nameEntry.grid(row = r, column = 0, columnspan = 2, pady = 3)
        self.addButton.grid(row = r+1, column = 0, sticky = S+W, pady = 3)
        self.remButton.grid(row = r+1, column = 1, sticky = S+E, pady = 3)

    def generateButtons(self):
        r = len(self.list)
        self.nameEntry = Entry(self, width = 18, justify = CENTER)
        self.addButton = Button(self, command = self.add, text = "ADD", width = 10, height = 3)
        self.remButton = Button(self, command = self.remove, text = "REM", width = 10, height = 3)
        self.nameEntry.grid(row = r, column = 0, columnspan = 2, pady = 3)
        self.addButton.grid(row = r+1, column = 0, sticky = S+W, pady = 3)
        self.remButton.grid(row = r+1, column = 1, sticky = S+E, pady = 3)

    def moveToActive(self, hk):
        def LAMBDA():
            self.alpha.orderingActivity.add(hk)
        return LAMBDA

class HousekeeperLister(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, bg = "brown3")
        self.alpha = master
        self.list = HousekeeperList(self, self.alpha)
        self.add = self.list.add
        self.remove = self.list.remove
        self.list.grid(row = 0, column = 0)

class OrderList(Frame):
    def __init__(self, master, alpha):
        self.alpha = alpha
        self.master = master
        self.activeHousekeepers = []
        self.list = []
        for r in range(8):            
            ph = Button(self.master, height = 3, width = 1)
            ph.grid(row = r, column = 0, pady = 3)
            ph.lower()
        autoOrder = Button(self.master, command = self.autoOrder, text = "Auto Order",
                                width = 20, height = 3)
        autoOrder.grid(row = 8, column = 0, pady = 3, padx = 20)
        self.autoOrder = autoOrder

        phLabel = Label(self.master, height = 1, width = 45)
        phLabel.grid(row = 10, column = 1)
        phLabel.lower()

        GO = Button(self.master, command = self.GO, text = "GO!",
                                width = 20, height = 3)
        GO.grid(row = 8, column = 2, pady = 3, padx = 20)
        self.GO = GO
        
    def GO(self):
        self.alpha.GO(self.activeHousekeepers)

    def add(self, hk):
        if hk in self.activeHousekeepers: return 
        newButton = Button(self.master, command = self.moveToInactive(hk),
                                text = hk.name, width = 20, height = 3)
        self.list.append(newButton)
        self.activeHousekeepers.append(hk)
        self.redraw()

    def remove(self, hk):
        for button in self.list:
            if button['text'] == hk.name:
                self.list.remove(button)
                button.destroy()
                break
        self.activeHousekeepers.remove(hk)
        self.redraw()

    def redraw(self):
        for button in self.list:
            button.grid_forget()
        r = 0
        for button in reversed(self.list):
            button.grid(row = r, column = 1, pady = 3, padx = 20)
            r += 1


    def buttonPriority(self, button):
        for hk in self.activeHousekeepers:
            if button["text"] == hk.name:
                return hk.priority

    def hkPriority(self, hk):
        return hk.priority
    
    def autoOrder(self):
        self.list.sort(key = self.buttonPriority, reverse = True)
        self.activeHousekeepers.sort(key = self.hkPriority, reverse = True)
        self.redraw()

    def moveToInactive(self, name):
        def LAMBDA():
            self.alpha.orderingActivity.remove(name)
        return LAMBDA

class HousekeeperOrderer(Frame):
    def __init__(self, master):
        file_name = "bg" + str(randint(1, 2)) + ".gif"
        self.photo = PhotoImage(file = file_name)
        Frame.__init__(self, master, width = 750, height = 700)
        self.grid_propagate(0)
        self.bg_label = Label(self, image = self.photo)
        self.bg_label.place(x = 0, y = 0, relwidth = 1, relheight = 1)
        self.alpha = master
        self.list = OrderList(self, self.alpha)
        self.add = self.list.add
        self.remove = self.list.remove
        

class HKGUI(Frame):
    def __init__(self, master, allHouseKeepers): 
        Frame.__init__(self, master, bg = "brown3")
        self.root = master
        self.allHouseKeepers = allHouseKeepers
        self.programBanner = TitleBanner(self)
        self.housekeeperList = HousekeeperLister(self)
        self.orderingActivity = HousekeeperOrderer(self)
        self.activeHousekeepers = []
        for x in range(5):
            self.grid_columnconfigure(x, weight = 1)
            self.grid_rowconfigure(x, weight = 1)
        self.programBanner.grid(row = 0, column = 0, columnspan = 2, sticky = W+E+N+S)
        self.housekeeperList.grid(row = 1, column = 0, sticky = N+W+E)
        self.orderingActivity.grid(row = 1, column = 1, sticky = N+W+E)

    def GO(self, activeHousekeepers):
        self.activeHousekeepers = activeHousekeepers
        self.root.destroy()

def launchHKGUI(ahk):
    window = Tk()
    w = 900
    h = 700
    ws = window.winfo_screenwidth() 
    hs = window.winfo_screenheight() 
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    window.geometry('%dx%d+%d+%d' % (w, h, x, y))
    program = HKGUI(window, ahk)
    program.grid(row = 0, column = 0, sticky = W+E+N+S)
    window.mainloop()
    return program
