import pygame
from constants import *
import random


class Block:
    def __init__(self, pos, dimensions, colour):
        self.img = pygame.Surface(dimensions)
        self.img.fill(colour)
        self.hitbox = self.img.get_rect(topleft=pos)
        self.gravity = 0
        self.damage = False


class RandBlock(Block):
    def __init__(self, spawn_height, palette):
        self.n_spawns = 25
        # randomise
        self.colour = pygame.Color(palette[BLOCK])
        for i in range(0,3):
            n = random.randint(-15, 15)
            if 0 <= (self.colour[i] + n) <= 255:
                self.colour[i] += n
        # rainbow blocks, self.colour = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.size = random.randint(1,2) * 60
        self.pos = (random.randint(0, self.n_spawns) * (WIDTH - self.size)/self.n_spawns, spawn_height)
        super().__init__(self.pos, (self.size, self.size), self.colour)
        self.gravity = random.randint(1,3) + 3
