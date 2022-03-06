
import pyglet
from pyglet.window import key

class SpeedClock(pyglet.clock.Clock):
    __time = 0
    speed = 1.0

    def __init__(self):
        pyglet.clock.Clock.__init__(self, time_function=self.get_time)
        pyglet.clock.schedule(self.advance)

    def advance(self, time):
        self.__time += time * self.speed        
        self.tick()

    def get_time(self):
        return self.__time
