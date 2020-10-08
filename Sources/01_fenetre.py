import pygame

# Initialisation de la bibliotheque pygame
pygame.init()

# creation de la fenetre
largeur = 640
hauteur = 480
fenetre=pygame.display.set_mode((largeur,hauteur))

# la boucle infinie dans laquelle on reste coince
i=1;
continuer=1
while continuer:
    i= i+1;
    print (i)

# fin du programme principal.
# On n'y accedera jamais dans le cas de ce programme
pygame.quit()
