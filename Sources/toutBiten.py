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
