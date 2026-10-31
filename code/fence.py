import pygame
from settings import TILESIZE

class Fence(pygame.sprite.Sprite):
    def __init__(self, pos, groups, surface):
        super().__init__(groups)

        self.image = pygame.transform.scale(surface, (128, 128))
        self.rect = self.image.get_rect(midbottom=(
            pos[0] + TILESIZE // 2,
            pos[1] + TILESIZE
        ))
        self.hitbox = pygame.Rect(0, 0, 96, 12)
        self.hitbox.midbottom = self.rect.midbottom - pygame.Vector2(0, 36)
        self.sort_y = self.hitbox.centery