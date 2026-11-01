import pygame
from settings import WORLD_MAP, TILESIZE, weapon_data, rarity_data
from tile import Tile
from player import Player, YSortCameraGroup
from support import import_csv_layout
from weapon import Weapon
from ui import UI
from enemy import Enemy
from particles import AnimationPlayer
from magic import MagicPlayer
from upgrade import Upgrade
from tree import Tree
from cottage import Cottage
from fence import Fence
from chest import Chest
from random import choice, choices
from reflection import Reflection

class Level:
    def __init__(self):

        self.display_surface = pygame.display.get_surface()

        self.game_paused = False

        self.game_over = False

        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.interaction_sprites = pygame.sprite.Group()

        self.current_attack = None

        self.reflection = None
        self.active_chest = None

        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        self.create_map()

        self.ui = UI()

        self.upgrade = Upgrade(self.player)

        self.animation_player = AnimationPlayer()
        self.magic_player = MagicPlayer(self.animation_player)

    def create_map(self):
        layout = import_csv_layout('map/world.csv')

        dirt_surface = pygame.image.load('graphics/environment/dirt.png').convert()
        tree_surface = pygame.image.load('graphics/environment/tree.png').convert_alpha()
        cottage_surface = pygame.image.load('graphics/environment/cottage.png').convert_alpha()
        fence_surface = pygame.image.load('graphics/environment/fence.png').convert_alpha()

        for row_index, row in enumerate(layout):
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE

                if col in ('d', 'p', 's'):
                    Tile(
                        (x, y),
                        [self.visible_sprites.floor_sprites],
                        dirt_surface
                    )

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

        tree_positions = [
            (3, 2), (7, 3), (15, 3), (19, 6), (5, 8), (20, 10), (4, 13), (15, 14)
        ]

        for col, row in tree_positions:
            Tree(
                (col * TILESIZE, row * TILESIZE),
                [self.visible_sprites, self.obstacle_sprites],
                tree_surface
            )

        cottage_positions = [
            (5, 3), (18, 10)
        ]

        for col, row in cottage_positions:
            Cottage(
                (col * TILESIZE, row * TILESIZE),
                [self.visible_sprites, self.obstacle_sprites],
                cottage_surface
            )

        decoration_positions = {
            'bush': [
                (3, 3), (7, 5), (13, 6), (6, 10), (17, 12), (21, 13)
            ],
            'flowers': [
                (2, 4), (6, 5), (9, 3), (10, 6), (7, 9), (12, 12), (18, 12), (20, 14)
            ]
        }

        for style, positions in decoration_positions.items():
            surface = pygame.image.load(f'graphics/environment/{style}.png').convert_alpha()

            for col, row in positions:
                Tile(
                    (col * TILESIZE, row * TILESIZE),
                    [self.visible_sprites.floor_sprites],
                    surface
                )

        fence_positions = [
            (3, 5), (7, 5), (16, 12), (20, 12)
        ]

        for col, row in fence_positions:
            Fence(
                (col * TILESIZE, row * TILESIZE),
                [self.visible_sprites, self.obstacle_sprites],
                fence_surface
            )

        Chest(
            (21 * TILESIZE, 13 * TILESIZE),
            [
                self.visible_sprites,
                self.obstacle_sprites,
                self.interaction_sprites
            ],
            cursed=True
        )

    def create_attack(self):
        self.current_attack = Weapon(
            self.player,
            [self.visible_sprites, self.attack_sprites]
        )

        if self.reflection is not None and self.reflection.alive():
            self.reflection.queue_attack(self.player.weapon, self.player.get_full_weapon_damage())

    def create_magic(self, style, strength, cost):
        cast = False

        if style == 'heal':
            cast = self.magic_player.heal(
                self.player,
                strength,
                cost,
                [self.visible_sprites]
            )
        elif style == 'flame':
            cast = self.magic_player.flame(
                self.player,
                cost,
                [self.visible_sprites, self.attack_sprites]
            )

        if cast and self.reflection is not None and self.reflection.alive():
            self.reflection.queue_magic(style, strength)

    def create_reflection_magic(self, reflection, style, strength):
        if style == 'flame':
            flames = self.magic_player.create_flames(
                reflection,
                [self.visible_sprites, reflection.magic_sprites]
            )

            for flame in flames:
                flame.damage = strength
        elif style == 'heal' and reflection.health < reflection.max_health:
            reflection.health = min(
                reflection.max_health,
                reflection.health + strength
            )

            for particle_type in ('aura', 'heal'):
                self.animation_player.create_particles(
                    particle_type,
                    reflection.rect.center,
                    [self.visible_sprites]
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

    def reflection_attack_logic(self):
        if self.reflection is None or self.reflection.health <= 0:
            return

        attack = self.reflection.current_attack

        if attack is not None and attack.rect.colliderect(self.player.hitbox):
            self.damage_player(self.reflection.attack_damage, 'slash')

        for flame in self.reflection.magic_sprites:
            if flame.rect.colliderect(self.player.hitbox):
                self.damage_player(flame.damage, 'flame')

    def damage_player(self, amount, attack_type):
        if self.game_over or self.game_paused:
            return

        if self.player.vulnerable:
            self.player.health = max(0, self.player.health - amount)
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()

            self.animation_player.create_particles(
                attack_type,
                self.player.rect.center,
                [self.visible_sprites]
            )

            if self.player.health <= 0:
                self.game_over = True
                self.game_paused = False
                self.destroy_attack()

    def trigger_death_particles(self, pos, particle_type):
        self.animation_player.create_particles(
            particle_type,
            pos,
            [self.visible_sprites]
        )

    def add_exp(self, amount):
        self.player.exp += amount

    def get_interaction_target(self):
        if self.game_over or self.game_paused or self.player.attacking or self.active_chest is not None:
            return None

        player_pos = pygame.math.Vector2(self.player.hitbox.center)
        target = None
        closest_distance = TILESIZE * 1.5

        for sprite in self.interaction_sprites:
            if not sprite.get_interaction_text():
                continue

            distance = player_pos.distance_to(sprite.hitbox.center)

            if distance <= closest_distance:
                target = sprite
                closest_distance = distance

        return target

    def start_reflection_duel(self, chest):
        if self.active_chest is not None or not chest.start_duel():
            return

        self.active_chest = chest
        self.reflection = Reflection(
            (18 * TILESIZE, 13 * TILESIZE),
            [self.visible_sprites, self.attackable_sprites],
            self.player,
            self.obstacle_sprites,
            [self.visible_sprites],
            self.create_reflection_magic
        )

    def check_reflection_duel(self):
        if self.active_chest is None or self.reflection.alive():
            return

        self.active_chest.unlock()
        self.active_chest = None
        self.reflection = None

    def open_chest(self):
        chest = self.get_interaction_target()

        if chest is None:
            return

        if chest.state == 'sealed':
            self.start_reflection_duel(chest)
            return

        if not chest.open():
            return

        weapon = choice(list(weapon_data.keys()))
        rarities = list(rarity_data.keys())
        weights = [rarity_data[rarity]['weight'] for rarity in rarities]
        rarity = choices(rarities, weights=weights, k=1)[0]
        collected = self.player.collect_weapon(weapon, rarity)

        self.ui.show_loot(weapon, rarity, collected)

    def toggle_menu(self):
        if not self.game_over:
            self.game_paused = not self.game_paused

    def run(self):
        if not self.game_over and not self.game_paused:
            self.visible_sprites.update()
            self.visible_sprites.enemy_update(self.player)

            if not self.game_over:
                self.player_attack_logic()
                self.reflection_attack_logic()

                if not self.game_over:
                    self.check_reflection_duel()
        elif self.game_paused and self.reflection is not None:
            self.reflection.last_update = pygame.time.get_ticks()

        self.visible_sprites.custom_draw(self.player)
        self.ui.display(self.player)

        if self.game_over:
            self.ui.show_game_over()
        elif self.game_paused:
            self.upgrade.display()
        else:
            target = self.get_interaction_target()

            if target is not None:
                pos = pygame.math.Vector2(target.rect.midtop)
                pos -= self.visible_sprites.offset
                pos.y -= 12

                self.ui.show_interaction(target.get_interaction_text(), pos)
