from tkinter import *
from tkinter import messagebox
import os
from PIL import Image, ImageTk
import time
import random

class SpaceInvadersGame:
    def __init__(self):
        # Initialisation de la fenêtre principale
        self.window = Tk()
        self.window.title("Space Invaders")
        self.window.overrideredirect(True)
        self.screen_width = self.window.winfo_screenwidth()
        self.screen_height = self.window.winfo_screenheight()
        self.window.geometry(f"{self.screen_width}x{self.screen_height}")
        self.window.config(bg="black")

    def lancer_jeu(self):
        """Affiche le jeu après avoir masqué la fenêtre d'accueil."""
        # Masquer les widgets de l'accueil
        for widget in self.window.winfo_children():
            widget.destroy()

        # Créer et lancer le jeu
        canvas = Canvas(self.window, width=self.screen_width, height=self.screen_height, bg="black")
        canvas.pack()
        game = Game(self.window, canvas, self.screen_width, self.screen_height)
        game.run()

    def afficher_regles(self):
        """Affiche une fenêtre avec les règles du jeu."""
        # Créer une nouvelle fenêtre (Toplevel)
        regles_fenetre = Toplevel(self.window)
        regles_fenetre.title("Règles du jeu")
        regles_fenetre
        regles_fenetre.geometry("400x300+50+350")
        regles_fenetre.config(bg="black")
    
    # Ajouter un texte pour les règles
        regles_label = Label(
            regles_fenetre,
            text=(
                "           Bienvenue dans Space Invaders !\n\n"
                "-  Utilisez les flèches gauche et droite pour vous déplacer.\n"
                "- Appuyez sur Espace pour tirer.\n"
                "- Éliminez tous les aliens pour gagner.\n"
                "- Attention à leurs tirs !"
            ),
            font=("Helvetica", 12),
            justify="left",
            bg="white",
            wraplength=380
        )
        regles_label.pack(pady=20, padx=20)

    # Bouton pour fermer la fenêtre
        bouton_fermer = Button(
            regles_fenetre,
            text="Fermer",
            command=regles_fenetre.destroy,
            font=("Helvetica", 12),
            bg="red",
            fg="white"
        )
        bouton_fermer.pack(pady=10)



    def afficher_accueil(self):
        """Affiche une fenêtre d'accueil avec un bouton 'Jouer'."""
        accueil_frame = Frame(self.window, bg="black", width=8000, height=6000)
        accueil_frame.pack_propagate(False)
        accueil_frame.pack(fill="both", expand=True)

        label = Label(
            accueil_frame,
            text="Bienvenue dans Space Invaders",
            font=("Helvetica", 24),
            fg="white",
            bg="black",
        )
        label.pack(pady=50)
        
     

        bouton_jouer = Button(
            accueil_frame,
            text="    Jouer    ",
            font=("Helvetica", 30),
            bg="Blue",
            fg="white",
            command=self.lancer_jeu,  # Appel à la fonction pour afficher le jeu
        )
        bouton_jouer.pack(pady=50)

        bouton_regles = Button(
            accueil_frame,
            text="Règles du jeu",
            font=("Helvetica", 30),
            bg="blue",
            fg="white",
            command=self.afficher_regles,  # Appel à la méthode afficher_regles
        )
        bouton_regles.pack(pady=50)

        bouton_quitter = Button(
            accueil_frame,
            text="    Quitter    ",
            font=("Helvetica", 30),
            bg="Blue",
            fg="white",
            command=self.window.destroy,
        )
        bouton_quitter.pack(pady=50)


        self.window.mainloop()


class Game:
    def __init__(self, window, canvas, screen_width, screen_height):
        self.window = window
        self.canvas = canvas
        self.screen_width = screen_width
        self.screen_height = screen_height


        # Canvas pour le jeu
        self.canvas = canvas
        self.canvas.pack()

        #image press start 
        image_path = os.path.join(os.path.dirname(__file__), "pressstart.jpg")  # Remplacez par le nom de votre image
        image = Image.open(image_path).resize((500, 500))  # Redimensionner si nécessaire
        self.center_image = ImageTk.PhotoImage(image)
       

        # Calculer la position centrale
        center_x = self.screen_width / 2
        center_y = self.screen_height / 1.5

        
        # Ajouter l'image au canvas
        self.center_image_id = self.canvas.create_image(center_x, center_y, image=self.center_image)
        
        #score 
        self.score = 0  # Score initialself
        self.score_text = self.canvas.create_text(10, self.screen_height*0.95 , text="Score: 0", anchor="w", fill="white", font=("Arial", 20))

        #fin
        self.over = False

        # Initialisation des entités du jeu
        self.player = Player(self)
        self.alien_fleet = AlienFleet(self)
        
        #quitter
        self.window.bind("<Escape>",self.leave)
        
        #entrer pour lancer
        self.window.bind("<Return>",self.start)
        self.start = 0

        #mainloop
        self.window.mainloop()



    def start(self, event=None):
        if self.start == 0:

            # Lancer les tirs des aliens après l'initialisation complète
            self.canvas.delete(self.center_image_id)
            self.start_alien_shooting()
            # Lier les commandes clavier
            self.run()
            self.bind_keys()
            self.start = 1

    def update(self):

        if self.over:  # Vérifie si le jeu est terminé
            return
        """Fonction qui met à jour l'état du jeu (vérifie les collisions, etc.)."""
        # Vérifier les collisions bullet joueur alien
            # Vérifier les collisions entre les bullets du joueur et les aliens
        for bullet in self.player.bullets[:]:
            bullet.update()  # Mise à jour de la position du bullet
            if bullet.y < 0:  # Si le bullet sort du haut de l'écran
                self.player.remove_bullet(bullet)  # Supprimer le bullet
            else:
                # Vérifier les collisions avec les aliens
                for row in self.alien_fleet.aliens:
                    for alien in row:
                        if self.check_collision(bullet, alien):
                            self.score += alien.score
                            self.update_score_display()
                            self.handle_collision(bullet, alien)
                            break

        # Vérifier les collisions entre les bullets des aliens et le joueur
        for bullet in self.alien_fleet.bullets[:]:
            bullet.update()
            if bullet.y > self.screen_height:  # Si le bullet sort du bas de l'écran
                self.alien_fleet.remove_alien_bullet(bullet)  # Supprimer le bullet
                self.canvas.delete(bullet)
            else:
                if self.check_collision(bullet, self.player):  # Vérifier collision avec le joueur
                    self.score -= 100
                    self.update_score_display()
                    self.handle_collision(bullet, "coeur")
                    break

        
        # Mettre à jour le jeu toutes les 30ms
        
        self.canvas.after(30, self.update)


    def check_collision(self, bullet, entity):
        if isinstance(entity, Player):
            # Cas spécial pour la collision avec le joueur
            entity_coords = self.canvas.coords(entity.player)
            if not entity_coords:
                return False
            entity_x, entity_y = entity_coords
            entity_width = 100  # La largeur de votre image de joueur
            entity_height = 100  # La hauteur de votre image de joueur
            entity_x1 = entity_x - entity_width / 2
            entity_y1 = entity_y - entity_height / 2
            entity_x2 = entity_x + entity_width / 2
            entity_y2 = entity_y + entity_height / 2
        else:
            # Collision avec un alien
            entity_coords = self.canvas.coords(entity.alien)
            if not entity_coords:
                return False
            entity_x, entity_y = entity_coords
            entity_width = entity.image.width()
            entity_height = entity.image.height()
            entity_x1 = entity_x - entity_width / 2
            entity_y1 = entity_y - entity_height / 2
            entity_x2 = entity_x + entity_width / 2
            entity_y2 = entity_y + entity_height / 2

    # Récupérer les coordonnées du bullet
        bullet_coords = self.canvas.coords(bullet.bullet)
        if not bullet_coords:
            return False
        bullet_x1, bullet_y1, bullet_x2, bullet_y2 = bullet_coords

    # Détecter la collision (vérifier si le bullet est dans les coordonnées de l'entité)
        if (bullet_x2 >= entity_x1 and bullet_x1 <= entity_x2 and bullet_y2 >= entity_y1 and bullet_y1 <= entity_y2):
            return True
        return False

    def handle_collision(self, bullet, alien):
        """Gère la collision : supprime l'alien et le bullet."""
        if alien == "coeur":
            if self.player.vie == 1:
                self.canvas.delete(self.player.life1)
                self.player.vie = 0
                self.over = True
                image_path = os.path.join(os.path.dirname(__file__), "gameover.png")  # Remplacez par le nom de votre image
                image = Image.open(image_path).resize((300, 300))  # Redimensionner si nécessaire
                self.center_image = ImageTk.PhotoImage(image)
                self.center_image_id = self.canvas.create_image(self.screen_width / 2, self.screen_height / 2, image=self.center_image)
            if self.player.vie == 2:
                self.canvas.delete(self.player.life2)
                self.player.vie = 1
            if self.player.vie == 3:
                self.canvas.delete(self.player.life3)
                self.player.vie = 2
            self.alien_fleet.remove_alien_bullet(bullet)
            self.canvas.delete(bullet.bullet)
        else:
            # Supprimer l'alien et le bullet du canvas
            self.alien_fleet.remove_alien(alien)
            self.player.remove_bullet(bullet)
            

    def update_score_display(self):
        """Met à jour l'affichage du score."""
        self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")

    def bind_keys(self):
        """Associe les touches du clavier aux actions du joueur."""
        self.window.bind("<Left>", self.player.move_left)
        self.window.bind("<Right>", self.player.move_right)
        self.window.bind("<space>", self.player.shoot)

    def run(self):
        if not self.over:
            self.update()
        else:
            return

    def start_alien_shooting(self):
        """Fait tirer les aliens toutes les 2 secondes."""
        if self.over:  # Vérifie si le jeu est terminé
            return
        self.shoot_alien_bullet()
        self.canvas.after(700, self.start_alien_shooting)  # Répète toutes les 2 secondes

    def shoot_alien_bullet(self):
        """Tire un bullet depuis un alien aléatoire."""
        alien = alien = self.alien_fleet.select_random_alien()
        if alien:
            bullet = Bullet(self, alien.x, alien.y + 20, -10)  # Position sous l'alien
            self.alien_fleet.bullets.append(bullet)

    def leave(self, event=None):
        self.window.destroy()
class Player: 
    def __init__(self, game):
        self.game = game
        self.canvas = game.canvas
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
        current_time = int(time.time() * 1000)  # Temps actuel en millisecondes
        if current_time - self.last_shot_time >= self.cooldown:
            bullet = Bullet(self.game, self.x, self.y - 20, 20)
            self.bullets.append(bullet)
            self.last_shot_time = current_time  # Met à jour l'heure du dernier tir

    def remove_bullet(self, bullet):
        """Supprime le bullet de la liste des tirs et du canvas."""
        self.bullets.remove(bullet)  # Retirer le bullet de la liste des bullets
        self.canvas.delete(bullet.bullet)  # Supprimer le bullet du canvas
class Bullet:
    def __init__(self, game, x, y, speed):
        self.game = game
        self.canvas = game.canvas
        self.x = x
        self.y = y
        self.speed = speed
        self.bullet = self.canvas.create_rectangle(x - 2, y - 10, x + 2, y, fill="red")

        self.last_move_time = 0
        self.cooldown_move = 50  # en millisecondes
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

    def update(self):
        if self.bullet:
            self.canvas.move(self.bullet, 0, -self.speed)  # Déplace le bullet vers le haut
            self.y -= self.speed  # Met à jour la position Y du bullet
            

class Alien:
    def __init__(self, game, x, y, image, score):
        self.score = score
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



# Initialisation et démarrage
if __name__ == "__main__":
    jeu = SpaceInvadersGame()
    jeu.afficher_accueil()

   