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
        dx= dx / dist * self.vitesse
        dy = dy /dist * self.vitesse
        self.rect.x += dx
        self.rect.y += dy

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
