import game
import game.util as u
import game.constants as c

import py2d.Math as m
import math

import fish

class Food(game.PhysicsEntity):

    def __init__(self, mode, position=m.Vector(0, 0), direction=m.Vector(0, 0), nutrition_value=c.FOOD_NUTRITION_VALUE):
        super(Food, self).__init__(mode, position, direction)

        self.nutrition_value = nutrition_value


    def apply_force(self):
        pass

    def update(self, time_elapsed):
        pass

    def render(self):
        scr = self.mode.game.screen
        cam = self.mode.camera.position
        u.draw_cross(scr, self.position - cam, color=(255, 255, 0), radius = math.sqrt(self.nutrition_value))
