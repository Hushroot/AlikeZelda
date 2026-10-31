import pygame
from settings import TILESIZE

class Cottage(pygame.sprite.Sprite):
    def __init__(self, pos, groups, surface):
        super().__init__(groups)

        self.image = pygame.transform.scale(surface, (192, 192))
        self.rect = self.image.get_rect(midbottom=(
            pos[0] + TILESIZE // 2,
            pos[1] + TILESIZE
        ))
        self.hitbox = pygame.Rect(0, 0, 120, 64)
        self.hitbox.midbottom = self.rect.midbottom - pygame.Vector2(0, 20)

        self.sort_y = self.hitbox.centery