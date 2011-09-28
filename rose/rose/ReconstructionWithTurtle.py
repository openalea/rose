
import openalea.plantgl.all as pgl
from openalea.mtg.turtle import pre_order2_with_filter
from openalea.mtg.plantframe import *
from openalea.mtg.traversal import pre_order2_with_filter

def ReconstructionWithTurtle(g, visitor, power=3.):
    '''    builds a scene from "4pts leaflet" MTGs
    
    .. todo:: Add some constant in the arguments
    '''
    # Compute the radius with pipe model
    
    diameter = g.property('Diameter')
    for v in g:
        if g.class_name(v) == 'R':
            diameter[v] = 0.75

    drf = DressingData(LeafClass=['F', 'S'], 
        FlowerClass='O', FruitClass='B',
        MinTopDiameter=dict(E=0.5))
    pf = PlantFrame(g, TopDiameter='Diameter', DressingData=drf, 
        Exclude = 'F S O B T'.split())
    diameter = pf.algo_diameter(power=power)
    g.properties()['Diameter'] = diameter
    thscene=TurtleFrame(g, visitor)
    # return outputs
    return thscene,

#### Copy from mtg.turtle ###
def traverse_with_turtle(g, vid, visitor, turtle=None):
    if turtle is None:
        turtle = PglTurtle()

    def push_turtle(v):
        if g.edge_type(v) == '+':
            turtle.push()
            #turtle.startGC()
            turtle.setId(v)
        return True

    def pop_turtle(v):
        if g.edge_type(v) == '+':
            #turtle.stopGC()
            turtle.pop()

    turtle.push()
    turtle.startGC()

    visitor(g,vid,turtle)
    turtle.stopGC()
    for v in pre_order2_with_filter(g, vid, None, push_turtle, pop_turtle):
        if v == vid: continue
        turtle.startGC()
        visitor(g,v,turtle)
        turtle.stopGC()
    turtle.pop()
    return turtle.getScene()
 
######################################################
def TurtleFrame(g, visitor):
    n = g.max_scale()
    turtle = pgl.PglTurtle()
    #
    for plant_id in g.vertices(scale=1):
        plant_node = g.node(plant_id)
        # moved the "position" function away
        origin = pgl.Vector3(plant_node.XX, plant_node.YY, plant_node.ZZ)
        turtle.move(origin)

        vid =  g.component_roots_at_scale(plant_id, scale=n).next()
        traverse_with_turtle(g, vid, visitor, turtle)
    return turtle.getScene()
