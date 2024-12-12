# Initialisation et démarrage
from tkinter import *
import os
from PIL import Image, ImageTk
import time
from Bullet import Bullet
from Game import *
class Player: 
    def __init__(self, game):
        self.game = game
        self.canvas = game.canvas
        self.image_dir = "image_dir"
        self.image = self.load_image("spaceship.png", (100, 100))
        self.life = self.load_image("life.png", (30, 30))
        self.vie = 3

        # Position initiale
        self.x = self.game.screen_width * 0.5
        self.y = self.game.screen_height * 0.88 
        self.speed = 20
        self.player = self.canvas.create_image(self.x, self.y, image=self.image)


        self.life1 = self.canvas.create_image(self.game.screen_width * 0.93 , self.game.screen_height * 0.960, image=self.life)
        self.life2 = self.canvas.create_image(self.game.screen_width * 0.93 + 40, self.game.screen_height * 0.960, image=self.life)
        self.life3 = self.canvas.create_image(self.game.screen_width * 0.93 + 80, self.game.screen_height * 0.960, image=self.life)

        # Limites de déplacement
        self.x_min = 25
        self.x_max = self.game.screen_width - 25

        # Liste des tirs
        self.bullets = []

        #cooldown
        self.last_shot_time = 0
        self.cooldown = 500  # en millisecondes
        

    def load_image(self, filename, size):
        # Construire le chemin absolu de l'image
        image_path = os.path.join(os.path.dirname(__file__),"img", filename)
        # Charger et redimensionner l'image
        img = Image.open(image_path)
        img = img.resize(size)
        return ImageTk.PhotoImage(img)

    def move_left(self, event):
        if self.game.pause ==0 and self.game.over==False:
            if self.x > self.x_min:
                self.canvas.move(self.player, -self.speed, 0)
                self.x -= self.speed
            

    def move_right(self, event):
        if self.game.pause ==0 and self.game.over==False:
            if self.x < self.x_max:
                self.canvas.move(self.player, self.speed, 0)
                self.x += self.speed
            

    def shoot(self, event):
        current_time = int(time.time() * 1000)  # Temps actuel en millisecondes
        if current_time - self.last_shot_time >= self.cooldown:
            bullet = Bullet(self.game, self.x, self.y - 20, 20)
            self.bullets.append(bullet)
            self.last_shot_time = current_time  # Met à jour l'heure du dernier tir

    def remove_bullet(self, bullet):
        """Supprime le bullet de la liste des tirs et du canvas."""
        self.bullets.remove(bullet)  # Retirer le bullet de la liste des bullets
        self.canvas.delete(bullet.bullet)  # Supprimer le bullet du canvas