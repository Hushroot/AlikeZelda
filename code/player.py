import pygame
from settings import TILESIZE, weapon_data, magic_data, rarity_data
from support import import_folder
from entity import Entity

class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites, create_attack, destroy_attack, create_magic):
        super().__init__(groups)

        self.import_player_assets()
        self.status = 'down'

        self.image = self.animations['down_idle'][0]
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -26)

        self.speed = 5
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None
        self.obstacle_sprites = obstacle_sprites

        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        self.inventory = {'sword': 'common'}

        self.can_switch_weapon = True
        self.weapon_switch_time = None
        self.switch_duration_cooldown = 200

        self.magic_index = 0
        self.magic = list(magic_data.keys())[self.magic_index]
        self.can_switch_magic = True
        self.magic_switch_time = None

        self.stats = {
            'health': 100,
            'energy': 60,
            'attack': 10,
            'magic': 4,
            'speed': 5
        }
        self.max_stats = {
            'health': 300,
            'energy': 140,
            'attack': 20,
            'magic': 10,
            'speed': 10
        }
        self.upgrade_cost = {
            'health': 100,
            'energy': 100,
            'attack': 100,
            'magic': 100,
            'speed': 100
        }
        self.health = self.stats['health'] * 0.5
        self.energy = self.stats['energy'] * 0.8
        self.exp = 0

        self.create_magic = create_magic

        self.vulnerable = True
        self.hurt_time = None
        self.invulneravility_duration = 500

    def import_player_assets(self):
        character_path = 'graphics/player/'

        self.animations = {
            'up': [],
            'down': [],
            'left': [],
            'right': [],
            'up_idle': [],
            'down_idle': [],
            'left_idle': [],
            'right_idle': [],
            'up_attack': [],
            'down_attack': [],
            'left_attack': [],
            'right_attack': [],
        }
        for animation in self.animations:
            full_path = character_path + animation
            frames = import_folder(full_path)

            self.animations[animation] = [pygame.transform.scale(frame, (TILESIZE, TILESIZE)) for frame in frames ]

    def input(self):
        if not self.attacking:
            keys = pygame.key.get_pressed()

            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0

            if keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = 'right'
            elif keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = 'left'
            else:
                self.direction.x = 0

            if keys[pygame.K_SPACE]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()

            if keys[pygame.K_q] and self.can_switch_weapon and not self.attacking:
                self.can_switch_weapon = False
                self.weapon_switch_time = pygame.time.get_ticks()

                weapons = list(self.inventory.keys())
                current_index = weapons.index(self.weapon)
                next_index = (current_index + 1) % len(weapons)

                self.weapon = weapons[next_index]
                self.weapon_index = list(weapon_data.keys()).index(self.weapon)

            if keys[pygame.K_e] and self.can_switch_magic and not self.attacking:
                self.can_switch_magic = False
                self.magic_switch_time = pygame.time.get_ticks()

                if self.magic_index < len(list(magic_data.keys())) -1:
                    self.magic_index += 1
                else:
                    self.magic_index = 0

                self.magic = list(magic_data.keys())[self.magic_index]

            if keys[pygame.K_LCTRL] and not self.attacking:
                style = self.magic
                strength = magic_data[style]['strength'] + self.stats['magic']
                cost = magic_data[style]['cost']
                can_cast = self.energy >= cost

                if style == 'heal' and self.health >= self.stats['health']:
                    can_cast = False

                if can_cast:
                    self.attacking = True
                    self.attack_time = pygame.time.get_ticks()
                    self.create_magic(style, strength, cost)

    def get_status(self):
        if self.direction.x == 0 and self.direction.y == 0:
            if 'idle' not in self.status and not 'attack' in self.status:
                self.status = self.status + '_idle'

        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0

            if not 'attack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle', '_attack')
                else:
                    self.status = self.status + '_attack'
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack', '')

    def animate(self):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed

        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

        if not self.vulnerable:
            self.image.set_alpha(self.wave_value())
        else:
            self.image.set_alpha(255)

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False
                self.destroy_attack()

        if not self.can_switch_weapon:
            if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
                self.can_switch_weapon = True

        if not self.can_switch_magic:
            if current_time - self.magic_switch_time >= self.switch_duration_cooldown:
                self.can_switch_magic = True

        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invulneravility_duration:
                self.vulnerable = True

    def collect_weapon(self, weapon, rarity):
        if weapon in self.inventory:
            current_rarity = self.inventory[weapon]
            current_multiplier = rarity_data[current_rarity]['multiplier']

            if rarity_data[rarity]['multiplier'] <= current_multiplier:
                return False

        self.inventory[weapon] = rarity
        self.weapon = weapon
        self.weapon_index = list(weapon_data.keys()).index(weapon)
        return True

    def get_full_weapon_damage(self):
        base_damage = self.stats['attack']
        weapon_damage = weapon_data[self.weapon]['damage']
        rarity = self.inventory[self.weapon]
        multiplier = rarity_data[rarity]['multiplier']

        return base_damage + weapon_damage * multiplier

    def get_full_magic_damage(self, style):
        base_damage = self.stats['magic']
        spell_damage = magic_data[style]['strength']

        return base_damage + spell_damage

    def energy_recovery(self):
        self.energy = min(
            self.stats['energy'],
            self.energy + 0.01 * self.stats['magic']
        )

    def get_value_by_index(self, index):
        return list(self.stats.values())[index]

    def get_cost_by_index(self, index):
        return list(self.upgrade_cost.values())[index]

    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.stats['speed'])
        self.energy_recovery()

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_width() // 2
        self.half_height = self.display_surface.get_height() // 2
        self.offset = pygame.math.Vector2()

        self.floor_sprites = pygame.sprite.Group()

        self.grass_surface = pygame.image.load('graphics/environment/grass.png').convert()
        self.grass_surface = pygame.transform.scale(self.grass_surface, (TILESIZE, TILESIZE))

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        start_x = -int(self.offset.x % TILESIZE)
        start_y = -int(self.offset.y % TILESIZE)

        for y in range(start_y, self.display_surface.get_height(), TILESIZE):
            for x in range(start_x, self.display_surface.get_width(), TILESIZE):
                self.display_surface.blit(self.grass_surface, (x, y))

        for sprite in self.floor_sprites:
            offset_pos = sprite.rect.topleft - self.offset

            self.display_surface.blit(sprite.image, offset_pos)

        for sprite in sorted(
            self.sprites(),
            key=lambda sprite: getattr(sprite, 'sort_y', sprite.rect.centery)
        ):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

    def enemy_update(self, player):
        enemy_sprites = [
            sprite for sprite in self.sprites()
            if hasattr(sprite, 'sprite_type')
            and sprite.sprite_type == 'enemy'
        ]
        for enemy in enemy_sprites:
            enemy.enemy_update(player)