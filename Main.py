from Accueil import Accueil
from Game import Game 
from Player import Player
from Alien import Alien
from AlienFleet import AlienFleet
import random
from tkinter import *
import os
from PIL import Image, ImageTk


if __name__ == "__main__":
    jeu = Accueil()
    jeu.afficher_accueil()