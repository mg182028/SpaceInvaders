from tkinter import *
import random
import time


tk = Tk()
tk.title("Ps Portion - Andrew")
tk.resizable(0, 0)
tk.wm_attributes("-topmost", 1)
canvas = Canvas(tk, width=500, height=500, bd=0, highlightthickness=0)
canvas.pack()
canvas.configure(background='pink')
tk.update()

class PlayerShip:
        
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.id = canvas.create_rectangle(0, 0, 28, 32, fill=color)
        self.canvas.move(self.id, 200, 375)
        self.x = 0
        self.canvas_width = self.canvas.winfo_width()
        self.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        self.canvas.bind_all('<KeyPress-Right>', self.turn_right)
        self.canvas.bind_all('<KeyPress-a>', self.turn_left)
        self.canvas.bind_all('<KeyPress-d>', self.turn_right)
        
    def turn_left(self, evt):
        pos = self.canvas.coords(self.id)
        if pos[0] > 0:
            self.x = -10
        
    def turn_right(self, evt):
        pos = self.canvas.coords(self.id)
        if pos[2] <= (self.canvas_width-10):
            self.x = 10

    def draw(self):
        self.canvas.move(self.id, self.x, 0)
        if self.canvas.bind_all('<KeyPress-Left>', self.turn_left) or self.canvas.bind_all('<KeyPress-a>', self.turn_left) :
            self.x = 0

PlayerShip = PlayerShip(canvas, 'purple')

while 1:
    PlayerShip.draw()
    tk.update_idletasks()
    time.sleep(0.001)
    tk.update()
 
