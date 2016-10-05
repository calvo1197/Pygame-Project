import pygame
import os,sys

ALTO = 600
ANCHO = 1000
ROJO = (255,0,0)
TURQUEZA = (64,224,208)

class Arma(pygame.sprite.Sprite):
    def __init__(self,archivo):
        pygame.sprite.Sprite.__init__(self)
        self.click = False
        self.image = pygame.image.load(archivo).convert_alpha()
        self.rect = self.image.get_rect()
        self.click = False
        #self.image = pygame.Surface(self.rect.size).convert()

    def update(self,surface):
        if self.click:
            self.rect.center = pygame.mouse.get_pos()
        surface.blit(self.image,self.rect)



class Cuadro(pygame.sprite.Sprite):
    def __init__(self,rect,archivo):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(rect)
        self.click = False
        self.image = pygame.image.load(archivo).convert_alpha()
        self.rect = self.image.get_rect()
        #self.image = pygame.Surface(self.rect.size).convert()

    def update(self,surface):
        if self.click:
            self.rect.center = pygame.mouse.get_pos()
        surface.blit(self.image,self.rect)

def main(pantalla,cuadro):
    Juego(cuadro)
    pantalla.fill(0)
    paleta = pygame.image.load('fondojeje.jpg').convert_alpha()
    pantalla.blit(paleta,(0,500))
    cuadro.update(pantalla)

def Juego(cuadro):
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if cuadro.rect.collidepoint(event.pos):
                cuadro.click = True
        elif event.type == pygame.MOUSEBUTTONUP:
            cuadro.click = False
        elif event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


if __name__ == "__main__":
    os.environ['SLD_VIDEO_CENTERED'] = '1'
    pygame.init()
    pantalla = pygame.display.set_mode((1000,600))
    arma = Arma('cubo.jpg')
    todos = pygame.sprite.Group()
    todos.add(arma)
    arma.rect.center = pantalla.get_rect().center

    iconos = pygame.sprite.Group()
    icono = Arma('cubo.jpg')
    icono.rect.y = ALTO-75
    icono.rect.x = 50
    iconos.add(icono)
    todos.add(icono)


    reloj = pygame.time.Clock()

    fin = False
    while not fin:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if arma.rect.collidepoint(event.pos):
                    arma.click = True
                for ic in iconos:
                    if ic.rect.collidepoint(event.pos):
                        print "icono"

            elif event.type == pygame.MOUSEBUTTONUP:
                arma.click = False
            elif event.type == pygame.QUIT:
                fin = True

        todos.update(pantalla)
        todos.draw(pantalla)
        pygame.display.update()
        pantalla.fill(0)
        reloj.tick(60)
