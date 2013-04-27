import game
import game.util as u
import game.constants as c

import py2d.Math as m

import math

class Fish(game.PhysicsEntity):

    def __init__(self, swarm, position=m.Vector(0, 0), direction=m.Vector(0, 0)):
        super(Fish, self).__init__(swarm.mode, position, direction, max_velocity=c.FISH_MAX_VELOCITY, max_angular_velocity=c.FISH_MAX_ANGULAR_VELOCITY, velocity_decay=c.FISH_VELOCITY_DECAY, angular_velocity_decay=c.FISH_ANGULAR_VELOCITY_DECAY)

        self.swarm = swarm
        self.food = c.FISH_BABY_FOOD

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

        neighbors = [ n for n in self.swarm.fishes if (n.position - self.position).length_squared < snd_squared]
        neighbors_direction = sum(  (n.angle + 2*math.pi) % (2*math.pi) for n in neighbors ) / len(neighbors)

        neighbors_direction = neighbors_direction % (2*math.pi)

        fd_squared = c.FISH_FOOD_DISTANCE ** 2

        foods = [ f for f in self.mode.foods if (f.position - self.position).length_squared < fd_squared]
        if foods:
            closest_food = sorted(foods, key=lambda f: (f.position - self.position).length_squared)[0]

            go_to_swarm = closest_food.position - self.position
            if go_to_swarm.length < c.FISH_EAT_DISTANCE:
                go_to_swarm = m.VECTOR_NULL
                closest_food.nutrition_value -= 1
                self.food += 1

                if closest_food.nutrition_value <= 0:
                    self.mode.foods.remove(closest_food)


        repel_sum = m.Vector(0, 0)
        rd_squared = c.SWARM_NEIGHBOR_REPEL_DISTANCE ** 2
        for n in neighbors:
            repel = self.position - n.position
            if repel.length_squared <= rd_squared:
                repel_sum += repel * ( c.FISH_REPEL_STRENGTH / (1 + repel.length))

        self.target_direction = go_to_swarm * c.FISH_W_GO_TO_SWARM + repel_sum * c.FISH_W_REPEL
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
        self.food -= c.FISH_STARVATION * time_elapsed

        if self.food >= 2 * c.FISH_BABY_FOOD:
            self.food -= c.FISH_BABY_FOOD
            self.swarm.fishes.append(Fish(self.swarm, self.position))

    def render(self):
        scr = self.mode.game.screen
        cam = self.mode.camera.position

        u.draw_pos_dir(scr, self.position - cam, self.direction, color=(0, 255, 0), radius=math.sqrt(self.food)+2)

        #u.draw_text(scr, self.position, "ta={:.2f} a={:.2f}, r={:.2f}, av={:.2f}".format(self.target_angle, self.angle, self.target_rotation, self.angular_velocity))
