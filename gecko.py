import sys, os
import time
import math

# To avoid the start-up message
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame
import numpy as np

# Empty color with zero alpha
empty = pygame.Color(0,0,0,0)

BACKGROUND_COLOR = pygame.Color(255,255,255)
WIDTH, HEIGHT = 800, 600
HALF_SCREEN = [WIDTH/2, HEIGHT/2]

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Gecko Graphics')
try:
    pygame.display.set_icon(pygame.image.load('images/gecko3.png'))
except:
    pass

screen.fill(BACKGROUND_COLOR)
pygame.display.update()

path_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA, 32).convert_alpha()

def update():
    screen.fill(BACKGROUND_COLOR)
    screen.blit(path_surface, (0,0))
    for gecko in geckos:
        gecko.draw_body()
    pygame.display.update()

def screen_pos(position):
    return position*[1,-1]+HALF_SCREEN

def draw_line(color, start, end, width=1):
    pygame.draw.line(path_surface, color, start, end, width)

geckos = []

class Gecko:
    
    def __init__(self, position=[0,0], angle=0):
        geckos.append(self)
        
        self.position = np.array(position, dtype=np.float64)
        self.angle = angle

        self.shape = 'triangle'
        self.color = pygame.Color(0,0,0)
        self.size = 4
        self.pencolor = self.color
        self.pensize = 1

        self.surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.trace_gecko = True
        self.show_gecko = True

        self.auto_update = True

        self.first_position = self.position.copy()
        self.set_last_position()

    @property
    def properties(self):
        p = {
            'position':self.position,
            'angle':self.angle,
            'shape':self.shape,
            'color':self.color,
            'size':self.size,
            'pencolor':self.pencolor,
            'pensize':self.pensize,
            'trace_gecko':self.trace_gecko,
            'show_gecko':self.show_gecko,
            }
        return p

    def _update(self):

        if self.auto_update == True:
            update()

    def tracing_on(self):
        self.trace_gecko = True

    def tracing_off(self):
        self.trace_gecko = False
        
    def set_last_position(self):
        self.last_position = self.position.copy()

    def draw_path_line(self):
        if self.trace_gecko:
            draw_line(self.pencolor, screen_pos(self.last_position), screen_pos(self.position), self.pensize)
            self.set_last_position()

    def show(self):
        self.show_gecko = True
        self._update()

    def hide(self):
        self.show_gecko = False
        self._update()

    def set_color(self, color):
        self.color = pygame.Color(color)
        self._update()

    def set_pencolor(self, color):
        self.pencolor = pygame.Color(color)
        self._update()

    def set_position(self, *position):
        if len(position) == 1:
            position = np.array(*position)
        elif len(position) == 2:
            position = np.array(position)
        else:
            raise ValueError
        self.position = position
        self.draw_path_line()
        self._update()

    setpos = set_pos = goto = setposition = set_position

    def move(self, *offset):
        if len(offset) == 1:
            offset = np.array(*offset)
        elif len(offset) == 2:
            offset = np.array(offset)
        else:
            raise ValueError
        self.position += offset
        self.draw_path_line()
        self._update()

    def draw_body(self):
        if self.show_gecko:
            self.surf.fill(empty)
            if self.shape == 'circle':
                pygame.draw.circle(self.surf, self.color, screen_pos(self.position)+1, self.size)
            elif self.shape == 'square':
                pygame.draw.rect(self.surf, self.color, pygame.Rect(screen_pos(self.position)-self.size+1, (2*self.size, 2*self.size)))
            elif self.shape == 'triangle':

                # These positions form a triangle that points in the direction of the Gecko
                pos0 = self.position + [6*math.cos(math.radians(self.angle)), 6*math.sin(math.radians(self.angle))]
                pos1 = self.position + [6*math.cos(math.radians(self.angle+150)), 6*math.sin(math.radians(self.angle+120))]
                pos2 = self.position + [6*math.cos(math.radians(self.angle+210)), 6*math.sin(math.radians(self.angle+240))]
                
                pygame.draw.polygon(self.surf, self.color, [screen_pos(pos0),screen_pos(pos1),screen_pos(pos2)])
            
            screen.blit(self.surf, (0,0))

    def rotate(self, angle):
        self.angle += angle

    def left(self, angle):
        self.rotate(angle)

    def right(self, angle):
        self.rotate(-angle)

    def forward(self, distance):
        self.move([distance*math.cos(math.radians(self.angle)), distance*math.sin(math.radians(self.angle))])

    def backward(self, distance):
        self.move([-distance*math.cos(math.radians(self.angle)), -distance*math.sin(math.radians(self.angle))])

    fd, bk = forward, backward

    def clone(self, name):
        clone = Gecko()
        globals().update({name: clone})
        clone.tracing_off()
        
        clone.position = self.position
        clone.angle = self.angle
        clone.shape = self.shape
        clone.color = self.color
        clone.size = self.size
        clone.pencolor = self.pencolor
        clone.pensize = self.pensize

        clone.tracing_on()

        return clone

    def __repr__(self):
        return f"Gecko object at [{round(self.position[0],1)}, {round(self.position[1],1)}]"

def q():
    pygame.quit()

def main():

    g = Gecko()
    g.set_color(pygame.Color(255,0,0))
    g.set_pencolor(pygame.Color(0,255,0))

    for i in range(0):
        for n in range(360):
            g.forward(2)
            g.rotate(1*(2*(i%2)-1))
            update()

if __name__ == '__main__':
    print("Enter 'q()' to close the window")
    main()
else:
    print("Gecko has been loaded. Enter 'gecko.q()' to close the window")
