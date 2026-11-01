import pygame
from random import randint
from settings import TILESIZE

class MagicPlayer:
    def __init__(self, animation_player):
        self.animation_player = animation_player

    def heal(self, player, strength, cost, groups):
        if player.energy >= cost and player.health < player.stats['health']:
            player.health += strength
            player.energy -= cost

            if player.health >= player.stats['health']:
                player.health = player.stats['health']

            self.animation_player.create_particles('aura', player.rect.center, groups)
            self.animation_player.create_particles('heal', player.rect.center, groups)
            return True
        return False

    def flame(self, player, cost, groups):
        if player.energy < cost:
            return False

        player.energy -= cost
        self.create_flames(player, groups)
        return True

    def create_flames(self, caster, groups):
        directions = {
            'right': pygame.math.Vector2(1, 0),
            'left': pygame.math.Vector2(-1, 0),
            'up': pygame.math.Vector2(0, -1),
            'down': pygame.math.Vector2(0, 1)
        }

        direction = directions[caster.status.split('_')[0]]
        flames = []

        for i in range(1, 6):
            pos = pygame.math.Vector2(caster.rect.center)
            pos += direction * i * TILESIZE
            pos.x += randint(-TILESIZE // 3, TILESIZE // 3)
            pos.y += randint(-TILESIZE // 3, TILESIZE // 3)

            flame = self.animation_player.create_particles( 'flame', pos, groups)
            flames.append(flame)

        return flames
