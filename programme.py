from tkinter import *
import os
from PIL import Image, ImageTk

class Game:
    def __init__(self):
        # Initialisation de la fenêtre principale
        self.window = Tk()
        self.window.title("Space Invaders")
        self.window.overrideredirect(True)
        self.screen_width = self.window.winfo_screenwidth()
        self.screen_height = self.window.winfo_screenheight()
        self.window.geometry(f"{self.screen_width}x{self.screen_height}")
        self.window.config(bg="black")
        
        #menu en haut 
        #menubar
        menubar = Menu(self.window)
        menuoption = Menu(menubar, tearoff=0)
        menuoption.add_command(label = "Quitter", command= self.window.destroy)
        menubar.add_cascade(label="Option", menu= menuoption)

        self.window.config(menu=  menubar)

        # Canvas pour le jeu
        self.canvas = Canvas(self.window, width=self.screen_width, height=self.screen_height, bg="black")
        self.canvas.pack()

        # Initialisation des entités du jeu
        self.player = Player(self)
        self.alien_fleet = AlienFleet(self)

        # Lier les commandes clavier
        self.bind_keys()

    def bind_keys(self):
        """Associe les touches du clavier aux actions du joueur."""
        self.window.bind("<Left>", self.player.move_left)
        self.window.bind("<Right>", self.player.move_right)
        self.window.bind("<space>", self.player.shoot)

    def run(self):
        """Démarre le jeu."""
        self.window.mainloop()


class Player:
    def __init__(self, game):
        self.game = game
        self.canvas = game.canvas
        self.image = self.load_image("spaceship.png", (100, 100))

        # Position initiale
        self.x = self.game.screen_width * 0.5
        self.y = self.game.screen_height * 0.9
        self.speed = 20
        self.player = self.canvas.create_image(self.x, self.y, image=self.image)

        # Limites de déplacement
        self.x_min = 25
        self.x_max = self.game.screen_width - 25

        # Liste des tirs
        self.bullets = []

    def load_image(self, filename, size):
        """Charge et redimensionne une image."""
        path = os.path.join(os.path.dirname(__file__), filename)
        image = Image.open(path).resize(size)
        return ImageTk.PhotoImage(image)

    def move_left(self, event):
        """Déplace le joueur vers la gauche."""
        if self.x > self.x_min:
            self.canvas.move(self.player, -self.speed, 0)
            self.x -= self.speed

    def move_right(self, event):
        """Déplace le joueur vers la droite."""
        if self.x < self.x_max:
            self.canvas.move(self.player, self.speed, 0)
            self.x += self.speed

    def shoot(self, event):
        """Crée un tir depuis la position du joueur."""
        bullet = Bullet(self.game, self.x, self.y - 20)
        self.bullets.append(bullet)

class Bullet:
    def __init__(self, game, x, y):
        self.game = game
        self.canvas = game.canvas
        self.x = x
        self.y = y
        self.speed = 10
        self.bullet = self.canvas.create_rectangle(x - 2, y - 10, x + 2, y, fill="red")

        # Déplacer le tir
        self.move()

    def move(self):
        """Déplace le tir vers le haut."""
        if self.y > 0:
            self.canvas.move(self.bullet, 0, -self.speed)
            self.y -= self.speed
            self.canvas.after(20, self.move)
        else:
            self.canvas.delete(self.bullet)


class Alien:
    def __init__(self, game, x, y, image):
        self.game = game
        self.canvas = game.canvas
        self.x = x
        self.y = y
        self.image = image
        self.alien = self.canvas.create_image(x, y, image=self.image)


class AlienFleet:
    def __init__(self, game):
        self.game = game
        self.canvas = game.canvas

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
        for i in range(1, 6):
            path = os.path.join(os.path.dirname(__file__), f"alien{i}.jpg")
            alien_image = Image.open(path).resize((80, 80))
            alien_images.append(ImageTk.PhotoImage(alien_image))
        return alien_images

    def create_fleet(self):
        """Crée une grille d'aliens."""
        aliens = []
        for row in range(5):
            alien_row = []
            for col in range(11):
                x = self.start_x + col * self.x_offset
                y = self.start_y + row * self.y_offset
                alien = Alien(self.game, x, y, self.alien_images[row])
                alien_row.append(alien)
            aliens.append(alien_row)
        return aliens


# Lancer le jeu
if __name__ == "__main__":
    game = Game()
    game.run()
