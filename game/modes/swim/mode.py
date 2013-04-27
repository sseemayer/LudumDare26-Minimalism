import pygame

import py2d.Math as m

import game
import game.constants as c
import game.util as u
import swarm

class SwimMode(game.Mode):

    def __init__(self, g):
        game.Mode.__init__(self, g)

        self.swarm = swarm.Swarm(self, c.SCREEN_DIMENSIONS / 2)

    def update(self, time_elapsed):
        self.swarm.target_position = self.game.mouse_pos

        self.swarm.update(time_elapsed)

    def render(self):

        scr = self.game.screen

        scr.fill(c.BACKGROUND_COLOR)

        self.swarm.render()
