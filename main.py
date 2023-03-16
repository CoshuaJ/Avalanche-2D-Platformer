import pygame
from level import *
from player import *

'''
Avalanche clone by Josh Costa
Inspired by 'Avalanche' developed by The Game Homepage, found at: https://www.addictinggames.com/action/avalanche
Hard Mode WR: 953 by Me, 08/03/23
'''

# Initialize Pygame
pygame.init()

# display settings
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Avalanche")
clock = pygame.time.Clock()

# game data
START = 0
GAME_ON = 1
is_easy = False
game_state = START
PB_score = 0
last_score = 0
FONT = pygame.font.Font('retro.ttf', 30)

palette = rand_palette()
level = Level(screen, palette)

# main game loop
window_running = True
while window_running:
    # window logic
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            window_running = False
        elif event.type == pygame.KEYDOWN:
            # esc close game
            if event.key == pygame.K_ESCAPE:
                window_running = False
                continue
    # record current frame inputs
    keys = pygame.key.get_pressed()
    mouse_pos = pygame.mouse.get_pos()
    mouse_btns = pygame.mouse.get_pressed()
    # start menu
    if game_state == START:
        # surfaces
        background = pygame.Surface((WIDTH, HEIGHT))
        easy_btn = pygame.Surface((WIDTH * 0.6, HEIGHT * 0.15))
        hard_btn = pygame.Surface((WIDTH * 0.6, HEIGHT * 0.15))
        cursor = pygame.Surface((5, 5))
        # hitboxes and positions
        background_hitbox = background.get_rect(topleft=(0, 0))
        easy_hitbox = easy_btn.get_rect(topleft=(WIDTH * 0.2, HEIGHT * 0.5))
        hard_hitbox = hard_btn.get_rect(topleft=(WIDTH * 0.2, HEIGHT * 0.75))
        cursor_hitbox = cursor.get_rect(center=mouse_pos)
        # colours
        background.fill(palette[SKY])
        easy_btn.fill(palette[BLOCK])
        hard_btn.fill(palette[LAVA])
        cursor.fill(palette[PLAYER])
        # drawing
        screen.blit(background, background_hitbox)
        screen.blit(easy_btn, easy_hitbox)
        screen.blit(hard_btn, hard_hitbox)
        screen.blit(cursor, cursor_hitbox)
        # text
        pb_text = FONT.render("PB: " + str(PB_score), False, palette[GROUND])
        last_text = FONT.render("LAST: " + str(last_score), False, palette[GROUND])
        easy_txt = FONT.render("EASY", False, palette[GROUND])
        hard_txt = FONT.render("HARD", False, palette[GROUND])
        screen.blit(pb_text, (WIDTH-180, 0))
        screen.blit(last_text, (5, 0))
        screen.blit(easy_txt, (easy_hitbox.x + 130, easy_hitbox.y + 35))
        screen.blit(hard_txt, (hard_hitbox.x + 130, hard_hitbox.y + 35))
        # click btn
        if mouse_btns[0]:
            if easy_hitbox.collidepoint(mouse_pos):
                level = EasyLevel(screen, palette)
                game_state = GAME_ON
                is_easy = True
            elif hard_hitbox.collidepoint(mouse_pos):
                level = Level(screen, palette)
                game_state = GAME_ON
                is_easy = False
        if keys[pygame.K_r]:
            if is_easy:
                level = EasyLevel(screen, palette)
            else:
                level = Level(screen, palette)
            game_state = GAME_ON

    # level logic
    elif game_state == GAME_ON:
        if not level.running:
            # PB check
            if level.max_score > PB_score:
                PB_score = level.max_score
            last_score = int(level.max_score)
            game_state = START
            palette = rand_palette()
        else:
            # reset key
            if keys[pygame.K_r]:
                if is_easy:
                    level = EasyLevel(screen, palette)
                else:
                    level = Level(screen, palette)
            level.update()
            level.draw()

    # error screen
    else:
        screen.fill('black')
        print("game_state invalid")
        window_running = False

    # Update the display
    pygame.display.update()
    # caps framerate
    clock.tick(FPS)

# close Pygame
pygame.quit()
