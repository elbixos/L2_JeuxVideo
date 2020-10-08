import pygame

# Initialisation de la bibliotheque pygame
pygame.init()

# Creation de la fenetre
largeur = 640
hauteur = 480
fenetre=pygame.display.set_mode((largeur,hauteur))

# la boucle dont on veut sortir :
#   - en appuyant sur ESCAPE
#   - en cliquant sur le bouton de fermeture
i=0;
continuer=1
while continuer:

    i=i+1;
    print (i)

    # on recupere l'etat du clavier
    touches = pygame.key.get_pressed();

    # si la touche ESC est enfoncee, on sortira
    # au debut du prochain tour de boucle
    if touches[pygame.K_ESCAPE] :
        continuer=0

    # Si on a clique sur le bouton de fermeture on sortira
    # au debut du prochain tour de boucle
    # Pour cela, on parcours la liste des evenements
    # et on cherche un QUIT...
    for event in pygame.event.get(): # parcours de la liste des evenements recus
        if event.type == pygame.QUIT: # Si un de ces evenements est de type QUIT
            continuer = 0

# fin du programme principal...
pygame.quit()
