import pygame
import pymunk
from config import *

class Block(pygame.sprite.Sprite):
    def __init__(self, pos, size, space, material='wood'):
        super().__init__()
        self.size = size
        self.material = material

        # Pymunk physics body
        mass = 10
        if self.material == 'steel':
            mass = 25
        elif self.material == 'glass':
            mass = 5

        moment = pymunk.moment_for_box(mass, self.size)
        self.body = pymunk.Body(mass, moment)
        self.body.position = pos
        self.shape = pymunk.Poly.create_box(self.body, self.size)
        self.shape.friction = 0.7
        space.add(self.body, self.shape)

        # Pygame surface
        self.image = pygame.Surface(self.size)
        self.rect = self.image.get_rect(center=self.body.position)
        self.update_color()

    def update_color(self):
        if self.material == 'wood':
            self.image.fill((139, 69, 19))
        elif self.material == 'steel':
            self.image.fill((169, 169, 169))
        elif self.material == 'glass':
            self.image.fill((173, 216, 230))

    def update(self):
        self.rect.center = self.body.position
        # We can add logic here later for breaking blocks

class Bomb(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.Surface(size)
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=pos)
        self.pos = pos
