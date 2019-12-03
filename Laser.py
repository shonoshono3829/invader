import tkinter as tk

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


    def moveCallback(self, event):
        (x1, y1, x2, y2) = self.canvas.coords(self.shooter)

        if x1 > 0 and event.keysym == "a":
            self.canvas.move(self.shooter, -10, 0)  # Max 28 steps to the right
        elif x2 < 640 and event.keysym == "d":
            self.canvas.move(self.shooter, 10, 0)   # Max 32 steps to the left
        elif x1 > 0 and event.keysym == "Left":
            self.canvas.move(self.shooter, -10, 0)
        elif x2 < 640 and event.keysym == "Right":
            self.canvas.move(self.shooter, 10, 0)
        else:
            pass

    def laserCallback(self, event):
        if event.keysym == "Return":
            self.canvas.delete(self.laser)
            (x1, y1, x2, y2) = self.canvas.coords(self.shooter)
            laserInit = (x1 + x2) / 2
            self.laser = self.canvas.create_rectangle(0, 0, 5, 20, fill="lightgreen")
            self.canvas.move(self.laser, laserInit, y1)
        self.laserAuto()

    def laserAuto(self):
        self.canvas.move(self.laser, 0, -10)
        self.mainWin.after(100, self.laserAuto)

    def run(self):
        self.mainWin.mainloop()
# ------------------ Main program ----------------------

myGui = Main()
myGui.run()