from tkinter import *
from PIL import Image, ImageTk
import time
import random
from Game import Game

class Accueil:
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
        """Affiche une fenêtre avec les règles du jeu de manière stylée."""
        # Créer une nouvelle fenêtre (Toplevel)
        regles_fenetre = Toplevel(self.window)
        regles_fenetre.title("Règles du jeu")
        regles_fenetre.geometry("600x600+100+100")
        regles_fenetre.config(bg="#1c1c1c")
        
        # Ajouter une image en haut
        try:
            img = Image.open("img/rules_icon.png")  # Remplacez par une icône si vous en avez une
            img = img.resize((80, 80))  # Redimensionner l'image
            img_tk = ImageTk.PhotoImage(img)
            img_label = Label(regles_fenetre, image=img_tk, bg="#1c1c1c")
            img_label.image = img_tk  # Garder une référence à l'image
            img_label.pack(pady=20)
        except FileNotFoundError:
            print("Image des règles non trouvée.")
        
        # Titre des règles
        regles_title = Label(
            regles_fenetre,
            text="Règles du Jeu",
            font=("Helvetica", 24, "bold"),
            fg="white",
            bg="#1c1c1c",
        )
        regles_title.pack(pady=10)

        # Description des règles avec du texte stylé
        regles_label = Label(
            regles_fenetre,
            text=(
                "Le but est de tuer tous les aliens.\n\n"
                "Si les aliens franchissent la ligne rouge, c'est perdu !\n"
                "Attention, vous n'avez que 3 vies et les aliens tirent.\n"
                "Moins ils sont nombreux, plus ils tirent vite !\n\n"
                "Score :\n"
                "10 points pour la première ligne,\n"
                "20 points pour la deuxième,\n"
                "etc.\n\n"
                "Touches :\n"
                "- Espace : Tirer\n"
                "- Entrée : Commencer la partie\n"
                "- Flèche gauche/droite : Se déplacer\n"
                "- P : Pause\n\n"
                "Conseil : Éliminez les aliens du bas et sur les côtés pour les ralentir."
            ),
            font=("Helvetica", 14),
            fg="white",
            bg="#1c1c1c",
            justify="left",
            padx=20, pady=10,
            wraplength=500
        )
        regles_label.pack(pady=20)

        # Bouton fermer
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
