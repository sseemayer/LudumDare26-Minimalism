import pygame
from pygame.locals import *

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
import decoration
import trawl

import game.world

import game.modes.death.mode

class SwimMode(game.Mode):

    def __init__(self, g):
        game.Mode.__init__(self, g)


        self.sector_history = []
        self.distance_travelled = 0
        self.food_eaten = 0
        self.fishies_spawned = c.START_FISHES
        self.fishies_max = c.START_FISHES


        self.swarm = swarm.Swarm(self, c.SECTOR_SIZE / 2)
        self.camera = camera.Camera(self, position = self.swarm.position-c.SCREEN_DIMENSIONS/2)
        self.mouse_pos_world = self.swarm.position

        self.foods = []
        self.predators = []
        self.shore = []
        self.decorations = []
        self.trawl = None

        self.active_sectors = set()
        self.change_sector(c.START_SECTOR[0], c.START_SECTOR[1])

        around_start = lambda e: (e.position - self.swarm.position).length > c.START_SAFEZONE
        self.predators = [ p for p in self.predators if around_start(p)]

        self.cursor = pygame.image.load("data/images/cursor.png").convert_alpha()
        self.cursor_size = m.Vector(self.cursor.get_width(), self.cursor.get_height())



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

            self.decorations.append(decoration.Decoration(self, x*y, tl + c.SECTOR_SIZE/2 ))

            #print("Sector {}, {} (depth {}): Added {} predators and {} food items".format(x, y, depth, n_predators, n_food))

        else:
            self.shore.append(shore.Shore(self, tl, game.world.data['WORLD'].get_at((x,y))))

    def change_sector(self, x, y):

        if (x - c.GOAL_SECTOR[0]) ** 2 + (y - c.GOAL_SECTOR[1]) ** 2 < c.GOAL_RADIUS ** 2:
            self.game.win(self)

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
        self.decorations = [d for d in self.decorations if in_range(d)]


        #print("foods: {} (before: {}), predators: {} (before: {})".format(len(self.foods), nf, len(self.predators), np))

        self.active_sectors = newactive_sectors

        self.sector_x = x
        self.sector_y = y

        self.color = game.world.data['WORLD'].get_at((x, y))
        self.depth = game.world.depth((x,y))

        self.sector_history.append((x, y))

        if not self.trawl:
            p_trawl = c.TRAWL_PROBABILITY(self.depth)
            if random.random() < p_trawl:
                self.spawn_trawl()


    def spawn_trawl(self):
        trawl_dir = u.random_dir(1, 1)
        self.trawl = trawl.Trawl(self, self.swarm.position + trawl_dir * c.TRAWL_DISTANCE, trawl_dir * -1)


    def get_sector(self, e):
        return (
            int(math.floor(e.position.x / c.SECTOR_SIZE[0])) + c.START_SECTOR[0],
            int(math.floor(e.position.y / c.SECTOR_SIZE[1])) + c.START_SECTOR[1]
        )


    def update(self, time_elapsed):

        if self.game.keys[K_a]:
            self.swarm.swarm_mode = -1

        if self.game.keys[K_s]:
            self.swarm.swarm_mode = 0

        if self.game.keys[K_d]:
            self.swarm.swarm_mode = 1

        if self.game.keys[K_t]:
            self.spawn_trawl()

        self.camera.update(time_elapsed)
        self.mouse_pos_world = self.game.mouse_pos + self.camera.position
        self.swarm.target_position = self.mouse_pos_world


        secX, secY = self.get_sector(self.swarm)

        if secX != self.sector_x or secY != self.sector_y:
            self.change_sector(secX, secY)

        self.swarm.update(time_elapsed)

        if self.trawl:
            self.trawl.update(time_elapsed)

            if (self.trawl.position  - self.swarm.position).length > 10 * c.TRAWL_DISTANCE:
                self.trawl = None

        for p in self.predators:
            p.update(time_elapsed)


        if not self.swarm.fishes:
            self.game.die(self)

    def render(self):

        scr = self.game.screen

        scr.fill(self.color)

        for d in self.decorations:
            d.render()

        self.camera.render()

        for s in self.shore:
            s.render()

        for f in self.foods:
            f.render()

        for p in self.predators:
            p.render()

        self.swarm.render()

        if self.trawl:
            self.trawl.render()

        if self.swarm.fishes:
            self.render_gui()

    def render_gui(self):
        scr = self.game.screen
        cam = self.camera.position

        tl = m.Vector(c.SECTOR_SIZE.x * (self.sector_x - c.START_SECTOR[0]), c.SECTOR_SIZE.y * (self.sector_y-c.START_SECTOR[1])) - cam

        pygame.draw.rect(scr, (255, 255, 255), ((9, 9), (game.world.WORLD_WINDOW[0] + 2, game.world.WORLD_WINDOW[1] + 2)))
        game.world.render(scr, (10, 10), (self.sector_x, self.sector_y))

        scr.blit(self.cursor, (self.mouse_pos_world - cam - self.cursor_size / 2).as_tuple())

        #u.draw_line(scr, tl, m.Vector(tl.x + c.SECTOR_SIZE.x, tl.y))
        #u.draw_line(scr, m.Vector(tl.x, tl.y + c.SECTOR_SIZE.y), m.Vector(tl.x + c.SECTOR_SIZE.x, tl.y + c.SECTOR_SIZE.y))
        #u.draw_line(scr, tl, m.Vector(tl.x, tl.y + c.SECTOR_SIZE.y))
        #u.draw_line(scr, m.Vector(tl.x + c.SECTOR_SIZE.x, tl.y), m.Vector(tl.x + c.SECTOR_SIZE.x, tl.y + c.SECTOR_SIZE.y))
