import tkinter as tk
import random

### We want to implement the laser function "reset speed when reached top" from Laser 1.2
### But for to make our testing easier, we will keep at max speed for now.

# ------------------ GUI class and methods ----------------

class Main:

    def __init__(self):
        self.mainWin = tk.Tk()

        self.canvas = tk.Canvas(self.mainWin, width=640, height=800, bg="black")
        self.canvas.grid(row=0, column=0)

        self.shooter = self.canvas.create_rectangle(0, 0, 40, 20,
                                                    fill="lightgreen")
        self.canvas.move(self.shooter, 320, 700)

        # Shooter Move Controls
        self.mainWin.bind("<a>", self.moveCallback)
        self.mainWin.bind("<d>", self.moveCallback)
        self.mainWin.bind("<Left>", self.moveCallback)
        self.mainWin.bind("<Right>", self.moveCallback)

        # Shooter Laser Controls
        self.laser = self.canvas.create_rectangle(0, 0, 5, 20, fill="lightgreen")

        self.mainWin.bind("<Return>", self.laserCallback)

        # Invaders
        self.invader1 = self.canvas.create_rectangle(10, 30, 30, 50, fill="red", tag="1")
        self.invader2 = self.canvas.create_rectangle(70, 30, 90, 50, fill="red", tag="2")
        self.invader3 = self.canvas.create_rectangle(130, 30, 150, 50, fill="red", tag="3")
        self.invader4 = self.canvas.create_rectangle(190, 30, 210, 50, fill="red", tag="4")
        self.invader5 = self.canvas.create_rectangle(250, 30, 270, 50, fill="red", tag="5")
        self.invader6 = self.canvas.create_rectangle(310, 30, 330, 50, fill="red", tag="6")

        self.aliveInvaders = [self.invader1, self.invader2, self.invader3, self.invader4, self.invader5, self.invader6]
        self.deadInvaders = []

        self.invaderMove()

    def moveCallback(self, event):
        (x1, y1, x2, y2) = self.canvas.coords(self.shooter)

        if x1 > 0 and event.keysym == "a":
            self.canvas.move(self.shooter, -10, 0)  # Max 28 steps to the right
        elif x2 < 640 and event.keysym == "d":
            self.canvas.move(self.shooter, 10, 0)  # Max 32 steps to the left
        elif x1 > 0 and event.keysym == "Left":
            self.canvas.move(self.shooter, -10, 0)
        elif x2 < 640 and event.keysym == "Right":
            self.canvas.move(self.shooter, 10, 0)
        else:
            pass

    def laserCallback(self, event):
        if event.keysym == "Return":
            # self.mainWin.after_cancel(self.laserAuto())
            self.canvas.delete(self.laser)
            (x1, y1, x2, y2) = self.canvas.coords(self.shooter)
            laserInitX = (x1 + x2) / 2
            laserInitY = y1 - 20    # Make sure the laser isn't touching the shooter initially.
            self.laser = self.canvas.create_rectangle(0, 0, 5, 20, fill="lightgreen")
            self.canvas.move(self.laser, laserInitX, laserInitY)
            self.laserAuto()

    # I tried to fix this, the laser gets faster and faster because after function has no after.cancel method. I couldn't fix.
    def laserAuto(self):
        self.canvas.move(self.laser, 0, -10)
        self.checkShotInvader()                            # Moved checkShotInvader() and if's below, from invaderAuto to laserAuto.
        if self.checkShotInvader == True:                  # checkShotInvader wasn't functioning in some cases, probably because
            self.canvas.delete(self.laser)          # checkShotInvader was only called everytime the invader was moving.
            #self.canvas.create_text(320, 400, text="HIT!", fill="yellow", font="Arial 50", anchor=tk.CENTER)

            # self.canvas.after(200, self.canvas.delete(hit))
        t1 = self.mainWin.after(100, self.laserAuto)
        return t1

    def checkShotInvader(self):
        (x1, y1, x2, y2) = self.canvas.coords(self.laser)   # Causes error when laser is deleted upon shotdown
        shotObject = self.canvas.find_overlapping(x1, y1, x2, y2)   # On canvas, finding overlap with area (xy)
        if len(shotObject) > 1:     # canvas is constantly in "shotObject"
            for item in shotObject:
                if item in self.aliveInvaders:
                    self.canvas.delete(item)
                    self.aliveInvaders.remove(item)
                    self.deadInvaders.append(item)
        return True

    # This move function moves the entire row of invaders, it's pretty cool
    def invaderMove(self):
        for i in self.aliveInvaders:
            (x1, y1, x2, y2) = self.canvas.coords(i)
            if x1 <= 640:
                self.canvas.move(i, 10, 0)
            # index = self.aliveInvaders.index(i)
            # if x1 > 640:
            #     self.aliveInvaders[index] = self.canvas.create_rectangle((10, (y1 + 100), (30, (y2 + 100))),
            #                                                                  fill="red", tag="1")
        self.invaderLaserShoot()
        self.canvas.after(200, self.invaderMove)

    def invaderLaserShoot(self):
        yesnoList = ["Yep", "Nope", "Nope", "Nope"]
        randomYesNo = random.choice(yesnoList)
        if randomYesNo == "Yep":
            # print("yep")
            randomInvader = random.choice(self.aliveInvaders)
            (x11, y11, x22, y22) = self.canvas.coords(randomInvader)
            invaderLaserInitX = (x11 + x22) / 2
            invaderLaserInitY = y11 + 20    # Make sure the laser isn't touching the shooter initially.
            self.invaderLaser = self.canvas.create_rectangle(0, 0, 5, 20, fill="red")
            self.canvas.move(self.invaderLaser, invaderLaserInitX, invaderLaserInitY)
            self.invaderLaserAuto()
        else:
            # print("nope")
            pass

    def invaderLaserAuto(self):
        (x11, y11, x22, y22) = self.canvas.coords(self.invaderLaser)
        if y22 < 800:
            self.canvas.move(self.invaderLaser, 0, 10)
        self.checkShotShooter()  # Moved checkShotInvader() and if's below, from invaderAuto to laserAuto.
        if self.checkShotShooter == True:  # checkShotInvader wasn't functioning in some cases, probably because
            self.canvas.delete(self.invaderLaser)
        self.mainWin.after(100, self.invaderLaserAuto)

    def checkShotShooter(self):
        (x11, y11, x22, y22) = self.canvas.coords(self.invaderLaser)  # Causes error when laser is deleted upon shotdown
        shotObject = self.canvas.find_overlapping(x11, y11, x22, y22)  # On canvas, finding overlap with area (xy)
        if len(shotObject) > 1:  # canvas is constantly in "shotObject"
            if self.shooter in shotObject:
                return True
        else:
            pass

    def run(self):
        self.mainWin.mainloop()

    def exit(self):
        self.mainWin.destroy()


# ------------------ Main program ----------------------

myGui = Main()
myGui.run()