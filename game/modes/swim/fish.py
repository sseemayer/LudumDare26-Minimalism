import pygame
from pygame.locals import *

import game
import game.util as u
import game.constants as c

import py2d.Math as m

import math
import random

import food


class Fish(game.PhysicsEntity):
    frames = None

    def __init__(self, swarm, position=m.Vector(0, 0), direction=m.Vector(0, 0), color=[255, 255, 255]):
        super(Fish, self).__init__(swarm.mode, position, direction, max_velocity=c.FISH_MAX_VELOCITY, max_angular_velocity=c.FISH_MAX_ANGULAR_VELOCITY, velocity_decay=c.FISH_VELOCITY_DECAY, angular_velocity_decay=c.FISH_ANGULAR_VELOCITY_DECAY)

        if not Fish.frames:
            Fish.frames = [pygame.image.load("data/images/fish_{}.png".format(i)).convert_alpha() for i in range(8)]

        self.swarm = swarm
        self.food = c.FISH_BABY_FOOD
        self.color = [cl for cl in color]

        self.anim_timer = random.uniform(0, len(Fish.frames)) * c.FISH_ANIM_DELAY

    def modify_food(self, delta):
        self.food += delta

        if self.food <= 0:
            self.mode.foods.append(food.Food(self.mode, self.position, nutrition_value = c.FOOD_NUTRITION_VALUE_CORPSE))

            if self in self.swarm.fishes:
                self.swarm.fishes.remove(self)

        if self.food >= c.FISH_BABY_THRESHOLD:
            self.modify_food(-c.FISH_BABY_COST)

            self.mode.game.audio.play("grow")

            self.mode.fishies_spawned += 1
            self.mode.fishies_max = max(self.mode.fishies_max, len(self.swarm.fishes))
            self.swarm.fishes.append(Fish(self.swarm, self.position, color=self.color))

    def apply_force(self):

        # behavior:
        #
        # 1. position
        # a) go to at least c.SWARM_MIN_DISTANCE units from swarm center
        # b) avoid other fish
        #
        # 2. angle
        # a) align with other fish
        # b) rotate so that we move into direction

        go_to_swarm = self.swarm.position - self.position
        if go_to_swarm.length < c.SWARM_MIN_DISTANCE:
            go_to_swarm = m.VECTOR_NULL

        snd_squared = c.SWARM_NEIGHBOR_DISTANCE ** 2


        flee_from_predator_sum = m.Vector(0, 0)
        pd_squared = c.FISH_AVOID_PREDATOR_DISTANCE ** 2
        predators = [ p for p in self.swarm.mode.predators if (p.position - self.position).length_squared < pd_squared]
        for p in predators:
            flee_from_predator_sum += (self.position - p.position)


        neighbors = [ n for n in self.swarm.fishes if (n.position - self.position).length_squared < snd_squared]
        neighbors_direction = sum(  (n.angle + 2*math.pi) % (2*math.pi) for n in neighbors ) / len(neighbors)

        neighbors_direction = neighbors_direction % (2*math.pi)

        fd_squared = c.FISH_FOOD_DISTANCE ** 2

        foods = [ f for f in self.mode.foods if (f.position - self.position).length_squared < fd_squared]
        if foods and go_to_swarm.length < c.SWARM_MAX_DISTANCE:
            closest_food = sorted(foods, key=lambda f: (f.position - self.position).length_squared)[0]

            go_to_swarm = closest_food.position - self.position

            if go_to_swarm.length < c.FISH_EAT_DISTANCE * 0.2:
                go_to_swarm = m.VECTOR_NULL

            if go_to_swarm.length < c.FISH_EAT_DISTANCE:
                closest_food.nutrition_value -= c.FISH_EAT_DAMAGE
                self.modify_food(c.FISH_EAT_DAMAGE)
                self.mode.food_eaten += c.FISH_EAT_DAMAGE

                self.mode.game.audio.play("eat")

                color_ratio = 1 / self.food

                for i in range(3):
                    self.color[i] = (1-color_ratio) * self.color[i] + color_ratio * closest_food.color[i]

                if closest_food.nutrition_value <= 0:
                    self.mode.foods.remove(closest_food)


        repel_sum = m.Vector(0, 0)
        rd_squared = c.SWARM_NEIGHBOR_REPEL_DISTANCE ** 2
        for n in neighbors:
            repel = self.position - n.position
            if repel.length_squared <= rd_squared:
                repel_sum += repel * ( c.FISH_REPEL_STRENGTH / (1 + repel.length))

        self.target_direction = flee_from_predator_sum +  go_to_swarm * c.FISH_W_GO_TO_SWARM + repel_sum * c.FISH_W_REPEL
        self.target_direction = self.target_direction.clamp()

        move_angle = math.atan2(self.target_direction.y, self.target_direction.x)

        #self.target_angle = move_angle
        self.target_angle = neighbors_direction * c.FISH_W_ALIGN + move_angle * (1 - c.FISH_W_ALIGN) + math.pi * 2
        self.target_angle %= math.pi * 2

        self.target_rotation = u.angle_steer(self.target_angle, self.angle)

        #self.acceleration += self.target_direction * c.FISH_ACCELERATION

        self.angular_velocity -= self.target_rotation * c.FISH_ANGULAR_ACCELERATION
        acc = m.Vector(math.cos(self.angle), math.sin(self.angle))

        self.acceleration += acc *  (acc * self.target_direction.clamp()) * c.FISH_ACCELERATION

    def update(self, time_elapsed):
        game.PhysicsEntity.update(self, time_elapsed)
        self.direction = m.Vector(math.cos(self.angle), math.sin(self.angle)) * 10
        self.modify_food(-c.FISH_STARVATION * time_elapsed)

        self.anim_timer += time_elapsed * self.acceleration.length
        self.anim_timer %= c.FISH_ANIM_DELAY * len(Fish.frames)


    def render(self):
        scr = self.mode.game.screen
        cam = self.mode.camera.position

        frame = int(self.anim_timer / c.FISH_ANIM_DELAY)

        sprite_stretch = pygame.transform.rotozoom(Fish.frames[frame], -self.angle / math.pi * 180, math.sqrt(self.food / c.FISH_BABY_THRESHOLD))

        sprite_stretch.fill(self.color, special_flags=BLEND_MULT)

        sprite_dim = m.Vector(sprite_stretch.get_width(), sprite_stretch.get_height())

        scr.blit(sprite_stretch, (self.position - cam - sprite_dim / 2).as_tuple())

        #u.draw_pos_dir(scr, self.position - cam, self.direction, color=(0, 255, 0), radius=math.sqrt(self.food)+2)

        #u.draw_text(scr, self.position, "ta={:.2f} a={:.2f}, r={:.2f}, av={:.2f}".format(self.target_angle, self.angle, self.target_rotation, self.angular_velocity))
