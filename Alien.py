class Alien:
    def __init__(self, game, x, y, image, score):
        """
        Constructeur de la classe Alien qui représente un extraterrestre du jeu Space Invaders.

        :param game: Référence à l'instance du jeu en cours, utilisé pour accéder au canvas.
        :param x: Position en x de l'alien (coordonnée horizontale).
        :param y: Position en y de l'alien (coordonnée verticale).
        :param image: Image qui représente l'alien.
        :param score: Le score associé à l'alien, généralement basé sur sa position.
        """
        self.score = score  # Score que rapporte l'alien lorsqu'il est détruit
        self.game = game  # Référence à l'objet jeu
        self.canvas = game.canvas  # Accéder au canvas du jeu pour dessiner l'alien
        self.x = x  # Position horizontale de l'alien
        self.y = y  # Position verticale de l'alien
        self.image = image  # L'image à afficher pour cet alien
        self.alien = self.canvas.create_image(x, y, image=self.image)  # Créer l'image sur le canvas à la position spécifiée
