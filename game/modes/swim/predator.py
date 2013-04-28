import pygame
from pygame.locals import *

import game
import game.util as u
import game.constants as c

import py2d.Math as m

import math
import random


class Predator(game.PhysicsEntity):
    frames = None

    def __init__(self, mode, position=m.Vector(0, 0), direction=m.Vector(0, 0)):
        super(Predator, self).__init__(mode, position, direction, max_velocity=c.PREDATOR_MAX_VELOCITY, max_angular_velocity=c.PREDATOR_MAX_ANGULAR_VELOCITY, velocity_decay=c.PREDATOR_VELOCITY_DECAY, angular_velocity_decay=c.PREDATOR_ANGULAR_VELOCITY_DECAY )

        if not Predator.frames:
            Predator.frames = [pygame.image.load("data/images/predator_{}.png".format(i)).convert_alpha() for i in range(8)]


        self.target = None
        self.anim_timer = random.uniform(0, len(Predator.frames)) * c.PREDATOR_ANIM_DELAY

        self.random_walk_direction = m.Vector(0, 0)
        self.new_random_walk_dir()

    def apply_force(self):


        # behavior:
        #
        # 1. position
        # a) go to closest fish
        # b) avoid other predators
        # c) random walk
        #
        # 2. angle
        # a) rotate so that we move into direction

        preys = [ f for f in self.mode.swarm.fishes if (f.position - self.position).length < c.PREDATOR_SENSES]
        if self.target:
            preys.append(self.target)

        go_to_prey = self.random_walk_direction
        if preys:
            new_target = sorted(preys, key=lambda p: (p.position - self.position).length_squared)[0]
            if self.target != new_target:
                self.mode.game.audio.play("attack")

            self.target = new_target

            go_to_prey = self.target.position - self.position

            if new_target.swarm.swarm_mode == -1:
                go_to_prey = go_to_prey * -1

        neighbors = [ p for p in self.mode.predators if (p.position - self.position).length < c.PREDATOR_REPEL_DISTANCE ]
        repel_sum = m.Vector(0, 0)
        for n in neighbors:
            repel = self.position - n.position
            repel_sum += repel * (c.PREDATOR_REPEL_STRENGTH / (1 + repel.length))

        self.target_direction = go_to_prey * c.PREDATOR_W_GO_TO_PREY + repel_sum * c.PREDATOR_W_REPEL
        self.target_direction = self.target_direction.clamp()

        self.target_angle = math.atan2(self.target_direction.y, self.target_direction.x)
        self.target_angle %= math.pi * 2

        self.target_rotation = u.angle_steer(self.target_angle, self.angle)

        self.angular_velocity -= self.target_rotation * c.PREDATOR_ANGULAR_ACCELERATION
        acc = m.Vector(math.cos(self.angle), math.sin(self.angle))

        acceleration = c.PREDATOR_HUNT_ACCELERATION if self.target else c.PREDATOR_ACCELERATION
        self.acceleration += acc *  (acc * self.target_direction.clamp()) * acceleration

    def new_random_walk_dir(self):
        self.random_walk_direction = u.random_dir() * c.PREDATOR_RANDOM_WALK_RADIUS

    def update(self, time_elapsed):
        game.PhysicsEntity.update(self, time_elapsed)

        if random.random() < time_elapsed * c.PREDATOR_RANDOM_WALK_CHANCE :
            self.new_random_walk_dir()


        self.anim_timer += time_elapsed * self.acceleration.length
        self.anim_timer %= c.PREDATOR_ANIM_DELAY * len(Predator.frames)


        self.max_velocity = c.PREDATOR_HUNT_MAX_VELOCITY if self.target else c.PREDATOR_MAX_VELOCITY


        if self.target:

            if self.target.food <= 0:
                self.target = None
                return

            target_distance = (self.target.position - self.position).length

            if target_distance  > c.PREDATOR_DEAGGRO_DISTANCE:
                p_deaggro = time_elapsed * c.PREDATOR_DEAGGRO_CHANCE * (1 - 1 / (1 + target_distance))
                if random.random() < p_deaggro:
                    self.target = None

            if target_distance < c.PREDATOR_EAT_DISTANCE:
                self.target.modify_food( -c.PREDATOR_EAT_DAMAGE)
                self.mode.game.audio.play("hurt")



    def render(self):
        scr = self.mode.game.screen
        cam = self.mode.camera.position


        frame = int(self.anim_timer / c.PREDATOR_ANIM_DELAY)

        sprite_stretch = pygame.transform.rotozoom(Predator.frames[frame], -self.angle / math.pi * 180, c.PREDATOR_SCALE)

        #sprite_stretch.fill(self.color, special_flags=BLEND_MULT)

        sprite_dim = m.Vector(sprite_stretch.get_width(), sprite_stretch.get_height())

        scr.blit(sprite_stretch, (self.position - cam - sprite_dim / 2).as_tuple())

        #u.draw_pos_dir(scr, self.position - cam, self.direction * 20, color=(255, 0, 0))

        #if self.target:
        #    u.draw_line(scr, self.position - cam, self.target.position - cam, color=(255, 0, 0))
