# main.py
import pygame
import settings
from ui import game_over_screen, draw_text
from game import Game

def main_menu(screen):
    clock = pygame.time.Clock()
    while True:
        screen.fill((0, 0, 0))
        draw_text(screen, "Soul Knight Inspired Game", 40, (255, 255, 255), (150, 100))
        play_button_rect = pygame.Rect(150, 200, 200, 50)
        pygame.draw.rect(screen, (128, 128, 128), play_button_rect)
        draw_text(screen, "PLAY", 30, (255, 255, 255), (play_button_rect.x + 60, play_button_rect.y + 10))
        exit_button_rect = pygame.Rect(150, 300, 200, 50)
        pygame.draw.rect(screen, (128, 128, 128), exit_button_rect)
        draw_text(screen, "EXIT", 30, (255, 255, 255), (exit_button_rect.x + 60, exit_button_rect.y + 10))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "exit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = event.pos
                    if play_button_rect.collidepoint(mouse_pos):
                        return "gameplay"
                    elif exit_button_rect.collidepoint(mouse_pos):
                        return "exit"
        clock.tick(settings.FPS)

def main():
    pygame.init()
    screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption("Soul Knight Inspired Game")
    state = "main_menu"
    clock = pygame.time.Clock()
    game = None

    while True:
        if state == "main_menu":
            result = main_menu(screen)
            if result == "gameplay":
                state = "gameplay"
            else:
                pygame.quit()
                exit()
        elif state == "gameplay":
            game = Game(screen)
            game.run()
            state = "game_over"
        elif state == "game_over":
            game_over_screen(screen, game.score, game.rooms_cleared)
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            state = "gameplay"
                            waiting = False
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            exit()
                clock.tick(settings.FPS)

if __name__ == "__main__":
    main()
