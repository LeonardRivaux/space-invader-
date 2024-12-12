# Header
'''La classe Bullet gère les projectiles tirés par le joueur ou les aliens. 

Ce programme :
Initialise et affichage le projectile sur le canvas.
Gère le déplacement vertical du projectile.
Supprimme automatique le projectile lorsqu'il sort de l'écran.
Mets a jour la position du projectile'''


class Bullet:
    def __init__(self, game, x, y, speed):
        """
        Constructeur de la classe Bullet. Cette classe gère le tir de projectiles du joueur
        ou des aliens et leur déplacement.

        :param game: Référence à l'instance du jeu (pour accéder à l'écran de jeu et aux données de jeu)
        :param x: Position X initiale du tir
        :param y: Position Y initiale du tir
        :param speed: Vitesse à laquelle le tir se déplace (en pixels par frame)
        """
        self.game = game  # Référence à l'instance du jeu
        self.canvas = game.canvas  # Référence au canvas de tkinter pour dessiner le tir
        self.x = x  # Position X initiale du tir
        self.y = y  # Position Y initiale du tir
        self.speed = speed  # Vitesse du tir (distance parcourue par le tir chaque mise à jour)
        
        # Crée un rectangle pour représenter le tir sur l'écran
        self.bullet = self.canvas.create_rectangle(x - 2, y - 10, x + 2, y, fill="red")

        # Variable pour gérer le délai entre les déplacements du tir
        self.last_move_time = 0
        self.cooldown_move = 50  # Temps de cooldown pour chaque mouvement (en millisecondes)

        # Déplacer le tir
        self.move()

    def move(self):
        """
        Déplace le tir verticalement vers le haut. Si le tir dépasse le haut de l'écran, il est supprimé.
        Cette méthode utilise une boucle avec un délai pour déplacer le tir de façon continue.
        """
        if not self.game.over:  # Vérifie si le jeu est terminé
            if self.y > 0:  # Si le tir est encore à l'écran (pas au-dessus)
                self.canvas.move(self.bullet, 0, -self.speed)  # Déplace le tir vers le haut
                self.y -= self.speed  # Met à jour la position Y du tir
            else:  # Si le tir dépasse le haut de l'écran, le supprimer
                self.canvas.delete(self.bullet)
                return
        # Appelle la méthode move toutes les 20 ms pour un mouvement continu
        self.canvas.after(20, self.move)

    def update(self):
        """
        Met à jour la position du tir. Cette méthode est similaire à `move`, mais est conçue pour
        être utilisée à des fins de mise à jour ou de rafraîchissement si nécessaire.
        """
        if self.bullet:  # Si le tir existe toujours
            self.canvas.move(self.bullet, 0, -self.speed)  # Déplace le tir vers le haut
            self.y -= self.speed  # Mise à jour de la position Y du tir
