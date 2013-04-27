import pygame

import py2d.Math as m

import game
import game.constants as c
import game.util as u
import game.modes.swim.swarm as swarm

class SwimMode(game.Mode):

    def __init__(self, g):
        game.Mode.__init__(self, g)

        self.swarm_origin = swarm.Swarm()

    def update(self, time_elapsed):
        self.swarm_origin.position = self.game.mouse_pos

    def render(self):

        scr = self.game.screen

        scr.fill(c.BACKGROUND_COLOR)

        game.util.draw_pos_dir(scr, self.swarm_origin)
