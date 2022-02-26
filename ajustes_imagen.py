import pygame

class ajustes_imagen():
    def __init__(self,imagen):
        self.sheet = imagen

    def obtener_imagen(self,frame,width,height,scale,colour):
        imagen=pygame.Surface((width,height)).convert_alpha()
        imagen.blit(self.sheet,(0,0),((frame * width),0,width,height))
        imagen=pygame.transform.scale(imagen,(int(width*scale),int(height*scale)))

        return imagen