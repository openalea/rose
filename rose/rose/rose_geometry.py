#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

from openalea.mtg.aml import MTG
import math
from openalea.mtg.plantframe import *

from openalea.core.external import * 
from openalea.core.logger  import *

# for TurtleFrame
import openalea.plantgl.all as pgl
from openalea.mtg.turtle import pre_order2_with_filter
#from openalea.mtg.plantframe import *
from openalea.mtg.traversal import pre_order2_with_filter

from rose_colors import *

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
    #Up=side^front
    Up=front^side
    Up.normalize()
    return Up
# end computeUpAxis

def headTo(turtle, direction):
    direction.normalize()
    upAxis=computeUpAxis(direction, Vector3(1,0,0))
    # ifever the direction  goes along the x axis :
    if abs(norm(upAxis)) < 0.001 :
        upAxis=computeUpAxis(direction, Vector3(0,1,0))
    turtle.setHead(direction,upAxis)

def printPoints(points):
    """ debug info """
    print "Zs : %7.3f  %7.3f %7.3f %7.3f"%(points[0][2],points[1][2],points[2][2],points[3][2])

################################################ BUD
def rawBud():
    ''' returns a function to draw 'raw' buds wiht a sphere and a cone'''
    
    def computeRawBud(points, turtle=None):
        #print "points= %s" %  points
        turtle.push()

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
        # ray of the floral receptacle
        step=norm(budAxis) /12.
        budAxis.normalize()
        #print "step=%f" % step
        #print "len(points)=%d" % len(points)

        turtle.push() #
        # prolongation of ped
        turtle.oLineTo(points[0])
        #turtle.setColor(4) # 
        ## we must orient the turtle before to draw 
        ## this makes better fitting of the sphere and the paraboloid
        headTo(turtle,budAxis)

        #radiusOfOvary=step /12. 
        #centerOfOvary=botPt + budAxis/12.
        # we prolongate the axis to intersect with the receptacle

        turtle.move(botPt + budAxis *step )
        # the ray of the receptacle is increased by 20% to intersect the upper sphere  
        turtle.customGeometry(Sphere(step * 1.2,lStride ), 1)
        # we draw the upper sphere of the bud (the one formd by the sepals)
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

        ## visual control test
        #turtle.move(topPt)
        #turtle.setColor(0)
        #turtle.customGeometry(Sphere(step/2.), 1)
        ## end test
        #turtle.move(Vector3(0,0,1) * step*1.5)
        
        turtle.pop()
    # end computeBuiltBud
        
    return computeBuiltBud
    # end builtBud

class BuiltBud(Node):
    def __init__(self):
        Node.__init__(self)
        self.add_input( name = 'stride', interface = IInt )
        self.add_output( name = 'compute_bud', 
                         interface = IFunction )
    def __call__( self, inputs ):
        stride=self.get_input('stride')
        return builtBud(stride)
   
###################################### Revolution Bud
def pointArray():
    ''' returns an array of points to feed a revolution object '''
    #print "Inside pointArray()" 
    pts=[Vector2(0.10, 0.00),
         Vector2(0.50, 0.06),
         Vector2(0.40, 0.14),
         Vector2(0.60, 0.18),
         Vector2(1.00, 0.30),
         Vector2(0.90, 0.42),
         Vector2(0.50, 0.60),
         Vector2(0.30, 0.84),
         Vector2(1.00, 1.00)] # to be edited
    return pts

def budArray():
    ''' returns an array of points to feed a revolution object
    Values are Vector2(ray, axial position) '''
    #print "Inside pointArray()" 
    pts=[Vector2(0.1, 0.00),
         Vector2(0.50, 0.06),
         Vector2(0.40, 0.14),
         Vector2(0.60, 0.18),
         Vector2(1.00, 0.30),
         Vector2(0.90, 0.42),
         Vector2(0.50, 0.60),
         Vector2(0.30, 0.84),
         Vector2(0.00, 1.00)]
    return pts

def fineBudArray():
    ''' returns an array of points to feed a revolution object 
    Values are Vector2(ray, axial position)'''
    #print "Inside pointArray()" 
    pts=[Vector2( 0.10, 0.00),
         Vector2( 0.40, 0.02),
         Vector2( 0.50, 0.06),
         Vector2( 0.50, 0.10),
         Vector2( 0.40, 0.14),
         Vector2( 0.40, 0.16),
         Vector2( 0.60, 0.18,),
         Vector2( 0.90, 0.24),
         Vector2( 1.00, 0.30 ),
         Vector2( 1.0, 0.34),
         Vector2( 0.707, 0.42),
         Vector2( 0.55, 0.48),
         Vector2( 0.40,0.60 ),
         Vector2( 0.30, 0.72),
         Vector2( 0.22, 0.84),
         Vector2( 0.10, 0.96),
         Vector2( 0.00,1.00 )]
    return pts

def revolution(points=None, stride=8):
    ''' returns a revolution volume made from the input points'''
    #lStride = stride
    if stride < 5:
        stride = 5

    if points is None:
        points=budArray()
    #print points
    pa=Point2Array(points)
    pl=Polyline2D(pa)
    rev=Revolution(pl,stride)
    return rev

def revolutionBud(revVol=None ):
    ''' We return a func that draws a bud from a revolution volume '''
    lRevVol=revVol
    if lRevVol is None:
        lRevVol=revolution(budArray())
    def drawRevBud(points, turtle=None):
            
        botPt=points[0]
        topPt=points[-1]
        budAxis=Vector3(topPt-botPt)
        lengthVector=budAxis
        length=norm(lengthVector)
        budAxis.normalize() # necessary ?

        turtle.push() #
        # prolongation of ped
        turtle.oLineTo(points[0])
        #turtle.push()
        turtle.oLineTo(points[0]+budAxis*4) # + 4 units (mm)
        #turtle.pop()
        #turtle.setColor(4) # 
       
        # we must orient the turtle before to draw 
        headTo(turtle,budAxis)

        revBud=Scaled(Vector3(length *0.2, length *0.2, length),  lRevVol)
        #revBud=Oriented(upAxis, budAxis, revBud)
        # we are ready to draw the rev'bud
        turtle.customGeometry(revBud,1)
        
        ## visual control test 
        #turtle.move(topPt)
        #turtle.setColor(0)
        #turtle.customGeometry(Sphere(length/12.), 1)
        ## end test # SUCCESSFUL @ 20111019

        turtle.pop()

    return drawRevBud

class PointArray(Node):
    def __init__(self):
        Node.__init__(self)
        self.add_output( name = 'pts_array', 
                         interface = ISequence )
    def __call__( self, inputs ):
        return pointArray()
  
class BudArray(Node):
    def __init__(self):
        Node.__init__(self)
        self.add_output( name = 'bud_array', 
                         interface = ISequence )
    def __call__( self, inputs ):
        return budArray()
  
class FineBudArray(Node):
    def __init__(self):
        Node.__init__(self)
        self.add_output( name = 'bud_array', 
                         interface = ISequence )
    def __call__( self, inputs ):
        return fineBudArray()
  

class RevolutionFig(Node):
    def __init__(self):
        Node.__init__(self)
        self.add_input( name = 'pointArray', interface = ISequence, value=None )
        self.add_input( name = 'stride', interface = IInt,  value=8)
        self.add_output( name = 'rev_fig', 
                         interface = IData )
    def __call__( self, inputs ):
        pointArray=self.get_input('pointArray')
        stride=self.get_input('stride')
        return revolution(pointArray, stride)

class RevolutionBud(Node):
    def __init__(self):
        Node.__init__(self)
        self.add_input( name = 'revFig', interface = IData, value=None )
        self.add_output( name = 'rev_bud', 
                         interface = IFunction )
    def __call__( self, inputs ):
        revFig=self.get_input('revFig')
        return (revolutionBud(revFig))
   
 ## GROUPING items for buds
class drawBuds(Node):
    def __init__(self):
        Node.__init__(self)
        self.add_output( name = 'budsComputers', 
                         interface = ISequence )

    def __call__( self, inputs ):
        return (noThing, rawBud(), builtBud(), revolutionBud() )
    

################################################ LEAFLET
def  displayNormalVector(turtle,points,color):
    turtle.push()
    turtle.move(points[0] +(points[2]-points[0]) *.5)
    turtle.setColor(color)
    turtle.customGeometry(Cone(2,13), 1)
    turtle.pop()

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

        # Half leaflets
        # A: the /right/ leaflet ("right" accordingly to the digitization protocol : 
        # the ending leaflet close to the observer).
        # Note that the points 2 and 4 of most leaflets has been swapped in
        # the program that converts the txt files to MTGs in order to turn
        # the leaflets upside-down in the MTG building, so that they get oriented UP.
        # So we treat the data as if the folks had turned CCw to digitize the leaflets.
        # 1st : compute the up axis of the (new) left(*) part of the leaflet
        # (*) left is seen from the bottom of the leaflet.
        #

        Axis=points[2]-points[0]
        axisLength=norm(Axis)
        Axis.normalize()

        # leftmost leaflet
        # normal Axis
        side=points[3]-points[0]
        sideLength=norm(side)
        side.normalize()
        normAxis=computeUpAxis(Axis,side)
        # dbg
        if abs(norm(normAxis)) < 0.001 :
            print "Z.bug= %s" % points[0][2]
        
        # 2nd : compute the width of this half leaflet (sideLength * sin(angle))
        halfWidth =  sideLength * norm(Axis^side)

        # jessica's code for  building the mesh
        # I tried to use zMesh, but it has had no efect.
        ls_pts=[Vector3(0.,0.,0.)]
        for i in xrange(len(xMesh)-1):
            ls_pts.append(Vector3(xMesh[i],yMesh[i],0))
            ls_pts.append(Vector3(xMesh[i],0,0))
        ls_pts.append(Vector3(1.,0.,0.))
        # we build triangles C O U N T E R Clockwise
        ls_ind=[Index3(0,2,1),Index3(1,2,3),Index3(2,4,3),Index3(3,4,5),Index3(4,6,5),Index3(5,6,7)]        
        triangleSet=TriangleSet(Point3Array(ls_pts),Index3Array(ls_ind))

        geom=triangleSet
        geom=Scaled((axisLength,halfWidth,1),geom)
        #setHead sets the turtle such as the xy plane is displayed by it side 
        turtle.setHead(normAxis,Axis)
        turtle.customGeometry(geom, 1)

        # 4 testing : display normal vector for this half-leaflet
        #displayNormalVector(turtle,points,0)

        # Rightmost leaflet
        # normAxis Axis
        side=points[1]-points[0]
        sideLength=norm(side)
        side.normalize()
        normAxis=computeUpAxis(side, Axis)
        
        #  compute the width of the right half leaflet
        halfWidth =  sideLength * norm(side^Axis)

        # we change the sign of the y coordinates of the mesh
        for meshPoint in ls_pts:
            meshPoint[1] *= -1.
        # As the Y coordinate has changed its sign, we build 
        # the triangles C C W again.
        ls_ind=[Index3(0,1,2),Index3(1,3,2),Index3(2,3,4),Index3(3,5,4),Index3(4,5,6),Index3(5,7,6)]
        triangleSet=TriangleSet(Point3Array(ls_pts),Index3Array(ls_ind))
        geom=triangleSet
        geom=Scaled((axisLength,halfWidth,1),geom)
        # setHead() see previously
        turtle.setHead(normAxis, Axis)
        turtle.customGeometry(geom, 1)

        # 4 testing
        #displayNormalVector(turtle,points,3)

#P        # polygon code for testing if it maps to the meshed leaves
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
#S        Lateral = computeLateralAxis(Axis, normAxis)
#S        turtle.setHead(Lateral,distance)
#S        geometry= Translated(Vector3(radius*10,0,0), Sphere(radius))
#S        turtle.setColor(0) # grey 
#S        turtle.customGeometry(geometry, 1)
#S        turtle.pop()

        turtle.pop() # against 1st push()
        
    # return outputs
    return meshedLeaflet

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
    return rawLeaflet
# end polygonLeaflet

class PolygonLeaflet(Node):
    def __init__(self):
        Node.__init__(self)
        self.add_output( name = 'compute_leaf', 
                         interface = IFunction )

    def __call__( self, inputs ):
        return polygonLeaflet()

 ## GROUPING items for leaves
class drawLeaves(Node):
    def __init__(self):
        Node.__init__(self)
        self.add_output( name = 'leavesComputers', 
                         interface = ISequence )

    def __call__( self, inputs ):
        return (noThing, rawLeaflet, computeLeaflet4pts() )
    

######################################## FLOWER
def bezierPatchFlower(controlpointmatrix=None,ustride=8,vstride=8,colorFunc=None):
    ''' interface to return bpFlower ''' 
    bpFlower=None
    #print "BezierPatchFlower called ; uStride is %s" % ustride
    # write the node code here.
    lControlpointmatrix=controlpointmatrix

    #print "controlpointmatrix = %s" % controlpointmatrix
    if controlpointmatrix is None:
        # the return value of ctrlpointMatrix() yields an error. Why ?
        #lControlpointmatrix = ctrlpointMatrix()
        lControlpointmatrix= [[Vector4(0,-0.2,0,1),Vector4(0,0.2,0,1)],
                              [Vector4(0.28,-0.38,0.13,1),Vector4(0.28,0.38,0.13,1)],
                              [Vector4(.56,-0.56,0.17,1),Vector4(.56,0.56,0.17,1)],
                              [Vector4(0.86,-0.7,0.21,1),Vector4(.86,.7,0.5,1)],
                              [Vector4(1,-0.25,1,1),Vector4(1,0.25,1,1)]]
    #print "lControlpointmatrix = %s" % lControlpointmatrix
    myColorFunc=colorFunc
    if colorFunc is None:
        myColorFunc=setTurtlePink # custom 
        
    def bpFlower(pointsnDiameters, turtle=None,):
        ''' computes a flower from two points and the diameters associated to 
        the flower.
        @param points : list of pairs[Vector3, scalar] resp. (position;diameter)
        '''
        luStride=ustride
        lvStride=vstride
        if luStride < 5:
            luStride = 5
        if lvStride < 5:
            lvStride = 5
        #ustride=5 
        #vstride=5 

        basePos=pointsnDiameters[0][0]
        topPos=pointsnDiameters[1][0]
        pedDiam=pointsnDiameters[0][1]
        flowerRay=pointsnDiameters[1][1] * 0.5
        flowerHeight=norm(topPos-basePos)
        baseRay=max(flowerRay *0.2, flowerHeight*0.2) # arbitrarily
        deltaRay=flowerRay-baseRay
        petalLength=math.sqrt(flowerHeight*flowerHeight + deltaRay*deltaRay)

        # we build the generic patch
        petalMesh=BezierPatch(lControlpointmatrix,luStride, lvStride)
        # patch is scaled according to the global flower dimensions
        petalMesh=Scaled(Vector3(petalLength,max(baseRay,flowerRay)*1.1,baseRay),petalMesh)
        # 
        rad5eTour=math.pi/2.5 # a fifth of a tour

        # compute the pitch angle (flower opening)
        if deltaRay > 0 : # opened flower
            openingAngle=math.atan(flowerHeight/(deltaRay))
        elif deltaRay < 0 : # flower not opened yet
            openingAngle=math.pi*0.5+math.atan((-deltaRay)/flowerHeight)
        else: # say half opened
            openingAngle=math.pi*0.5

        #ovary=Disc(baseRay ,luStride)
        ovary=Sphere(baseRay ,luStride)

        turtle.push() # we draw now

        #  orient the turtle 
        flowerAxis=topPos-basePos
        headTo(turtle,flowerAxis)
        #turtle.setColor(4) # kind of yellow-green
        turtle.customGeometry(ovary, 1) # 

        myColorFunc(turtle)

        for iIndex in range(0,5):
            # closing the flower : 
            petal=AxisRotated((0,1,0),-openingAngle,petalMesh)
            # twisting a bit to limit collisions [Todo in the patch]
            # NOTWIST 4 test petal=AxisRotated((1,0,0),openingAngle*0.05,petal)
            petal=AxisRotated((1,0,0),openingAngle*0.055, petal)# HALFTWIST 4 test 
            angle=iIndex*rad5eTour
            petal=AxisRotated((0,0,1),angle,petal)
            petal=Translated(Vector3(baseRay *math.cos(angle) *0.8,\
                                         baseRay *math.sin(angle) *0.8,\
                                         0),\
                                 petal)
            turtle.customGeometry(petal, 1) #flowerHeight) #  

        ## visual control test 
        #turtle.move(topPos)
        #turtle.setColor(0)
        #turtle.customGeometry(Sphere(flowerHeight/10.), 1)
        ## successful @20111003 : sphere in flower axis

        turtle.pop()

    return bpFlower

class BezierPatchFlower(Node):
    ''' '''
    def __init__(self):
        Node.__init__(self)
        self.add_input( name='controlpointmatrix', interface=ISequence, value=None)
        self.add_input(name='ustride', interface=IInt)
        self.add_input(name='vstride', interface=IInt)
        self.add_input( name='colorFunc', interface=IFunction, value=None)
        self.add_output( name = 'compute_flower', interface = IFunction )
        
    def __call__( self, inputs ): 
        controlpointmatrix=self.get_input('controlpointmatrix')
        ustride=self.get_input('ustride')
        vstride=self.get_input('vstride')
        colorFunc=self.get_input('colorFunc')
        
        return bezierPatchFlower(controlpointmatrix, ustride, vstride, colorFunc)
        #return bezierPatchFlower()
    
########################################
def coneFlower(colorFunc=None):
    """ default function to draw up a flower 
    """
    # write the node code here.
    myColorFunc=colorFunc
    if colorFunc is None:
        myColorFunc=setTurtlePink # custom 
        
    def rawFlower(pointsnDiameters, turtle=None):
        '''    computes a flower from 2 pairs [position, diameter]
        '''
        # 
        turtle.push()
        # 
        myColorFunc(turtle)
        #print "point= %s" % pointsnDiameters
        
        turtle.oLineTo(pointsnDiameters[0][0])
        Diameter=pointsnDiameters[1][1]
        turtle.oLineTo(pointsnDiameters[1][0])
        turtle.setWidth(Diameter*.5)
        turtle.pop()
        # end rawFlower
    # return outputs
    return rawFlower
# end coneFlower

class RawFlower(Node):
    def __init__(self):
        Node.__init__(self)
        self.add_input( name='colorFunc', interface=IFunction, value=None)
        self.add_output( name = 'compute_flower', 
                         interface = IFunction )

    def __call__( self, inputs ):
        colorFunc=self.get_input('colorFunc')
        return coneFlower(colorFunc)

def taperedFlower(ctrlPntMatrix=None,ustride=8,vstride=8, colorFunc=None):
    ''' interface to return bpFlower ''' 
    bpFlower=None
    #print "BezierPatchFlower called ; uStride is %s" % ustride
    # write the node code here.
    lCtrlPntMatrix=ctrlPntMatrix

    #print "ctrlPntMatrix = %s" % ctrlPntMatrix
    if ctrlPntMatrix is None:
        # the return value of ctrlpointMatrix() yields an error. Why ?
        lCtrlPntMatrix= [[Vector4(0,-0.40,0,1),Vector4(0,0.4,0,1)],
                         [Vector4(0.28,-0.45,0.08,1),Vector4(0.28,0.45,0.08,1)],
                         [Vector4(.56,-0.45,0.31,1),Vector4(.56,0.45,0.31,1)],
                         [Vector4(0.86,-0.45,0.73,1),Vector4(.86,0.45,0.75,1)],
                         [Vector4(0.95,-0.5,0.9,1),Vector4(.96,0.5,0.9,1)],
                         [Vector4(0.98,-0.45,0.96,1),Vector4(.98,.45,0.96,1)],
                         [Vector4(1,-0.10,1,1),Vector4(1,0.10,1,1)]]
    #print "lCtrlPntMatrix = %s" % lCtrlPntMatrix
    myColorFunc=colorFunc
    if colorFunc is None:
        myColorFunc=setTurtlePink # custom 
       
    def tpFlower(pointsnDiameters, turtle=None,):
        ''' computes a flower from two points and the diameters associated to 
        the flower.
        @param pointsnDiameters : list of pairs[Vector3, scalar] resp. (position;diameter)
        '''
        luStride=ustride
        lvStride=vstride
        if luStride < 5:
            luStride = 5
        if lvStride < 5:
            lvStride = 5
        #ustride=5 
        #vstride=5 
        basePos=pointsnDiameters[0][0]
        topPos=pointsnDiameters[1][0]
        pedDiam=pointsnDiameters[0][1]
        flowerRay=pointsnDiameters[1][1] * 0.5
        flowerHeight=norm(topPos-basePos)
        baseRay=max(flowerRay *0.2, flowerHeight*0.2) # arbitrarily
        #deltaRay=flowerRay-baseRay
        #petalLength=math.sqrt(flowerHeight*flowerHeight + deltaRay*deltaRay)
        rad5eTour=math.pi/2.5 # a fifth of a tour

        # we build the generic patch
        petalMesh=BezierPatch(lCtrlPntMatrix,luStride, lvStride)

        turtle.push()

        #  orient the turtle 
        flowerAxis=topPos-basePos
        headTo(turtle,flowerAxis)

        #ovary=Disc(baseRay ,luStride)
        ovary=Sphere(baseRay ,luStride)
        #turtle.setColor(4) # kind of yellow-green
        turtle.customGeometry(ovary, 1) #  we draw the ovary now

        myColorFunc(turtle) 
        
        # we shall draw two rows of petals
        moreRoll=0.
        for row in range(0,2):
            
            baseRay=max(flowerRay *0.2, flowerHeight*0.2) # arbitrarily
            deltaRay=flowerRay-baseRay
            petalLength=math.sqrt(flowerHeight*flowerHeight + deltaRay*deltaRay)
            localMesh=Tapered(baseRay/flowerRay,1,petalMesh)
            # patch is scaled according to the global flower dimensions
            localMesh=Scaled(Vector3(petalLength,
                                     max(baseRay,flowerRay)*1.1,
                                     baseRay),
                             localMesh)

            # compute the pitch angle (flower opening)
            if deltaRay > 0 : # opened flower
                openingAngle=math.atan(flowerHeight/(deltaRay))
            elif deltaRay < 0 : # flower not opened yet
                openingAngle=math.pi*0.5+math.atan((-deltaRay)/flowerHeight)
            else: # say half opened
                openingAngle=math.pi*0.5


            # TODO : compute the closing angle of the petals from height and width

            for iIndex in range(0,5):
                # closing the flower : 
                petal=AxisRotated((0,1,0),-openingAngle,localMesh)
                # twisting a bit to limit collisions [Todo in the patch]
                #petal=AxisRotated((1,0,0),openingAngle*0.05,petal)
                angle=(iIndex+moreRoll)*rad5eTour
                petal=AxisRotated((0,0,1),angle,petal)
                petal=Translated(Vector3(baseRay *math.cos(angle) *0.8,\
                                             baseRay *math.sin(angle) *0.8,\
                                             0),\
                                     petal)
                turtle.customGeometry(petal, 1) #flowerHeight) #  
            moreRoll=0.5
            flowerRay *= 0.8

        ## visual control test 
        #turtle.move(topPos)
        #turtle.setColor(0)
        #turtle.customGeometry(Sphere(flowerHeight/10.), 1)
        ## successful @20111003 : sphere in flower axis

        turtle.pop()


    return tpFlower

class TaperedFlower(Node):
    def __init__(self):
        Node.__init__(self)
        self.add_input( name='controlpointmatrix', interface=ISequence, value=None)
        self.add_input(name='ustride', interface=IInt, value=5 )
        self.add_input(name='vstride', interface=IInt, value=5 )
        self.add_input( name='colorFunc', interface=IFunction, value=None)
        self.add_output( name = 'compute_flower', 
                         interface = IFunction )

    def __call__( self, inputs ):
        controlpointmatrix=self.get_input('controlpointmatrix')
        ustride=self.get_input('ustride')
        vstride=self.get_input('vstride')
        colorFunc=self.get_input('colorFunc')
        return taperedFlower(controlpointmatrix, ustride, vstride, colorFunc)

######################################## Fruit

def simpleFruit(colorFunc=None):
    """ default function to draw up a flower 
    """
    # write the node code here.
    myColorFunc=colorFunc
    if colorFunc is None:
        myColorFunc=setTurtleOrange # custom 
        
    def rawFruit(points, turtle=None):
        '''    computes a fruit from a pair or positions
        '''
        # 
        turtle.push()
        # 
        myColorFunc(turtle)
        #print "point= %s" % pointsnDiameters
        
        turtle.oLineTo(points[0])
        #turtle.oLineTo(points[1])
        #turtle.setWidth(10)
        botPt=points[0]
        topPt=points[-1]
        fruitAxis=Vector3(topPt-botPt)
        # digit point is on top of etamins
        # etamins are not represented 
        fruitSize=norm(fruitAxis) * 0.5 
        fruitAxis.normalize()

        ## we must orient the turtle before to draw 
        ## this makes better fitting of the sphere and the paraboloid
        headTo(turtle, fruitAxis)

        turtle.move(botPt + fruitAxis * 0.5 )
        fruit=Scaled(Vector3(fruitSize*.66, fruitSize*.66 , fruitSize),  Sphere())

        turtle.customGeometry(fruit, 1)

        turtle.pop()
        # end rawFruit
    # return outputs
    return rawFruit
# end simpleFruit

class RawFruit(Node):
    def __init__(self):
        Node.__init__(self)
        self.add_input( name='colorFunc', interface=IFunction, value=None)
        self.add_output( name = 'compute_flower', 
                         interface = IFunction )

    def __call__( self, inputs ):
        colorFunc=self.get_input('colorFunc')
        return simpleFruit(colorFunc)



########################################

def noThing(points, turtle=None):
    """ """
    pass

def makeNoOrgan():
    '''    make no change to the turtle, so we can watch otherwise hidden details.
    '''
    # write the node code here.
    # return outputs
    return noThing
# end makeNoLeaflet

class NoOrgan(Node):
    def __init__(self):
        Node.__init__(self)
        self.add_output( name = 'compute_nothing', 
                         interface = IFunction )

    def __call__( self, inputs ):
        return makeNoOrgan()

########################################

ctpm = [[Vector4(0,-0.2,0,1),Vector4(0,0.2,0,1)],[Vector4(0.28,-0.38,0.13,1),Vector4(0.28,0.38,0.13,1)],[Vector4(.56,-0.56,0.17,1),Vector4(.56,0.56,0.17,1)],[Vector4(0.86,-0.7,0.21,1),Vector4(.86,.7,0.5,1)],[Vector4(1,-0.25,1,1),Vector4(1,0.25,1,1)]]

def ctrlpointMatrix():
    '''    control point matrix for bezier patches
    '''
    #ctpm = None; 
    # write the node code here.
    # with a scale factor : seems to cause problems with Translate
    #ctpm = [[Vector4(0,0,0,7.),Vector4(0,0,0,7.)],[Vector4(2,-2,-0.8,7.),Vector4(2,2,-0.8,7.)],[Vector4(4,-4,-1.2,7.),Vector4(4,4,-1.2,7.)],[Vector4(6,-5,-1.5,7.),Vector4(6,5,-0.5,7.)],[Vector4(7,0,0,7.),Vector4(7,0,0,7.)]]
    # the previous, normalized 
    #ctpm = [[Vector4(0,-0.2,0,1),Vector4(0,0.2,0,1)],            [Vector4(0.28,-0.38,-0.13,1),Vector4(0.28,0.38,-0.13,1)],            [Vector4(.56,-0.56,-0.17,1),Vector4(.56,0.56,-0.17,1)],            [Vector4(0.86,-0.7,-0.21,1),Vector4(.86,.7,-0.01,1)],            [Vector4(1,-0.25,0,1),Vector4(1,0.25,0,1)]]
    # a new shape
    ctpm=  [[Vector4(0,-0.40,0,1),Vector4(0,0.4,0,1)],
            [Vector4(0.28,-0.45,0.08,1),Vector4(0.28,0.45,0.08,1)],
            [Vector4(.56,-0.45,0.31,1),Vector4(.56,0.45,0.31,1)],
            [Vector4(0.86,-0.45,0.73,1),Vector4(.86,0.45,0.75,1)],
            [Vector4(0.95,-0.5,0.9,1),Vector4(.96,0.5,0.9,1)],
            [Vector4(0.98,-0.45,0.96,1),Vector4(.98,.45,0.96,1)],
            [Vector4(1,-0.10,1,1),Vector4(1,0.10,1,1)]]
    # return outputs
    return ctpm,

class ControlPointsMatrix(Node):
    def __init__(self):
        Node.__init__(self)
        self.add_output( name = 'ctpm', 
                         interface = IData )

    def __call__( self, inputs ):
        return ctrlpointMatrix()

def petalMatrix():
    '''    control point matrix for a bezier patch close to a petal
    '''
    from openalea.mtg.plantframe import Vector4 as V4
    ctpm = None; 
    # write the node code here.
    ctpm = [[V4(0,    -0.12,   0.,   1), V4(0,     0, -0,   1),  V4(0,     0.12,  0.,   1)],
            [V4(0.14, -0.25,  -0.2,  1), V4(0.14,  0, -0.25, 1),  V4(0.13, 0.25, -0.2,  1)],
            [V4(.28,  -0.25,   0.35, 1), V4(0.28,  0,  0.2 , 1),  V4(.28,  0.25,  0.35, 1)],
            [V4(.42,  -0.25,   0.55, 1), V4(0.42,  0,  0.3,  1),  V4(.42,  0.25,  0.55, 1)],
            [V4(0.56, -0.30,   0.6,  1), V4(0.56,  0,  0.15, 1),  V4(.56,  0.3,   0.6,  1)],
            [V4(0.7,  -0.33,   0.6,  1), V4(0.7,   0,  0.1,  1),  V4(.7,   0.48,  0.33, 1)],
            [V4(0.84, -0.42,   0.75, 1), V4(0.84,  0,  0.4 , 1),  V4(.84,   .42,  0.75, 1)],
            [V4(0.97, -0.38,   0.8,  1), V4(0.97,  0,  0.5,  1),  V4(.97,   .38,  0.8,  1)],
            [V4(0.95, -0.1,    0.95, 1), V4(1, 0,  1,        1),  V4(0.95, 0.1,   0.95, 1)]]
    # return outputs
    return ctpm,

class PetalMatrix(Node):
    def __init__(self):
        Node.__init__(self)
        self.add_output( name = 'ctpm', 
                         interface = IData )

    def __call__( self, inputs ):
        return petalMatrix()

########################################
def position(n):
    """ returns the position of the node in a Vector3 data """
    return Vector3(n.XX, n.YY, n.ZZ)
    
########################################
def vertexVisitor(leaf_factory=None, bud_factory=None, sepal_factory=None, flower_factory=None, fruit_factory=None ):
    '''    function to visit MTG nodes
    '''
    # write the node code here.   
    visitor = None; 

    if leaf_factory is None:
        leaf_factory=rawLeaflet
    if bud_factory is None:
        bud_factory=rawBud
    if sepal_factory is None:
        sepal_factory=polygonLeaflet() # rawLeaflet
    if flower_factory is None:
        flower_factory=coneFlower() # bug when flower_factory is None
    if fruit_factory is None:
        fruit_factory=simpleFruit() # bug "'tuple' object is not callable" if fruit_factory is None 

    # to store sepals whila awaiting for flower data
    lSepalStore=[]

    def visitor(g, v, turtle, \
                    leaf_computer=leaf_factory, \
                    bud_computer=bud_factory,\
                    sepal_computer=sepal_factory,\
                    flower_computer=flower_factory,\
                    fruit_computer=fruit_factory):
        n = g.node(v)
        pt = position(n)
        symbol = n.label[0]
        turtle.setId(v)
        currentColor=turtle.getColor()

        if symbol in ['E', 'R']:
            if n.Diameter is None:
                print 'ERROR: vertex %d (name: %s, line around %d)'%(v,n.label,n._line)
                n.Diameter = 0.75

            if n.edge_type() == '+'  or not n.parent():
                turtle.setWidth(n.Diameter / 2.)

            turtle.oLineTo(pt)
            turtle.setWidth(n.Diameter / 2.)

        elif n.label ==  'F1' :
            turtle.setColor(2) # internode
            points = [position(n.parent()), pt]
            while n.nb_children() == 1:
                n = list(n.children())[0]
                points.append(position(n))
            leaf_computer(points,turtle)

        elif n.label == 'S1' :
            turtle.setColor(4) # apple green
            points = [position(n.parent()), pt]
            while n.nb_children() == 1:
                n = list(n.children())[0]
                points.append(position(n))
            
            lSepalStore.append(points)
            #sepal_computer(points,turtle)
	    
        elif n.label == "B1" :
            turtle.setColor(4) # apple green
            # process sepals
            while lSepalStore:
                sepal_computer(lSepalStore.pop(),turtle)

            points = [position(n.parent()), pt]
            while n.nb_children() == 1:
                n = list(n.children())[0]
                points.append(position(n))
            bud_computer(points,turtle)

        elif n.label == "O1" :
            #turtle.oLineTo(pt) # pt is the top of the flower
            turtle.setColor(4) # apple green

            # process sepals
            while lSepalStore:
                sepal_computer(lSepalStore.pop(),turtle)

            points=[[position(n.parent()),n.parent().Diameter],[pt,n.Diameter]]
            flower_computer (points, turtle)

        elif n.label == "C1" :

            turtle.setColor(4) # apple green
            # process sepals
            while lSepalStore:
                sepal_computer(lSepalStore.pop(),turtle)

            points=[position(n.parent()), pt]
            fruit_computer (points, turtle)

            # process sepals
        elif n.label == "T1":
            # The turtle is supposed to be at the top of the previous vertex
            #turtle.stopGC() # not useful anymore
            turtle.setColor(2) # green
            #turtle.startGC()
            turtle.oLineTo(pt)
            turtle.setWidth(0.01)

        turtle.setColor(currentColor)

    # return outputs
    return visitor

class VertexVisitor(Node):
    def __init__(self):
        Node.__init__(self)
        self.add_input( name = 'leaf_factory',
                        interface = IFunction)
        self.add_input( name = 'bud_factory',
                        interface = IFunction)
        self.add_input( name = 'sepal_factory',
                        interface = IFunction)
        self.add_input( name = 'flower_factory',
                        interface = IFunction)
        self.add_input( name = 'fruit_factory',
                        interface = IFunction)
        self.add_output( name = 'VertexVisitor', 
                         interface = IFunction )

    def __call__( self, inputs ):
        leaf_factory=self.get_input('leaf_factory')
        bud_factory=self.get_input('bud_factory')
        sepal_factory=self.get_input('sepal_factory')
        flower_factory=self.get_input('flower_factory')
        fruit_factory=self.get_input('fruit_factory')
        return vertexVisitor(leaf_factory,bud_factory,sepal_factory,flower_factory,fruit_factory)


#################################### ReconstructWithTurtle ##########

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
    ## we want to change the default color
    ## let's wait to have scanned some photographs to set this
    #setTurtleStrand(turtle)

    for plant_id in g.vertices(scale=1):
        plant_node = g.node(plant_id)
        # moved the "position" function away
        origin = pgl.Vector3(plant_node.XX, plant_node.YY, plant_node.ZZ)
        turtle.move(origin)

        vid =  g.component_roots_at_scale(plant_id, scale=n).next()
        traverse_with_turtle(g, vid, visitor, turtle)
    return turtle.getScene()

def reconstructWithTurtle(mtg, visitor, powerParam):
    '''    builds a scene from "4pts leaflet" MTGs
    
    .. todo:: Add some constant in the arguments
    '''
    # Compute the radius with pipe model
    theScene=None
    diameter = mtg.property('Diameter')
    for v in mtg:
        if mtg.class_name(v) == 'R':
            diameter[v] = 0.75

    drf = DressingData(LeafClass=['F', 'S'], 
        FlowerClass='O', FruitClass='C',
        MinTopDiameter=dict(E=0.5))
    pf = PlantFrame(mtg, TopDiameter='Diameter', 
                    DressingData=drf, 
                    Exclude = 'F S O B T'.split())
    #diameter = pf.algo_diameter(power=powerParam)
    #mtg.properties()['Diameter'] = diameter 
    #test : 
    mtg.properties()['Diameter'] = pf.algo_diameter(power=powerParam)

    theScene=TurtleFrame(mtg, visitor)
    # return outputs
    return theScene,

class ReconstructWithTurtle(Node):
    def __init__(self):
        Node.__init__(self)
        self.add_input( name = 'g', interface=IData)
        self.add_input( name = 'Visitor', interface=IFunction)
        self.add_input( name = 'powerParam', value=2.2, interface=IFloat)
        self.add_output(name = 'TheScene', interface = IData)

    def __call__( self, inputs ):
        g = self.get_input( 'g' )
        Visitor = self.get_input( 'Visitor' )
        powerParam = self.get_input( 'powerParam' )
        return reconstructWithTurtle(g, Visitor, powerParam)
#end ReconstructWithTurtle
