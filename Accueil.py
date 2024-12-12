from tkinter import *  # Importation des modules nécessaires pour l'interface graphique
from PIL import Image, ImageTk  # Importation de PIL pour gérer les images
import time
import random
from Game import Game  # Importation de la classe Game pour lancer le jeu

class Accueil:
    def __init__(self):
        # Initialisation de la fenêtre principale (Tkinter)
        self.window = Tk()
        self.window.title("Space Invaders")  # Titre de la fenêtre
        self.window.overrideredirect(True)  # Retirer la barre de titre de la fenêtre
        self.screen_width = self.window.winfo_screenwidth()  # Largeur de l'écran
        self.screen_height = self.window.winfo_screenheight()  # Hauteur de l'écran
        self.window.geometry(f"{self.screen_width}x{self.screen_height}")  # Adapter la taille de la fenêtre à la taille de l'écran
        self.window.config(bg="black")  # Définir un fond noir pour la fenêtre

    def lancer_jeu(self):
        """Masque l'écran d'accueil et lance le jeu"""
        # Masquer les widgets actuels de la fenêtre d'accueil
        for widget in self.window.winfo_children():
            widget.destroy()

        # Créer un canvas (zone de dessin) pour afficher le jeu
        canvas = Canvas(self.window, width=self.screen_width, height=self.screen_height, bg="black")
        canvas.pack()  # Ajouter le canvas à la fenêtre
        game = Game(self.window, canvas, self.screen_width, self.screen_height)  # Création d'une instance de la classe Game
        game.run()  # Lancer le jeu

    def afficher_regles(self):
        """Affiche les règles du jeu dans une fenêtre distincte"""
        regles_fenetre = Toplevel(self.window)  # Créer une nouvelle fenêtre
        regles_fenetre.title("Règles du jeu")  # Titre de la fenêtre
        regles_fenetre.geometry("600x600+100+100")  # Dimensions de la fenêtre
        regles_fenetre.config(bg="#1c1c1c")  # Fond sombre pour la fenêtre des règles
        
        # Tente d'ajouter une icône pour les règles
        try:
            img = Image.open("img/rules_icon.png")  # Charger une image pour l'icône
            img = img.resize((80, 80))  # Redimensionner l'image
            img_tk = ImageTk.PhotoImage(img)
            img_label = Label(regles_fenetre, image=img_tk, bg="#1c1c1c")  # Ajouter l'image dans la fenêtre
            img_label.image = img_tk  # Référence pour ne pas perdre l'image
            img_label.pack(pady=20)
        except FileNotFoundError:
            print("Image des règles non trouvée.")  # Gestion des erreurs si l'image n'existe pas

        # Titre des règles
        regles_title = Label(
            regles_fenetre,
            text="Règles du Jeu",
            font=("Helvetica", 24, "bold"),
            fg="white",
            bg="#1c1c1c",
        )
        regles_title.pack(pady=10)  # Ajouter le titre dans la fenêtre

        # Description détaillée des règles avec un texte stylé
        regles_label = Label(
            regles_fenetre,
            text=("Le but est de tuer tous les aliens.\n\nSi les aliens franchissent la ligne rouge, c'est perdu !\n"
                  "Attention, vous n'avez que 3 vies et les aliens tirent.\nMoins ils sont nombreux, plus ils tirent vite !\n\n"
                  "Score :\n10 points pour la première ligne,\n20 points pour la deuxième,\netc.\n\n"
                  "Touches :\n- Espace : Tirer\n- Entrée : Commencer la partie\n- Flèche gauche/droite : Se déplacer\n- P : Pause\n\n"
                  "Conseil : Éliminez les aliens du bas et sur les côtés pour les ralentir."),
            font=("Helvetica", 14),
            fg="white",
            bg="#1c1c1c",
            justify="left",
            padx=20, pady=10,
            wraplength=500
        )
        regles_label.pack(pady=20)  # Ajouter les règles

        # Bouton pour fermer la fenêtre des règles
        bouton_fermer = Button(
            regles_fenetre,
            text="Fermer",
            command=regles_fenetre.destroy,
            font=("Helvetica", 14),
            bg="#ff5733",
            fg="white",
            relief=RAISED
        )
        bouton_fermer.pack(pady=20)

    def afficher_accueil(self):
        """Affiche l'écran d'accueil avec les boutons 'Jouer', 'Règles' et 'Quitter'"""
        accueil_frame = Frame(self.window, bg="black", width=8000, height=6000)  # Créer un cadre pour l'écran d'accueil
        accueil_frame.pack_propagate(False)  # Empêcher la modification automatique de la taille du cadre
        accueil_frame.pack(fill="both", expand=True)  # Remplir toute la fenêtre avec ce cadre

        # Titre du jeu
        label = Label(
            accueil_frame,
            text="Bienvenue dans Space Invaders",
            font=("Helvetica", 24),
            fg="white",
            bg="black",
        )
        label.pack(pady=50)  # Positionner le texte au centre

        # Bouton pour lancer le jeu
        bouton_jouer = Button(
            accueil_frame,
            text="    Jouer    ",
            font=("Helvetica", 30),
            bg="Blue",
            fg="white",
            command=self.lancer_jeu,  # Lancer le jeu
        )
        bouton_jouer.pack(pady=50)

        # Bouton pour afficher les règles
        bouton_regles = Button(
            accueil_frame,
            text="Règles du jeu",
            font=("Helvetica", 30),
            bg="blue",
            fg="white",
            command=self.afficher_regles,  # Afficher les règles
        )
        bouton_regles.pack(pady=50)

        # Bouton pour quitter l'application
        bouton_quitter = Button(
            accueil_frame,
            text="    Quitter    ",
            font=("Helvetica", 30),
            bg="Blue",
            fg="white",
            command=self.window.destroy,  # Quitter l'application
        )
        bouton_quitter.pack(pady=50)

        self.window.mainloop()  # Démarrer la boucle principale de l'application
