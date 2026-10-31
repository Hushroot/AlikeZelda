import pygame
from settings import TILESIZE

class Tree(pygame.sprite.Sprite):
    def __init__(self, pos, groups, surface):
        super().__init__(groups)

        self.image = pygame.transform.scale(surface, (128, 192))
        self.rect = self.image.get_rect(midbottom=(
            pos[0] + TILESIZE // 2,
            pos[1] + TILESIZE
        ))
        self.hitbox = pygame.Rect(0, 0, 32, 24)
        self.hitbox.midbottom = self.rect.midbottom - pygame.Vector2(0, 12)

        self.sort_y = self.hitbox.centery