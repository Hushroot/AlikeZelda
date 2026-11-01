import pygame
from support import import_folder

class AnimationPlayer:
    def __init__(self):
        self.frames = {
            'flame': import_folder('graphics/particles/flame/frames'),
            'aura': import_folder('graphics/particles/aura'),
            'heal': import_folder('graphics/particles/heal/frames'),
            'slash': import_folder('graphics/particles/slash'),
            'squid': import_folder('graphics/particles/smoke_orange')
        }

    def create_particles(self, animation_type, pos, groups):
        animation_frames = self.frames[animation_type]
        return ParticleEffect(pos, animation_frames, groups)

class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, pos, animtion_frames, groups):
        super().__init__(groups)

        self.sprite_type = 'magic'
        self.frame_index = 0
        self.animation_speed = 0.15
        self.frames = animtion_frames

        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)

    def animate(self):
        self.frame_index += self.animation_speed

        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self):
        self.animate()
