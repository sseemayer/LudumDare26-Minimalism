import pygame
WORLD = pygame.image.load("data/images/world.png")

WORLD_WINDOW = (74, 50)

def render(dest, dpos, sector):
    area = pygame.Rect((sector[0] - WORLD_WINDOW[0] / 2, sector[1] - WORLD_WINDOW[1] / 2), WORLD_WINDOW)

    dest.blit(WORLD, dpos, area)
    dest.set_at((dpos[0] + WORLD_WINDOW[0] / 2, dpos[1] + WORLD_WINDOW[1]/2), (255, 0, 0))


def depth(pos):
    # hues:
    # green: 103
    # blue: 212

    color = WORLD.get_at(pos).hsva

    v_max = 60
    v_min = 20

    v = 1 - (color[2] - v_min) / (v_max - v_min)
    if v < 0:
        v = None

    return v

