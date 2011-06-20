import openalea.plantgl.all as pgl
from openalea.mtg.turtle import traverse_with_turtle
from openalea.mtg.traversal import pre_order2_with_filter

radius =1.2 
def compute_leaf(points):
    # replace this function with your own one.
    barycenter = sum(points, pgl.Vector3())/len(points)
    distance = barycenter-points[0]
    radius = pgl.norm(distance)/10.
    return pgl.Translated(distance, pgl.Sphere(radius))
    
def visitor(g, v, turtle, leaf_factory=compute_leaf):
    n = g.node(v)
    pt = position(n)

    symbol = n.label[0]
    if symbol in ['E', 'R']:
        #if n.edge_type() == '+' :
        #    turtle.startGC()
        turtle.setId(v)
        turtle.lineTo(pt)
    if n.label =='F1':
        turtle.setId(v)
        turtle.incColor()
        points = [position(n.parent()), pt]
        while n.nb_children() == 1:
            n = list(n.children())[0]
            points.append(position(n))
        turtle.startPolygon()
        for pt in points[1:]:
            turtle.lineTo(pt)
        turtle.lineTo(points[0])
        turtle.stopPolygon()
        # set the shape to the turtle
        #geom = leaf_factory(points)
        #turtle.customGeometry(geom, 1)
        


def position(n):
    return pgl.Vector3(n.XX, n.YY, n.ZZ)

#############################
#### Copy from mtg.turtle ###
def traverse_with_turtle(g, vid, visitor, turtle=None):
    if turtle is None:
        turtle = pgl.PglTurtle()

    def push_turtle(v):
        if g.edge_type(v) == '+':
            turtle.push()
            turtle.startGC()
            turtle.setId(v)
        return True

    def pop_turtle(v):
        if g.edge_type(v) == '+':
            turtle.stopGC()
            turtle.pop()

    turtle.push()
    turtle.startGC()
    visitor(g,vid,turtle)
    for v in pre_order2_with_filter(g, vid, None, push_turtle, pop_turtle):
        if v == vid: continue
        visitor(g,v,turtle)
    turtle.stopGC()
    return turtle.getScene()

######################################################
def TurtleFrame(g, visitor=visitor):
    n = g.max_scale()
    turtle = pgl.PglTurtle()
    turtle.setWidth(radius)
    for plant_id in g.vertices(scale=1):
        plant_node = g.node(plant_id)
        origin = position(plant_node)
        turtle.move(origin)

        vid =  g.component_roots_at_scale(plant_id, scale=n).next()
        traverse_with_turtle(g, vid, visitor, turtle)
    return turtle.getScene()


