
import pygame

class AudioManager(object):

    def __init__(self):

        pygame.mixer.music.load("data/sounds/music.wav")
        pygame.mixer.music.play(-1)

        sounds = ['eat', 'hurt', 'grow', 'attack']

        self.sounds = { sname: pygame.mixer.Sound('data/sounds/{}.wav'.format(sname)) for sname in sounds }

    def play(self, sname):
        if sname in self.sounds:
            self.sounds[sname].play()

