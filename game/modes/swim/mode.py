import pygame
import itertools
import random
import math

import py2d.Math as m

import game
import game.constants as c
import game.util as u

import swarm
import camera
import food
import predator
import shore
import game.world

import game.modes.death.mode

class SwimMode(game.Mode):

    def __init__(self, g):
        game.Mode.__init__(self, g)

        self.swarm = swarm.Swarm(self, c.SECTOR_SIZE / 2)
        self.camera = camera.Camera(self, position = self.swarm.position-c.SCREEN_DIMENSIONS/2)
        self.mouse_pos_world = self.swarm.position

        self.foods = []
        self.predators = []
        self.shore = []

        self.active_sectors = set()
        self.change_sector(c.START_SECTOR[0], c.START_SECTOR[1])

        around_start = lambda e: (e.position - self.swarm.position).length > c.START_SAFEZONE
        self.predators = [ p for p in self.predators if around_start(p)]

    def die(self, message="All your fishies are dead :("):
        self.game.mode = game.modes.death.mode.DeathMode(self.game, self, message)

    def fill_sector(self, x, y):

        tl = m.Vector(c.SECTOR_SIZE.x * (x - c.START_SECTOR[0]), c.SECTOR_SIZE.y * (y-c.START_SECTOR[1]))
        depth = game.world.depth((x, y))

        if depth:
            n_predators = c.SECTOR_PREDATORS(depth)
            n_food = c.SECTOR_FOOD(depth)

            def uniform_point(x_min = tl.x, x_max=tl.x + c.SECTOR_SIZE.x, y_min=tl.y, y_max=tl.y + c.SECTOR_SIZE.y):
                return m.Vector(random.uniform(x_min, x_max), random.uniform(y_min, y_max))

            self.predators.extend(predator.Predator(self, uniform_point()) for _ in range(n_predators))
            self.foods.extend(food.Food(self, uniform_point()) for _ in range(n_food))

            #print("Sector {}, {} (depth {}): Added {} predators and {} food items".format(x, y, depth, n_predators, n_food))

        else:
            self.shore.append(shore.Shore(self, tl, game.world.WORLD.get_at((x,y))))

    def change_sector(self, x, y):

        newactive_sectors = set(itertools.product(
            range(x - c.SIMULATION_RADIUS, x + c.SIMULATION_RADIUS + 1),
            range(y - c.SIMULATION_RADIUS, y + c.SIMULATION_RADIUS + 1)
        ))

        add_sectors = newactive_sectors.difference(self.active_sectors)
        for i, j in add_sectors:
                self.fill_sector(i, j)


        in_range = lambda e: self.get_sector(e) in newactive_sectors

        nf = len(self.foods)
        np = len(self.predators)
        self.foods = [f for f in self.foods if in_range(f)]
        self.predators = [p for p in self.predators if in_range(p) or p.target]


        #print("foods: {} (before: {}), predators: {} (before: {})".format(len(self.foods), nf, len(self.predators), np))

        self.active_sectors = newactive_sectors

        self.sector_x = x
        self.sector_y = y

        self.color = game.world.WORLD.get_at((x, y))
        self.depth = game.world.depth((x,y))


        self.distance_travelled = 0
        self.food_eaten = 0
        self.fishies_spawned = c.START_FISHES
        self.fishies_max = c.START_FISHES


    def get_sector(self, e):
        return (
            int(math.floor(e.position.x / c.SECTOR_SIZE[0])) + c.START_SECTOR[0],
            int(math.floor(e.position.y / c.SECTOR_SIZE[1])) + c.START_SECTOR[1]
        )


    def update(self, time_elapsed):
        self.camera.update(time_elapsed)
        self.mouse_pos_world = self.game.mouse_pos + self.camera.position
        self.swarm.target_position = self.mouse_pos_world


        secX, secY = self.get_sector(self.swarm)

        if secX != self.sector_x or secY != self.sector_y:
            self.change_sector(secX, secY)

        self.swarm.update(time_elapsed)

        for p in self.predators:
            p.update(time_elapsed)


        if not self.swarm.fishes:
            self.die()

    def render(self):

        scr = self.game.screen

        scr.fill(self.color)

        self.camera.render()
        self.swarm.render()

        for s in self.shore:
            s.render()

        for f in self.foods:
            f.render()

        for p in self.predators:
            p.render()

        self.render_gui()

    def render_gui(self):
        scr = self.game.screen
        cam = self.camera.position

        tl = m.Vector(c.SECTOR_SIZE.x * (self.sector_x - c.START_SECTOR[0]), c.SECTOR_SIZE.y * (self.sector_y-c.START_SECTOR[1])) - cam

        game.world.render(scr, (0, 0), (self.sector_x, self.sector_y))

        u.draw_line(scr, tl, m.Vector(tl.x + c.SECTOR_SIZE.x, tl.y))
        u.draw_line(scr, m.Vector(tl.x, tl.y + c.SECTOR_SIZE.y), m.Vector(tl.x + c.SECTOR_SIZE.x, tl.y + c.SECTOR_SIZE.y))
        u.draw_line(scr, tl, m.Vector(tl.x, tl.y + c.SECTOR_SIZE.y))
        u.draw_line(scr, m.Vector(tl.x + c.SECTOR_SIZE.x, tl.y), m.Vector(tl.x + c.SECTOR_SIZE.x, tl.y + c.SECTOR_SIZE.y))
