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

class WorldmapMode(game.Mode):

    def __init__(self, g, swim_mode):
        game.Mode.__init__(self, g)

        self.swim_mode = swim_mode

        self.overlay_surf = pygame.Surface(c.GAMEOVER_DIMENSIONS.as_tuple(), flags=SRCALPHA)
        self.overlay_surf.fill((0,0,0,200))


        self.world = pygame.image.load("data/images/world.png")

        for x_from, x_to in zip(self.swim_mode.sector_history, self.swim_mode.sector_history[1:]):
            pygame.draw.line(self.world, (255, 128, 0), x_from, x_to)

        self.world = pygame.transform.scale(self.world, (int(self.world.get_width() * c.WORLDMAP_SCALE), int(self.world.get_height() * c.WORLDMAP_SCALE)) )
        self.world_size = m.Vector(self.world.get_width(), self.world.get_height())

        self.header_font = pgf.PyGameHieroFont("data/fonts/AmaticSC_52.fnt")
        self.main_font = pgf.PyGameHieroFont("data/fonts/Antic_22.fnt")

        self.surf_game_over = self.header_font.render("Travel Log")
        self.surf_keys = self.main_font.render("(R): Retry", color=(255,0,0))

        self.cursor = pygame.image.load("data/images/cursor.png")
        self.cursor_size = m.Vector(self.cursor.get_width(), self.cursor.get_height())


        self.button = pygame.image.load("data/images/button.png")
        self.button_hover = pygame.image.load("data/images/button_hover.png")
        self.button_size = m.Vector(self.button.get_width(), self.button.get_height())

        def menu():
            self.game.mode = game.modes.menu.mode.MenuMode(self.game)

        def retry():
            self.game.mode = game.modes.swim.mode.SwimMode(self.game)

        def stats():
            self.game.mode = game.modes.death.mode.DeathMode(self.game, self.swim_mode)

        self.buttons = [
            {"title": "Main Menu", "action": menu},
            {"title": "Retry", "action": retry},
            {"title": "Statistics", "action": stats}
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
            btn['pos'] = m.Vector(self.button_size.x / 2 + 20 + (10 + self.button_size.x) * i, c.SCREEN_DIMENSIONS.y / 2 + c.GAMEOVER_DIMENSIONS.y / 2 - self.button_size.y )


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

        self.swim_mode.render()

        scr = self.game.screen

        overlay_pos = c.SCREEN_DIMENSIONS / 2 - c.GAMEOVER_DIMENSIONS / 2

        scr.blit(self.overlay_surf, overlay_pos.as_tuple())

        scr.blit(self.surf_game_over, m.Vector(c.SCREEN_DIMENSIONS.x / 2 - self.surf_game_over.get_width() / 2, overlay_pos.y + 20).as_tuple())
        scr.blit(self.world, m.Vector(c.SCREEN_DIMENSIONS.x / 2 - self.world_size.x / 2, overlay_pos.y + 90).as_tuple())

        shadow = (c.SCREEN_DIMENSIONS / 2 - self.game.mouse_pos) * 0.1
        for i, btn in enumerate(self.buttons):
            if self.selected_button == i:
                scr.blit(btn['hsurf_shadow'], (btn['pos'] + shadow - self.button_size / 2).as_tuple())
                scr.blit(btn['hsurf'], (btn['pos'] - self.button_size / 2).as_tuple())
            else:

                scr.blit(btn['surf_shadow'], (btn['pos'] + shadow - self.button_size / 2).as_tuple())
                scr.blit(btn['surf'], (btn['pos'] - self.button_size / 2).as_tuple())

        scr.blit(self.cursor, (self.game.mouse_pos - self.cursor_size / 2).as_tuple())
