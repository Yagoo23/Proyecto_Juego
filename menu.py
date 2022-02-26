import pygame
import constantes


screen = pygame.display.set_mode((constantes.SCREEN_WIDTH, constantes.SCREEN_HEIGHT))
reloj = pygame.time.Clock()
FPS = 60


def text_format(message, textFont, textSize, textColor):
    newFont = pygame.font.Font(textFont, textSize)
    newText = newFont.render(message, 0, textColor)

    return newText


class Menu():
    selected = ""
    def main_menu():
        menu = True
        selected = "start"
        pygame.display.set_caption("Menú")
        while menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected = "start"
                    elif event.key == pygame.K_DOWN:
                        selected = "quit"
                    if event.key == pygame.K_RETURN:
                        if selected == "start":
                            print("Start")
                        if selected == "quit":
                            pygame.quit()
                            quit()

                # Main Menu UI
                screen.fill(constantes.blue)
                title = text_format("Saltos", constantes.font, 90, constantes.yellow)
                if selected == "start":
                    text_start = text_format("START", constantes.font, 75, constantes.white)
                else:
                    text_start = text_format("START", constantes.font, 75, constantes.black)
                if selected == "quit":
                    text_quit = text_format("QUIT", constantes.font, 75, constantes.white)
                else:
                    text_quit = text_format("QUIT", constantes.font, 75, constantes.black)

                title_rect = title.get_rect()
                start_rect = text_start.get_rect()
                quit_rect = text_quit.get_rect()
                screen.blit(title, (constantes.SCREEN_WIDTH / 2 - (title_rect[2] / 2), 80))
                screen.blit(text_start, (constantes.SCREEN_WIDTH / 2 - (start_rect[2] / 2), 300))
                screen.blit(text_quit, (constantes.SCREEN_WIDTH / 2 - (quit_rect[2] / 2), 360))
                pygame.display.update()
                reloj.tick(FPS)
                pygame.display.set_caption("Saltos")
