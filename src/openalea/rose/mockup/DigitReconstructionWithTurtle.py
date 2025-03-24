#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-
#
# $Id$
#
import openalea.plantgl.all as pgl
from openalea.mtg.traversal import pre_order2_with_filter


def DigitReconstructionWithTurtle(g, visitor):
    """builds a scene from "4pts leaflet" MTGs
    ToDo : ecrire les test de securite contre les entrees vides
    """
    scene = None
    # write the node code here.
    scene = TurtleFrame(g, visitor)
    # return outputs
    return (scene,)


radius = 1.2


#### Copy from mtg.turtle ###
def traverse_with_turtle(g, vid, visitor, turtle=None):
    if turtle is None:
        turtle = pgl.PglTurtle()

    def push_turtle(v):
        if g.edge_type(v) == "+":
            turtle.push()
            turtle.startGC()
            turtle.setId(v)
        return True

    def pop_turtle(v):
        if g.edge_type(v) == "+":
            turtle.stopGC()
            turtle.pop()

    turtle.push()
    turtle.startGC()
    visitor(g, vid, turtle)
    for v in pre_order2_with_filter(g, vid, None, push_turtle, pop_turtle):
        if v == vid:
            continue
        visitor(g, v, turtle)
    turtle.stopGC()
    return turtle.getScene()


######################################################
def TurtleFrame(g, visitor):
    n = g.max_scale()
    turtle = pgl.PglTurtle()
    turtle.setWidth(radius)
    for plant_id in g.vertices(scale=1):
        plant_node = g.node(plant_id)
        # moved the "position" function away
        origin = pgl.Vector3(plant_node.XX, plant_node.YY, plant_node.ZZ)
        turtle.move(origin)

        vid = next(g.component_roots_at_scale_iter(plant_id, scale=n))
        traverse_with_turtle(g, vid, visitor, turtle)
    return turtle.getScene()
