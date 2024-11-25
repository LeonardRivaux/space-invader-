import os
from PIL import Image, ImageTk
from Alien import Alien
from random import random


class AlienFleet:

    def __init__(self, game):
        self.game = game
        self.canvas = game.canvas
        self.bullets = []
        # Charger les images des aliens
        self.alien_images = self.load_alien_images()

        # Position initiale et configuration de la grille
        self.start_x = game.screen_width * 0.15
        self.start_y = game.screen_height * 0.1
        self.x_offset = game.screen_width * 0.07
        self.y_offset = game.screen_height * 0.08

        # Créer les aliens
        self.aliens = self.create_fleet()

    def load_alien_images(self):
        """Charge les images pour les aliens."""
        alien_images = []
        for i in range(1, 7):
            path = os.path.join(os.path.dirname(__file__), f"alien{i}.png")
            alien_image = Image.open(path).resize((80, 80))
            alien_images.append(ImageTk.PhotoImage(alien_image))
        return alien_images

    def create_fleet(self):
        """Crée une grille d'aliens."""
        aliens = []
        for row in range(6):
            alien_row = []
            for col in range(11):
                x = self.start_x + col * self.x_offset
                y = self.start_y + row * self.y_offset
                alien = Alien(self.game, x, y, self.alien_images[row], 60 - (10 * row))
                alien_row.append(alien)
            aliens.append(alien_row)  # Ajouter la ligne complète à la liste des aliens
        return aliens
    
    def remove_alien(self, alien):
        """Supprime un alien de la grille."""
        # Parcourir la grille des aliens et supprimer l'alien trouvé
        for row in self.aliens:
            if alien in row:
                row.remove(alien)  # Enlever l'alien de la liste de la ligne
                self.canvas.delete(alien.alien)  # Supprimer l'alien du canvas
                break
    
    def select_random_alien(self):
        """Sélectionne un alien aléatoire qui peut tirer."""
        living_aliens = [alien for row in self.aliens for alien in row if alien is not None]
        if living_aliens:
            return random.choice(living_aliens)
        return None

    def remove_alien_bullet(self, bullet):
        """Supprime un bullet d'alien."""
        if bullet in self.bullets:
            self.bullets.remove(bullet)