# The Migration

![Title](http://imgur.com/UREEGKp.png)  ![Gameplay](http://imgur.com/unl4vMp.png)

My entry for the [Ludum Dare 26 competition](http://www.ludumdare.com/compo/) is about leading a swarm of fish that migrates from the Falkland Islands in Southern America to the mediterranean sea. You indirectly control the swarm using the mouse. Fish eat plankton, if they eat enough of it, they will reproduce and your swarm will grow. Try to steer your swarm away from predator fish. 

As soon as you get out into the open water, the game will become more difficult. Be sure to take good care of your fish and you will be able to make it to the end!

## Controls

    Mouse   Steer
    
    A       Assemble swarm
    S       Standard formation
    D       Disperse swarm

## Installation and Running

### Binary distribution
If you have the binary release, just run the .exe file. Wine should work under Mac and Linux, too. 

### From source
If you like to see the code, you can find the GitHub repository at https://github.com/sseemayer/LudumDare26-Minimalism

For running the game from source, you will need:

  * Python 2.7 or better (not Python 3.x!)
  * Pygame
  * [glyph](http://code.google.com/p/glyph/)
  * [PyHiero](https://github.com/sseemayer/PyHiero)
  * [Py2D](https://github.com/sseemayer/Py2D)

Once you have all the dependencies, just run the the_migration.py file in the main directory.

#### Special Note for Macintosh Users

In order to access the 32-bit pygame libraries, you might need to run the game using

	$ arch -i386 python the_migration.py

## License
The code and content for Migration is under the MIT license. The libraries used may have different licenses

## Used tools

  * ArchLinux, AwesomeWM, vim, git
  * python, pygame, PyHiero, Py2D, py2exe, pygame2exe
  * GIMP, Inkscape
  * Wacom Intuos 3
  * inudge, bfxr, Audacity
  * glapse, gtk-recordMyDesktop

## Thanks
Thanks to my girlfriend Yue for the support, the Ludum Dare community for the discussions and you, for playing!
