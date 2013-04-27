import pygame
from pygame.locals import *

import itertools
import random
import math

import py2d.Math as m

import game
import game.constants as c
import game.util as u

import game.modes.swim.mode

import pyhiero.pygamefont as pgf

class MenuMode(game.Mode):

    def __init__(self, g):
        game.Mode.__init__(self, g)


        self.background = pygame.image.load("data/images/splash_bg.png")
        self.cursor = pygame.image.load("data/images/cursor.png")
        self.button = pygame.image.load("data/images/button.png")
        self.button_hover = pygame.image.load("data/images/button_hover.png")
        self.logo = pygame.image.load("data/images/logo.png")
        self.logo_blur = pygame.image.load("data/images/logo_blur.png")
        self.logo_blur.fill((0,0,0), special_flags = BLEND_MULT)

        self.main_font = pgf.PyGameHieroFont("data/fonts/Antic_22.fnt")


        self.button_size = m.Vector(self.button.get_width(), self.button.get_height())

        def play():
            self.game.mode = game.modes.swim.mode.SwimMode(self.game)

        def instructions():
            print("instructions")

        def about():
            print("about")

        self.buttons = [
            {"title": "Play", "action": play},
            {"title": "Instructions", "action": instructions},
            {"title": "About", "action": about},
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
            btn['pos'] = m.Vector(c.SCREEN_DIMENSIONS.x / 2, 230 + 60 * i)


        self.selected_button = None

        #self.surf_game_over = self.header_font.render("Travel Log")
        #self.surf_keys = self.main_font.render("(R): Retry", color=(255,0,0))


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


        scr.blit(self.cursor, (self.game.mouse_pos - m.Vector(self.cursor.get_width() / 2, self.cursor.get_height() / 2)).as_tuple())

        #scr.blit(self.surf_game_over, m.Vector(c.SCREEN_DIMENSIONS.x / 2 - self.surf_game_over.get_width() / 2, overlay_pos.y + 20).as_tuple())

