import random

import pygame
from constants import *
from player import Player, Player2, PlayerBot
from blocks import Block, RandBlock
import math
from itertools import groupby

class Level:
    def __init__(self, game_screen, palette, is_hard=True):
        # attributes
        self.FONT = pygame.font.Font(FONT_STR, 30)
        self.surface = game_screen
        self.palette = palette
        self.running = True
        self.countdown = COUNTDOWN
        self.is_hard = is_hard
        # create floor & lava
        self.floor = Block((0, HEIGHT-50), (WIDTH, HEIGHT/2), palette[GROUND])
        self.lava = Block((0, HEIGHT*1.4), (WIDTH, HEIGHT/2), palette[LAVA])
        self.lava.damage = True
        # player and blocks
        self.player = Player(((WIDTH - PLAYER_W) / 2, HEIGHT), palette[PLAYER])
        self.players = [self.player]
        self.blocks = [self.lava, self.floor]
        self.top_block = self.floor  # highest block which has landed
        self.landed_on_block = self.floor  # tracks which block player is/was last standing on
        self.max_score = 0
        # death animation
        self.animation_frames = -1
        self.animation_blocks = list()
        self.prev_pos = None
        # camera
        self.cam_offset = pygame.math.Vector2(0, 0)

    def x_collision(self):
        for player in self.players:
            if player.dead:
                return
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
        for player in self.players:
            if player.dead:
                return
            player.move_y()
            player.grounded = False
            for block in self.blocks:
                if block.hitbox.colliderect(player.hitbox):
                    # hit lava
                    if block.damage:
                        self.game_over(player)
                        return
                    # moving down
                    if player.direction.y > 0:
                        player.hitbox.bottom = block.hitbox.top
                        # landed on block
                        player.grounded = True
                        self.landed_on_block = block
                    # moving up
                    elif player.direction.y < 0:
                        player.hitbox.top = block.hitbox.bottom
                    # equal player gravity to block's
                    player.direction.y = block.gravity
            # max_score check
            curr_score = abs(player.hitbox.y - 646) // 10
            if curr_score > self.max_score:
                self.max_score = curr_score

    def drop_blocks(self):
        for block in self.blocks:
            # ensure not lava
            if not isinstance(block, RandBlock):
                continue
            # remove blocks below the lava
            if block.hitbox.top > self.lava.hitbox.top:
                self.blocks.remove(block)
                continue
            # block currently falling
            if block.gravity:
                block.hitbox.y += block.gravity
                # check for player collision
                for player in self.players:
                    if block.hitbox.colliderect(player.hitbox):
                        # player squashed
                        if player.grounded:  # or player.was_grounded:
                            self.game_over(player)
                            return
                        else:
                            # fix player position
                            player.hitbox.top = block.hitbox.bottom

                # check for block collisions
                for block2 in self.blocks:
                    if block.hitbox.colliderect(block2.hitbox) and block != block2 and block.hitbox.y <= block2.hitbox.y:
                        # make falling block match collided block's speed
                        block.gravity = block2.gravity
                        # fix hitboxes
                        block.hitbox.bottom = block2.hitbox.top
                        # check for highest landed block
                        if block.gravity == 0 and block.hitbox.y < self.top_block.hitbox.y:
                            self.top_block = block

    def align_camera(self):
        # self.cam_offset.y = -(self.player.hitbox.y - 450)
        min_height = HEIGHT
        for player in self.players:
            if player.hitbox.y < min_height:
                min_height = player.hitbox.y
        self.cam_offset.y = -(min_height - 450)

    def try_spawn_blocks(self):
        # HARD spawning batches
        if self.is_hard:
            if not self.countdown % 60:
                self.spawn_block()
            if not self.countdown % 250:
                self.spawn_block()
        # EASY spawning
        else:
            if not self.countdown % 100:
                self.spawn_block()
            if not self.countdown % 369:
                self.spawn_block()
        # countdown tick
        if self.countdown <= 0:
            self.countdown = COUNTDOWN
        else:
            self.countdown -= 1

    def spawn_block(self):
        new_block = RandBlock(self.player.hitbox.top - HEIGHT*1.1, self.palette)
        # slower blocks on easy
        if not self.is_hard:
            new_block.gravity -= 1
        self.blocks.append(new_block)
        return new_block

    def lava_rise(self):
        if abs(self.player.hitbox.y - self.lava.hitbox.y) > HEIGHT:
            self.lava.hitbox.y = self.player.hitbox.y + HEIGHT
        if not self.countdown % 2:
            self.lava.hitbox.y -= 1
        # slower lava on easy
        if not self.countdown % 3 and self.is_hard:
            self.lava.hitbox.y -= 1

    def game_over(self, player):
        print(f'Game Over. Height: {self.max_score}')
        self.animation_frames = 60
        player.dead = True

    def update_players(self):
        for player in self.players:
            player.update_dir()

    def update(self):
        # game not running
        if not self.running or self.animation_frames > 0:
            return
        # level
        self.try_spawn_blocks()
        self.drop_blocks()
        self.lava_rise()
        # player
        self.update_players()
        self.y_collision()
        self.x_collision()
        # only update prev_pos and camera if player hasn't died
        if self.animation_frames == -1:
            for player in self.players:
                player.prev_pos = player.hitbox.center
            self.align_camera()

    def draw(self):
        # background
        self.surface.fill(self.palette[SKY])
        # setup blocks list
        block_list = self.blocks.copy()
        block_list.reverse()
        # draw living player and/or death animation
        for player in self.players[::-1]:
            if player.dead:
                self.death_animation(player)
                block_list.extend(self.animation_blocks)
            else:
                player_offset = player.hitbox.topleft + self.cam_offset
                self.surface.blit(player.img, player_offset)
        # # check death_animation counter
        # if self.animation_frames > 0:
        #     self.death_animation()
        #     block_list.extend(self.animation_blocks)
        # else:
        #     self.surface.blit(self.player.img, player_offset)
        for block in block_list:
            block_offset = block.hitbox.topleft + self.cam_offset
            self.surface.blit(block.img, block_offset)
            # outline_rect = pygame.Rect(block_offset, block.img.get_size())
            # pygame.draw.rect(self.surface, (0, 0, 0), outline_rect, 2)
        score_txt = self.FONT.render(str(self.max_score), False, self.palette[GROUND])
        self.surface.blit(score_txt, (5, 0))

    def death_animation(self, player):
        self.animation_frames -= 1
        if self.animation_frames == 0:
            self.running = False
            return
        self.animation_blocks = list()
        directions = [
            (1, 0),  # Right
            (math.cos(math.pi / 4), math.sin(math.pi / 4)),  # Top Right
            (0, 1),  # Up
            (-math.cos(math.pi / 4), math.sin(math.pi / 4)),  # Top Left
            (-1, 0),  # Left
            (-math.cos(math.pi / 4), -math.sin(math.pi / 4)),  # Bottom Left
            (0, -1),  # Down
            (math.cos(math.pi / 4), -math.sin(math.pi / 4))  # Bottom Right
        ]
        for i in range(8):
            block = Block(player.prev_pos, (20, 20), player.colour)
            dist = (60 - self.animation_frames)
            block.hitbox.move_ip(directions[i][0] * dist, directions[i][1] * dist)
            # self.surface.blit(block.img, block.hitbox)
            self.animation_blocks.append(block)


'''
2-Player level, adds player2 to player list
'''
class Level2P(Level):
    def __init__(self, game_screen, palette, is_hard=True):
        super().__init__(game_screen, palette, is_hard=False)
        self.player.hitbox.x -= WIDTH/4  # move player1 over
        self.player2 = Player2(((WIDTH - PLAYER_W) / 2 + WIDTH/4, HEIGHT), palette[LAVA])
        self.players.append(self.player2)


'''
AI agent level, no manual control
'''
class LevelAI(Level):
    def __init__(self, game_screen, palette, is_hard=True):
        # set to easy level difficulty
        super().__init__(game_screen, palette, is_hard=False)
        # replace player with AI agent
        self.player = PlayerBot(((WIDTH - PLAYER_W) / 2, HEIGHT), palette[PLAYER])
        self.players = [self.player]

    # override manual controls
    def update_players(self):
        for player in self.players:
            # decide what inputs to press
            left = right = up = down = False
            left, right, up, down = self.agent_safety(player)
            # apply inputs to player
            player.left = left
            player.right = right
            player.up = up
            player.down = down
            # update player direction vector
            player.update_dir()

    # random inputs
    def agent_rand(self, player):
        left = bool(random.getrandbits(1))
        right = not left
        up = bool(random.getrandbits(1))
        return left, right, up, False

    # move towards highest landed block
    def agent_top(self, player):
        error = 5
        left = right = up = False
        target = self.top_block
        if player.hitbox.centerx < (target.hitbox.centerx - error):
            right = True
        elif player.hitbox.centerx > (target.hitbox.centerx + error):
            left = True
        if player.grounded or player.is_wallcling:
            up = True
        return left, right, up, False

    # targets largest gap between falling blocks
    def agent_dodge(self, player):
        domain = [0] * int(WIDTH / 10)
        for block in self.blocks:
            # skip landed blocks
            if not block.gravity:
                continue
            # check falling blocks, mark array
            for i in range(int(block.hitbox.left / 10), int(block.hitbox.right / 10)):
                domain[i] = abs(block.hitbox.bottom - player.hitbox.top)

        print(*domain)
        target = self.find_gap(domain) * 10
        print(target)
        error = 5
        left = right = up = False
        if player.hitbox.centerx < (target - error):
            right = True
        elif player.hitbox.centerx > (target + error):
            left = True
        if player.is_wallcling:
            up = True
        return left, right, up, False

    def find_gap(self, arr):
        max_gap = 0
        curr_gap = 0
        target_x = -1
        for i in range(len(arr)):
            if arr[i] == 0:
                curr_gap += 1
            else:
                if curr_gap > max_gap:
                    max_gap = curr_gap
                    target_x = i - curr_gap // 2
                curr_gap = 0
        # gap might reach until RHS of screen
        if curr_gap > max_gap:
            target_x = len(arr) - curr_gap // 2
        return target_x

    # Evaluates region safety using falling blocks distance and lava distance
    def agent_safety(self, player):
        interval = 3
        #
        blocks_safety = [999] * int(WIDTH/interval)
        lava_safety = [0] * int(WIDTH/interval)
        lava_height = self.lava.hitbox.top
        for block in self.blocks:
            # landed blocks
            if not block.gravity:
                # if landed and above lava, mark ground as safe
                if block.hitbox.top < lava_height:
                    for i in range(int(block.hitbox.left/interval), int(block.hitbox.right/interval)):
                        lava_safety[i] = max(lava_safety[i], abs(block.hitbox.top - lava_height))
            # falling blocks
            else:
                # block above player
                if block.hitbox.bottom < player.hitbox.centery:
                    for i in range(int(block.hitbox.left / interval), int(block.hitbox.right / interval)):
                        blocks_safety[i] = min(blocks_safety[i], abs(block.hitbox.bottom - player.hitbox.top))
                # block below player
                else:
                    pass

        #print(*blocks_safety)
        #print(*lava_safety)

        target_x = self.find_safest(blocks_safety, lava_safety, interval)
        #print(target_x)
        # movement output
        error = 3
        left = right = up = False
        player_x = player.hitbox.centerx
        # always walljump
        if player.grounded or player.is_wallcling:
            up = True
        # player close enough to target
        if abs(player_x - target_x) < error:
            up = False
        else:
            # player left of target
            if player_x < target_x:
                right = (target_x - player_x) < (player_x + WIDTH - target_x)
                left = not right
            # player right of target
            else:
                left = (player_x - target_x) < (target_x + WIDTH - player_x)
                right = not left
        
        return left, right, up, False

    '''
    Find safest position on current map, return pos
    '''
    def find_safest(self, blocks_safety, lava_safety, interval):
        target_x = -1
        # total safety value
        block_weight = 1
        lava_weight = 1
        #total_safety = [(x * block_weight) + (y * lava_weight) for x, y in zip(blocks_safety, lava_safety)]
        total_safety = [min(x * block_weight, y * lava_weight) for x, y in zip(blocks_safety, lava_safety)]

        # calc group areas
        groups = []
        start_index = 0
        # (safety value, group length, starting index)
        for key, group in groupby(total_safety):
            length = len(list(group))
            groups.append((key, length, start_index))
            start_index += length

        # check first and last tuple, combine if same value (use modulo on index)

        # sort groups by value and length
        def custom_sort(tuple_item):
            return (-tuple_item[0], -tuple_item[1])
        sorted_groups = sorted(groups, key=custom_sort)

        # find safest group, must have length >= player width / interval
        best_safety = 0
        best_len = 0
        min_len = math.ceil(PLAYER_W / interval)
        for (safety, length, start) in sorted_groups:
            # already found safest group
            if safety < best_safety:
                break
            #
            if safety > best_safety:
                if length >= max(min_len, best_len):
                    target_x = start + (length // 2)
                    best_safety = safety
            #print(f"curr target: {target_x}")

        '''
        # safezone variables
        max_safety_val = max(total_safety)
        curr_gap_len = 0
        max_gap_len = 0
        #
        for i in range(len(total_safety)):
            # same zone
            if total_safety[i] == max_safety_val:
                curr_gap_len += 1
            # new zone
            else:
                if curr_gap_len > max_gap_len:
                    max_gap_len = curr_gap_len
                    target_x = i - curr_gap_len//2
                curr_gap_len = 0
        # gap might reach until RHS of screen
        if curr_gap_len > max_gap_len:
            target_x = len(total_safety) - curr_gap_len//2
        '''

        #DEBUGGING
        # for i in range(len(total_safety)):
        #     total_safety[i] = int(total_safety[i] / 100)
        # print(*total_safety)
        # print(f"target_x: {target_x, total_safety[target_x]}")
        return target_x * interval








