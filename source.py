import pygame, sys
from pygame.locals import *
import os
import random

ANCHO = 750
ALTO = 800
os.environ['SDL_VIDEO_CENTERED'] = '1' # Centramos la ventana de nuestro juego al centro de nuestra pantalla

# Ahora crearemos el objeto para nuestra nave espacial.

class naveEspacial(pygame.sprite.Sprite):

    DISPARO_DELAY = 30 # Para poder tener un tiempo intermedio entre cada disparo
    NAVE = os.path.join('assets', 'nave1.png') # Cargamos la imagen de nuestra nave
    SHOOT = os.path.join('assets', 'shoot.wav')
    
    def __init__(self):
        
        super().__init__() # Llamamos al constructor de la super clase que en este caso es una clase propia de pygame de la que estamos heredando
        
        self.nave_img = pygame.image.load(self.NAVE)
        
        self.cuerpo = self.nave_img.get_rect()
        
        self.cuerpo.centerx = ANCHO/2 # Posicionamos nuestra nave en X a la mitada del ancho de la pantalla al iniciarse el juego
        
        self.cuerpo.centery = ALTO-45 # Posicionamos nuestra nave en Y en el alto de la pantalla - 45px al iniciarse el juego
        
        self.listaDisparo = [] # Creamos esta lista que más adelante nos servirá para nuestra nave dispare
        
        self.velocidad_movimiento = 4 # Creamos la velocidad de movimiento de nuestra nave
        
        self.bonificacion = False # Creamos esta variable que nos servira para identificar si la bonificación del bonus está activa.
        
        self.contador_regresivo = 0 # Esta variable nos permitira establecer un enfriamiento en el disparo de nuestra nave
        
        self.disparo = pygame.mixer.Sound(self.SHOOT) # Cargamos el sonido del disparo

    # Creamos el método para que nuestra nave se dibuje sola

    def dibujar(self, superficie):
        superficie.blit(self.nave_img, self.cuerpo)

    # Ahora creamos el método que delimitará el movimiento para que nuestra nave no se salga de las dimensiones de nuestra ventana de juego

    def delimitar_movimiento(self):
        
        if self.cuerpo.left <= 0:
            self.cuerpo.left = 0
        elif self.cuerpo.right >= 750:
            self.cuerpo.right = 750
        elif self.cuerpo.top <= 0:
            self.cuerpo.top = 0
        elif self.cuerpo.bottom >= 800:
            self.cuerpo.bottom = 800

    def disparar(self, x, y):

        disparo = Proyectil(x, y)
        self.listaDisparo.append(disparo)
        self.disparo.set_volume(0.02) # Le establecemos el volumen al sonido disparo
        self.disparo.play() # Reproducimos el sonido disparo

    # enfriamiento de disparo normal
    def enfriamiento_disparo(self):
        self.DISPARO_DELAY = 50
        if self.contador_regresivo >= self.DISPARO_DELAY:
            self.contador_regresivo = 0
        elif self.contador_regresivo > 0:
            self.contador_regresivo += 1 

    # enfriamiento de disparo con bonus activado
    def enfriamiento_disparo_bonus(self):
        self.DISPARO_DELAY = 15 # Disparamos más rápido
        if self.contador_regresivo >= self.DISPARO_DELAY:
            self.contador_regresivo = 0
        elif self.contador_regresivo > 0:
            self.contador_regresivo += 1

# Creamos la clase Proyectil que es la que llamaremos al momento de que nuestra nave dispare

class Proyectil(pygame.sprite.Sprite):

    DISPARO = os.path.join('assets', 'disparorojo1.png') # Cargamos la imagen de nuestro disparo
    
    def __init__(self, posx, posy):
        super().__init__()
        self.disparo_img = pygame.image.load(self.DISPARO)
        self.cuerpo = self.disparo_img.get_rect()
        self.velocidad_disparo = 5
        self.cuerpo.top = posy
        self.cuerpo.left = posx

    def trayectoria(self):
        self.cuerpo.top = self.cuerpo.top - self.velocidad_disparo

    def dibujar(self, superficie):
        superficie.blit(self.disparo_img, self.cuerpo) 

# Lo que sige es crear nuestro objeto Nube

class Nube(pygame.sprite.Sprite):
    
    NUBE = os.path.join('assets', 'nube2.png') # Obtenemos el directorio de la imagen de nuestra nube
    
    def __init__(self, posx, posy):
        
        super().__init__()
        
        self.nube_img = pygame.transform.scale((pygame.image.load(self.NUBE)), (random.randint(75,150), random.randint(85, 90))) # Cargamos la imagen de nuestra nube y con random.randint establecemos un ancho y un largo de forma aleatoria para nuestra nube
        
        self.cuerpo = self.nube_img.get_rect() # Obtenemos el rectangulo de la imagen de nuestra nube a la que hemos llamado cuerpo para hacer referencia al cuerpo de la nube
        
        self.velocidad_nube = 1 # asignamos una velocidad
        
        self.cuerpo.left = posx # asignamos un posicionamiento en el eje x
       
        self.cuerpo.top = posy # # asignamos un posicionamiento en el eje y

    # Creamos el método de la trayectoria de la nube para que esta se mueve desde arriba hacia abajo
    
    def trayectoria(self):
        self.cuerpo.top = self.cuerpo.top + self.velocidad_nube

    # Creamos el método dibujar para que nuestra nube se dibuje sola

    def dibujar(self, superficie):
        superficie.blit(self.nube_img, (self.cuerpo.left, self.cuerpo.top)) 

# Ahora creamos el objeto Misil

class Misil(pygame.sprite.Sprite):

    MISIL = os.path.join('assets', 'misil1.png') # Nuevamente obtenemos el directorio para nuestra imagen, en este caso el misil.
    EXPLOSION = os.path.join('assets', 'explosion1.png')

    def __init__(self, posx, posy):
        
        super().__init__()
        
        # Creamos todos los atributos de nuestro misil como lo hicimos con las dos clases anteriores
        
        self.misil_img = pygame.transform.scale((pygame.image.load(self.MISIL)), (random.randint(30,40), random.randint(50, 70)))
        
        self.cuerpo_misil = self.misil_img.get_rect()
        
        self.velocidad_min = 5 # Establecemos una velocidad minima del misil
        
        self.velocidad_max = 13 # Estabblecemos una velocidad máxima del misil
        
        self.velocidad_misil = random.randint(self.velocidad_min, self.velocidad_max) # Le enviamos como argumento al randint la velocidad minima del misil y la velocidad máxima, para que establezca una velocidad aleatoria al misil al momento de ser creado y esto hará que algunos misiles vayan más rápido que otros
        
        self.cuerpo_misil.left = posx # Posición en el eje X
        
        self.cuerpo_misil.top = posy # Posición en el eje Y

        #Misil destruido

        self.misil_dest = pygame.transform.scale((pygame.image.load(self.EXPLOSION)), (30,40))
        self.cuerpo_misil_dest = self.misil_dest.get_rect()

    # Método trayectoria para que nuestro misil se desplace de arriba a abajo

    def trayectoria(self):

        self.cuerpo_misil.top = self.cuerpo_misil.top + self.velocidad_misil

    # Método dibujar para que nuestro misil se dibuje solo

    def dibujar(self, superficie):

        superficie.blit(self.misil_img, (self.cuerpo_misil.left, self.cuerpo_misil.top))

class Bonus(pygame.sprite.Sprite):

    BONUS = os.path.join('assets', 'bonus1.png')

    def __init__(self, posx, posy):
        super().__init__()
        self.bonus_img = pygame.image.load(self.BONUS)
        self.cuerpo_bonus =  self.bonus_img.get_rect()
        self.cuerpo_bonus.left = posx
        self.cuerpo_bonus.top = posy
        self.velocidad_bonus = 5

    def trayectoria(self):
        self.cuerpo_bonus.top = self.cuerpo_bonus.top + self.velocidad_bonus

    def dibujar(self, superficie):
        superficie.blit(self.bonus_img, (self.cuerpo_bonus.left, self.cuerpo_bonus.top))

# Creamos una función llamada juego que es donde instanciaremos parte de la lógica y lo que se mostrará en nuestro juego y recibirá una variable llamada record = None, esto nos permitirá identificar si el esta comenzando por primera vez o estamos repitiendo el juego porque perdimos anteriormente.

def juego(record=None):

    pygame.init()
    VENTANA = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption('Data Science AllWomen - InvaSion')
    FONDO = os.path.join('assets', 'fondo.jpg')
    fondo_ventana = pygame.transform.scale(pygame.image.load(FONDO), (ANCHO, ALTO)) # Usamos pygame.transform.scale para que el fondo pueda adaptarse al tamaño de la pantalla
    jugador = naveEspacial()

    iniciar = True # Variable para determinar cuando se inicia o se sale del juego, mientras sea True el juego se ejecutara y cuando cambie a False el juego se cerrará
    
    # Establecemos los FPS y el reloj que tomará mas adelante esos FPS como parámetro

    FPS = 80
    clock = pygame.time.Clock()

    # Propiedades para el record y los puntos

    puntos = 0

    # Con la siguiente lógica detectamos si se esta repitiendo una vez más el juego para que así guarde el puntaje que se obtuvo en la partida anterior

    if record == None:
        record = 0
    else:
        record = record

    perdiste = False # Variable que indica si el jugador perdió o no
    
    # Propiedades para las nubes

    cantidad_nubes = []
    contador_nubes = 0

    # Propiedades para los misiles

    cantidad_misiles = []
    contador_misiles = 0
    cantidad_misiles_destruidos = [] # Esta lista la usamos para poder realizar la animación de explosión de los misiles
    contador_misiles_destruidos = []

    # Propiedad para el bonus

    contador_bonus = 0 # Establece cada cuanto se genera la instancia de un bonus
    cantidad_bonus = [] # Guarda los bonus que se van creando
    duracion_bonus = 0 # Establece cuanto dura el bonus cuando el jugador lo consume
    caida_bonus = 600 # Establece cada cuanto aparece el bonus en la pantalla de nuestro juego

    # Fonts

    texto_enjuego = pygame.font.SysFont('Courier', 30, bold=2) # Texto que aparecerá mientras jugamos
    texto_empezar = pygame.font.SysFont('Courier', 20, bold=2) # Texto que aparecerá en la pantalla de espera
    texto_titulo = pygame.font.SysFont('Courier', 35, bold=6) # Texto que aparecerá en la pantalla de espera en letras más grandes

    # Creamos una función para crear una pantalla de espera en nuestro juego

    def fondo_espera():

        while True:
            # Dibujar texto dentro de nuestra ventana
            empezar = texto_empezar.render('Press a key to start', 1, (205, 92, 92))
            titulo = texto_titulo.render('Data Science AllWomen', 1, (65,105,225))
            titulo2 = texto_titulo.render(' = Python InvaSion =', 1,(255,76,0))
            VENTANA.fill((0,0,0))
            VENTANA.blit(empezar, (80,450))
            VENTANA.blit(titulo, (80, 300))
            VENTANA.blit(titulo2, (80,350))
            pygame.display.update()
            
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:  # Quita el juego al presionar ESCAPE
                        pygame.quit()
                    return
                
    fondo_espera() # Ponemos en marcha nuestra función

    # Guardamos la ubicación de los sonidos en las siguientes variables

    MUSICA_FONDO = os.path.join('assets', 'musicajuego.mp3')
    FIN_JUEGO = os.path.join('assets', 'juegoterminado.wav')
    MISIL_DESTRUIDO = os.path.join('assets', 'destruido.wav')

    # Cargamos la musica de fondo y la reproducimos
    pygame.mixer.music.load(MUSICA_FONDO)
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play()

    # Cargamos los sonidos para poder reproducirlos luego
    juego_terminado = pygame.mixer.Sound(FIN_JUEGO)
    misil_destruido = pygame.mixer.Sound(MISIL_DESTRUIDO)

    while iniciar:

        if perdiste == False:
            puntos += 0.1
            _puntos = "{0:.0f}".format(puntos) # Formateamos los puntos para no mostrar decimales por pantalla en el juego

        # Llamamos al método que delimita el movimiento

        jugador.delimitar_movimiento()

        for evento in pygame.event.get():
            if evento.type == QUIT:
                iniciar = False
                sys.exit()
            if perdiste == False:
                if evento.type == MOUSEMOTION:
                    # Si se mueve el ratón, este se mueve adonde el cursor esté.
                    jugador.cuerpo.move_ip(evento.pos[0] - jugador.cuerpo.centerx, evento.pos[1] - jugador.cuerpo.centery)
        
        if perdiste == False:
            teclas = pygame.key.get_pressed() # Inicia una instancia que detecta las teclas que se pulsan
            if teclas[pygame.K_a] or teclas[pygame.K_LEFT]:
                jugador.cuerpo.left -= jugador.velocidad_movimiento
            if teclas[pygame.K_d] or teclas[pygame.K_RIGHT]:
                jugador.cuerpo.right += jugador.velocidad_movimiento
            if teclas[pygame.K_w] or teclas[pygame.K_UP]:
                jugador.cuerpo.top -= jugador.velocidad_movimiento
            if teclas[pygame.K_s] or teclas[pygame.K_DOWN]:
                jugador.cuerpo.bottom += jugador.velocidad_movimiento
            if teclas[pygame.K_SPACE]:
                x,y = jugador.cuerpo.center # el método .center me regresa el centro de la coordenada X y el centro de Y
                if jugador.contador_regresivo == 0:
                    jugador.disparar(x -50, y - 50)
                    jugador.contador_regresivo = 1 # igualamos a 1 para activar el contador

        
        VENTANA.blit(fondo_ventana, (0,0))

        # Creamos una sentencia que siempre sea True para sumar + 1 el contador 

        if True:
            contador_misiles += 1

        # Cuando el contador llegue a 50 añadiremos 1 nube y reniciamos el contador a 0 nuevamente para que constantemente se repita este ciclo gracias al bucle while.

        if contador_misiles == 50:
            contador_misiles = 0
            ejex = random.randint(0, 580) # Le damos una posición en x aleatoria al misil
            misil = Misil(ejex, -100)
            cantidad_misiles.append(misil)

        # Dibujamos cada misil y llamamos a su trayectoria para que se muevan hacia abajo

        for misil in cantidad_misiles:
            misil.dibujar(VENTANA)
            if perdiste == False:
                misil.trayectoria()
                if misil.cuerpo_misil.top > ALTO:
                    cantidad_misiles.remove(misil)
                    puntos -= 50 # Por cada misil que toque el final de la pantalla restaremos 50 puntos
                # Cuando un misil toque el cuerpo del jugador perderemos
                if misil.cuerpo_misil.colliderect(jugador.cuerpo):
                    pygame.mixer.music.stop() # detenemos la musica porque ha terminado el juego
                    juego_terminado.set_volume(0.05) # Establecemos el volumen del sonido juego terminado
                    juego_terminado.play() # Reproducimos el sonido juego terminado
                    perdiste = True
        
        # Creamos una sentencia que siempre sea True al igual como hicimos con los misiles

        if True:
            contador_nubes += 1
    
        if contador_nubes == 40:
            contador_nubes = 0
            ejex = random.randint(0, 650) # Le damos una posición en x aleatoria a la nube
            nube = Nube(ejex, -100)
            cantidad_nubes.append(nube) # Agregamos cada nube a la lista

        # Dibujamos cada nube y llamamos a su trayectoria para que se muevan hacia abajo.
        
        for nube in cantidad_nubes:
            nube.dibujar(VENTANA)
            if perdiste == False:
                nube.trayectoria()
                # Eliminamos las nubes que lleguen al final de la pantalla

        # Imprimimos los textos puntos y record en pantalla

        texto_puntos = texto_enjuego.render('Points :{}'.format(_puntos), 1, (255,151,151))
        #texto_record = texto_enjuego.render('Record:{}'.format(record), 1, (255,151,151))
        
        VENTANA.blit(texto_puntos, (10,10))
        #VENTANA.blit(texto_record, (10,50))
    
        jugador.dibujar(VENTANA) # Dibujamos el jugador

        texto_cohetes_destruidos = texto_enjuego.render('Rockets destroyed:{}'.format(len(contador_misiles_destruidos)), 1, (151,151,151)) # Pintamos el contador de misiles destruidos dentro de nuestra ventana
        VENTANA.blit(texto_cohetes_destruidos, (10,50))
        
        # Si la lista de disparos no esta vacia, ejecutará el código donde recorremos la lista y dibujamos cada dispara que haga nuestra nave espacial

        if len(jugador.listaDisparo):
            if perdiste == False:
                for x in jugador.listaDisparo:
                    x.dibujar(VENTANA)
                    x.trayectoria()
                    # Eliminamos el disparo que llegue a la parte superior de la pantalla
                    if x.cuerpo.top < 20:
                        jugador.listaDisparo.remove(x)
                    # Para saber si colisiona un disparo con un misil, colocamos un else con el siguiente código
                    else:   
                        for cohete in cantidad_misiles:
                            if x.cuerpo.colliderect(cohete.cuerpo_misil): # Si el disparo golpea a un enemigo, le decimos que lo elimine
                                destruido = pygame.mixer.Sound(MISIL_DESTRUIDO)
                                destruido.set_volume(0.05)
                                destruido.play()
                                cantidad_misiles_destruidos.append(cohete) # Guardamos los misiles que se vayan destruyendo en la otra lista
                                cantidad_misiles.remove(cohete) # Removemos los misiles destruidos de la lista
                                try: # Validamos si existe el disparo, porque arroja errores algunas veces durante la ejecución del juego.
                                    jugador.listaDisparo.remove(x) # Removemos el disparo del jugador
                                except ValueError:
                                    print('Se destruyeron dos misiles con un disparo, ¡GENIAL!')
                                    puntos += 500 # Por cada 2 misiles que destruyamos le sumaremos 500 puntos
                                    print('Ganaste 500 puntos')
                                puntos += 10 # Por cada misil que destruyamos le sumaremos 10 puntos
                                
        # Recorremos los misiles destruidos y le cambiamos su imagen para dar el efecto de misil destruido
        for cohete in cantidad_misiles_destruidos:
            cohete.misil_img = cohete.misil_dest
            cohete.dibujar(VENTANA)
            if cohete.cuerpo_misil_dest.top == 0:
                contador_misiles_destruidos.append(cohete)
                cantidad_misiles_destruidos.remove(cohete)

         # Llamamos al método enfriamiento_disparo o enfriamiento_disparo_bonus para poder hacer disparos normales o más rápidos dependiendo si el bonus está activo o no
        if jugador.bonificacion == True:
            jugador.enfriamiento_disparo_bonus()
        else:
            jugador.enfriamiento_disparo()

        # Creamos una sentencia que siempre sea True, así como lo hicimos anteriormente

        if True:
            contador_bonus += 1

        # Luego cremos la instancia del bonus cuando el contado llegue a 1800 que son aproximadamente casí 2 minutos
        
        if contador_bonus == caida_bonus:
            caida_bonus += 200 # Aumenta el tiempo de caida del bonus en 200 para el próximo bonus
            posx = random.randint(0, 580)
            bonus = Bonus(posx, -100)
            cantidad_bonus.append(bonus)
            contador_bonus = 0

        # Dibujamos el bonus

        if len(cantidad_bonus):
            if perdiste == False:
                for bonus in cantidad_bonus:
                    bonus.trayectoria()
                    bonus.dibujar(VENTANA)
                    if bonus.cuerpo_bonus.top > ALTO:
                        cantidad_bonus.remove(bonus)
                    else:
                        if bonus.cuerpo_bonus.colliderect(jugador.cuerpo):
                            jugador.bonificacion = True
                            cantidad_bonus.remove(bonus)
 
        # Lógica para determinar si el bonus se encuentra activado

        if jugador.bonificacion:
            duracion_bonus += 1
            if duracion_bonus > 500:
                duracion_bonus = 0
                jugador.bonificacion = False

        pygame.display.update()

        clock.tick(FPS)

        if perdiste == True:
            record = _puntos # Cuando perdamos los puntos obtenidos en dicha partida, se guardarán en la variable record 
            juego(record) # Acá llamamos nuevamente a la función de nuestro juego, la cual recibe el record y ejecutará la pantalla de espera. Cuando el jugador pulse cualquier tecla para volver a jugar, podrá ver en la pantalla la palabra record con el puntaje que obtuvo en la partida pasada donde perdió

juego()