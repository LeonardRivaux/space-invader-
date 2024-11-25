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
        if not self.game.over:  # Vérifie si le jeu est terminé
            if self.y > 0:
                self.canvas.move(self.bullet, 0, -self.speed)
                self.y -= self.speed
            else:
                self.canvas.delete(self.bullet)
                return
        self.canvas.after(20, self.move)

    def update(self):
        if self.bullet:
            self.canvas.move(self.bullet, 0, -self.speed)  # Déplace le bullet vers le haut
            self.y -= self.speed  # Met à jour la position Y du bullet
            