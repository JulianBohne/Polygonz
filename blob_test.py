from polygonz import Polygon
from pygame import Vector2
import math
import random
from ezgame import Game
from opensimplex import OpenSimplex

class Particle(Vector2):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.velocity = Vector2(0, 0)
    
    def update(self):
        pass

points = []

g = Game(800, 800, "Test Window")

noise = OpenSimplex()

offset = 0

numOVerts = 200
vari = 1
det = 1

def remap(x, a, b, c, d):
    return (x - a) / (b - a) * (d - c) + c

def newShape(sides, variance = 0.2, detail = 1):
    points.clear()
    for i in range(sides):
        direction = Particle(math.cos(math.pi*2*i/sides), math.sin(math.pi*2*i/sides))
        points.append(direction * ((noise.noise3d(direction.x * detail, direction.y * detail, offset) + 1) / 2  * variance + 1 - variance))

def update():
    global g, offset, points
    offset += 0.02
    newShape(numOVerts, vari, det)
    p = Polygon(points)
    p.setArea(0.7)
    print(p.getSignedArea())
    g.background((0,0,0))
    p.render(g, False, True, 3)
    pass

def mousePressed(pos, button):
    #print(f"Pressed at: {pos}\nButton {button} was pressed")
    global noise
    noise = OpenSimplex(seed=int(random.random()*1000))
    newShape(numOVerts, vari, det)

def keyPressed(key):
    if key == 'f':
        g.quit()

if __name__ == "__main__":
    g.addUpdate(update)
    g.addMousePressed(mousePressed)
    g.addKeyPressed(keyPressed)

    g.translate((g.width/2, g.height/2))
    g.scaleBy((g.width/2, -g.height/2))

    newShape(numOVerts, vari, det)

    p = Polygon(points)

    print(p.getSignedArea())

    g.start()
    quit()