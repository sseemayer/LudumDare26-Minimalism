import py2d.Math as m
import random

GAME_TITLE = 'Migration - Ludum Dare 26 entry by semi'
SCREEN_DIMENSIONS = m.Vector(640, 480)
GAMEOVER_DIMENSIONS = m.Vector(640, 400)
WORLDMAP_SCALE = 1.5

START_SECTOR = (123, 88)
START_SAFEZONE = 300
SECTOR_SIZE = m.Vector(600, 600)
SIMULATION_RADIUS = 1

TARGET_FPS = 40

BACKGROUND_COLOR = (0, 0, 128)

START_FISHES = 2

CAMERA_MIN_DISTANCE = 60
CAMERA_ACCELERATION = 0.0005
CAMERA_MAX_VELOCITY = 0.81
CAMERA_VELOCITY_DECAY = 0.9

SWARM_ACCELERATION = 0.002
SWARM_MAX_VELOCITY = 0.8
SWARM_VELOCITY_DECAY = 0.9

SWARM_MIN_DISTANCE = 50
SWARM_MAX_DISTANCE = 300
SWARM_NEIGHBOR_DISTANCE = 30
SWARM_NEIGHBOR_REPEL_DISTANCE = 10

FISH_AVOID_PREDATOR_DISTANCE = 80

FISH_FOOD_DISTANCE = 50
FISH_EAT_DISTANCE = 10
FISH_EAT_DAMAGE = 0.5

FISH_W_GO_TO_SWARM = 0.2
FISH_W_REPEL = 0.4

FISH_W_ALIGN = 0.1
FISH_REPEL_STRENGTH = 10

FISH_MAX_VELOCITY = 0.9
FISH_MAX_ANGULAR_VELOCITY = 0.6
FISH_ACCELERATION = 0.002
FISH_ANGULAR_ACCELERATION = 0.001
FISH_ANGULAR_VELOCITY_DECAY = 0.9
FISH_VELOCITY_DECAY = 0.5

FISH_BABY_THRESHOLD = 20
FISH_BABY_FOOD = 5
FISH_BABY_COST = 10
FISH_STARVATION = 0.00001

FISH_ANIM_DELAY = 0.1

FOOD_NUTRITION_VALUE = 1
FOOD_NUTRITION_VALUE_VAR = 10
FOOD_NUTRITION_VALUE_CORPSE = 7

PREDATOR_SENSES = 150
PREDATOR_REPEL_STRENGTH = 10
PREDATOR_REPEL_DISTANCE = 50
PREDATOR_W_GO_TO_PREY = 0.8
PREDATOR_W_REPEL = 0.4
PREDATOR_ANGULAR_ACCELERATION = 0.003
PREDATOR_ACCELERATION = 0.0005
PREDATOR_HUNT_ACCELERATION = 0.001

PREDATOR_DEAGGRO_CHANCE = 0.0008
PREDATOR_DEAGGRO_DISTANCE = 100
PREDATOR_EAT_DISTANCE = 20
PREDATOR_EAT_DAMAGE = 2

PREDATOR_RANDOM_WALK_CHANCE = 0.0001
PREDATOR_RANDOM_WALK_RADIUS = 1000


PREDATOR_HUNT_MAX_VELOCITY = 1.2
PREDATOR_MAX_VELOCITY = 0.9
PREDATOR_MAX_ANGULAR_VELOCITY = 0.4
PREDATOR_ANGULAR_VELOCITY_DECAY = 0.9
PREDATOR_VELOCITY_DECAY = 0.8

PREDATOR_ANIM_DELAY = 0.05
PREDATOR_SCALE = 0.5


SECTOR_PREDATORS = lambda depth: int(random.gammavariate(depth * 10, 1))
SECTOR_FOOD = lambda depth: int(random.gammavariate((1-depth) * 100, 0.1))
