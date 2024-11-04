from tkinter import *
import random
import math

window =Tk()
window.title("Space Invaders")
window.overrideredirect(True)
window.geometry(str(window.winfo_screenwidth())+"x"+str(window.winfo_screenheight()))
window.config(bg="black")

buttonQuit = Button (window , text="Quitter", fg ="blue", command=window.destroy)
buttonQuit.pack()

window.mainloop()