class Alien:
    def __init__(self, game, x, y, image, score):
        self.score = score
        self.game = game
        self.canvas = game.canvas
        self.x = x
        self.y = y
        self.image = image
        self.alien = self.canvas.create_image(x, y, image=self.image)
    