from openalea.plantgl.all import *
from openalea.mtg import aml
from math import cos, sin
from numpy import arange

def no_test():
    turtle = PglTurtle()
    turtle.setWidth(2)

    def position(n):
        return Vector3(n.XX, n.YY, n.ZZ)

    mtg_file = '../share/P1/9.mtg'
    g = aml.MTG(mtg_file)
    l =aml.Axis(g.component_roots_at_scale(0, g.max_scale()).next())
    l.insert(0, g.complex(l[0]))
    pts = [position(g.node(v)) for v in l]
    h=10
    r=10
    pts = [(r*sin(x), r*cos(x), h*x) for x in arange(0,10,1.)]

    def adv(pt):
        turtle.startGC()
        turtle.oLineTo(pt)
        #turtle.setWidth(r)
        turtle.stopGC()

    turtle.push()
    map(adv, pts)
    turtle.pop()
    Viewer.display(turtle.getScene())

