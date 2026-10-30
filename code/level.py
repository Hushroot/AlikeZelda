import pygame
from settings import WORLD_MAP, TILESIZE
from tile import Tile
from player import Player, YSortCameraGroup
from support import import_csv_layout
from weapon import Weapon
from ui import UI
from enemy import Enemy
from particles import AnimationPlayer
from magic import MagicPlayer
from upgrade import Upgrade

class Level:
    def __init__(self):

        self.display_surface = pygame.display.get_surface()

        self.game_paused = False

        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        self.current_attack = None

        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        self.create_map()

        self.ui = UI()

        self.upgrade = Upgrade(self.player)

        self.animation_player = AnimationPlayer()
        self.magic_player = MagicPlayer(self.animation_player)

    def create_map(self):
        layout = import_csv_layout('map/world.csv')
        for row_index, row in enumerate(layout):
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE

                if col == 'x':
                    Tile(
                        (x, y),
                        [self.visible_sprites, self.obstacle_sprites]
                    )
                elif col == 'p':
                    self.player = Player(
                        (x, y),
                        [self.visible_sprites],
                        self.obstacle_sprites,
                        self.create_attack,
                        self.destroy_attack,
                        self.create_magic
                    )
                elif col == 's':
                    Enemy(
                        'squid',
                        (x, y),
                        [self.visible_sprites, self.attackable_sprites],
                        self.obstacle_sprites,
                        self.damage_player,
                        self.trigger_death_particles,
                        self.add_exp
                    )

    def create_attack(self):
        self.current_attack = Weapon(
            self.player,
            [self.visible_sprites, self.attack_sprites]
        )

    def create_magic(self, style, strength, cost):
        if style == 'heal':
            self.magic_player.heal(
                self.player,
                strength,
                cost,
                [self.visible_sprites]
            )
        elif style == 'flame':
            self.magic_player.flame(
                self.player,
                cost,
                [self.visible_sprites, self.attack_sprites]
            )

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()

        self.current_attack = None

    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(
                    attack_sprite,
                    self.attackable_sprites,
                    False
                )
                for target_sprite in collision_sprites:
                    target_sprite.get_damage(
                        self.player,
                        attack_sprite.sprite_type
                    )

    def damage_player(self, amount, attack_type):
        if self.player.vulnerable:
            self.player.health = max(0, self.player.health - amount)
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()

            self.animation_player.create_particles(
                attack_type,
                self.player.rect.center,
                [self.visible_sprites]
        )

    def trigger_death_particles(self, pos, particle_type):
        self.animation_player.create_particles(
            particle_type,
            pos,
            [self.visible_sprites]
        )

    def add_exp(self, amount):
        self.player.exp += amount

    def toggle_menu(self):
        self.game_paused = not self.game_paused

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.ui.display(self.player)

        if self.game_paused:
            self.upgrade.display()
        else:
            self.visible_sprites.update()

            self.visible_sprites.enemy_update(self.player)
            self.player_attack_logic()