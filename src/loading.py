from tkinter import *
from random import *



class Loading(Toplevel):
    def __init__(self, master):
        Toplevel.__init__(self, master)
        self.master = master
        w = 275
        h = 250
        ws = self.winfo_screenwidth() 
        hs = self.winfo_screenheight() 
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.axes = Axes(self, w, h)
        self.axes.pack()
        self.loading()

    def loading(self):
        self.axes.loading()
        self.master.after(20, self.loading)

class Axes(Canvas):
    def __init__(self, master, w, h):
        Canvas.__init__(self, master, width = w, height = h, bg = "black")
        colorOptions = [["chartreuse2", "chartreuse2", "chartreuse2", "steelblue2", "steelblue2", "steelblue2"],
        ["slate blue", "slate blue", "brown1", "brown1", "gold", "gold"],
        ["hot pink", "purple1", "blue"]]
        colors = colorOptions[randint(0, len(colorOptions)-1)]
        self.width = w
        self.height = h
        #self.draw_axes()
        self.magicLines = []
        for i in range(50):
            self.magicLines.append(MagicLinePos(self, w, h, colors[i%len(colors)]))
            self.magicLines.append(MagicLineNeg(self, w, h, colors[i%len(colors)]))

    def draw_axes(self):
        self.create_line(self.width / 2, 0, self.width / 2, self.height)
        self.create_line(0, self.height / 2, self.width, self.height / 2)

    def loading(self):
        for line in self.magicLines:
            line.move()
        
class MagicLinePos():
    def __init__(self, canvas, w, h, color):
        self.canvas = canvas
        self.width = w
        self.height = h
        self.x = randint(0, int(self.width))
        zero = h // 2
        if self.x < zero:
            self.y = zero - self.x
        else:
            self.y = self.x - zero
        self.vel = randint(1, 2)
        self.xVel = self.vel
        self.yVel = self.vel
        self.model = canvas.create_line(self.x, self.height / 2,
                                       self.width / 2, self.y, fill = color)

    def move(self):
        if self.x < 0:
            self.xVel = self.vel
        if self.x > self.width:
            self.xVel = -1 * self.vel
        if self.y < 0:
            self.yVel = self.vel
        if self.y > self.height / 2:
            self.yVel = -1 * self.vel
        self.x += self.xVel
        self.y += self.yVel
        self.canvas.coords(self.model, self.x, self.height / 2,
                           self.width / 2, self.y)

class MagicLineNeg():
    def __init__(self, canvas, w, h, color):
        self.canvas = canvas
        self.width = w
        self.height = h
        self.x = randint(0, int(self.width))
        zero = h // 2
        if self.x < zero:
            self.y = zero + self.x
        else:
            self.y = self.x
        self.vel = randint(1, 2)
        self.xVel = self.vel
        self.yVel = self.vel
        self.model = canvas.create_line(self.x, self.height / 2,
                                       self.width / 2, self.y, fill = color)

    def move(self):
        if self.x < 0:
            self.xVel = self.vel
        if self.x > self.width:
            self.xVel = -1 * self.vel
        if self.y < self.height / 2:
            self.yVel = self.vel
        if self.y > self.height:
            self.yVel = -1 * self.vel
        self.x += self.xVel
        self.y += self.yVel
        self.canvas.coords(self.model, self.x, self.height / 2,
                           self.width / 2, self.y)


def loading():
    root = Tk()
    root.wm_title("Loading...")
    root.withdraw()
    p = Loading(root)
    root.mainloop()

if __name__ == "__main__":
    loading()
