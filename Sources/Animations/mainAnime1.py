from toutBiten import *
import pygame
import random

def lireImages():
  images = {}
  images["fond"] = pygame.image.load("background.jpg").convert()
  images["perso"] = pygame.image.load("perso.png").convert_alpha()
  images["balle"] = pygame.image.load("balle.png").convert_alpha()

  images["flame"] = []
  for i in range(4):
      images["flame"].append(pygame.image.load("flameBall_"+str(i)+".png").convert_alpha())

  return images

def ajouterBalles(balles, images, compteur, fps, duree):
  if compteur/fps % duree==0:
    balles.append(ElementAnime(fenetre,images["flame"],random.randint(0,largeur), random.randint(0,hauteur)))


## Initialisation de la fenetre et crÃ©ation
pygame.init()
#creation de la fenetre

largeur = 640
hauteur = 480
fenetre=pygame.display.set_mode((largeur,hauteur))

# lecture des images, bien rangées dans un dictionnaire
# on trouvera ainsi l'image du joueur dans :
# images["joueur"], et ainsi de suite
# ===============================
images = lireImages()

# creation des objets du jeu
# ===============================
fond = ElementGraphique(fenetre, images["fond"],0,0)

# creation du tableau de balles avec une balle dedans
balles=[]

joueur = ElementGraphique(fenetre,images["perso"], 20, 50)

horloge = pygame.time.Clock()

# En avant !
fps = 30
continuer = True
time = 0
while continuer == True :
    horloge.tick(fps)
    time+=1

    # Recuperation de l'etat du clavier et des evenements de souris
    touches = pygame.key.get_pressed();
    evenements = pygame.event.get()

    # on ajoute des balles toutes les 1 secondes.
    ajouterBalles(balles, images, time, fps, 1)


    # Affichage des elements
    fond.afficher()
    joueur.afficher()

    for b in balles:
        b.afficher()

    # raffraichissement de l'ecran
    pygame.display.flip()

    if touches[pygame.K_ESCAPE]:
        continuer=False


    # On vide la pile d'evenements et on verifie certains evenements
    for event in evenements:   # parcours de la liste des evenements recus
        if event.type == pygame.QUIT:     #Si un de ces evenements est de type QUIT
            continuer = 0	   # On arrete la boucle
