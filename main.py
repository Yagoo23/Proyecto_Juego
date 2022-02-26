import pygame
from PyQt5 import QtSql

import constantes
import random
import os
from pygame import mixer
from getpass import getuser
from datetime import datetime
from ajustes_imagen import ajustes_imagen
from enemigo import Enemigo
import conexion
import var


# https://www.youtube.com/watch?v=UTn8VWkIqbo&list=PLjcN1EyupaQlBSrfP4_9SdpJIcfnSJgzL&index=15 ejecutable empezar
mixer.init()
pygame.init()
""" 
creamos la ventana y le indicamos un titulo
 """
screen = pygame.display.set_mode((constantes.SCREEN_WIDTH, constantes.SCREEN_HEIGHT))
pygame.display.set_caption("SALTOS")
"""
definir los frames
"""
reloj = pygame.time.Clock()
FPS = 60

"""
Variables del juego
"""
SCROLL_TECHO = 470
gravedad = 1
Max_Platforms = 12
scroll = 0
fondo_scroll = 0
game_over = False
score = 0
fade_counter = 0

if os.path.exists('score.txt'):
    with open('score.txt', 'r') as file:
        high_score = int(score)
else:
    high_score = 0

"""
Definir fuente
"""
font_pequeña = pygame.font.SysFont('Retro.ttf', 20)
font_grande = pygame.font.SysFont('Retro.ttf', 34)
"""
Cargar la imagen de fondo
"""
fondo = pygame.image.load('img/fondo2.png').convert_alpha()
personajeDe_img = pygame.image.load('img/quieto.png').convert_alpha()
platform_img = pygame.image.load('img/platform.png').convert_alpha()
avion = pygame.image.load('img/bird.png').convert_alpha()
avion_aj = ajustes_imagen(avion)


def text_format(message, textFont, textSize, textColor):
    newFont = pygame.font.Font(textFont, textSize)
    newText = newFont.render(message, 0, textColor)

    return newText


# función para poner texto en la pantalla
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


# función para dibujar información en el panel
def dibujar_panel():
    pygame.draw.rect(screen, constantes.green, (0, 0, constantes.SCREEN_WIDTH, 30))
    pygame.draw.line(screen, constantes.green, (0, 30), (constantes.SCREEN_WIDTH, 30), 2)
    draw_text('SCORE: ' + str(score), font_pequeña, constantes.white, 0, 0)


def dibujar_fondo(fondo_scroll):
    # función para hacer aparecer el fondo
    screen.blit(fondo, (0, 0 + fondo_scroll))
    screen.blit(fondo, (0, -900 + fondo_scroll))


class Jugador():
    def __init__(self, x, y):
        self.image = pygame.transform.scale(personajeDe_img, (70, 90))
        self.width = 25
        self.height = 40
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (x, y)
        self.vel_y = 0
        self.flip = False

    def movimiento(self):
        scroll = 0
        dx = 0
        dy = 0
        tecla = pygame.key.get_pressed()
        if tecla[pygame.K_a]:
            dx = -10
            self.flip = True
        if tecla[pygame.K_d]:
            dx = 10
            self.flip = False

        # gravedad
        self.vel_y += gravedad
        dy += self.vel_y

        # asegurarse que no se sale de la pantalla
        if self.rect.left + dx < 0:
            dx = constantes.SCREEN_WIDTH - self.rect.right
        if self.rect.right + dx > constantes.SCREEN_WIDTH:
            self.rect.left = dx

        # comprobar la colisión con las plataformas
        for platform in platform_grupo:
            # colisión en la dirección y
            if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                # comprobar si es debajo del la plataforma
                if self.rect.bottom < platform.rect.centery:
                    if self.vel_y > 0:
                        self.rect.bottom = platform.rect.top
                        dy = 0
                        self.vel_y = -20
                        pygame.mixer.music.load('musica/salto.mp3')
                        pygame.mixer.music.set_volume(0.6)
                        pygame.mixer.music.play(1, 0.0)

        # comprobar la colisión con el suelo
        # if self.rect.bottom + dy > constantes.SCREEN_HEIGHT:
        #     dy = 0
        #     self.vel_y = -20

        # comprobar si el jugador toca el techo de la pantalla
        if self.rect.top <= SCROLL_TECHO:
            # si el jugador está saltando
            if self.vel_y < 0:
                scroll = -dy

        self.rect.x += dx
        self.rect.y += dy + scroll

        # update mask
        self.mask = pygame.mask.from_surface(self.image)

        return scroll

    def dibujar(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x - 20, self.rect.y - 25))

    # def inicio_juego(self):
    # https://freakspot.net/creacion-de-un-videojuego-con-pygame/


# Clase para la plataforma
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, movimientoPlat):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(platform_img, (width, 30))
        self.moving = movimientoPlat
        self.mov_contador = random.randint(0, 50)
        self.direccion = random.choice([-1, 1])
        self.velocidad = random.randint(1, 2)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, scroll):
        # moviendo las plataformas de lado a lado si son plataformas móviles
        if self.moving == True:
            self.mov_contador += 1
            self.rect.x += self.direccion * self.velocidad

        # cambiar la dirección de la plataforma o golpea una pared
        if self.mov_contador >= 100 or self.rect.left < 0 or self.rect.right > constantes.SCREEN_WIDTH:
            self.direccion *= -1
            self.mov_contador = 0
        # actualizar las posición vetical de las plataformas
        self.rect.y += scroll

        # comprobar si la plataforma sale de la pantalla
        if self.rect.top > constantes.SCREEN_HEIGHT:
            self.kill()


# Instancia de jugador
jumpy = Jugador(constantes.SCREEN_WIDTH // 2, constantes.SCREEN_HEIGHT - 200)

# crear grupos de plataformas
platform_grupo = pygame.sprite.Group()
enemigo_grupo = pygame.sprite.Group()

# crear plataforma de inicio
platform = Platform(constantes.SCREEN_WIDTH // 2 - 50, constantes.SCREEN_HEIGHT - 50, 100, False)
platform_grupo.add(platform)


while True:
    conexion.Conexion.create_BD(var.filedb)
    reloj.tick(FPS)
    if game_over == False:
        scroll = jumpy.movimiento()
        fondo_scroll += scroll
        if fondo_scroll >= 900:
            fondo_scroll = 0
        dibujar_fondo(fondo_scroll)

        # generar plataformas
        if len(platform_grupo) < Max_Platforms:
            p_w = random.randint(60, 90)
            p_x = random.randint(5, constantes.SCREEN_WIDTH - p_w)
            p_y = platform.rect.y - random.randint(60, 100)
            p_tipo = random.randint(1, 2)
            if p_tipo == 1 and score > 2000:
                p_mover = True
            else:
                p_mover = False
            platform = Platform(p_x, p_y, p_w, p_mover)
            platform_grupo.add(platform)

        # actualizar plataformas
        platform_grupo.update(scroll)

        # generar enemigos
        if len(enemigo_grupo) == 0 and score > 5000:
            enemigo = Enemigo(constantes.SCREEN_WIDTH, 100, avion_aj, 1.5)
            enemigo_grupo.add(enemigo)
        # update enemigos
        enemigo_grupo.update(scroll, constantes.SCREEN_WIDTH)

        # actualizar puntuación
        if scroll > 0:
            score += scroll

        # dibujar la línea con la puntuación máxima previa
        pygame.draw.line(screen, constantes.black, (0, score - high_score + SCROLL_TECHO),
                         (constantes.SCREEN_WIDTH, score - high_score + SCROLL_TECHO), 3)
        draw_text('HIGH SCORE', font_pequeña, constantes.black, constantes.SCREEN_WIDTH - 90,
                  score - high_score + SCROLL_TECHO)
        # dibuja
        platform_grupo.draw(screen)
        enemigo_grupo.draw(screen)
        jumpy.dibujar()

        # dibujar el panel
        dibujar_panel()

        # comprobar game over
        if jumpy.rect.top > constantes.SCREEN_HEIGHT:
            game_over = True
            pygame.mixer.music.load('musica/Caida.mp3')
            pygame.mixer.music.play(1, 0.0)
        # comprobar la colisión con enemigos
        if pygame.sprite.spritecollide(jumpy, enemigo_grupo, False):
            if pygame.sprite.spritecollide(jumpy, enemigo_grupo, False, pygame.sprite.collide_mask):
                game_over = True
                pygame.mixer.music.load('musica/GameOver.mp3')
                pygame.mixer.music.play(1, 0.0)
    else:
        if fade_counter < constantes.SCREEN_WIDTH:
            fade_counter += 5
            for y in range(0, 12, 2):
                pygame.draw.rect(screen, constantes.black, (0, y * 100, fade_counter, 100))
                pygame.draw.rect(screen, constantes.black,
                                 (constantes.SCREEN_WIDTH - fade_counter, (y + 1) * 100, constantes.SCREEN_WIDTH,
                                  100))
        else:
            draw_text('GAME OVER', font_grande, constantes.white, 170, 270)
            draw_text('SCORE: ' + str(score), font_grande, constantes.white, 170, 320)
            draw_text('PRESS SPACE TO PLAY AGAIN', font_grande, constantes.white, 80, 370)
            # actualizar high score

            if score > high_score:
                high_score = score
                with open('score.txt', 'w') as file:
                    newScore = []
                    conexion.Conexion.db_connect(var.filedb)
                    mensaje = "Nuevo record: "
                    usuario = getuser()
                    espacio = ". Usario: "
                    now = datetime.now()
                    momento = now.strftime("%d/%m/%Y, %H:%M:%S")
                    file.write(mensaje + str(high_score) + espacio + usuario + ". Hora y dia: " + str(momento))
                    #conexion.Conexion.high_score(newScore)
                    query = QtSql.QSqlQuery()
                    query.prepare('insert into record(high_score,user,date) VALUES(:high_score,:user,:date)')
                    query.bindValue(':high_score', str(high_score))
                    query.bindValue(':user', str(usuario))
                    query.bindValue(':date', str(momento))
                    if query.exec():
                        print('Inserción correcta')
                    else:
                        print('Error')

            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE]:
                # resetea variables
                game_over = False
                score = 0
                scroll = 0
                fade_counter = 0
                # reposicionar jumpy
                jumpy.rect.center = (constantes.SCREEN_WIDTH // 2, constantes.SCREEN_HEIGHT - 150)
                # resetear plataformas
                platform_grupo.empty()
                # resetear enemigos
                enemigo_grupo.empty()
                platform = Platform(constantes.SCREEN_WIDTH // 2 - 50, constantes.SCREEN_HEIGHT - 50, 100, False)
                platform_grupo.add(platform)
            # if key[pygame.K_RETURN]:
            #     game_over = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            # actualizar puntuación máxima
            if score > high_score:
                high_score = score
                with open('score.txt', 'w') as file:
                    mensaje = "Nuevo record: "
                    usuario = getuser()
                    espacio = ". Usario: "
                    now = datetime.now()
                    momento = now.strftime("%d/%m/%Y, %H:%M:%S")
                    file.write(mensaje + str(high_score) + espacio + usuario + ". Hora y dia: " + str(momento))
            quit()

    pygame.display.update()
