import pygame
import math

class ElementGraphique():
    # Le constructeur basique
    def __init__(self, window, img, x=0, y=0):
        self.image = img
        self.rect = self.image.get_rect()

        # puis on positionne l'element.
        self.rect.x = x
        self.rect.y = y
        self.window = window

    def afficher(self) :
        self.window.blit(self.image, self.rect)

'''
La classe des elements qui aparaissent sous forme d'une animation d'images
'''
class ElementAnime(ElementGraphique):

    def __init__(self, window, images, x=0, y=0):
        # Pour construire un element animé, on construit
        # d'abord un element graphique (avec la premiere image de la liste)
        super().__init__(window,images[0],x,y)

        # On ajoute toutes les variables utiles a la gestion de l'animation
        self.images = images
        self.timer = 0  # un timer pour l'animation
        self.numAnim = 0 # le numero de l'image courante

    def afficher(self) :
        self.timer+=1
        if self.timer > 10: # on change d'image tous les 10 tours de boucles...
            self.timer = 0
            self.numAnim+=1
            if self.numAnim >= len(self.images):
                self.numAnim=0
            self.image = self.images[self.numAnim]

        super().afficher()

'''
La classe des elements qui aparaissent sous forme d'une animation d'images
differentes en fonction de leur direction
'''
class ElementAnimeDir(ElementAnime):

    def __init__(self, window, images_all_dir, x=0, y=0):
        # Pour construire un element animé, on construit
        # d'abord un element graphique (avec la premiere image de la liste)
        super().__init__(window,images_all_dir["repos"],x,y)

        # On ajoute toutes les variables utiles a la gestion de l'animation
        self.images_all_dir = images_all_dir
        self.direction="repos"
        self.old_direction="repos"

    def afficher(self) :
        # l'element a changé de direction
        if self.old_direction != self.direction:
            # je mets la nouvelle liste d'images a utiliser dans images.
            self.images = self.images_all_dir[self.direction]

            # je remet le numéro d'anim a 0
            self.numAnim=0

            # je mémorise la direction actuelle comme déja commencée
            self.old_direction = self.direction

        # et je demande l'affichage de l'animation en cours.
        super().afficher()


'''
La classe des balles
'''
class Balle(ElementAnime):

    def __init__(self, window, images, x=0, y=0):
        # Pour construire un element animé, on construit
        # d'abord un element animé
        super().__init__(window,images,x,y)

        self.t = 0.0
        self.truc = 10
        self.centerx = x
        self.centery = y

    def deplacer(self):
        self.t+=1.0

        self.rect.x = 100*math.cos(self.t/self.truc) + self.centerx
        self.rect.y = 100*math.sin(self.t/self.truc) + self.centery


class DeplacementLineaire(ElementGraphique):
    def __init__(self, window, img, x=0, y=0):
        ElementGraphique.__init__(self, window, img, x, y)
        self.dx = 3
        self.dy = 4

    def deplacer(self):
        self.rect.x+=self.dx
        self.rect.y+=self.dy

class DeplacementTordu(ElementGraphique):
    def __init__(self, window, img, x=0, y=0):
        ElementGraphique.__init__(self, window, img, x, y)
        self.t = 0.0
        self.truc = 10
        self.centerx = x
        self.centery = y

    def deplacer(self):
        self.t+=1.0

        self.rect.x = 100*math.cos(self.t/self.truc) + self.centerx
        self.rect.y = 100*math.sin(self.t/self.truc) + self.centery

class Teleguide(ElementGraphique):
    def __init__(self, window, img, x=0, y=0):
        ElementGraphique.__init__(self, window, img, x, y)
        self.vitesse = 10.0

    def deplacer(self, target):
        dx = target.rect.x - self.rect.x
        dy = target.rect.y - self.rect.y

        dist = math.sqrt(dx*dx + dy*dy)
        if dist !=0:
            dx= dx / dist * self.vitesse
            dy = dy /dist * self.vitesse
        self.rect.x += dx
        self.rect.y += dy

class Joueur(ElementGraphique):
    def __init__(self, window, img, x=0, y=0):
        super().__init__(window, img, x, y)
        self.vies = 3
        self.vitesse = 5

    def deplacer(self, touches):
        if touches[pygame.K_LEFT] :

            self.rect.x-= self.vitesse
        if touches[pygame.K_RIGHT] :
            self.rect.x+= self.vitesse

class Joueur1(ElementAnimeDir):
    def __init__(self, window, img, x=0, y=0):
        super().__init__( window, img, x, y)
        self.vies = 3
        self.vitesse = 5

    def deplacer(self, touches):
        self.direction="repos"
        if touches[pygame.K_LEFT] :
            self.direction="gauche"
            self.rect.x-= self.vitesse
        if touches[pygame.K_RIGHT] :
            self.rect.x+= self.vitesse
            self.direction="droite"
