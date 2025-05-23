from openalea.core.path import path
from openalea.mtg.aml import MTG as myMTG
from openalea.mtg.plantframe import *
from openalea.rose import turtle, VertexVisitor, ReconstructionWithTurtle

position = VertexVisitor.position

datadir = path('../share/P3')
datadir_P1 = path('../share/P1')


def test1():
    mtg_file = '9.mtg'
    #mtg_file = '141.mtg'
    g = myMTG(datadir_P1/mtg_file)
    return run(g)

def test2():
    mtg_file = '136.mtg'
    #mtg_file = '141.mtg'
    g = myMTG(datadir/mtg_file)
    return run(g)

    
def run(g):
    _visitor, = VertexVisitor.VertexVisitor()
    scene, = ReconstructionWithTurtle.ReconstructionWithTurtle(g, _visitor, power=3.)
    return scene

def plant3d(mtg_file='136.mtg'):
    g = myMTG(datadir/mtg_file)

    diameter = g.property('Diameter')
    for v in g:
        if g.class_name(v) == 'R':
            diameter[v] = 0.75
    max_scale = g.max_scale()

    # F : leaflet, O : flower, B : flower bud, S: sepal
    drf = DressingData(LeafClass=['F', 'S'], FlowerClass='O', FruitClass='B',
        MinTopDiameter=dict(E=0.5))
    
    pf = PlantFrame(g, TopDiameter='Diameter', DressingData=drf, Exclude = 'F S O B T'.split())
    return pf

if __name__ == '__main__':
    from openalea.plantgl.all import Viewer
#X     pf = plant3d()
#X     g = pf.g
#X     diameter = pf.algo_diameter()
#X     #diameter = pf.linear_diameter(power=2)
#X     g.properties()['Diameter'] = diameter
#X 
#X     def hide(v):
#X         return g.class_name(v) in pf.exclude
#X     def colors(v):
#X         if g.class_name(v) == 'E':
#X             return (125,0,0)
#X         elif g.class_name(v) == 'R':
#X             return (0,200,10)
#X         else: return (0,0,0)
#X     scene = build_scene(g, pf._get_origin(2), pf.axes, pf.points, diameter, 0.5, 
#X     option='cylinder',colors=colors,hide=hide)
    scene = test1()
    Viewer.display(scene)
    
 
