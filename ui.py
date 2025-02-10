# ui.py
import pygame

def draw_health_bar(screen, x, y, current, maximum, width=200, height=20):
    # Background bar (red)
    pygame.draw.rect(screen, (255, 0, 0), (x, y, width, height))
    # Health bar (green)
    if maximum > 0:
        health_width = int(width * (current / maximum))
    else:
        health_width = 0
    pygame.draw.rect(screen, (0, 255, 0), (x, y, health_width, height))

def draw_text(screen, text, size, color, pos):
    font = pygame.font.SysFont(None, size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, pos)

def pause_menu(screen):
    # Simple pause menu overlay.
    overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))  # semi-transparent black
    screen.blit(overlay, (0, 0))
    draw_text(screen, "Paused", 50, (255, 255, 255), 
              (screen.get_width() // 2 - 70, screen.get_height() // 2 - 25))
    pygame.display.flip()

def game_over_screen(screen, score, rooms_cleared):
    screen.fill((0, 0, 0))
    draw_text(screen, "Game Over", 50, (255, 0, 0), 
              (screen.get_width() // 2 - 100, screen.get_height() // 2 - 50))
    draw_text(screen, f"Score: {score}", 30, (255, 255, 255), 
              (screen.get_width() // 2 - 70, screen.get_height() // 2 + 10))
    draw_text(screen, f"Rooms Cleared: {rooms_cleared}", 30, (255, 255, 255), 
              (screen.get_width() // 2 - 70, screen.get_height() // 2 + 50))
    draw_text(screen, "Press R to Restart or ESC to Quit", 25, (200, 200, 200), 
              (screen.get_width() // 2 - 150, screen.get_height() // 2 + 90))
    pygame.display.flip()
