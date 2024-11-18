import tkinter as tk
import random
from PIL import Image, ImageTk
import os


# Configuration de la fenêtre principale
window = tk.Tk()
window.title("Space Invader")
window.geometry("600x600")
window.resizable(False, False)

# Canvas pour le jeu
canvas = tk.Canvas(window, width=600, height=600, bg="black")
canvas.pack()

# Variables de contrôle
player_speed = 15
enemy_speed = 5
bullet_speed = 10

# Liste des ennemis et des tirs
enemies = []
bullets = []

# Création des ennemis
for i in range(5):  # 5 ennemis
    x = random.randint(50, 550)
    y = random.randint(50, 150)
    enemy = canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill="red")
    enemies.append(enemy)

# Mouvement du joueur
def move_left(event):
    if canvas.coords(player)[0] > 0:
        canvas.move(player, -player_speed, 0)

def move_right(event):
    if canvas.coords(player)[2] < 600:
        canvas.move(player, player_speed, 0)

# Tirs du joueur
def shoot(event):
    x1, y1, x2, y2 = canvas.coords(player)
    bullet = canvas.create_rectangle(x1 + 20, y1 - 10, x2 - 20, y1, fill="yellow")
    bullets.append(bullet)

# Mouvement des ennemis
def move_enemies():
    for enemy in enemies:
        canvas.move(enemy, 0, enemy_speed)
        if canvas.coords(enemy)[3] >= 600:  # Si l'ennemi atteint le bas
            canvas.coords(enemy, random.randint(50, 550), -20)

# Mouvement des tirs
def move_bullets():
    for bullet in bullets[:]:
        canvas.move(bullet, 0, -bullet_speed)
        if canvas.coords(bullet)[1] <= 0:
            canvas.delete(bullet)
            bullets.remove(bullet)

# Collision entre tirs et ennemis
def check_collisions():
    for bullet in bullets[:]:
        bullet_coords = canvas.coords(bullet)
        for enemy in enemies[:]:
            enemy_coords = canvas.coords(enemy)
            if (bullet_coords[2] > enemy_coords[0] and bullet_coords[0] < enemy_coords[2] and
                bullet_coords[3] > enemy_coords[1] and bullet_coords[1] < enemy_coords[3]):
                # Supprimer l'ennemi et le tir
                canvas.delete(bullet)
                canvas.delete(enemy)
                bullets.remove(bullet)
                enemies.remove(enemy)

# Mise à jour du jeu
def update_game():
    move_enemies()
    move_bullets()
    check_collisions()
    window.after(50, update_game)

# Liaisons clavier
window.bind("<Left>", move_left)
window.bind("<Right>", move_right)
window.bind("<space>", shoot)

# Lancement de la boucle du jeu
update_game()
window.mainloop()