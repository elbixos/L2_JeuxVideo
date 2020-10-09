import pygame

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


class DeplacementLineaire(ElementGraphique):
    def __init__(self, window, img, x=0, y=0):
        ElementGraphique.__init__(self, window, img, x=0, y=0)
        self.dx = 3
        self.dy = 4

    def deplacer(self):
        self.rect.x+=self.dx
        self.rect.y+=self.dy


class Joueur(ElementGraphique):
    def __init__(self, window, img, x=0, y=0):
        ElementGraphique.__init__(self, window, img, x=0, y=0)
        self.vies = 3
        self.vitesse = 5

    def deplacer(self, touches):
        if touches[pygame.K_UP] :
            self.rect.x-= self.vitesse
        if touches[pygame.K_DOWN] :
            self.rect.x+= self.vitesse
