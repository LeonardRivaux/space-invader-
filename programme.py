import os

# Chemin absolu basé sur le dossier du script
current_dir = os.path.dirname(__file__)  # Dossier contenant le script
image_path = os.path.join(current_dir, "spaceship.png")
print(image_path)

