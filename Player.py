# Initialisation et démarrage
from tkinter import *
import os
from PIL import Image, ImageTk
import time
from Bullet import Bullet
from Game import *

class Player: 
    def __init__(self, game):
        # Initialisation du joueur
        self.game = game  # Référence à l'objet 'Game', pour accéder aux propriétés du jeu
        self.canvas = game.canvas  # Récupère le canvas du jeu où le joueur sera affiché
        self.image_dir = "image_dir"  # Dossier des images (chemin relatif)
        self.image = self.load_image("spaceship.png", (100, 100))  # Chargement de l'image du joueur (vaisseau spatial)
        self.life = self.load_image("life.png", (30, 30))  # Chargement de l'image représentant la vie du joueur
        self.vie = 3  # Le joueur commence avec 3 vies

        # Position initiale du joueur
        self.x = self.game.screen_width * 0.5  # Position horizontale centrée
        self.y = self.game.screen_height * 0.88  # Position verticale proche du bas de l'écran
        self.speed = 20  # Vitesse de déplacement du joueur
        self.player = self.canvas.create_image(self.x, self.y, image=self.image)  # Création de l'image du joueur sur le canvas

        # Affichage des vies restantes du joueur (en haut à droite de l'écran)
        self.life1 = self.canvas.create_image(self.game.screen_width * 0.93 , self.game.screen_height * 0.960, image=self.life)
        self.life2 = self.canvas.create_image(self.game.screen_width * 0.93 + 40, self.game.screen_height * 0.960, image=self.life)
        self.life3 = self.canvas.create_image(self.game.screen_width * 0.93 + 80, self.game.screen_height * 0.960, image=self.life)

        # Limites de déplacement du joueur (pour éviter de sortir de l'écran)
        self.x_min = 25  # Limite gauche
        self.x_max = self.game.screen_width - 25  # Limite droite

        # Liste des tirs du joueur
        self.bullets = []

        # Variables de cooldown pour limiter le taux de tir
        self.last_shot_time = 0  # Temps du dernier tir
        self.cooldown = 500  # Délai entre deux tirs en millisecondes

    def load_image(self, filename, size):
        """Charge une image, la redimensionne et la renvoie."""
        image_path = os.path.join(os.path.dirname(__file__), "img", filename)  # Crée le chemin absolu de l'image
        img = Image.open(image_path)  # Ouvre l'image
        img = img.resize(size)  # Redimensionne l'image
        return ImageTk.PhotoImage(img)  # Retourne l'image redimensionnée au format Tkinter

    def move_left(self, event):
        """Déplace le joueur à gauche."""
        if self.game.pause == 0 and self.game.over == False:  # Le jeu doit être en cours et non en pause
            if self.x > self.x_min:  # Vérifie si le joueur peut encore se déplacer vers la gauche
                self.canvas.move(self.player, -self.speed, 0)  # Déplace l'image du joueur
                self.x -= self.speed  # Met à jour la position du joueur

    def move_right(self, event):
        """Déplace le joueur à droite."""
        if self.game.pause == 0 and self.game.over == False:  # Le jeu doit être en cours et non en pause
            if self.x < self.x_max:  # Vérifie si le joueur peut encore se déplacer vers la droite
                self.canvas.move(self.player, self.speed, 0)  # Déplace l'image du joueur
                self.x += self.speed  # Met à jour la position du joueur

    def shoot(self, event):
        """Fait tirer le joueur."""
        current_time = int(time.time() * 1000)  # Temps actuel en millisecondes
        if current_time - self.last_shot_time >= self.cooldown:  # Vérifie si le cooldown est terminé
            bullet = Bullet(self.game, self.x, self.y - 20, 20)  # Crée un bullet juste au-dessus du joueur
            self.bullets.append(bullet)  # Ajoute le bullet à la liste des tirs
            self.last_shot_time = current_time  # Met à jour le temps du dernier tir

    def remove_bullet(self, bullet):
        """Supprime un bullet de la liste et du canvas."""
        self.bullets.remove(bullet)  # Retire le bullet de la liste
        self.canvas.delete(bullet.bullet)  # Supprime le bullet du canvas
