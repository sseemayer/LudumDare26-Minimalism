import pygame

import py2d.Math as m

import game
import game.constants as c
import game.util as u

import swarm
import camera
import food
import predator
import game.world

class SwimMode(game.Mode):

    def __init__(self, g):
        game.Mode.__init__(self, g)

        self.swarm = swarm.Swarm(self, m.Vector(0, 0))
        self.camera = camera.Camera(self, position= c.SCREEN_DIMENSIONS/-2)
        self.mouse_pos_world = self.swarm.position

        self.foods = [food.Food(self, m.VECTOR_X * x * 10 + u.random_dir() * 30 ) for x in range(50, 100)]

        self.predators = [predator.Predator(self, m.VECTOR_X * 100 + m.VECTOR_Y * y * 100 + u.random_dir() * 30 ) for y in range(3, 10)]

        self.change_sector(c.START_SECTOR[0], c.START_SECTOR[1])

    def change_sector(self, x, y):
        self.sector_x = x
        self.sector_y = y

        self.color = game.world.WORLD.get_at((x, y))
        self.depth = game.world.depth((x,y))

    def update(self, time_elapsed):
        self.camera.update(time_elapsed)
        self.mouse_pos_world = self.game.mouse_pos + self.camera.position
        self.swarm.target_position = self.mouse_pos_world

        secX = c.START_SECTOR[0] + int(self.swarm.position.x / c.SECTOR_SIZE.x)
        secY = c.START_SECTOR[1] + int(self.swarm.position.y / c.SECTOR_SIZE.y)

        if secX != self.sector_x or secY != self.sector_y:
            self.change_sector(secX, secY)

        self.swarm.update(time_elapsed)

        for p in self.predators:
            p.update(time_elapsed)

    def render(self):

        scr = self.game.screen

        scr.fill(self.color)

        self.camera.render()
        self.swarm.render()

        for f in self.foods:
            f.render()

        for p in self.predators:
            p.render()


        game.world.render(scr, (0, 0), (self.sector_x, self.sector_y))
