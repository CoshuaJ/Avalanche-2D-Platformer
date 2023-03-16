import pygame
from constants import *

class Player():
    def __init__(self, pos, palette):
        self.palette = palette
        self.img = pygame.Surface((PLAYER_W, PLAYER_H))
        self.img.fill(palette[PLAYER])
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

    ''' Checks user inputs, considering player's current state, alters the direction vector
        Also runs jump() '''
    def get_input(self):
        keys = pygame.key.get_pressed()
        if not self.locked_x:
            # not pressing either OR pressing both, slowdown
            if (not keys[pygame.K_a] and not keys[pygame.K_d]) or (keys[pygame.K_a] and keys[pygame.K_d]):
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
                if keys[pygame.K_a] and self.direction.x > -self.speed:
                    self.direction.x -= self.accel
                    #print(f"L: {self.direction.x}")
                elif keys[pygame.K_d] and self.direction.x < self.speed:
                    self.direction.x += self.accel
                    #print(f"R: {self.direction.x}")

        # pressing jump
        #print(f'{self.grounded} / {self.was_grounded}')

        if keys[pygame.K_w]:
            if (self.grounded or self.was_grounded or self.is_wallcling) and self.jump_released:
                self.jump()


        # not pressing jump
        else:
            self.jump_released = True


    def apply_gravity(self):
        if self.is_wallcling and self.direction.y > self.slide_cap:
            self.direction.y = self.slide_cap
        else:
            self.direction.y += self.gravity


    def move_y(self):
        self.hitbox.y += self.direction.y

    def move_x(self):
        self.hitbox.x += self.direction.x

    ''' Alters direction vector, checks for wallcling
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
        self.grounded = False
        self.is_wallcling = False


    def update_dir(self):
        self.was_grounded = self.grounded
        self.get_input()
        self.apply_gravity()
        if self.locked_x:
            self.locked_x -= 1

