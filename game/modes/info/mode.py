import pygame
from pygame.locals import *

import itertools
import random
import math

import py2d.Math as m

import game
import game.constants as c
import game.util as u

import game.world

import pyhiero.pygamefont as pgf
import glyph

class InfoMode(game.Mode):

    def __init__(self, g, info_surf):
        game.Mode.__init__(self, g)

        self.background = pygame.image.load("data/images/splash_bg.png").convert()
        self.info_surf = info_surf

        self.main_font = pgf.PyGameHieroFont("data/fonts/Antic_22.fnt")

        self.cursor = pygame.image.load("data/images/cursor.png").convert_alpha()
        self.cursor_size = m.Vector(self.cursor.get_width(), self.cursor.get_height())

        self.button = pygame.image.load("data/images/button.png").convert_alpha()
        self.button_hover = pygame.image.load("data/images/button_hover.png").convert_alpha()
        self.button_size = m.Vector(self.button.get_width(), self.button.get_height())

        self.logo = pygame.image.load("data/images/logo.png").convert_alpha()
        self.logo_blur = pygame.image.load("data/images/logo_blur.png").convert_alpha()
        self.logo_blur.fill((0,0,0), special_flags = BLEND_MULT)


        def menu():
            self.game.mode = game.modes.menu.mode.MenuMode(self.game)

        self.buttons = [
            {"title": "Main Menu", "action": menu}
        ]

        for i, btn in enumerate(self.buttons):
            surf = pygame.Surface(self.button_size.as_tuple(), flags=SRCALPHA)
            surf_shadow = pygame.Surface(self.button_size.as_tuple(), flags=SRCALPHA)

            hsurf = pygame.Surface(self.button_size.as_tuple(), flags=SRCALPHA)
            hsurf_shadow = pygame.Surface(self.button_size.as_tuple(), flags=SRCALPHA)

            surf.blit(self.button, (0, 0))
            hsurf.blit(self.button_hover, (0, 0))

            txt = self.main_font.render(btn['title'])
            surf.blit(txt, (surf.get_width() / 2 - txt.get_width() / 2, surf.get_height() / 2 - txt.get_height() / 2))
            hsurf.blit(txt, (hsurf.get_width() / 2 - txt.get_width() / 2, hsurf.get_height() / 2 - txt.get_height() / 2), special_flags = BLEND_RGBA_SUB)

            surf_shadow.blit(surf, (0,0))
            hsurf_shadow.blit(hsurf, (0,0))
            surf_shadow.fill((0,0,0), special_flags=BLEND_MULT)
            hsurf_shadow.fill((0,0,0), special_flags=BLEND_MULT)

            btn['surf'] = surf
            btn['surf_shadow'] = surf_shadow
            btn['hsurf'] = hsurf
            btn['hsurf_shadow'] = hsurf_shadow
            btn['pos'] = m.Vector(self.button_size.x / 2 + 20 + (10 + self.button_size.x) * i, c.SCREEN_DIMENSIONS.y - self.button_size.y )


        self.selected_button = None

        overlay_pos = c.SCREEN_DIMENSIONS / 2 - c.GAMEOVER_DIMENSIONS / 2


    def click(self):
        if self.selected_button != None:
            self.buttons[self.selected_button]['action']()

    def update(self, time_elapsed):

        self.selected_button = None

        for i, btn in enumerate(self.buttons):
            btn_tl = btn['pos'] - self.button_size / 2
            btn_br = btn['pos'] + self.button_size / 2

            if self.game.mouse_pos.x >= btn_tl.x and self.game.mouse_pos.x <= btn_br.x and self.game.mouse_pos.y >= btn_tl.y and self.game.mouse_pos.y <= btn_br.y:
                   self.selected_button = i
                   break

    def render(self):
        scr = self.game.screen

        scr.blit(self.background, (0,0))
        scr.blit(self.info_surf, (0,0))


        logo_pos = m.Vector(c.SCREEN_DIMENSIONS.x / 2, 100)

        shadow = (c.SCREEN_DIMENSIONS / 2 - self.game.mouse_pos) * 0.1

        scr.blit(self.logo_blur, (logo_pos + shadow - m.Vector(self.logo_blur.get_width(), self.logo_blur.get_height()) / 2).as_tuple())
        scr.blit(self.logo, (logo_pos - m.Vector(self.logo.get_width(), self.logo.get_height()) / 2).as_tuple())

        for i, btn in enumerate(self.buttons):
            if self.selected_button == i:
                scr.blit(btn['hsurf_shadow'], (btn['pos'] + shadow - self.button_size / 2).as_tuple())
                scr.blit(btn['hsurf'], (btn['pos'] - self.button_size / 2).as_tuple())
            else:

                scr.blit(btn['surf_shadow'], (btn['pos'] + shadow - self.button_size / 2).as_tuple())
                scr.blit(btn['surf'], (btn['pos'] - self.button_size / 2).as_tuple())

        scr.blit(self.cursor, (self.game.mouse_pos - self.cursor_size / 2).as_tuple())
