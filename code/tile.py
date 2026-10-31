import pygame
from settings import TILESIZE

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, surface=None):
        super().__init__(groups)

        if surface is None:
            surface = pygame.image.load('graphics/test/rock.png').convert_alpha()

        self.image = pygame.transform.scale(surface, (TILESIZE, TILESIZE))
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)