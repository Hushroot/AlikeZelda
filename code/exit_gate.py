import pygame
from settings import TILESIZE

class ExitGate(pygame.sprite.Sprite):
    def __init__(self, pos, groups, get_progress):
        super().__init__(groups)
        self.get_progress = get_progress

        self.locked_image = pygame.Surface((128, 128), pygame.SRCALPHA)
        pygame.draw.rect(self.locked_image, '#66616d', (8, 0, 112, 128))
        pygame.draw.rect(self.locked_image, '#28232f', (24, 16, 80, 112))
        pygame.draw.rect(self.locked_image, '#704629', (28, 20, 72, 108))

        for x in range(40, 100, 16):
            pygame.draw.line(self.locked_image, '#38251d', (x, 20), (x, 127), 4)

        for y in (40, 96):
            pygame.draw.rect(self.locked_image, '#b89355', (28, y, 72, 8))

        pygame.draw.polygon(self.locked_image, '#bb66ff', [(64, 48), (80, 64), (64, 80), (48, 64)])

        self.open_image = self.locked_image.copy()
        pygame.draw.rect(self.open_image, '#18151f', (24, 16, 80, 112))
        pygame.draw.rect(self.open_image, '#d9ad55', (24, 16, 80, 112), 4)

        self.image = self.locked_image
        self.rect = self.image.get_rect(midbottom=(
            pos[0] + TILESIZE // 2,
            pos[1] + TILESIZE
        ))

        self.hitbox = pygame.Rect(0, 0, 96, 24)
        self.hitbox.midbottom = self.rect.midbottom - pygame.math.Vector2(0, 8)
        self.sort_y = self.hitbox.centery

    def can_open(self):
        claimed, total = self.get_progress()
        return total > 0 and claimed == total

    def get_interaction_text(self):
        if self.can_open():
            return 'Press F to escape'

        claimed, total = self.get_progress()
        return f'Exit locked: claim cursed loot ({claimed}/{total})'

    def update(self):
        self.image = self.open_image if self.can_open() else self.locked_image
