from tkinter import *
import random
import math

window =Tk()
window.title("Space Invaders")
window.overrideredirect(True)
window.geometry(str(window.winfo_screenwidth())+"x"+str(window.winfo_screenheight()))
window.config(bg="black")


menubar = Menu(window)
menuoption = Menu(menubar, tearoff=0)
menuoption.add_command(label = "Quitter", command= window.destroy)
menubar.add_cascade(label="Option", menu= menuoption)

window.config(menu=  menubar)


window.mainloop()