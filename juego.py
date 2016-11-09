import pygame
import ConfigParser

ANCHO=700
ALTO=448

BLANCO = [250,250,250]
NEGRO = [0,0,0]
ROJO = [250,0,0]
AZUL = [0,0,250]

class kami(pygame.sprite.Sprite):
    def __init__(self, img_sprite,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=img_sprite
        self.rect=self.image.get_rect()
        self.rect.x= x
        self.rect.y= y

class yerba(pygame.sprite.Sprite):
    def __init__(self, img_sprite,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=img_sprite
        self.rect=self.image.get_rect()
        self.rect.x= x
        self.rect.y= y

class fin(pygame.sprite.Sprite):
    def __init__(self, img_sprite,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=img_sprite
        self.rect= img_sprite.get_rect()
        self.rect.x= x
        self.rect.y= y
        self.vida = 10


def Recortar(archivo, anc, alc):
    matriz=[]
    imagen=pygame.image.load(archivo).convert_alpha()
    i_ancho, i_alto=imagen.get_size()
    #print i_ancho, ' ', i_alto
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
        self.vida = 10

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

        #print self.pini, self.pfin
        if self.pini[0]>self.pfin[0]:
            self.var_x*=-1


    def update(self,pantalla):
        #print self.rect.x,self.pini[0] ,self.pfin[0]
        if self.pini[0]<self.pfin[0]:
            if self.rect.x>=self.pini[0] and self.rect.x<self.pfin[0]:
                self.rect.x+=self.var_x
                self.dir = 2
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
                self.dir = 0
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
        self.tipo = 0
        self.disponible = 0


    def newSprite(self,archivo):
        self.image  = pygame.image.load(archivo).convert_alpha()

'''    def update(self,archivo):
        if self.disponible < 100:
            self.newSprite("cajita.png")
            print "no disponible jeje"
        if self.disponible >= 100:
            self.newSprite(archivo)'''

class Torre(pygame.sprite.Sprite):
    def __init__(self,archivo1,archivo2,px,py):
        pygame.sprite.Sprite.__init__(self)
        self.le = []
        self.arch1 = pygame.image.load(archivo1).convert_alpha()
        self.arch2 = pygame.image.load(archivo2).convert_alpha()
        self.image  = self.arch1
        self.rect = self.image.get_rect()
        self.click = False
        self.rect.x = px
        self.rect.y = py
        self.id = 0
        self.vida = 100
        self.swag = False

        self.radar = Radar(px,py,200,30,30)
        self.disparar = 0
        self.objetivo = []


    def update(self,surface):
        if self.swag:
            self.image  = self.arch2
        else:
            self.image  = self.arch1

        if self.click :
            self.rect.center = pygame.mouse.get_pos()
        surface.blit(self.image,self.rect)
        self.radar.rect.x = self.rect.x
        self.radar.rect.y = self.rect.y

class Radar(pygame.sprite.Sprite):
    def __init__(self,xo,yo,radio,xd,yd):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([radio,radio])
        self.rect = self.image.get_rect()
        self.image.fill(AZUL)
        self.cy = radio/2
        self.cx = radio/2
        nx = self.cx - (xd/radio)
        ny = self.cy - (yd/radio)
        self.rect.x = xo - nx
        self.rect.y = yo - ny

"""def BarMenu(pantalla,color):
    puntos = [[576,0],[700,0],[700,ALTO],[576,ALTO]]
    pygame.draw.polygon(pantalla,color,puntos)
"""
class Bala2(pygame.sprite.Sprite):
    def __init__(self,archivo,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load(archivo)
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.dir=0
        self.contador=0
        self.linea=[]

        self.sonidoBala = pygame.mixer.Sound("boom1.wav")
        self.sonidoBala.set_volume(0.1)

       # self.sonido7=pygame.mixer.Sound("sonidos/golpeRoca.wav")

    def update(self,surface):
        if self.contador < len(self.linea):
          self.rect.x=self.linea[self.contador][0]
          self.rect.y=self.linea[self.contador][1]
          self.contador+=10
        else:
            self.kill()
           # self.sonido7.play()

#-----------------------------------------------------------
def get_line(start, end):

        """Bresenham's Line Algorithm
        Produces a list of tuples from start and end
        """
        # Setup initial conditions
        x1, y1 = start
        x2, y2 = end
        dx = x2 - x1
        dy = y2 - y1

        # Determine how steep the line is
        is_steep = abs(dy) > abs(dx)

        # Rotate line
        if is_steep:
            x1, y1 = y1, x1
            x2, y2 = y2, x2

        # Swap start and end points if necessary and store swap state
        swapped = False
        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
            swapped = True

        # Recalculate differentials
        dx = x2 - x1
        dy = y2 - y1

        # Calculate error
        error = int(dx / 2.0)
        ystep = 1 if y1 < y2 else -1

        # Iterate over bounding box generating points between start and end
        y = y1
        points = []
        for x in range(x1, x2 + 1):
            coord = (y, x) if is_steep else (x, y)
            points.append(coord)
            error -= abs(dy)
            if error < 0:
                y += ystep
                error += dx

        # Reverse the list if the coordinates were swapped
        if swapped:
            points.reverse()
        return points

#Disparos colisiones
def ColDisparos(listaenemis,listabalas,listatodos):
    for paloma in listaenemis:
        colison = pygame.sprite.spritecollide(paloma,listabalas,True)
        for ele in colison:
            paloma.vida -= 2
            #print paloma.vida
            if paloma.vida <= 0:
                listatodos.remove(paloma)
                listaenemis.remove(paloma)
            listatodos.remove(ele)
            listabalas.remove(ele)

#---------------------------------------------------------------

if __name__ == '__main__':
    pygame.init()
    pantalla=pygame.display.set_mode([ANCHO,ALTO])
    todos=pygame.sprite.Group()
    listabotones= pygame.sprite.Group()
    listabloques = pygame.sprite.Group()
    listaenemis = pygame.sprite.Group()
    TorreCenter = pygame.sprite.Group()
    final = pygame.sprite.Group()


    sonidoFondo = pygame.mixer.Sound("100real.ogg")
    sonidoFondo.play()

    #fainal = fin(image,13,17)
    #todos.add(fainal)
    #final.add(fainal)

    balas = pygame.sprite.Group()
    TorreLava = pygame.sprite.Group()
    contador = 0
    temporizador = 200
    delay = 0
    num_enemis = 6
    pase = True
    colitions = []
    retraso = 35
    disp = 100
    con_Torre = 0
    flag = True

    boton1 = boton("calvocaja.png",623,100,"caja")
    boton1.tipo = 0
    todos.add(boton1)
    listabotones.add(boton1)

    boton2 = boton("pelucaja.png",623,300,"caja")
    boton2.tipo = 1
    todos.add(boton2)
    listabotones.add(boton2)

    animalx = 9
    animaly = 0
    animal=Recortar('dragon.png',32,32)
    jp=Jugador(animal[animalx][animaly])
    todos.add(jp)
    listaenemis.add(jp)

#trazado camino
    lector=ConfigParser.ConfigParser()
    lector.read('mapaviernes.map')
    origen = lector.get('nivel1','origen')
    ialo=int(lector.get('nivel1','alto'))
    iano=int(lector.get('nivel1','ancho'))
    mapa=lector.get('nivel1','mapa').split("\n")

#FONDO
    sansi=Recortar('terrenogen.png',32,32)
    lol = sansi[13][9]
    pic = sansi[8][3]
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
            if fila[x] == 'Q':
                pez = yerba(pic,xact,yact)
                TorreCenter.add(pez)
            if fila[x] == 'k' or fila[x] == 'p':
                lava = kami(lol,xact,yact)
                TorreLava.add(lava)

            if fila[x] == 'X':
                fainal = fin(lol,xact,yact)
                final.add(fainal)

        yact+=ialo
    jp.camino=ls_p
    jp.Nuevo_camino(0)

    reloj=pygame.time.Clock()
    fin=False
    dale = True
    oleada = 2

    while not fin:
        contador += 1

        for b in listabotones:
            if not flag:
                if b.tipo == 0:
                    b.newSprite("nocalvocaja.png")
                if b.tipo == 1:
                    b.newSprite("nopelucaja.png")
            if flag:
                if b.tipo == 0:
                    b.newSprite("calvocaja.png")
                if b.tipo == 1:
                    b.newSprite("pelucaja.png")

#control de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fin=True
#BOTONES
            if event.type == pygame.MOUSEBUTTONDOWN:
                for b in listabotones:
                    if b.rect.collidepoint(event.pos):
                        b.disponible = disp
                        if b.disponible < 100:
                            flag = 0
                            print "no disponible jeje"
                        if b.disponible >= 100:
                            flag = 1
                            if b.tipo == 0:
                                bloqueT = Torre("calvo2.png","calvo.png",300,100)
                                bloqueT.id = contador
                                bloqueT.swag = False
                                contador += 1
                                col = True
                                disp = 0
                            if b.tipo == 1:
                                bloqueT = Torre("pelu2.png","pelu.png",100,320)
                                bloqueT.id = contador
                                bloqueT.swag = False
                                contador += 1
                                col = True
                                disp = 0
                            #COLISION DEL CAMINO
                            while dale:
                                dale = False
                                colision = pygame.sprite.spritecollide(bloqueT,listabloques,False)
                                for bl in colision:
                                    if bloqueT.id != bl.id:
                                        bloqueT.rect.left = bl.rect.right
                                        dale = True
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
#CONTROL DE OLEADAS
        if pase:
            if (temporizador == 0 and num_enemis > 0):
                    jp = Jugador(animal[animalx][animaly])
                    jp.var_x = 6
                    #p.dir = 2
                    todos.add(jp)
                    listaenemis.add(jp)
                    temporizador = 200
                    num_enemis -= 1
                    jp.camino = ls_p
                    jp.Nuevo_camino(0)

            for r in listaenemis:
                r.image = animal[animalx + r.con][r.dir]
                jp.image=animal[animalx +jp.con][jp.dir]
                if(oleada == 1):
                    jp.vida = 15
                    #print jp.vida


        if(delay == 300):
            num_enemis = 6
            temporizador = 200
            delay = 0
            pase = False
            oleada -=1

        elif(oleada > 0):
            pase = True
            if oleada == 1:
                animalx = 9
                animaly = 4
            if oleada == 2:
                animalx = 3
                animaly = 2


#PONERLO EN LA PLANCHA
        for torre in listabloques:
            col = pygame.sprite.spritecollide(torre,TorreCenter,False)
            for plancha in col:
                torre.rect.x = plancha.rect.x
                torre.rect.y = plancha.rect.y

#PONERLO EN LA MIERDA
        for torre in listabloques:
            col = pygame.sprite.spritecollide(torre,TorreLava,False)
            for plancha in col:
                torre.rect.x = 400
                torre.rect.y = 50
            col = pygame.sprite.spritecollide(torre,listabloques,False)
            for plancha in col:
                if torre.id != plancha.id:
                    torre.rect.x = plancha.rect.right


#DISPAROS
        for bloqueT in listabloques:
            col = pygame.sprite.spritecollide(bloqueT.radar,listaenemis,False)
            for enemy in col:
                if retraso == 35:
                    bloqueT.swag = True
                    FinalB=Bala2('bala.png',bloqueT.rect.x,bloqueT.rect.y)
                    FinalB.linea=get_line((bloqueT.rect.x,bloqueT.rect.y),(enemy.rect.x,enemy.rect.y))
                    balas.add(FinalB)
                    todos.add(FinalB)
                    FinalB.sonidoBala.play()
                if retraso > 35:
                    bloqueT.swag = False
                    retraso = 0
                #print bloqueT.id

#CONDICION DE GANADA/PERDIDA
        for mia in final:
        	colition = pygame.sprite.spritecollide(mia,listaenemis,True)
        	for sisas in colition:
        		fainal.vida -= 1
        		#print fainal.vida

    #CUADROS DE VIDA JEJEJE
        letraVida = pygame.font.SysFont("Arial",20)
        imagenTextoVida = letraVida.render("MIA'S LIFE: " + str(fainal.vida),True, (200,200,200), (0,0,0) )
        cuadroVida = imagenTextoVida.get_rect()
        cuadroVida.centerx = 500
        cuadroVida.centery = 30

#carga o refresco
        #BarMenu(pantalla,AZUL)
        if fainal.vida > 0:
            #print str (len(listaenemis)) , "ACA ESTA ESTE MEN"
            image = pygame.image.load('mia64.png')
            pantalla.blit(image, (544, 384))
            ColDisparos(listaenemis,balas,todos)
            todos.update(pantalla)
            todos.draw(pantalla)
            pantalla.blit(imagenTextoVida,cuadroVida)
            temporizador-=10
            delay += 1
            retraso += 5
            disp += 1
        if fainal.vida == 0:
            image = pygame.image.load('imagen700.png')
            pantalla.blit(image,(0,0))
        elif oleada == 0 and len(listaenemis) == 0:
            image = pygame.image.load('mia700.png')
            pantalla.blit(image,(0,0))

        #print oleada
        pygame.display.flip()
        reloj.tick(10)
