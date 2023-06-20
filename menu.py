import pygame
from constants import *
import level

class Menu:
    def __init__(self, game_screen, palette):
        # attributes
        self.FONT = pygame.font.Font(FONT_STR, 30)
        self.surface = game_screen
        self.palette = palette
        # surfaces
        self.background = pygame.Surface((WIDTH, HEIGHT))
        self.solo_btn = pygame.Surface((WIDTH * 0.3, HEIGHT * 0.15))
        self.duo_btn = pygame.Surface((WIDTH * 0.3, HEIGHT * 0.15))
        self.ai_btn = pygame.Surface((WIDTH * 0.3, HEIGHT * 0.15))
        self.prac_btn = pygame.Surface((WIDTH * 0.3, HEIGHT * 0.15))
        self.cursor = pygame.Surface((5, 5))
        # hitboxes and positions
        self.background_hitbox = self.background.get_rect(topleft=(0, 0))
        self.solo_hitbox = self.solo_btn.get_rect(midtop=(WIDTH * 0.5, HEIGHT * 0.35))
        self.duo_hitbox = self.duo_btn.get_rect(midtop=self.solo_hitbox.bottomleft)
        self.ai_hitbox = self.ai_btn.get_rect(midtop=self.solo_hitbox.bottomright)
        self.prac_hitbox = self.prac_btn.get_rect(topleft=self.duo_hitbox.midbottom)
        self.cursor_hitbox = self.cursor.get_rect(center=(-1, -1))
        # colours
        self.background.fill(self.palette[SKY])
        self.solo_btn.fill(self.palette[BLOCK])
        self.duo_btn.fill(self.palette[BLOCK])
        self.ai_btn.fill(self.palette[BLOCK])
        self.prac_btn.fill(self.palette[BLOCK])
        self.cursor.fill(self.palette[PLAYER])
        # text
        self.solo_txt = self.FONT.render("SOLO", False, palette[GROUND])
        self.duo_txt = self.FONT.render("2-P", False, palette[GROUND])
        self.ai_txt = self.FONT.render("AI", False, palette[GROUND])
        self.prac_txt = self.FONT.render("WARMUP", False, palette[GROUND])
        self.title_txt = (pygame.font.Font(FONT_STR, 50)).render("ERUPTION", False, palette[GROUND])
        # text hitboxes
        self.solo_txt_hitbox = self.solo_txt.get_rect(center=self.solo_hitbox.center)
        self.duo_txt_hitbox = self.duo_txt.get_rect(center=self.duo_hitbox.center)
        self.ai_txt_hitbox = self.ai_txt.get_rect(center=self.ai_hitbox.center)
        self.prac_txt_hitbox = self.prac_txt.get_rect(center=self.prac_hitbox.center)
        self.title_txt_hitbox = self.title_txt.get_rect(centerx=WIDTH // 2, top=HEIGHT*0.1)


    def draw(self):
        # drawing
        self.surface.blit(self.background, self.background_hitbox)
        self.surface.blit(self.solo_btn, self.solo_hitbox)
        self.surface.blit(self.duo_btn, self.duo_hitbox)
        self.surface.blit(self.ai_btn, self.ai_hitbox)
        self.surface.blit(self.prac_btn, self.prac_hitbox)
        self.surface.blit(self.cursor, self.cursor_hitbox)

        self.surface.blit(self.solo_txt, self.solo_txt_hitbox)
        self.surface.blit(self.duo_txt, self.duo_txt_hitbox)
        self.surface.blit(self.ai_txt, self.ai_txt_hitbox)
        self.surface.blit(self.prac_txt, self.prac_txt_hitbox)

        self.surface.blit(self.title_txt, self.title_txt_hitbox)

    def update(self, keys, mouse_pos, mouse_btns):
        # update cursor pos
        self.cursor_hitbox = self.cursor.get_rect(center=mouse_pos)

        # check overlap
        # singleplayer button
        if self.solo_hitbox.collidepoint(mouse_pos):
            self.solo_btn.fill(self.palette[LAVA])
            if mouse_btns[0]:
                return level.Level(self.surface, self.palette)
        else:
            self.solo_btn.fill(self.palette[BLOCK])

        # doubles button
        if self.duo_hitbox.collidepoint(mouse_pos):
            self.duo_btn.fill(self.palette[LAVA])
            if mouse_btns[0]:
                return None
        else:
            self.duo_btn.fill(self.palette[BLOCK])

        # AI button
        if self.ai_hitbox.collidepoint(mouse_pos):
            self.ai_btn.fill(self.palette[LAVA])
            if mouse_btns[0]:
                return None
        else:
            self.ai_btn.fill(self.palette[BLOCK])

        # practice button
        if self.prac_hitbox.collidepoint(mouse_pos):
            self.prac_btn.fill(self.palette[LAVA])
            if mouse_btns[0]:
                return level.Level(self.surface, self.palette, False)
        else:
            self.prac_btn.fill(self.palette[BLOCK])

        return None

