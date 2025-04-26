# The virtual tabletop (until I figure out how to make a GUI)
# import os

# class Tabletop:
#     def __init__(self):
# Import the required libraries
from tkinter import *
from dice import Dice

root = Tk()
root.title("Technical Adventuring Companion")
root.geometry('400x500')
d20 = Dice(20)

result = Label(root, text="")
result.grid(column=1, row=0)

def roll():
    result.config(text=f"{d20.roll()}")
btn20 = Button(root, text="Roll d20", command=roll)
btn20.grid(column=0, row=0)

root.mainloop()