import pygame

# Initialisation de la bibliotheque pygame
pygame.init()

#creation de la fenetre
largeur = 640
hauteur = 480
fenetre=pygame.display.set_mode((largeur,hauteur))


# lecture de l'image du perso
imagePerso = pygame.image.load("perso.png").convert_alpha()

# creation d'un rectangle pour positioner l'image du personnage
rectPerso = imagePerso.get_rect()
rectPerso.x = 60
rectPerso.y = 80

# lecture de l'image du fond
imageFond = pygame.image.load("background.jpg").convert()

# creation d'un rectangle pour positioner l'image du fond
rectFond = imageFond.get_rect()
rectFond.x = 0
rectFond.y = 0

## Ajoutons un texte fixe dans la fenetre :
# Choix de la police pour le texte
font = pygame.font.Font(None, 34)

# Creation de l'image correspondant au texte
imageText = font.render('<Escape> pour quitter', True, (255, 255, 255))

# creation d'un rectangle pour positioner l'image du texte
rectText = imageText.get_rect()
rectText.x = 10
rectText.y = 10

# servira a regler l'horloge du jeu
horloge = pygame.time.Clock()

# la boucle dont on veut sortir :
#   - en appuyant sur ESCAPE
#   - en cliquant sur le bouton de fermeture
i=1;
continuer=1
while continuer:

    # fixons le nombre max de frames / secondes
    horloge.tick(30)

    i=i+1
    print (i)

    # on recupere l'etat du clavier
    touches = pygame.key.get_pressed();

    # si la touche ESC est enfoncee, on sortira
    # au debut du prochain tour de boucle
    if touches[pygame.K_ESCAPE] :
        continuer=0

    # Affichage du fond
    fenetre.blit(imageFond, rectFond)

    # Affichage Perso
    fenetre.blit(imagePerso, rectPerso)

    # Affichage du Texte
    fenetre.blit(imageText, rectText)

    # rafraichissement
    pygame.display.flip()

    # Si on a clique sur le bouton de fermeture on sortira
    # au debut du prochain tour de boucle
    # Pour cela, on parcours la liste des evenements
    # et on cherche un QUIT...
    for event in pygame.event.get():   # parcours de la liste des evenements recus
        if event.type == pygame.QUIT:     #Si un de ces evenements est de type QUIT
            continuer = 0	   # On arrete la boucle

# fin du programme principal...
pygame.quit()
