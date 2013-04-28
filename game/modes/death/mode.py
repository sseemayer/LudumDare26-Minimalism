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


import game.modes.worldmap.mode

class DeathMode(game.Mode):

    def __init__(self, g, swim_mode, message):
        game.Mode.__init__(self, g)

        self.swim_mode = swim_mode
        self.message = message

        self.overlay_surf = pygame.Surface(c.GAMEOVER_DIMENSIONS.as_tuple(), flags=SRCALPHA)
        self.overlay_surf.fill((0,0,0,200))

        self.fishbones = pygame.image.load("data/images/fishbones.png")
        self.fishbones = pygame.transform.scale(self.fishbones, (self.fishbones.get_width() * 4, self.fishbones.get_height() * 4) )
        self.fishbones_size = m.Vector(self.fishbones.get_width(), self.fishbones.get_height())

        self.header_font = pgf.PyGameHieroFont("data/fonts/AmaticSC_52.fnt")
        self.main_font = pgf.PyGameHieroFont("data/fonts/Antic_22.fnt")

        self.surf_game_over = self.header_font.render("Game Over")
        self.surf_message = self.main_font.render(self.message)

        self.surf_keys = self.main_font.render("(L): Travel Log, (R): Retry", color=(255,0,0))

        overlay_pos = c.SCREEN_DIMENSIONS / 2 - c.GAMEOVER_DIMENSIONS / 2

        g_rect = pygame.Rect((overlay_pos[0], overlay_pos[1] + 200), (c.GAMEOVER_DIMENSIONS.x, c.GAMEOVER_DIMENSIONS.y - 250 ))

        stats = {
            "distance": self.swim_mode.distance_travelled,
            "food": self.swim_mode.food_eaten,
            "fishies": self.swim_mode.fishies_spawned,
            "fishies_max": self.swim_mode.fishies_max
        }

        self.g_stats = glyph.Glyph(g_rect, bkg=pygame.Color(0,0,0,0), font=self.main_font)
        self.g_stats.image = pygame.Surface(g_rect.size, flags=SRCALPHA)
        self.g_stats.image.fill(pygame.Color(0,0,0,0))
        self.g_stats.input("Before dying, you have travelled {distance} m, eaten {food} kg of food and had {fishies} fishies, {fishies_max} at one time.".format(**stats))
        self.g_stats.update()


    def update(self, time_elapsed):

        if self.game.keys[K_l]:
            self.game.mode = game.modes.worldmap.mode.WorldmapMode(self.game, self.swim_mode)

        if self.game.keys[K_r]:
            self.game.mode = game.modes.swim.mode.SwimMode(self.game)

    def render(self):

        self.swim_mode.render()

        scr = self.game.screen

        overlay_pos = c.SCREEN_DIMENSIONS / 2 - c.GAMEOVER_DIMENSIONS / 2

        scr.blit(self.overlay_surf, overlay_pos.as_tuple())

        scr.blit(self.surf_game_over, m.Vector(c.SCREEN_DIMENSIONS.x / 2 - self.surf_game_over.get_width() / 2, overlay_pos.y + 20).as_tuple())
        scr.blit(self.fishbones, m.Vector(c.SCREEN_DIMENSIONS.x / 2 - self.fishbones_size.x / 2, overlay_pos.y + 90).as_tuple())
        scr.blit(self.surf_message, m.Vector(c.SCREEN_DIMENSIONS.x / 2 - self.surf_message.get_width() / 2, overlay_pos.y + 150).as_tuple())
        scr.blit(self.g_stats.image, m.Vector(c.SCREEN_DIMENSIONS.x / 2 - self.g_stats.image.get_width() / 2, overlay_pos.y + 200).as_tuple())

        scr.blit(self.surf_keys, m.Vector(overlay_pos.x + 10, overlay_pos.y + c.GAMEOVER_DIMENSIONS.y - 40).as_tuple())
