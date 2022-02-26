import pygame
import constantes
import random
class Enemigo(pygame.sprite.Sprite):
    def __init__(self,SCREEN_WIDTH, y,img,scale):
        pygame.sprite.Sprite.__init__(self)
        #definir variables
        self.animacion_lista =[]
        self.frame_index = 0
        self.update_tiempo= pygame.time.get_ticks()
        self.direccion=random.choice([-1,1])
        if self.direccion == 1:
            self.flip = True
        else:
            self.flip = False

        #cargar las imáganes
        animacion_pasos = 8
        for animacion in range(animacion_pasos):
            imagen= img.obtener_imagen(animacion,32,32,scale,(0,0,0))
            image=pygame.transform.flip(imagen,self.flip,False)
            image.set_colorkey((0,0,0))
            self.animacion_lista.append(image)
        #seleccionar la imagen inicial y crear un rectángulo con ella
        self.image=self.animacion_lista[self.frame_index]
        self.rect = self.image.get_rect()

        if self.direccion == 1:
            self.rect.x = 0
        else:
            self.rect.x = constantes.SCREEN_WIDTH
        self.rect.y=y

    def update(self,scroll,SCREEN_WIDTH):
        #update animación
        cooldown_animacion = 50
        #update imagen dependiendo del frame actual
        self.image=self.animacion_lista[self.frame_index]
        #comprobar si pasó tiempo suficiente desde la última actualización
        if pygame.time.get_ticks() - self.update_tiempo > cooldown_animacion:
            self.update_tiempo = pygame.time.get_ticks()
            self.frame_index += 1
        # si la animación está en 8 vuelve al inicio
        if self.frame_index >= len(self.animacion_lista):
            self.frame_index = 0

        #mover el enemigo
        self.rect.x += self.direccion * 2
        self.rect.y += scroll

        #ver si sale de la pantalla
        if self.rect.right < 0 or self.rect.left > constantes.SCREEN_WIDTH:
            self.kill()

