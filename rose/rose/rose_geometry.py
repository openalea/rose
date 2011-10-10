#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

from openalea.mtg.aml import MTG
import math
from openalea.mtg.plantframe import *

from openalea.core.external import * 
from openalea.core.logger  import *

#import openalea.plantgl.all as pgl

def computeLateralAxis(front, up):
    """ Computes and returns a vector that is
    - normal to front 
    - in the <front,side> plan
    - such as lateral is by the other side from front than side """
    Lateral=front^up
    Lateral.normalize()
    return Lateral
# end computeLateralAxis

def computeUpAxis(front,side):
    """ Computes and returns a vector that is normal to front and
    supposed to point upside the half leaflet
    """
    Up=side^front
    Up.normalize()
    return Up
# end computeUpAxis

def printPoints(points):
    """ debug info """
    print "Zs : %7.3f  %7.3f %7.3f %7.3f"%(points[0][2],points[1][2],points[2][2],points[3][2])



def computeLeaflet4pts(xMesh=[0.25, 0.5, 0.75, 1],yMesh=[0.81, 0.92, 0.94, 0],zMesh=[0,0,0,0]):
    '''    compute leaflet geometry from 4 points
    '''
    compute_leaf = None ; 
    # write the node code here.
    def meshedLeaflet(points, turtle=None):
        '''    compute leaflet geometry from 4 points
        '''
        geometry = None; 

        #print "1:",printPoints(points)

        # if the list of points is not a complete leaf
        # we have to return without pushing the turtle ;
        #We could display a red sphere to make the miss very visible, as well
        if len(points) < 4:
            return


        turtle.push()

        # We compute the main rib vector as "Axis"
        Axis=points[2]-points[0]
        axisLength=norm(Axis)
        Axis.normalize()

        # Half leaflets
        # A: the /right/ leaflet ("right" accordingly to the digitization protocol : 
        # the ending leaflet close to the observer).
        # Note that the points 2 and 4 of most leaflets has been swapped in order to turn
        # the leaflets upside-down in the MTG building, so that they get oriented UP.
        # So we treat the data as if the folks had turned CCw to digitize the leaflets.
        # 1st : compute the lateral axis of the right part of the leaflet
        #
        # DBG : anti-3points leaflets
        # side=points[-1]-points[0]
        side=points[3]-points[0]
        sideLength=norm(side)
        side.normalize()
        Up=computeUpAxis(Axis,side)
        Lateral = -computeLateralAxis(Axis,Up)
        # for debug purposes ()

        # Debug information
        #print "A:%s"% Axis
        #print "L:%s"% Lateral
        #print "U:%s"% Up
        
        # 2nd : compute the width of the right half leaflet (sin(angle) * sideLength)
        halfWidth =  sideLength * norm(side^Axis)

        # jessica's code for  building the mesh
        # I tried to use zMesh, but it has had no efect.
        ls_pts=[Vector3(0.,0.,0.)]
        for i in xrange(len(xMesh)-1):
            ls_pts.append(Vector3(xMesh[i],-yMesh[i],0))
            ls_pts.append(Vector3(xMesh[i],0,0))
        ls_pts.append(Vector3(1.,0.,0.))
        # we reverse them triangles Cwise
        ls_ind=[Index3(0,2,1),Index3(1,2,3),Index3(2,4,3),Index3(3,4,5),Index3(4,6,5),Index3(5,6,7)]        
        triangleSet=TriangleSet(Point3Array(ls_pts),Index3Array(ls_ind))

        geom=triangleSet
        #turtle.push() #try
        geom=Scaled((axisLength,halfWidth,1),geom)
        # Oriented() makes the ribs where the polygon leaf doesn't.
        #geom=Oriented(Axis,Lateral,geom)
        # setHead() works when swapping arguments relatively to the 
        # error message we get when calling setHead with no arguments.
        turtle.setHead(Up,Axis)
        turtle.customGeometry(geom, 1)

        # Half left leaflet
        # 3 : compute the  lateral axis
        side=points[1]-points[0]
        sideLength=norm(side)
        side.normalize()
        Up=computeUpAxis(Axis,side)
        Lateral = -computeLateralAxis(Axis,Up)
        #print Lateral
        
        # 4 : compute the width of the left half leaflet
        halfWidth =  sideLength * norm(side^Axis)

        # list of index (CCwise)   
        ls_ind=[Index3(0,1,2),Index3(1,3,2),Index3(2,3,4),Index3(3,5,4),Index3(4,5,6),Index3(5,7,6)]
        triangleSet=TriangleSet(Point3Array(ls_pts),Index3Array(ls_ind))

        geom=triangleSet
        geom=Scaled((axisLength,halfWidth,1),geom)
        #geom=Oriented(Axis,Lateral,geom)
        # setHead() see previously
        turtle.setHead(Up,Axis)
        turtle.customGeometry(geom, 1)

#P        # polygon code for testing if it maps the meshed leaves
#P        turtle.push()
#P        turtle.startPolygon()
#P        for pt in points[1:]:
#P            turtle.lineTo(pt)
#P        turtle.lineTo(points[0])
#P        turtle.stopPolygon()
#P        turtle.pop()

#S        # C.Pradal's verbatim code 4 testing : a sphere at the barycenter of the leaflet
#S        turtle.push()
#S        barycenter = sum(points, Vector3())/len(points)
#S        distance = barycenter-points[0]
#S        radius = norm(distance)/10.
#S        geometry= Translated(distance, Sphere(radius))
#S        turtle.setColor(3) # red 
#S        turtle.customGeometry(geometry, 1)
#S        turtle.pop()
#S
#S        # Code 4 testing : a sphere really at the barycenter of the leaflet
#S        turtle.push()
#S        barycenter = sum(points, Vector3())/len(points)
#S        distance = barycenter-points[0] 
#S        radius = norm(distance)/10.
#S        turtle.setHead(Lateral,distance)
#S        geometry= Translated(Vector3(radius*10,0,0), Sphere(radius))
#S        turtle.setColor(0) # grey 
#S        turtle.customGeometry(geometry, 1)
#S        turtle.pop()

        turtle.pop() # against 1st push()
        
    # return outputs
    return meshedLeaflet,

class ComputeLeaflet4pts(Node):
    def __init__(self):
        Node.__init__(self)
        self.add_output( name = 'compute_leaf', 
                         interface = IFunction )

    def __call__( self, inputs ):
        return computeLeaflet4pts()

#########################################
def rawLeaflet(points, turtle=None):
    '''    compute leaflet geometry from 4 points
    '''
    turtle.push()
    turtle.startPolygon()
    for pt in points[1:]:
        turtle.lineTo(pt)
    turtle.lineTo(points[0])
    turtle.stopPolygon()
    turtle.pop()
# end rawleaflet

########################################""
def polygonLeaflet():
    """ default function to draw up a leaflet 
    NOTE : without the turtle.push() and turtle.pop(),
    it hangs the viewer up with a message to the father shell :
        *** glibc detected *** /usr/bin/python: double free or corruption (out): 0x0000000004bfebd0 ***
    """
    compute_leaf = None ; 
    # write the node code here.
#R    def rawLeaflet(points, turtle=None):
#R        '''    compute leaflet geometry from 4 points
#R        '''
#R        turtle.push()
#R        turtle.startPolygon()
#R        for pt in points[1:]:
#R            turtle.lineTo(pt)
#R        turtle.lineTo(points[0])
#R        turtle.stopPolygon()
#R        turtle.pop()
    # return outputs
    return rawLeaflet,
# end polygonLeaflet

class PolygonLeaflet(Node):
    def __init__(self):
        Node.__init__(self)
        self.add_output( name = 'compute_leaf', 
                         interface = IFunction )

    def __call__( self, inputs ):
        return polygonLeaflet()

########################################""

def makeNoLeaflet():
    '''    make no leaflets, so we can watch the plantframe  
    '''
    noLeaflet  = None; 
    # write the node code here.
    def noLeaflet(points, turtle=None):
	    """ """
	    geometry = None; 
    # return outputs
    return noLeaflet,
# end makeNoLeaflet

class NoLeaflet(Node):
    def __init__(self):
        Node.__init__(self)
        self.add_output( name = 'compute_leaf', 
                         interface = IFunction )

    def __call__( self, inputs ):
        return makeNoLeaflet()

########################################""
def position(n):
    """ returns the position of the node in a Vector3 data """
    return Vector3(n.XX, n.YY, n.ZZ)
    
#Odef compute_leaflet(points, turtle):
#O    """ default function to draw up a leaflet 
#O    NOTE : without the turtle.push() and turtle.pop(),
#O    it hangs the viewer up with a message to the father shell :
#O        *** glibc detected *** /usr/bin/python: double free or corruption (out): 0x0000000004bfebd0 ***
#O    """
#O    turtle.push()
#O    turtle.startPolygon()
#O    for pt in points[1:]:
#O        turtle.lineTo(pt)
#O    turtle.lineTo(points[0])
#O    turtle.stopPolygon()
#O    turtle.pop()

def vertexVisitor(leaf_factory=None):
    '''    function to visit MTG nodes
    '''
    # write the node code here.   
    visitor = None; 


    if leaf_factory is None:
        leaf_factory=rawLeaflet

    def visitor(g, v, turtle, leaf_computer=leaf_factory):
        n = g.node(v)
        pt = position(n)
        symbol = n.label[0]
        turtle.setId(v)

        if symbol in ['E', 'R']:
            if n.Diameter is None:
                print 'ERROR: vertex %d (name: %s, line around %d)'%(v,n.label,n._line)
                n.Diameter = 0.75

            if n.edge_type() == '+'  or not n.parent():
                turtle.setWidth(n.Diameter / 2.)

            turtle.oLineTo(pt)
            turtle.setWidth(n.Diameter / 2.)

        elif n.label in [ 'F1', 'S1' ]:
            if symbol == 'F':
                turtle.incColor()
            else :
                turtle.setColor(4)
            
            points = [position(n.parent()), pt]
            while n.nb_children() == 1:
                n = list(n.children())[0]
                points.append(position(n))

            # Odd code 4 testing
            #turtle.push()
            #barycenter = sum(points, Vector3())/len(points)
            #distance = barycenter-points[0]
            #radius = norm(distance)/10.
            #geometry= Translated(distance, Sphere(radius))
            #turtle.setColor(3)
            #turtle.customGeometry(geometry, 1)
            #turtle.pop()
            # End odd code
            leaf_computer(points,turtle)
	    
        elif n.label == "B1" :
            # 4 testing
            oldPt=turtle.getPosition()
            radiusOfBud=(pt-oldPt)*0.5
            centerOfBud=oldPt + radiusOfBud
            turtle.oLineTo(centerOfBud)
            turtle.push()
            #turtle.incColor()
            turtle.setColor(4) # apple green
            radius = norm(radiusOfBud)
            geometry=  Sphere(radius)
            #return Translated(distance, Sphere(radius))
            #geom = leaf_factory(points)
            turtle.customGeometry(geometry, 1)
            turtle.pop()
            turtle.setWidth(radius*.8)
        elif n.label == "O1" :
            turtle.push()
            #turtle.stopGC()
            #turtle.startGC()	    
            turtle.setColor(3) # red
            # CPL
            turtle.setWidth(n.parent().Diameter*.5)   
            turtle.oLineTo(pt)
            turtle.setWidth(n.Diameter*.5)
            turtle.pop()

        elif symbol == "T":
            # The turtle is supposed to be at the top of the previous vertex
            #turtle.stopGC() # not useful anymore
            couleur=turtle.getColor()
            if n.parent().label=="B1":
                turtle.setColor(4)
            else:
                turtle.incColor()
            #turtle.startGC()
            turtle.oLineTo(pt)
            turtle.setWidth(0.01)	    
            turtle.setColor(couleur)

    # return outputs
    return visitor,

class VertexVisitor(Node):
    def __init__(self):
        Node.__init__(self)
        self.add_input( name = 'leaf_factory',
                        interface = IFunction)
        self.add_output( name = 'VertexVisitor', 
                         interface = IFunction )

    def __call__( self, inputs ):
        leaf_factory=self.get_input('leaf_factory')
        return vertexVisitor(leaf_factory)
