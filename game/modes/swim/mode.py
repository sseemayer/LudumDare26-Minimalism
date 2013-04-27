import pygame

import py2d.Math as m

import game
import game.constants as c
import game.util as u
import swarm
import camera
import food

class SwimMode(game.Mode):

    def __init__(self, g):
        game.Mode.__init__(self, g)

        self.swarm = swarm.Swarm(self, c.SCREEN_DIMENSIONS / 2)
        self.camera = camera.Camera(self)
        self.mouse_pos_world = self.swarm.position

        self.foods = [food.Food(self, m.VECTOR_X * x * 100) for x in range(5, 10)]

    def update(self, time_elapsed):
        self.camera.update(time_elapsed)
        self.mouse_pos_world = self.game.mouse_pos + self.camera.position
        self.swarm.target_position = self.mouse_pos_world


        self.swarm.update(time_elapsed)


    def render(self):

        scr = self.game.screen

        scr.fill(c.BACKGROUND_COLOR)

        self.camera.render()
        self.swarm.render()

        for f in self.foods:
            f.render()
