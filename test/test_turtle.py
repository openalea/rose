from openalea.core.path import path
from openalea.rose import turtle
from openalea.mtg.aml import MTG

datadir = path(turtle.__file__).dirname()

def test(mtg_file='test2011OK.mtg'):
    g = MTG(datadir/mtg_file)
    scene = turtle.TurtleFrame(g)
    return scene

if __name__ == '__main__':
    from openalea.plantgl.all import Viewer
    scene = test()
    Viewer.display(scene)
    
