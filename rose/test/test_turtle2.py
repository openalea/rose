from openalea.plantgl.all import *
from random import randint

turtle = PglTurtle()
pts = [(0,0,1), (0,1,2), (0,1,3), (0,2,3.3)]

def adv(pt):
    turtle.startGC()
    turtle.setId(randint(1,100000))
    turtle.oLineTo(pt)
    turtle.stopGC()
turtle.move((0,0,0))
turtle.push()
map(adv, pts)
turtle.pop()
Viewer.display(turtle.getScene())

