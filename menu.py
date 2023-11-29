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
        self.solo_btn = Button((WIDTH * 0.5, HEIGHT * 0.35), "SOLO", self.palette)
        self.duo_btn = Button(self.solo_btn.rect.bottomleft, "2-P", self.palette)
        self.ai_btn = Button(self.solo_btn.rect.bottomright, "AI", self.palette)
        self.prac_btn = Button(self.duo_btn.rect.bottomright, "WARMUP", self.palette)
        self.buttons = [self.solo_btn, self.duo_btn, self.ai_btn, self.prac_btn]
        self.cursor = pygame.Surface((5, 5))
        # hitboxes and positions
        self.background_hitbox = self.background.get_rect(topleft=(0, 0))
        self.cursor_hitbox = self.cursor.get_rect(center=(-1, -1))
        # colours
        self.background.fill(self.palette[SKY])
        self.cursor.fill(self.palette[PLAYER])
        # text
        self.title_txt = (pygame.font.Font(FONT_STR, 50)).render("AVALANCHE", False, palette[GROUND])
        # text hitboxes
        self.title_txt_hitbox = self.title_txt.get_rect(centerx=WIDTH // 2, top=HEIGHT*0.1)


    def draw(self):
        # drawing
        self.surface.blit(self.background, self.background_hitbox)
        for button in self.buttons:
            button.draw(self.surface)
        self.surface.blit(self.title_txt, self.title_txt_hitbox)
        self.surface.blit(self.cursor, self.cursor_hitbox)

    def update(self, keys, mouse_pos, mouse_btns):
        # update cursor pos
        self.cursor_hitbox = self.cursor.get_rect(center=mouse_pos)
        # check button collisions
        for button in self.buttons:
            button.update_colours()
            if button.rect.collidepoint(mouse_pos) and mouse_btns[0]:
                # SOLO
                if button == self.solo_btn:
                    return Leveltype.SOLO
                # SOLO
                elif button == self.duo_btn:
                    return Leveltype.DUO
                # AI
                elif button == self.ai_btn:
                    return Leveltype.AI
                # PRAC
                elif button == self.prac_btn:
                    return Leveltype.PRAC
                else:
                    return None

        return None


class Button(pygame.sprite.Sprite):
    def __init__(self, position, text, palette):
        super().__init__()
        self.image = pygame.Surface((WIDTH * 0.3, HEIGHT * 0.15))
        self.rect = self.image.get_rect(midtop=position)
        self.FONT = pygame.font.Font(FONT_STR, 30)
        self.text = self.FONT.render(text, False, palette[PLAYER])
        self.text_rect = self.text.get_rect(center=self.rect.center)
        self.palette = palette
        self.update_colours()

    def update_colours(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.image.fill(self.palette[LAVA])
        else:
            self.image.fill(self.palette[BLOCK])

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        surface.blit(self.text, self.text_rect)

