import pygame
import ConfigParser

ANCHO=700
ALTO=448

BLANCO = [250,250,250]
NEGRO = [0,0,0]
ROJO = [250,0,0]
AZUL = [0,0,250]

def Recortar(archivo, anc, alc):
    matriz=[]
    imagen=pygame.image.load(archivo).convert_alpha()
    i_ancho, i_alto=imagen.get_size()
    print i_ancho, ' ', i_alto
    for x in range(0, i_ancho/anc):
        linea=[]
        for y in range(0,i_alto/alc):
            cuadro=(x*anc, y*alc, anc, alc)
            linea.append(imagen.subsurface(cuadro))
        matriz.append(linea)
    return matriz


class Jugador(pygame.sprite.Sprite):
    camino=None
    def __init__(self, img_sprite):
        pygame.sprite.Sprite.__init__(self)
        self.image=img_sprite
        self.rect=self.image.get_rect()
        self.rect.x=100
        self.rect.y=100
        self.var_x=6
        self.var_y=6
        self.con=0
        self.conc=0
        self.dir=2

    def iguales(self, pa,pb):
        iguales=True
        if pa[0]!=pb[0]:
            iguales=False
        if pa[1]!=pb[1]:
            iguales=False
        return iguales

    def Nuevo_camino(self, conc):
        self.finx=False
        self.finy=False
        self.pini=self.camino[conc]
        self.pfin=self.camino[conc]
        if conc==0:
            self.rect.x=self.pini[0]
            self.rect.y=self.pini[1]

        for i in range(len(self.camino)-1):
            if self.iguales(self.pini,self.camino[i]):
                self.pfin=self.camino[i+1]

        print self.pini, self.pfin
        if self.pini[0]>self.pfin[0]:
            self.var_x*=-1


    def update(self,pantalla):
        #print self.rect.x,self.pini[0] ,self.pfin[0]
        if self.pini[0]<self.pfin[0]:
            if self.rect.x>=self.pini[0] and self.rect.x<self.pfin[0]:
                self.rect.x+=self.var_x
            else:
                self.finx=True
        else:
            if self.rect.x<=self.pini[0] and self.rect.x>self.pfin[0]:
                self.rect.x+=self.var_x
            else:
                self.finx=True


        if self.finx==True:
            if self.rect.y>=self.pini[1] and self.rect.y<self.pfin[0]:
                self.rect.y+=self.var_y
            else:
                self.finy=True

        if self.finx==True and self.finy==True:
            self.conc+=1
            #print self.conc ,len(self.camino)
            if self.conc < len(self.camino):
                self.Nuevo_camino(self.conc)

        if self.con<2:
            self.con+=1
        else:
            self.con=0



class boton (pygame.sprite.Sprite):
    def __init__(self,archivo,xi,yi,nombre):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(archivo).convert_alpha()
        self.rect = self.image.get_rect()
        self.nombre = nombre
        self.rect.x = xi
        self.rect.y = yi


class Cuadro(pygame.sprite.Sprite):
    def __init__(self,archivo,xi,yi):
        pygame.sprite.Sprite.__init__(self)
        self.image  = pygame.image.load(archivo).convert_alpha()
        self.rect = self.image.get_rect()
        self.click = False
        self.rect.x = xi
        self.rect.y = yi
        self.id = 0

    def update(self,surface):
        if self.click :
            self.rect.center = pygame.mouse.get_pos()
        surface.blit(self.image,self.rect)


def BarMenu(pantalla,color):
    puntos = [[576,0],[700,0],[700,ALTO],[576,ALTO]]
    pygame.draw.polygon(pantalla,color,puntos)


if __name__ == '__main__':
    pygame.init()
    pantalla=pygame.display.set_mode([ANCHO,ALTO])
    todos=pygame.sprite.Group()
    listabotones= pygame.sprite.Group()
    listabloques = pygame.sprite.Group()

    boton1 = boton("cajita.png",580,100,"caja")
    todos.add(boton1)
    listabotones.add(boton1)

    animal=Recortar('animales.png',32,32)
    jp=Jugador(animal[6][2])
    todos.add(jp)

    #trazado camino
    lector=ConfigParser.ConfigParser()
    lector.read('mapaviernes.map')
    origen = lector.get('nivel1','origen')
    ialo=int(lector.get('nivel1','alto'))
    iano=int(lector.get('nivel1','ancho'))
    mapa=lector.get('nivel1','mapa').split("\n")


    fondo = Recortar(origen,iano,ialo)
    ls_p=[]
    yact=0
    for fila in mapa:
        xact=0
        for x in range(len(fila)):
            xp=int(lector.get(fila[x],'x'))
            yp=int(lector.get(fila[x],'y'))
            xact=(x*iano)
            pantalla.blit(fondo[xp][yp],(xact,yact))
            if fila[x]=='p':
                pto=[xact,yact]
                ls_p.append(pto)
            
        yact+=ialo

    print ls_p
    jp.camino=ls_p
    jp.Nuevo_camino(0)


    contador = 0

    reloj=pygame.time.Clock()
    fin=False
    while not fin:
        contador += 1
        #control de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fin=True

            if event.type == pygame.MOUSEBUTTONDOWN:
                for b in listabotones:
                    if b.rect.collidepoint(event.pos):

                        bloqueT = Cuadro("caja.png",300,300)
                        print "pase"
                        bloqueT.id = contador
                        contador += 1
                        print contador
                        col = True
                        """
                        while col:
                            col = False
                            colision = pygame.sprite.spritecollide(bloqueT,listabloques,False)
                            for bl in colision:
                                if bloqueT.id != bl.id:
                                    bloqueT.rect.left = bl.rect.right
                                    col = True
                        """          
                        listabloques.add(bloqueT)
                        todos.add(bloqueT)

                for bloque in listabloques:
                    if bloque.rect.collidepoint(event.pos):
                        bloque.update(pantalla)
                        bloque.click = True
            elif event.type == pygame.MOUSEBUTTONUP:
                for bloque in listabloques:
                        bloque.update(pantalla)
                        bloque.click = False
                        col = True

        fondo = Recortar(origen,iano,ialo)
        yact=0
        for fila in mapa:
            xact=0
            for x in range(len(fila)):
                xp=int(lector.get(fila[x],'x'))
                yp=int(lector.get(fila[x],'y'))
                xact=(x*iano)
                pantalla.blit(fondo[xp][yp],(xact,yact))
            yact+=ialo

        jp.image=animal[6+jp.con][jp.dir]
        #carga o refresco
        BarMenu(pantalla,AZUL)
        todos.update(pantalla)
        todos.draw(pantalla)
        pygame.display.flip()
        reloj.tick(15)
