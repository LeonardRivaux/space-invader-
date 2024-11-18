from tkinter import *
import random
import math
import os
from PIL import Image, ImageTk



window =Tk()
window.title("Space Invaders")
window.overrideredirect(True)
window.geometry(str(window.winfo_screenwidth())+"x"+str(window.winfo_screenheight()))
window.config(bg="black")

#menubar
menubar = Menu(window)
menuoption = Menu(menubar, tearoff=0)
menuoption.add_command(label = "Quitter", command= window.destroy)
menubar.add_cascade(label="Option", menu= menuoption)

window.config(menu=  menubar)

# Canvas pour le jeu
canvas = Canvas(window, width=window.winfo_screenwidth(), height=window.winfo_screenheight(), bg="black")
canvas.pack()

#joueur
current_dir = os.path.dirname(__file__)  # Dossier contenant le script
image_path = os.path.join(current_dir, "spaceship.png")
player_image = Image.open(image_path)  # Remplacez par le nom de votre image
player_image = player_image.resize((70, 70))  # Ajuster la taille si nécessaire
player_photo = ImageTk.PhotoImage(player_image)

# Ajouter le joueur (image)
player = canvas.create_image(window.winfo_screenwidth()*0.5, window.winfo_screenheight()*0.9, image=player_photo)

player_speed = 20
player_x_min = 25  # Limite gauche
player_x_max = window.winfo_screenwidth() - 25  # Limite droite

bullet_speed = 10
bullets = []

#ajouter aliens
alien_images = []
for i in range(1, 6):  # Supposons que les images sont nommées alien1.jpg à alien6.jpg
    alien_path = os.path.join(current_dir, f"alien{i}.jpg")
    alien_image = Image.open(alien_path).resize((80, 80))  # Ajustez la taille si nécessaireN
    alien_images.append(ImageTk.PhotoImage(alien_image))

# Ajouter les aliens en 5 lignes de 11 colonnes
aliens = []
start_x, start_y = window.winfo_screenwidth()*0.2, window.winfo_screenheight()*0.2  # Position de départ pour les aliens
x_offset, y_offset = 100, 100  # Espacement horizontal et vertical

for row in range(5):  # 5 lignes
    alien_row = []
    for col in range(11):  # 11 colonnes
        x = start_x + col * x_offset
        y = start_y + row * y_offset
        alien = canvas.create_image(x, y, image=alien_images[row])
        alien_row.append(alien)
    aliens.append(alien_row)



# Mouvement du joueur
def move_left(event):
    x, y = canvas.coords(player)
    if x > player_x_min:
        canvas.move(player, -player_speed, 0)

def move_right(event):
    x, y = canvas.coords(player)
    if x < player_x_max:
        canvas.move(player, player_speed, 0)

def shoot(event):
    x, y = canvas.coords(player)
    bullet = canvas.create_rectangle(x - 2, y - 10, x + 2, y, fill="red")  # Créer un rectangle rouge
    bullets.append(bullet)
    move_bullet(bullet)

# Déplacement des tirs
def move_bullet(bullet):
    if canvas.coords(bullet)[1] > 0 or 1==1:  # Si le tir est encore dans l'écran
        canvas.move(bullet, 0, -bullet_speed)
        window.after(20, move_bullet, bullet)
    else:
        canvas.delete(bullet)  # Supprimer le tir lorsqu'il sort de l'écran
        bullets.remove(bullet)

# Liaison des touches du clavier
window.bind("<Left>", move_left)
window.bind("<Right>", move_right)
window.bind("<space>", shoot)

window.mainloop()