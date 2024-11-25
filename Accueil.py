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