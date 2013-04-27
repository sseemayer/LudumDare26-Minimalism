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
            pygame.draw.line(self.world, (255, 0, 0), x_from, x_to)

        self.world = pygame.transform.scale(self.world, (int(self.world.get_width() * c.WORLDMAP_SCALE), int(self.world.get_height() * c.WORLDMAP_SCALE)) )
        self.world_size = m.Vector(self.world.get_width(), self.world.get_height())

        self.header_font = pgf.PyGameHieroFont("data/fonts/AmaticSC_52.fnt")
        self.main_font = pgf.PyGameHieroFont("data/fonts/Antic_22.fnt")

        self.surf_game_over = self.header_font.render("Travel Log")
        self.surf_keys = self.main_font.render("(R): Retry", color=(255,0,0))

        overlay_pos = c.SCREEN_DIMENSIONS / 2 - c.GAMEOVER_DIMENSIONS / 2

    def update(self, time_elapsed):
        if self.game.keys[K_r]:
            self.game.mode = game.modes.swim.mode.SwimMode(self.game)



    def render(self):

        self.swim_mode.render()

        scr = self.game.screen

        overlay_pos = c.SCREEN_DIMENSIONS / 2 - c.GAMEOVER_DIMENSIONS / 2

        scr.blit(self.overlay_surf, overlay_pos.as_tuple())

        scr.blit(self.surf_game_over, m.Vector(c.SCREEN_DIMENSIONS.x / 2 - self.surf_game_over.get_width() / 2, overlay_pos.y + 20).as_tuple())
        scr.blit(self.world, m.Vector(c.SCREEN_DIMENSIONS.x / 2 - self.world_size.x / 2, overlay_pos.y + 90).as_tuple())

        scr.blit(self.surf_keys, m.Vector(overlay_pos.x + 10, overlay_pos.y + c.GAMEOVER_DIMENSIONS.y - 40).as_tuple())

