#!/usr/bin/env python2

if __name__ == '__main__':
    import game.main
    try:
        import pygame._view
    except ImportError:
        pass
    game.main.run()
