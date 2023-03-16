import pygame
from constants import *
from player import Player
from blocks import Block, RandBlock

class Level():
    def __init__(self, game_screen, palette):
        # attributes
        self.FONT = pygame.font.Font('retro.ttf', 30)
        self.surface = game_screen
        self.palette = palette
        self.running = True
        self.countdown = COUNTDOWN
        # create floor & lava
        self.floor = Block((0, HEIGHT-50), (WIDTH, HEIGHT/2), palette[GROUND])
        self.lava = Block((0, HEIGHT*1.4), (WIDTH, HEIGHT/2), palette[LAVA])
        self.lava.damage = True
        # player and blocks
        self.player = Player(((WIDTH - PLAYER_W) / 2, HEIGHT), palette)
        self.blocks = [self.lava, self.floor]
        self.top_block_y = self.floor.hitbox.y
        self.max_score = 0
        # camera
        self.cam_offset = pygame.math.Vector2(0, 0)

    def x_collision(self):
        player = self.player
        player.move_x()
        player.is_wallcling = False

        # screen wrap
        if player.hitbox.centerx < 0:
            player.hitbox.centerx = WIDTH
        elif player.hitbox.centerx > WIDTH:
            player.hitbox.centerx = 0
        # collisions
        for block in self.blocks:
            if block.hitbox.colliderect(player.hitbox):
                # moving left
                if player.direction.x < 0:
                    player.hitbox.left = block.hitbox.right
                # moving right
                elif player.direction.x > 0:
                    player.hitbox.right = block.hitbox.left
                # enable wallcling
                player.is_wallcling = True

    def y_collision(self):
        player = self.player
        player.move_y()
        player.grounded = False
        for block in self.blocks:
            if block.hitbox.colliderect(player.hitbox):
                # hit lava
                if block.damage:
                    self.game_over()
                    return
                # moving down
                if player.direction.y > 0:
                    player.hitbox.bottom = block.hitbox.top
                    # landed on block
                    player.grounded = True
                # moving up
                elif player.direction.y < 0:
                    player.hitbox.top = block.hitbox.bottom
                # equal player gravity to block's
                player.direction.y = block.gravity
        # max_score check
        curr_score = abs(self.player.hitbox.y - 646) // 10
        if curr_score > self.max_score:
            self.max_score = curr_score

    def drop_blocks(self):
        for block in self.blocks:
            # block currently falling
            if isinstance(block, RandBlock) and block.gravity:
                block.hitbox.y += block.gravity
                # check for player collision
                if block.hitbox.colliderect(self.player.hitbox):
                    # player squashed
                    if self.player.grounded or self.player.was_grounded:
                        self.game_over()
                        return
                    else:
                        # fix player position
                        self.player.hitbox.top = block.hitbox.bottom

                # check for block collisions
                for block2 in self.blocks:
                    if block.hitbox.colliderect(block2.hitbox) and block != block2 and block.hitbox.y <= block2.hitbox.y:
                        # make falling block match collided block's speed
                        block.gravity = block2.gravity
                        # fix hitboxes
                        block.hitbox.bottom = block2.hitbox.top
                        # check for highest landed block
                        if block.gravity == 0 and block.hitbox.y < self.top_block_y:
                            self.top_block_y = block.hitbox.y

    def align_camera(self):
        self.cam_offset.y = -(self.player.hitbox.y - 450)

    def try_spawn(self):
        # spawning batches
        if not self.countdown % 60:
            self.spawn_block()
        if not self.countdown % 250:
            self.spawn_block()
        # countdown tick
        if self.countdown <= 0:
            self.countdown = COUNTDOWN
        else:
            self.countdown -= 1

    def spawn_block(self):
        self.blocks.append(RandBlock(self.top_block_y - HEIGHT, self.palette))

    def lava_rise(self):
        if abs(self.player.hitbox.y - self.lava.hitbox.y) > HEIGHT:
            self.lava.hitbox.y = self.player.hitbox.y + HEIGHT
        if not self.countdown % 2:
            self.lava.hitbox.y -= 1
        if not self.countdown % 3:
            self.lava.hitbox.y -= 1

    def game_over(self):
        print(f'Game Over. Height: {self.max_score}')
        self.running = False

    def update(self):
        # game not running
        if not self.running:
            return
        # level
        self.try_spawn()
        self.drop_blocks()
        self.lava_rise()
        # player
        self.player.update_dir()
        self.y_collision()
        self.x_collision()
        self.align_camera()

    def draw(self):
        self.surface.fill(self.palette[SKY])
        player_offset = self.player.hitbox.topleft + self.cam_offset
        self.surface.blit(self.player.img, player_offset)
        for block in self.blocks[::-1]:
            block_offset = block.hitbox.topleft + self.cam_offset
            self.surface.blit(block.img, block_offset)
        score_txt = self.FONT.render(str(self.max_score), False, self.palette[GROUND])
        self.surface.blit(score_txt, (5, 0))


'''
EASY MODE
'''


class EasyLevel(Level):
    def __init__(self, game_screen, palette):
        super().__init__(game_screen, palette)

    # slower lava
    def lava_rise(self):
        if abs(self.player.hitbox.y - self.lava.hitbox.y) > HEIGHT:
            self.lava.hitbox.y = self.player.hitbox.y + HEIGHT
        if not self.countdown % 2:
            self.lava.hitbox.y -= 1

    # slower blocks
    def spawn_block(self):
        new_block = RandBlock(self.top_block_y - HEIGHT, self.palette)
        new_block.gravity -= 1
        self.blocks.append(new_block)

    # fewer blocks
    def try_spawn(self):
        # spawning batches
        if not self.countdown % 100:
            self.spawn_block()
        if not self.countdown % 369:
            self.spawn_block()
        # countdown tick
        if self.countdown <= 0:
            self.countdown = COUNTDOWN
        else:
            self.countdown -= 1
