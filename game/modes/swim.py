import pygame

import py2d.Math as m

import game.constants as c

import game.mode
import game.entity
import game.util

class SwimMode(game.mode.Mode):

    def __init__(self, g):
        game.mode.Mode.__init__(self, g)

        self.swarm_origin = game.entity.Entity()

    def update(self, time_elapsed):
        self.swarm_origin.position = self.game.mouse_pos

    def render(self):

        scr = self.game.screen

        scr.fill(c.BACKGROUND_COLOR)

        game.util.draw_pos_dir(scr, self.swarm_origin)
