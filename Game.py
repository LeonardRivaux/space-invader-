#Header
'''Ce fichier implémente la mécanique principale du jeu. Il gère les interactions entre le joueur, les aliens, et les éléments de l'environnement. 
Ce programme :
Crée la fenêtre de jeu et le canvas pour l'affichage.
Gère les contrôles du joueur.
Création et gestion d'une flotte d'aliens avec des tirs aléatoires.
Vérifie et gère les collisions.
Gère les scores, les vies et les conditions de victoire ou de défaite.
Gère les événements de jeu : début, pause, fin.
Démarre et contrôle des animations, tirs et mouvements des entités.
Met à jour le jeu à intervalles réguliers (30ms) '''

import os
from PIL import Image, ImageTk
from random import random
from Player import *
from AlienFleet import *
from Bullet import *
import time


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
        image_path = os.path.join(os.path.dirname(__file__),"img", "pressstart.jpg")  
        image = Image.open(image_path).resize((500, 500))  # Redimensionner si nécessaire
        self.center_image = ImageTk.PhotoImage(image)
       
        # Ajouter une ligne à 4/5 de l'écran
        self.line_y = screen_height * 7 / 10
        self.line_id = self.canvas.create_line(
            0, self.line_y, screen_width, self.line_y, fill="red", width=2
        )

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
        self.fin = 0 
        # Initialisation des entités du jeu
        self.player = Player(self)
        self.alien_fleet = AlienFleet(self)
        
        #quitter
        self.window.bind("<Escape>",self.leave)
        
        #entrer pour lancer
        self.window.bind("<Return>",self.start)
        self.start = 0

        #pause
        self.window.bind("<p>",self.pause)
        self.pause = 0

        #time
        self.time = int(time.time() * 1000)  # Temps actuel en millisecondes

        #mainloop
        self.window.mainloop()



    def start(self, event=None):
        if self.start == 0:

            # Lancer les tirs des aliens après l'initialisation complète
            self.canvas.delete(self.center_image_id)
            self.start_alien_shooting()
            self.start_alien_movement()
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
        #verification victoire
        remaining_aliens = sum(len(row) for row in self.alien_fleet.aliens)
        if remaining_aliens == 0:  # Si aucune ligne n'a d'aliens restants
            self.victory()
        #verification défaite
        self.check_line_breach()

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
                image_path = os.path.join(os.path.dirname(__file__),"img", "gameover.png")  
                image = Image.open(image_path).resize((300, 300))  # Redimensionner si nécessaire
                self.center_image = ImageTk.PhotoImage(image)
                self.center_image_id = self.canvas.create_image(self.screen_width / 2, self.screen_height / 2, image=self.center_image)
                self.fin = 1
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

    def start_alien_movement(self):
        """Démarre le mouvement des aliens."""
        if not self.over and self.pause==0:  # Vérifie que le jeu n'est pas terminé
            self.alien_fleet.move_aliens()  # Déplace les aliens
        self.canvas.after(200, self.start_alien_movement)

    def shoot_alien_bullet(self):
        """Tire un bullet depuis un alien aléatoire."""
        alien = alien = self.alien_fleet.select_random_alien()
        if alien:
            bullet = Bullet(self, alien.x, alien.y + 20, -10)  # Position sous l'alien
            self.alien_fleet.bullets.append(bullet)

    def check_line_breach(self):
        """Vérifie si un alien dépasse la ligne rouge."""
        for row in self.alien_fleet.aliens:
            for alien in row:
                alien_coords = self.canvas.coords(alien.alien)
                if alien_coords and alien_coords[1] >= self.line_y:
                    self.player.vie = 0
                    self.over = True
                    image_path = os.path.join(os.path.dirname(__file__),"img", "gameover.png")  
                    image = Image.open(image_path).resize((300, 300))  # Redimensionner si nécessaire
                    self.center_image = ImageTk.PhotoImage(image)
                    self.center_image_id = self.canvas.create_image(self.screen_width / 2, self.screen_height / 2, image=self.center_image)
                    self.fin = 1

    def leave(self, event=None):
        self.window.destroy()
    
    def pause(self, event=None):
        current_time = int(time.time() * 1000)
        if self.fin == 1:
            return
        if current_time - self.time >= 2000:
            if self.pause == 0:
                self.over = True 
                count = 1
                image_path = os.path.join(os.path.dirname(__file__),"img", "pause.png")  
                image = Image.open(image_path).resize((300, 300))  # Redimensionner si nécessaire
                self.center_image = ImageTk.PhotoImage(image)
                self.center_image_id = self.canvas.create_image(self.screen_width / 2, self.screen_height / 2, image=self.center_image)
        if self.pause == 1:
            self.over = False
            count = 0
            self.canvas.delete(self.center_image_id)            
            self.update()
            self.time = int(time.time() * 1000)  # Temps actuel en millisecondes
            time.sleep(1)
            self.start_alien_shooting()

        self.pause = count

    def victory(self, event=None):
        self.over = True
        image_path = os.path.join(os.path.dirname(__file__),"img", "victory.jpg")  
        image = Image.open(image_path).resize((300, 300))  # Redimensionner si nécessaire
        self.center_image = ImageTk.PhotoImage(image)
        self.center_image_id = self.canvas.create_image(self.screen_width / 2, self.screen_height / 2, image=self.center_image)
        self.fin = 1




