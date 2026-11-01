import pygame
from entity import Entity
from weapon import Weapon

class Reflection(Entity):
    def __init__(self, pos, groups, player, obstacle_sprites, attack_groups, create_magic):
        super().__init__(groups)

        self.player = player
        self.obstacle_sprites = obstacle_sprites
        self.weapon = player.weapon
        self.health = player.stats['health']
        self.max_health = self.health

        self.vulnerable = True
        self.hit_time = 0
        self.invincibility_duration = 300

        self.speed = 3
        self.stop_distance = 70

        self.create_magic = create_magic
        self.magic_sprites = pygame.sprite.Group()

        self.attack_groups = attack_groups
        self.attack_queue = []
        self.current_attack = None
        self.attack_damage = 0
        self.echo_delay = 1000
        self.attack_duration = 400
        self.attack_end = 0
        self.time = 0
        self.last_update = pygame.time.get_ticks()

        self.animations = {}

        for status, frames in player.animations.items():
            self.animations[status] = []

            for frame in frames:
                image = frame.copy()
                image.fill(
                    (110, 70, 170, 255),
                    special_flags=pygame.BLEND_RGBA_MULT
                )
                image.set_alpha(190)
                self.animations[status].append(image)

        self.status = 'down_idle'
        self.image = self.animations[self.status][0]
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -26)

    def get_damage(self, player, attack_type):
        if not self.vulnerable or self.health <= 0:
            return

        if attack_type == 'weapon':
            damage = player.get_full_weapon_damage()
        elif attack_type == 'magic':
            damage = player.get_full_magic_damage('flame')
        else:
            return

        self.health = max(0, self.health - damage)
        self.vulnerable = False
        self.hit_time = self.time

        if self.health <= 0:
            if self.current_attack is not None:
                self.current_attack.kill()
                self.current_attack = None

            for flame in self.magic_sprites:
                flame.kill()

            self.attack_queue.clear()
            self.kill()

    def queue_attack(self, weapon, damage):
        self.attack_queue.append({
            'time': self.time + self.echo_delay,
            'type': 'weapon',
            'weapon': weapon,
            'damage': damage
        })

    def queue_magic(self, style, strength):
        self.attack_queue.append({
            'time': self.time + self.echo_delay,
            'type': 'magic',
            'style': style,
            'strength': strength
        })

    def repeat_attacks(self):
        if self.current_attack and self.time >= self.attack_end:
            self.current_attack.kill()
            self.current_attack = None

        if self.time < self.attack_end or not self.attack_queue:
            return

        if self.time < self.attack_queue[0]['time']:
            return

        attack = self.attack_queue.pop(0)
        self.status = self.status.split('_')[0] + '_attack'
        self.frame_index = 0
        self.attack_end = self.time + self.attack_duration

        if attack['type'] == 'weapon':
            self.weapon = attack['weapon']
            self.attack_damage = attack['damage']
            self.current_attack = Weapon(self, self.attack_groups)
        else:
            self.create_magic(self, attack['style'], attack['strength'])

    def follow_player(self):
        player_pos = pygame.math.Vector2(self.player.hitbox.center)
        reflection_pos = pygame.math.Vector2(self.hitbox.center)
        offset = player_pos - reflection_pos

        if offset.magnitude() <= self.stop_distance:
            self.direction = pygame.math.Vector2()
            self.status = self.status.split('_')[0] + '_idle'
            return

        self.direction = offset.normalize()

        if abs(self.direction.x) > abs(self.direction.y):
            self.status = 'right' if self.direction.x > 0 else 'left'
        else:
            self.status = 'down' if self.direction.y > 0 else 'up'

    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed

        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

        self.image.set_alpha(190 if self.vulnerable else self.wave_value())

    def update(self):
        current_time = pygame.time.get_ticks()
        self.time += current_time - self.last_update
        self.last_update = current_time
        if not self.vulnerable:
            if self.time - self.hit_time >= self.invincibility_duration:
                self.vulnerable = True

        self.repeat_attacks()

        if self.time < self.attack_end:
            self.direction = pygame.math.Vector2()
        else:
            self.follow_player()

        self.move(self.speed)
        self.animate()
