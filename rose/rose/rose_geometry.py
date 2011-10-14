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

################################################ BUD
def rawBud():
    ''' returns a function to draw 'raw' buds wiht a sphere and a cone'''
    
    def computeRawBud(points, turtle=None):
        #print "points= %s" %  points
        turtle.push()
        turtle.setColor(4) # apple green

        oldPt=points[0]
        radiusOfBud=(points[1]-oldPt)*0.5
        centerOfBud=oldPt + radiusOfBud
        turtle.oLineTo(centerOfBud)
        turtle.push()
        radius = norm(radiusOfBud)
        geometry=  Sphere(radius)
        #return Translated(distance, Sphere(radius))
        #geom = leaf_factory(points)
        turtle.customGeometry(geometry, 1)
        turtle.pop()
        turtle.setWidth(radius*.8)
        if len(points) >2: # i.e top not forgotten
            turtle.oLineTo(points[2])
            turtle.setWidth(0.01)	    
        turtle.pop()
    # end computeRawBud

    return computeRawBud

class RawBud(Node): 
    def __init__(self):
        Node.__init__(self)
        self.add_output( name = 'compute_bud', 
                         interface = IFunction )

    def __call__( self, inputs ):
        return rawBud()

################################################ BUD
def builtBud(stride=10):
    ''' returns a function to draw buds'''
    
    def computeBuiltBud(points, turtle=None):
        '''draw a bud with 2 spheres and a paraboloid '''
        # TODO1 : adjust the paraboloid onto the upper sphere
        # TODO2 : parametrize and simplify that stuff of variables

        # fineness of drawing definition
        lStride = stride
        if lStride < 5:
            lStride = 5
            
        botPt=points[0]
        topPt=points[-1]
        budAxis=Vector3(topPt-botPt)
        step=norm(budAxis) /12.
        budAxis.normalize()
        #print "step=%f" % step
        #print "len(points)=%d" % len(points)

        turtle.push() #
        # prolongation of ped
        turtle.oLineTo(points[0])
        turtle.setColor(4) # 
       
        # we must orient the turtle before to draw 
        # this makes better fitting of the sphere and the paraboloid
        upAxis=computeUpAxis(budAxis,Vector3(1,0,0))
        # ifever a bud grows along the x axis :
        if abs(norm(upAxis)) < 0.001 :
            upAxis=computeUpAxis(budAxis,Vector3(0,1,0))
        turtle.setHead(budAxis,upAxis)

        #radiusOfOvary=step /12. 
        #centerOfOvary=botPt + budAxis/12.
        turtle.move(botPt + budAxis *step )
        turtle.customGeometry(Sphere(step * 1.2,lStride ), 1)
        turtle.move(botPt +budAxis * step*4)
        turtle.customGeometry(Sphere(step*2, lStride ), 1)

        # we move to the center of the 2nd sph plus a half ray, 
        # i.e ray * sin(pi/6) (step *5, say) ajusted to 4.9 because 
        # the base of the paraboloid appears rather dark if visible.
        turtle.move(botPt +budAxis *step * 4.9) 
        # so the base diameter of the paraboloid is ray * cos(pi/6)
        # its length is bud heigth * (12 -4.9) / 12
        # its concavity is fitted to make it tangent to the sphere
        para=Paraboloid(step* 1.732,step*7.1,0.4,True, lStride,lStride)
        turtle.customGeometry(para,1)

        # visual control test
        #turtle.move(topPt)
        #turtle.setColor(0)
        #turtle.customGeometry(Sphere(step/2.), 1)
        # end test
        #turtle.move(Vector3(0,0,1) * step*1.5)
        
        turtle.pop()
    # end computeBuiltBud
        
    return computeBuiltBud
    # end revolutionBud

class BuiltBud(Node):
    def __init__(self):
        Node.__init__(self)
        self.add_input( name = 'stride', interface = IInt )
        self.add_output( name = 'compute_bud', 
                         interface = IFunction )
    def __call__( self, inputs ):
        stride=self.get_input('stride')
        return builtBud(stride)
   

################################################ LEAFLET
def computeLeaflet4pts(xMesh=[0.25, 0.5, 0.75, 1],yMesh=[0.81, 0.92, 0.94, 0]):
    '''    compute leaflet geometry from 4 points
    '''
    meshedLeaflet = None ; 
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
        # dbg
        if abs(norm(Up)) < 0.001 :
            print "Z.bug= %s" % points[0][2]
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
        self.add_input( name='xMesh',
                        interface=ISequence)
        self.add_input(name='yMesh',
                       interface=ISequence)
        self.add_output( name = 'compute_leaf', 
                         interface = IFunction )

    def __call__( self, inputs ):
        xMesh=self.get_input('xMesh')
        yMesh=self.get_input('yMesh')
        return computeLeaflet4pts(xMesh,yMesh)

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


######################################## FLOWER
def bezierPatchFlower(controlpointmatrix=None,ustride=8,vstride=8):
    ''' interface to return bpFlower ''' 
    bpFlower=None
    #print "BezierPatchFlower called ; uStride is %s" % ustride
    # write the node code here.
    def bpFlower(points, turtle=None,):
        ''' computes a flower from two points and the diameters associated to 
        the flower.
        @param points : list of pairs[Vector3, scalar] resp. (position;diameter)
        '''
        if controlpointmatrix is None:
            return
        #else:  print "controlpointmatrix = %s" % controlpointmatrix
        luStride=ustride
        lvStride=vstride
        if luStride < 5:
            luStride = 5
        if lvStride < 5:
            lvStride = 5
        #ustride=5 
        #vstride=5 
        basePos=points[0][0]
        topPos=points[1][0]
        pedDiam=points[0][1]
        flowerRay=points[1][1] * 0.5
        flowerHeight=norm(topPos-basePos)
        baseRay=max(flowerRay *0.2, flowerHeight*0.2) # arbitrarily
        deltaRay=flowerRay-baseRay
        petalLength=math.sqrt(flowerHeight*flowerHeight + deltaRay*deltaRay)

        # we build the generic patch
        petalMesh=BezierPatch(controlpointmatrix,luStride, lvStride)
        # patch is scaled according to the global flower dimensions
        petalMesh=Scaled(Vector3(petalLength,max(baseRay,flowerRay)*1.1,baseRay),petalMesh)
        # 
        rad5eTour=math.pi/2.5 # a fifth of a tour

        # compute the pitch angle (flower opening)
        if deltaRay > 0 : # opened flower
            pitchAngle=math.atan(flowerHeight/(deltaRay))
        elif deltaRay < 0 : # flower not opened yet
            pitchAngle=math.pi*0.5+math.atan((-deltaRay)/flowerHeight)
        else: # say half opened
            pitchAngle=math.pi*0.5

        #ovary=Disc(baseRay ,luStride)
        ovary=Sphere(baseRay ,luStride)

        turtle.push() # we draw now
        # mat=Material(Color3(255,127,127)) # just 6 colors here
        turtle.setColor(4) # kind of yellow-green

        turtle.customGeometry(ovary, 1) # 
        #petalMesh=Translated(Vector3(flowerRay * 0.01 , 0, 0), petalMesh)

        # TODO : compute the closing angle of the petals from height and width
        turtle.setColor(3) # red
        for iIndex in range(0,5):
            # closing the flower : 
            petal=AxisRotated((0,1,0),-pitchAngle,petalMesh)
            # twisting a bit to limit collisions [Todo in the patch]
            petal=AxisRotated((1,0,0),pitchAngle*0.05,petal)
            angle=iIndex*rad5eTour
            petal=AxisRotated((0,0,1),angle,petal)
            petal=Translated(Vector3(baseRay *math.cos(angle) *0.8,\
                                         baseRay *math.sin(angle) *0.8,\
                                         0),\
                                 petal)
            turtle.customGeometry(petal, 1) #flowerHeight) #  

        turtle.pop()

    return bpFlower

class BezierPatchFlower(Node):
    ''' '''
    def __init__(self):
        Node.__init__(self)
        self.add_input( name='controlpointmatrix', interface=IData)
        self.add_input(name='ustride', interface=IInt)
        self.add_input(name='vstride', interface=IInt)
        self.add_output( name = 'compute_flower', interface = IFunction )
        
    def __call__( self, inputs ): 
        controlpointmatrix=self.get_input('controlpointmatrix')
        ustride=self.get_input('ustride')
        vstride=self.get_input('vstride')
        return bezierPatchFlower(controlpointmatrix, ustride, vstride)
        #return bezierPatchFlower()
    
########################################
def rawFlower(points, turtle=None):
    '''    computes a flower from 2 pairs [position, diameter]
    '''
    # 
    turtle.push()
    turtle.setColor(3) # red
    #print "point= %s" % points
   
    turtle.oLineTo(points[0][0])
    Diameter=points[1][1]
    turtle.oLineTo(points[1][0])
    turtle.setWidth(Diameter*.5)
    turtle.pop()
# end rawFlower

def coneFlower():
    """ default function to draw up a flower 
    """
    # write the node code here.
    # return outputs
    return rawFlower,
# end coneFlower

class RawFlower(Node):
    def __init__(self):
        Node.__init__(self)
        self.add_output( name = 'compute_flower', 
                         interface = IFunction )

    def __call__( self, inputs ):
        return coneFlower()
########################################""

def noThing(points, turtle=None):
    """ """
    pass

def makeNoOrgan():
    '''    make no change to the turtle, so we can watch otherwise hidden details.
    '''
    # write the node code here.
    # return outputs
    return noThing,
# end makeNoLeaflet

class NoOrgan(Node):
    def __init__(self):
        Node.__init__(self)
        self.add_output( name = 'compute_nothing', 
                         interface = IFunction )

    def __call__( self, inputs ):
        return makeNoOrgan()

########################################

def ctrlpointMatrix():
    '''    control point matrix for bezier patches
    '''
    ctpm = None; 
    # write the node code here.
    # with a scale factor : seems to cause problems with Translate
    #ctpm = [[Vector4(0,0,0,7.),Vector4(0,0,0,7.)],[Vector4(2,-2,-0.8,7.),Vector4(2,2,-0.8,7.)],[Vector4(4,-4,-1.2,7.),Vector4(4,4,-1.2,7.)],[Vector4(6,-5,-1.5,7.),Vector4(6,5,-0.5,7.)],[Vector4(7,0,0,7.),Vector4(7,0,0,7.)]]
    # the previous, normalized 
    #ctpm = [[Vector4(0,-0.2,0,1),Vector4(0,0.2,0,1)],[Vector4(0.28,-0.38,-0.13,1),Vector4(0.28,0.38,-0.13,1)],[Vector4(.56,-0.56,-0.17,1),Vector4(.56,0.56,-0.17,1)],[Vector4(0.86,-0.7,-0.21,1),Vector4(.86,.7,-0.01,1)],[Vector4(1,-0.25,0,1),Vector4(1,0.25,0,1)]]
    # a new shape
    ctpm = [[Vector4(0,-0.2,0,1),Vector4(0,0.2,0,1)],[Vector4(0.28,-0.38,0.13,1),Vector4(0.28,0.38,0.13,1)],[Vector4(.56,-0.56,0.17,1),Vector4(.56,0.56,0.17,1)],[Vector4(0.86,-0.7,0.21,1),Vector4(.86,.7,0.5,1)],[Vector4(1,-0.25,1,1),Vector4(1,0.25,1,1)]]

    # return outputs
    return ctpm,

class ControlPointsMatrix(Node):
    def __init__(self):
        Node.__init__(self)
        self.add_output( name = 'ctpm', 
                         interface = IData )

    def __call__( self, inputs ):
        return ctrlpointMatrix()

########################################
def position(n):
    """ returns the position of the node in a Vector3 data """
    return Vector3(n.XX, n.YY, n.ZZ)
    
########################################
def vertexVisitor(leaf_factory=None, bud_factory=None, flower_factory=None ):
    '''    function to visit MTG nodes
    '''
    # write the node code here.   
    visitor = None; 

    if leaf_factory is None:
        leaf_factory=rawLeaflet
    if bud_factory is None:
        bud_factory=rawBud
    if flower_factory is None:
        flower_factory=rawFlower

    def visitor(g, v, turtle, \
                    leaf_computer=leaf_factory, \
                    bud_computer=bud_factory,\
                    flower_computer=flower_factory):
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
            points = [position(n.parent()), pt]
            while n.nb_children() == 1:
                n = list(n.children())[0]
                points.append(position(n))
            bud_computer(points,turtle)
#B            # 4 testing
#B            oldPt=turtle.getPosition()
#B            radiusOfBud=(pt-oldPt)*0.5
#B            centerOfBud=oldPt + radiusOfBud
#B            turtle.oLineTo(centerOfBud)
#B            turtle.push()
#B            #turtle.incColor()
#B            turtle.setColor(4) # apple green
#B            radius = norm(radiusOfBud)
#B            geometry=  Sphere(radius)
#B            #return Translated(distance, Sphere(radius))
#B            #geom = leaf_factory(points)
#B            turtle.customGeometry(geometry, 1)
#B            turtle.pop()
#B            turtle.setWidth(radius*.8)

        elif n.label == "O1" :
            #turtle.oLineTo(pt) # pt is the top of the flower
            points=[[position(n.parent()),n.parent().Diameter],[pt,n.Diameter]]
            flower_computer (points, turtle)

        elif n.label == "T1":
            # The turtle is supposed to be at the top of the previous vertex
            #turtle.stopGC() # not useful anymore
            turtle.incColor()
            #turtle.startGC()
            turtle.oLineTo(pt)
            turtle.setWidth(0.01)	    
            turtle.decColor()

    # return outputs
    return visitor,

class VertexVisitor(Node):
    def __init__(self):
        Node.__init__(self)
        self.add_input( name = 'leaf_factory',
                        interface = IFunction)
        self.add_input( name = 'bud_factory',
                        interface = IFunction)
        self.add_input( name = 'flower_factory',
                        interface = IFunction)
        self.add_output( name = 'VertexVisitor', 
                         interface = IFunction )

    def __call__( self, inputs ):
        leaf_factory=self.get_input('leaf_factory')
        bud_factory=self.get_input('bud_factory')
        flower_factory=self.get_input('flower_factory')
        return vertexVisitor(leaf_factory,bud_factory,flower_factory)
