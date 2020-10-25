# Les animations

Bon, vu que certains ont du mal avec la notion de hierarchie de classes,
je vais reprendre calmement...

## Point de départ : pas d'animations

On repart avec nos classes :
- *ElementGraphique* : une image, un rect, sait s'afficher
- *Joueur* : un *ElementGraphique* avec un nombre de vies et une fonction de
deplacement dépendant des touches appuyées...

Pour le moment, notre main ressemble à ceci (j'ai supprimé le texte pour simplifier un peu) :

```python
from toutBiten import *
import pygame
import random

def lireImages():
  images = {}
  images["fond"] = pygame.image.load("background.jpg").convert()
  images["perso"] = pygame.image.load("perso.png").convert_alpha()
  images["balle"] = pygame.image.load("balle.png").convert_alpha()

  return images

def ajouterBalles(balles, images, compteur, fps, duree):
  if compteur/fps % duree==0:
    balles.append(ElementGraphique(fenetre,images["balle"],random.randint(0,largeur), random.randint(0,hauteur)))


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

# creation du tableau de balles vide
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
        print(b.rect)

    # raffraichissement de l'ecran
    pygame.display.flip()

    if touches[pygame.K_ESCAPE]:
        continuer=False


    # On vide la pile d'evenements et on verifie certains evenements
    for event in evenements:   # parcours de la liste des evenements recus
        if event.type == pygame.QUIT:     #Si un de ces evenements est de type QUIT
            continuer = 0	   # On arrete la boucle
```

Tout ceci est réuni dans deux fichiers :
- [main.py](../Sources/Animations/main.py) : le pg principal
- [toutBiten.py](../Sources/Animations/toutBiten.py) : les classes

notez que le fichier *toutBiten.py* contient déja toutes les classes que nous
utiliserons plus bas dans ce cours...

## Transformations des balles en animations.

Je veux modifier mon code pour que les balles qui aparaissent soient maintenant animées. **Mais**, je ne veux pas tout casser.

- rien de ce qui ne concerne pas les balles ne doit être modifié
- ce qui concerne les balles doit être modifié aussi peu que possible.

Voyons ce "aussi peu que possible"...

### Lecture des Images de l'animation

Il me faut des images pour l'animation. J'ai pris une flamme,
avec 4 images... Chaque image a un nom de type *flameBall_X.png*
avec *X* un entier.

![image0](../Sources/Animations/flameBall_0.png)
![image0](../Sources/Animations/flameBall_1.png)
![image0](../Sources/Animations/flameBall_2.png)
![image0](../Sources/Animations/flameBall_3.png)

Recupérez les et sauvez les dans le répertoire de votre main...

Celui ci doit les lire, et les ranger. Pour des raisons pratiques, je vais les
mettre dans une liste, elle meme rangée dans mon dictionnaire d'images qui sert
à tout mon jeu.
Cette lecture d'image est toujours faite au début du jeu, par la fonction
*lireImages*.

La fonction lecture *lireImages* devient donc :
```python
def lireImages():
  images = {}
  images["fond"] = pygame.image.load("background.jpg").convert()
  images["perso"] = pygame.image.load("perso.png").convert_alpha()
  images["balle"] = pygame.image.load("balle.png").convert_alpha()

  images["flame"] = []
  for i in range(4):
      images["flame"].append(pygame.image.load("flameBall_"+str(i)+".png").convert_alpha())

  return images
```

Dans mon dictionnaire, dans la case *"flame"*, j'ai bien un tableau dont chaque
case contient une image de la flamme.

### Création d'une classe pour les elements animés.

Encore une fois, je ne veux pas modifier le code concernant le fond ou le
joueur. Je veux juste avoir la possibilité que certains éléments soient en fait
animés...

=> **Je ne modifie pas la classe ElementGraphique**. Elle est très bien.
Par contre, je vais ajouter une nouvelle classe pour représenter ces éléments
animés.

Cette classe doit aussi avoir une image a afficher et un rect...
c'est donc un *ElementGraphique*, sauf que l'image a afficher va changer
parfois...

Je vais donc créer une classe *ElementAnime*, héritant de *ElementGraphique*.

```python
class ElementAnime(ElementGraphique):
```

#### Constructeur (abus de langage)

Pour la construire, il me faut une méthode *__init__*
à laquelle je passe non plus une image, mais un tableau d'images.

La premiere chose que je vais faire, c'est construire un *ElementGraphique* pour représenter cet objet. Or la classe *ElementAnime* hérite de *ElementGraphique*. *ElementGraphique* est donc la **classe parente** de *ElementAnime*.

Je vais donc appeler la méthode *__init__* d'ElementGraphique
avec une ligne comme suit (*super* veut dire **classe parente** ):
```python
        super.__init__(les param dont a besoin cette fonction)
```

 Mais pour construire un *ElementGraphique*, il lui faut une image, pas une liste. Pas de problème : je lui donne comme image la premiere de ma liste. Ce sera mon image courante dans l'animation.

Puis je définis les variables **spécifiques à ma classe animée**. Je stocke :
- le tableau d'images (*self.images*)
- un timer (pour savoir quand changer d'image)
- le numéro de l'image courante.

Voici donc ma méthode *__init__* de la classe *ElementAnime*
```python

    def __init__(self, window, images, x=0, y=0):
        # Pour construire un element animé, on construit
        # d'abord un element graphique (avec la premiere image de la liste)
        super.__init__(window,images[0],x,y)

        # On ajoute toutes les variables utiles a la gestion de l'animation
        self.images = images
        self.timer = 0  # un timer pour l'animation
        self.numAnim = 0 # le numero de l'image courante
```

#### méthode d'affichage

Reste à s'occuper de l'affichage de l'animation.
Comme je veux changer le moins possible mon code, cette classe va aussi avoir une méthode *afficher* sans argument, comme *ElementGraphique*. On dit qu'on **surcharge** (override) la méthode *afficher*.

Comme la fonction *afficher* est appelée à chaque tour de boucle
par le main, c'est elle qui va incrémenter le timer. Si celui ci dépasse une certaine valeur, on change l'image courante (et on remet le timer à 0).

Puis, on affiche l'image courante, en appelant la méthode afficher de la **classe parente** de *ElementAnime*.
C'est bien *

Le code qui suit est relativement simple, sauf la derniere ligne que je vais expliquer plus bas... dites moi si vous avez du mal.

```python
    def afficher(self) :
        self.timer+=1
        if self.timer > 10: # on change d'image tous les 10 tours de boucles...
            self.timer = 0
            self.numAnim+=1
            if self.numAnim >= len(self.images):
                self.numAnim=0
            self.image = self.images[self.numAnim]

        super().afficher()
```
Tout le contenu du *if* ne servait qu'à mettre la bonne image
dans *self.image*, au bon moment. A la sortie du *if*,
je veux afficher mon image, comme d'habitude. Le plus simple est de dire "Je veux lancer la fonction d'affichage normale d'un *ElementGraphique*". De fait, cette dernière ligne appelle la fonction *afficher* de la classe parente.

Et voila. Reste a s'en servir.

#### Modification du main

Bon, ne reste plus qu'a transformer toutes mes balles créees par mon jeu en *ElementAnime*. Comme je les crées toutes dans la fonction *ajouterBalles*, celle ci devient donc :

```python
def ajouterBalles(balles, images, compteur, fps, duree):
  if compteur/fps % duree==0:
    balles.append(ElementAnime(fenetre,images["flame"],random.randint(0,largeur), random.randint(0,hauteur)))
```
J'ai modifié le type d'élément a créer, et lui ai passé la liste d'images de flammes...

Que modifier de plus ? Rien !

La seule chose que fait le programme principal, c'est afficher les balles avec les lignes suivantes :

```python
for b in balles:
    b.afficher()
```

Maintenant que chaque balle *b* est un *ElementAnime*,
c'est bien la méthode *afficher* de *ElementAnime* qui est appelée.
Donc mes balles sont animées...


Voila.
Tous les éléments que je voudrais animer devront donc hériter de cette classe
(et appeler son constructeur)

le fichier nécessaire est ici :
[mainAnime2.py](../Sources/Animations/mainAnime1.py). Les classes, vous les avez déja
dans *toutBiten.py*

#### Ajout de fonctionnalites pour les balles.

Si maintenant je veux creer des balles qui soient animées et qui bougent, le plus simple est de créer une classe *Balle*.
Celle ci héritera de *ElementAnime* et je lui ajouterais une méthode déplacer (que je vais recopier de ceux que je connais).

Je déconseille pour le moment l'héritage multiple. C'est bien, mais ca pose plein de problèmes...

Je pourrais donc faire quelque chose comme suit.
La classe Balle hérite de *ElementAnime*, je lui ajoute quelques parametres utiles pour les déplacements, et une méthode déplacer.

```python
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
```

Reste à s'en servir...
Quand j'ajoute une balle, cela doit maintenant être un objet de type *Balle*; donc ma fonction d'ajout devient :

```python
def ajouterBalles(balles, images, compteur, fps, duree):
  if compteur/fps % duree==0:
    balles.append(Balle(fenetre,images["flame"],random.randint(0,largeur), random.randint(0,hauteur)))
```

Et j'ajoute quelque part dans la boucle while de mon *main* une boucle pour déplacer toutes les balles...


```python
  for b in balles:
      b.deplacer()
```

Et c'est tout ! (et ça se met a bouger de partout)

le fichier nécessaire est ici :
[mainAnime2.py](../Sources/Animations/mainAnime2.py). Les classes, vous les avez déja
dans *toutBiten.py*

#### Conclusion

Tout le jeu, en programmation Objet, consiste a créer les "bonnes classes", celles dont les objets vont hériter pour obtenir rapidement les bonnes méthodes et les bons attributs.

Il convient donc de réfléchir un peu à qui doit hériter de quoi...

pour le moment, mon graphe des classes est comme suit :
... TODO ...
