import pygame
pygame.init()
font = pygame.font.font(None,30)

def debug(info,y = 10, x = 10):
    display_surface = pygame.display.get_surface()