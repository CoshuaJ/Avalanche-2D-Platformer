import pygame
from constants import *


class Player:
    def __init__(self, pos, colour):

        self.img = pygame.Surface((PLAYER_W, PLAYER_H))
        self.img.fill(colour)
        self.hitbox = self.img.get_rect(topleft=pos)

        # movement
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 6
        self.accel = 1
        self.decel = 0.5
        self.gravity = 0.53
        self.slide_cap = 2.0
        self.jump_speed = -12.5
        self.grounded = False
        self.was_grounded = False
        self.is_wallcling = False
        self.jump_released = True
        self.locked_x = 0
        self.error_val = 0.1

        # curr inputs
        self.left = False
        self.right = False
        self.up = False
        self.down = False

        # death animation
        self.colour = colour
        self.dead = False
        self.prev_pos = None

    ''' Checks user inputs, considering player's current state, alters the direction vector
        Also runs jump() '''
    def apply_inputs(self):
        left = self.left
        right = self.right
        up = self.up
        down = self.down

        if not self.locked_x:
            # not pressing either OR pressing both, slowdown
            if (not left and not right) or (left and right):
                # moving left
                if self.direction.x < 0:
                    self.direction.x += self.decel
                    #print(f"slowing: {self.direction.x}")
                # moving right
                elif self.direction.x > 0:
                    self.direction.x -= self.decel
                    #print(f"slowing: {self.direction.x}")
                # avoid rounding errors
                if abs(self.direction.x) <= self.error_val:
                    self.direction.x = 0
                    #print(f"zero'd: {self.direction.x}")
            # pressing a direction
            else:
                if left and self.direction.x > -self.speed:
                    self.direction.x -= self.accel
                    #print(f"L: {self.direction.x}")
                elif right and self.direction.x < self.speed:
                    self.direction.x += self.accel
                    #print(f"R: {self.direction.x}")

        # pressing jump
        #print(f'{self.grounded} / {self.was_grounded}')

        if up:
            if (self.grounded or self.was_grounded or self.is_wallcling) and self.jump_released:
                self.jump()
        # not pressing jump
        else:
            self.jump_released = True

    # record directional inputs
    def get_inputs(self):
        keys = pygame.key.get_pressed()
        self.left = keys[pygame.K_a]
        self.right = keys[pygame.K_d]
        self.up = keys[pygame.K_w]
        self.down = keys[pygame.K_s]

    def apply_gravity(self):
        if self.is_wallcling and self.direction.y > self.slide_cap:
            self.direction.y = self.slide_cap
        else:
            self.direction.y += self.gravity

    def move_y(self):
        self.hitbox.y += self.direction.y

    def move_x(self):
        self.hitbox.x += self.direction.x

    '''
    Alters direction vector, checks for wallcling
    '''
    def jump(self):
        self.direction.y = self.jump_speed
        if self.is_wallcling and not self.grounded:
            # moving left, jump right
            if self.direction.x < 0:
                self.direction.x = self.speed
            # moving right, jump left
            elif self.direction.x > 0:
                self.direction.x = -self.speed
            else:
                pass
                #print("walljumped without direction somehow")
            # lock direction
            self.locked_x = 7
        # update states
        self.jump_released = False

    def update_dir(self):
        self.get_inputs()
        self.apply_inputs()
        self.apply_gravity()
        self.was_grounded = self.grounded
        if self.locked_x:
            self.locked_x -= 1


class Player2(Player):
    def __init__(self, pos, colour):
        super().__init__(pos, colour)

    # override direction keys
    def get_inputs(self):
        keys = pygame.key.get_pressed()
        self.left = keys[pygame.K_LEFT]
        self.right = keys[pygame.K_RIGHT]
        self.up = keys[pygame.K_UP]
        self.down = keys[pygame.K_DOWN]


class PlayerBot(Player):
    def __init__(self, pos, colour):
        super().__init__(pos, colour)

    def get_inputs(self):
        pass


