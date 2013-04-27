import game
import game.util as u
import game.constants as c

import py2d.Math as m

import math
import random

class Predator(game.PhysicsEntity):

    def __init__(self, mode, position=m.Vector(0, 0), direction=m.Vector(0, 0)):
        super(Predator, self).__init__(mode, position, direction, max_velocity=c.PREDATOR_MAX_VELOCITY, max_angular_velocity=c.PREDATOR_MAX_ANGULAR_VELOCITY, velocity_decay=c.PREDATOR_VELOCITY_DECAY, angular_velocity_decay=c.PREDATOR_ANGULAR_VELOCITY_DECAY )

        self.target = None

    def apply_force(self):


        # behavior:
        #
        # 1. position
        # a) go to closest fish
        # b) avoid other predators
        #
        # 2. angle
        # a) rotate so that we move into direction

        preys = [ f for f in self.mode.swarm.fishes if (f.position - self.position).length < c.PREDATOR_SENSES]

        go_to_prey = m.Vector(0, 0)
        if not self.target and preys:
            self.target = sorted(preys, key=lambda p: (p.position - self.position).length_squared)[0]

        if self.target:
            go_to_prey = self.target.position - self.position

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

        self.acceleration += acc *  (acc * self.target_direction.clamp()) * c.PREDATOR_ACCELERATION


    def update(self, time_elapsed):
        game.PhysicsEntity.update(self, time_elapsed)

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



    def render(self):
        scr = self.mode.game.screen
        cam = self.mode.camera.position
        u.draw_pos_dir(scr, self.position - cam, self.direction * 20, color=(255, 0, 0))

        if self.target:
            u.draw_line(scr, self.position - cam, self.target.position - cam, color=(255, 0, 0))
