#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-
#
# $Id$
#
"""
.. module rose_geometry
.. moduleauthor:: H. Autret <herve.autret@inra.fr>
"""

import json
import os
import re

import numpy as np

# for TurtleFrame
import openalea.plantgl.all as pgl
from openalea.core.external import (
    Node,
    IFunction,
    ISequence,
    IDict,
    IInt,
    IData,
    IFloat,
    IStr,
)  # *
from openalea.core.logger import logging  # *
from openalea.mtg import DressingData, PlantFrame  # , MTG

# walk through MTG trees
from openalea.mtg.traversal import pre_order2_with_filter
from openalea.plantgl.math import Vector4, Vector3, Vector2, norm, cross, dot

from openalea.rose.mockup import rose_colors as myColors
from openalea.rose.mockup import rose_time

# from openalea.plantgl import PglTurtle

deg2rad = np.pi / 180.0  # convert degrees to radians
rad2deg = 1 / deg2rad


## G E N E R A L  functions
def computeHeading(points):
    """computes the unity vector Hf that points from the 1st to
    the last point of the list, and computes their distance lf.
    returns a pair (Hf, lf)

    :param points: a list of points
    :return: a pair (Hf, lf)
    """
    basePos = points[0]

    topPos = points[-1]
    axis = topPos - basePos
    distance = norm(axis)
    axis.normalize()

    return axis, distance


# end computeHeading(points)


def computeLateralAxis(front, up):
    """
    Computes and returns a *Lateral* normalized vector that is:
      - normal to the <front,up> plane
      - such as (front, Lateral, up) is a direct mark

    :param front: front vector (say **x**)
    :param up: up vector (say **z**)
    :return: a vector pointing on the left side direction (say **y**)
    :note: The parameters and the return value are supposed to be openalea.mtg.plantframe::Vector3
    """
    Lateral = front ^ up
    Lateral.normalize()
    return Lateral


# end computeLateralAxis(front, up)


def computeFacingFromUp(Up):
    """
    Computes and returns a *Facing* normalized vector (say the local *i*) that is:
      - normal to Up
      - such as Up ^ Facing is horizontal and is the local *y*

     To do so, it does compute a horizontal direction Yo such as : Yo . Up = 0.
     Because Yo is horizontal and exists by construction, so Facing = Yo cross Up

    :param up: local up vector (the local **z**)
    :return: a vector pointing in the front direction (the local **x**)
    :note: The parameter and the return value are supposed to be openalea.mtg.plantframe::Vector3
    """
    epsilon = 1e-4
    Up.normalize()
    Ux = Up[0]
    Uy = Up[1]
    if abs(Ux) <= epsilon:
        Hy = 0
        Hx = -Uy
    elif abs(Uy) <= epsilon:
        Hx = 0
        Hy = -Ux
    else:
        Hx = 1
        Hy = -Ux / Uy
    Horiz = Vector3([Hx, Hy, 0])
    Horiz.normalize()

    # Now, let's compute Facing
    Facing = cross(Horiz, Up)
    return Facing


# end computeFacingFromUp(Up)


def computeUpAxis(front, side):
    """Computes and returns a vector that is normal to front and
    supposed to point upside the half leaflet.

    :param front: a vector pointing in the front direction (say **x**)
    :param side: a vector pointing on the left side direction (say **y**)
    :return: the heading (up) direction (say **z**)

    :note: The parameters and the return value are supposed to be openalea.mtg.plantframe::Vector3

    """
    # Up=side^front
    Up = front ^ side
    Up.normalize()
    return Up


# end computeUpAxis(front,side)


def faceTo(turtle, facingDirection):
    """This routine makes the turtle point its face to facingDirection,
    with a local up vector orthogonal to that direction. The lateral direction will be horizontal.

    :param turtle: an openalea.plantgl.all::PglTurtle object that is to be oriented
    :param facingDirection: an openalea.mtg.plantframe::Vector3 object that points to the future **x** direction.
    :note: the new heading of the turtle might be not as vertical as possible.

    To do so, it should take to compute :

    - Lo = facingDirection cross (0,0,1) so that Lo is horizontal or very small.
        - if Lo is horizontal, so Head=Lo cross facingDirection,
        - else Head=(1,0,0) or so because facingDirection is about vertical, so there !
    """
    facingDirection.normalize()
    upAxis = computeUpAxis(facingDirection, Vector3(1, 0, 0))
    # ifever the direction  goes along the x axis :
    if abs(norm(upAxis)) < 0.001:
        upAxis = computeUpAxis(facingDirection, Vector3(0, 1, 0))
    turtle.setHead(facingDirection, upAxis)


# end faceTo(turtle, facingDirection)


def getSiCo(angle):
    """Computes sine and cosine of the angle in radians

    :param angle: the angle to process
    :return: a pair (sin(angle), cos(angle))
    """
    return np.sin(angle), np.cos(angle)


# end fgetSiCo(angle)


def printPoints(points):
    """prints the z coordinate of the points

    :param points: unchecked list of 4 Vector3 (or Vector4 as well).
    :note: this a debugging purpose routine.
    """
    print(
        "Zs : %7.3f  %7.3f %7.3f %7.3f"
        % (points[0][2], points[1][2], points[2][2], points[3][2])
    )


# end printPoints(points)


def inSector(candidat, center, marge):
    """We check if candidate is in the neighborhood of center modulo 2.Pi
    I.e. if candidate belongs to [center-marge, center+marge[

    :param candidat: the value to be tested
    :param center: the center of a left-closed and right opened interval
    :param marge: the half-width of the interval
    return: True if candidate belongs to the interval
    """
    # get center inside the 1st tour
    while center > 2 * np.pi:
        center -= 2 * np.pi
    while center < 0:
        center += 2 * np.pi
    # get candidat inside the 1st tour
    while candidat > 2 * np.pi:
        candidat -= 2 * np.pi
    while candidat < 0:
        candidat += 2 * np.pi

    return center - marge <= candidat < center + marge

# end inSector(candidat, center, marge)


# %% ########################################### BUD
def rawBud():
    """We define here a function (computeRawBud) that draws a raw bud
     with a sphere and a cone.

    :returns: the function computeRawBud
    """

    def computeRawBud(points, turtle=None):
        """draws a bud by using a sphere and a cone :
        puts the sphere at the bottom using the "haut1" point
        and then draws the cone from the bottom to the top "haut2".

        :param points: a list of 3 Vector3
        :param turtle: an openalea.plantgl.all::PglTurtle object to draw objects on
        :note: this rather a test routine.
        """
        turtle.push()

        oldPt = points[0][0]
        radiusOfBud = (points[1][0] - oldPt) * 0.5
        centerOfBud = oldPt + radiusOfBud
        turtle.oLineTo(centerOfBud)
        turtle.push()
        radius = norm(radiusOfBud)
        geometry = pgl.Sphere(radius)
        turtle.customGeometry(geometry, 1)
        turtle.pop()
        turtle.setWidth(radius * 0.8)
        # top not forgotten
        turtle.oLineTo(points[2][0])
        turtle.setWidth(0.01)
        turtle.pop()

    # end computeRawBud

    return computeRawBud


# end rawBud()


class RawBud(Node):
    def __init__(self):
        Node.__init__(self)
        self.add_output(name="compute_bud", interface=IFunction)

    def __call__(self, inputs):
        return rawBud()


# end RawBud      (rawBud wrapper)


################################################ BILTBUD
def builtBud(stride=10):
    """
    we define here a nested function (computeBuiltBud) to draw buds with a sphere and a Paraboloid.
    The paraboloid is imported from openalea.mtg.plantframe

    :param stride: the stride of the paraboloid
    :returns: the computeBuiltBud function
    """

    def computeBuiltBud(points, turtle=None):
        """draw a bud with 2 spheres and a paraboloid

        :param points: a list of coordinates in Vector3 (openalea.mtg.plantframe::Vector3)
        :note: we use the bottom point "ped" and the top point "haut2"
        :todo: adjust the paraboloid onto the upper sphere
        """
        # TODO2 : parametrize and simplify that stuff of variables

        # fineness of drawing definition
        lStride = stride
        if lStride < 5:
            lStride = 5

        botPt = points[0][0]
        topPt = points[2][0]
        budAxis = Vector3(topPt - botPt)
        # ray of the floral receptacle
        step = norm(budAxis) / 12.0
        budAxis.normalize()

        turtle.push()  #
        # prolongation of ped
        turtle.oLineTo(points[0][0])
        turtle.setColor(4)  #
        ## we must orient the turtle before to draw
        ## this makes better fitting of the sphere and the paraboloid
        faceTo(turtle, budAxis)

        # radiusOfOvary=step /12.
        # centerOfOvary=botPt + budAxis/12.
        # we prolong the axis to intersect with the receptacle

        turtle.move(botPt + budAxis * step)
        # the ray of the receptacle is increased by 20% to intersect the upper sphere
        turtle.customGeometry(pgl.Sphere(step * 1.2, lStride), 1)
        # we draw the upper sphere of the bud (the one formed by the sepals)
        turtle.move(botPt + budAxis * step * 4)
        turtle.customGeometry(pgl.Sphere(step * 2, lStride), 1)

        # we move to the center of the 2nd sph plus a half ray,
        # i.e ray * sin(pi/6) (step *5, say) adjusted to 4.9 because
        # the base of the paraboloid appears rather dark if visible.
        turtle.move(botPt + budAxis * step * 4.9)
        # so the base diameter of the paraboloid is ray * cos(pi/6)
        # its length is bud heigth * (12 -4.9) / 12
        # its concavity is fitted to make it tangent to the sphere
        para = pgl.Paraboloid(step * 1.732, step * 7.1, 0.4, True, lStride, lStride)
        turtle.customGeometry(para, 1)

        #        # visual control test
        #        turtle.move(topPt)
        #        turtle.setColor(0)
        #        turtle.customGeometry(Sphere(step/2.), 1)
        #        # end test
        #        turtle.move(Vector3(0,0,1) * step*1.5)

        turtle.pop()

    # end computeBuiltBud

    return computeBuiltBud


# end builtBud(stride)


class BuiltBud(Node):
    def __init__(self):
        Node.__init__(self)
        self.add_input(name="stride", interface=IInt)
        self.add_output(name="compute_bud", interface=IFunction)

    def __call__(self, inputs):
        stride = self.get_input("stride")
        return builtBud(stride)


# end BuiltBud    (builtBud wrapper)

############################################# End Generic _BUD_


def flower(points, turtle=None, lSepales=None, diameter=None):
    """
    We compute the angles of the sepals, if some are deployed,
    we draw the organ.

    :param points:  points of the bud in the MTG object,
    :param turtle: the turtle to draw the bud in.
    """
    ## variables
    if lSepales is None:
        lSepales = []
    Heading = Vector3(0, 0, 1)
    height = 30
    Radius = Vector3(0, 1, 0)
    lSepalAngles = [80, 90]
    lSepalDims = [20, 30]
    lPetalAngles = [20, 30]
    lPetalDims = 20

    stade = None
    PcStade = 0

    (
        Heading,
        height,
        Radius,
        lSepalAngles,
        lSepalDims,
        lPetalAngles,
        lPetalDims,
        lNoSepals,
    ) = flowerParameters(points, stade, PcStade, lSepales, diameter)

    # All the angles are known, now we draw the thing.
    floralOrgan(
        Heading,
        height,
        Radius,
        lSepalAngles,
        lSepalDims,
        lPetalAngles,
        lPetalDims,
        turtle,
        lNoSepals,
    )


# end flower


class Flower(Node):
    def __init__(self):
        Node.__init__(self)
        self.add_output(name="compute_flower", interface=IFunction)

    def __call__(self, inputs):
        return flower


# end Flower     (flower wrapper)


###################################### Revolution Bud
def pointArray():
    """
    :returns: an array of points to feed a revolution object"""
    pts = [
        Vector2(0.10, 0.00),
        Vector2(0.50, 0.06),
        Vector2(0.40, 0.14),
        Vector2(0.60, 0.18),
        Vector2(1.00, 0.30),
        Vector2(0.90, 0.42),
        Vector2(0.50, 0.60),
        Vector2(0.30, 0.84),
        Vector2(1.00, 1.00),
    ]
    return pts


# end pointArray()


def budArray():
    """We define a list of points to feed a revolution object.
    The values are openalea.mtg.plantframe::Vector2 which contain :

    - ray
    - axial coordinate

    :return: the list  of points
    """
    pts = [
        Vector2(0.1, 0.00),
        Vector2(0.50, 0.06),
        Vector2(0.40, 0.14),
        Vector2(0.60, 0.18),
        Vector2(1.00, 0.30),
        Vector2(0.90, 0.42),
        Vector2(0.50, 0.60),
        Vector2(0.30, 0.84),
        Vector2(0.00, 1.00),
    ]
    return pts


# end budArray()


def fineBudArray():
    """We define an array of 17 points to feed a revolution object
    Values are pairs of (ray, axial position) coordinates in a cylindrical mark.

    :returns: this array
    """
    pts = [
        Vector2(0.10, 0.00),
        Vector2(0.40, 0.02),
        Vector2(0.50, 0.06),
        Vector2(0.50, 0.10),
        Vector2(0.40, 0.14),
        Vector2(0.40, 0.16),
        Vector2(
            0.60,
            0.18,
        ),
        Vector2(0.90, 0.24),
        Vector2(1.00, 0.30),
        Vector2(1.0, 0.34),
        Vector2(0.707, 0.42),
        Vector2(0.55, 0.48),
        Vector2(0.40, 0.60),
        Vector2(0.30, 0.72),
        Vector2(0.22, 0.84),
        Vector2(0.10, 0.96),
        Vector2(0.00, 1.00),
    ]
    return pts


# endef fineBudArray()


def revolution(points=None, stride=8):
    """
    We build here a revolution volume (openalea.mtg.plantframe::Revolution) from the input points stride

    :param points: a list of (ray, position). Must be of type openalea.mtg.plantframe::Vector2
    :param stride: the stride of the revolution figure (nr of interpolated points along a tour of rotation.
    :returns: the  revolution figure
    """
    # lStride = stride
    if stride < 5:
        stride = 5

    if points is None:
        points = budArray()
    pa = pgl.Point2Array(points)
    pl = pgl.Polyline2D(pa)
    rev = pgl.Revolution(pl, stride)
    return rev


# endef revolution(points=None, stride=8)


def revolutionBud(revVol=None):
    """We define a nested function (drawRevBud) that returns a function that draws a bud from a revolution volume

    :param revVol: a revolution volume that will be scaled and oriented
    :return: the drawRevBud function
    """
    lRevVol = revVol
    if lRevVol is None:
        lRevVol = revolution(budArray())

    def drawRevBud(points, turtle=None):
        """
        This function draws a revolution bud

        :param points: coordinates of the bud (bottom to top)
        :param turtle: openalea.plantgl.all::PglTurtle to draw the bud in
        """

        botPt = points[0][0]
        topPt = points[2][0]
        budAxis = Vector3(topPt - botPt)
        lengthVector = budAxis
        length = norm(lengthVector)
        budAxis.normalize()  # necessary ?

        # prolongation of ped
        # turtle.oLineTo(points[0])
        # turtle.push()
        turtle.oLineTo(points[0][0] + budAxis * 4)  # + 4 units (mm)
        turtle.push()  #
        turtle.setColor(4)  # apple green

        # we must orient the turtle before to draw
        faceTo(turtle, budAxis)

        revBud = pgl.Scaled(Vector3(length * 0.2, length * 0.2, length), lRevVol)
        # revBud=Oriented(upAxis, budAxis, revBud)
        # we are ready to draw the rev'bud
        turtle.customGeometry(revBud, 1)

        ## visual control test
        # turtle.move(topPt)
        # turtle.setColor(0)
        # turtle.customGeometry(Sphere(length/12.), 1)
        ## end test # SUCCESSFUL @ 20111019

        turtle.pop()

    return drawRevBud


# endef revolutionBud(revVol=None )


class PointArray(Node):
    def __init__(self):
        Node.__init__(self)
        self.add_output(name="pts_array", interface=ISequence)

    def __call__(self, inputs):
        return pointArray()


# end PointArray   (pointArray wrapper)


class BudArray(Node):
    def __init__(self):
        Node.__init__(self)
        self.add_output(name="bud_array", interface=ISequence)

    def __call__(self, inputs):
        return budArray()


# end BudArray     (budArray wrapper)


class FineBudArray(Node):
    def __init__(self):
        Node.__init__(self)
        self.add_output(name="bud_array", interface=ISequence)

    def __call__(self, inputs):
        return fineBudArray()


# end FineBudArray     (fineBudArray wrapper)


class RevolutionFig(Node):
    def __init__(self):
        Node.__init__(self)
        self.add_input(name="pointArray", interface=ISequence, value=None)
        self.add_input(name="stride", interface=IInt, value=8)
        self.add_output(name="rev_fig", interface=IData)

    def __call__(self, inputs):
        pointArray = self.get_input("pointArray")
        stride = self.get_input("stride")
        return revolution(pointArray, stride)


# end RevolutionFig    (revolution  wrapper)


class RevolutionBud(Node):
    def __init__(self):
        Node.__init__(self)
        self.add_input(name="revFig", interface=IData, value=None)
        self.add_output(name="rev_bud", interface=IFunction)

    def __call__(self, inputs):
        revFig = self.get_input("revFig")
        return revolutionBud(revFig)


# end RevolutionBud  (revolutionBud wrapper)


class drawBuds(Node):
    """:return: a list of drawing bud functions"""

    def __init__(self):
        Node.__init__(self)
        self.add_output(name="budsComputers", interface=ISequence)

    def __call__(self, inputs):
        return noThing, rawBud(), builtBud(), revolutionBud(), Flower()


# end drawBuds


################################################  K N O P
def computeKnop4pts():
    """
    We build a knop as a tetrahedron  where the outermost edge
    is joining the rachis and the internode ;
    The 1st triangle is facing the right and the second one is facing the left,
    The 3rd one lies against the stem and the last one goes against the rachis.
    The mtg file builder says :
      # face droite (vu depuis la tige) : (1, 0, 2)
      # face gauche (vu depuis la tige) : (0, 1, 3)
    """

    def tetraKnop(points, turtle=None):
        if len(points) < 4:
            return
        turtle.push()
        myColors.setTurtleAnthocyan(turtle)

        ## The 4 triangles
        # the right one (facing right of the axilla)
        turtle.move(points[2])
        turtle.startPolygon()
        turtle.lineTo(points[1])
        turtle.lineTo(points[0])
        turtle.lineTo(points[2])  # closing is really needed
        turtle.stopPolygon()
        # the left one (facing left of the axilla)
        turtle.move(points[3])
        turtle.startPolygon()
        turtle.lineTo(points[0])
        turtle.lineTo(points[1])
        turtle.lineTo(points[3])  # closing...
        turtle.stopPolygon()
        # the rear one (facing the stem)
        turtle.move(points[0])
        turtle.startPolygon()
        turtle.lineTo(points[3])
        turtle.lineTo(points[2])
        turtle.lineTo(points[0])  # closing
        turtle.stopPolygon()
        # the bottom one (facing the rachis)
        turtle.move(points[1])
        turtle.startPolygon()
        turtle.lineTo(points[2])
        turtle.lineTo(points[3])
        turtle.lineTo(points[1])  # closing
        turtle.stopPolygon()

        turtle.pop()

    # fin tetraKnop
    return tetraKnop


# fin computeKnop4pts()


class drawKnops(Node):
    """:return: a list of drawing bud functions"""

    def __init__(self):
        Node.__init__(self)
        self.add_output(name="knopComputers", interface=ISequence)

    def __call__(self, inputs):
        return noThing, computeKnop4pts()


# end drawKnops


################################################  S T I P U L E
def drawStipule3pts():
    """
    We build a stipule as a triangle the partially occultates the axil bud
    """

    # node code here.
    def triangleStipuLe(points, turtle=None):
        if len(points) < 3:
            return
        turtle.push()
        turtle.setColor(2)
        # myColors.setTurtleLightBlue(turtle) #  colour by default : the stem's

        ## The triangle
        # the right one (facing right of the axilla)
        turtle.move(points[0])
        turtle.startPolygon()
        turtle.lineTo(points[1])
        turtle.lineTo(points[2])
        turtle.lineTo(points[0])  # closing is really needed
        turtle.stopPolygon()

        turtle.pop()
        # fin triangleStipuLe

    return triangleStipuLe


# fin drawStipule3pts()


class drawStipule(Node):
    """:return: a list of drawing stipule functions"""

    def __init__(self):
        Node.__init__(self)
        self.add_output(name="stipuleComputer", interface=ISequence)

    def __call__(self, inputs):
        return noThing, drawStipule3pts()


# end drawStipule


################################################  L E A F L E T
def displayNormalVector(turtle, points, color):
    """displays a nail (or something sharp) to show up the normal direction of a surface

    :param turtle: the openalea.plantgl.all::PglTurtle object to draw onto
    :param points: set of points
    :param color: the index of the color to use for the nail
    """
    turtle.push()
    turtle.move(points[0] + (points[2] - points[0]) * 0.5)
    turtle.setColor(color)
    turtle.customGeometry(pgl.Cone(2, 13), 1)
    turtle.pop()


# endef  displayNormalVector(turtle,points,color)


# globale calculee dans meshedLeaflet
# anglOuverture=0.
def computeLeafletFrom4pts(xMesh=None, yMesh=None):  # was : [0.81, 0.92 , 0.94, 0]
    """We define here a nested function (meshedLeaflet) that computes a meshed leaflet geometry from 4 points.
    :param xMesh: the mesh coordinates along the axis of the leaf, as percent of the leaflet length.
    :param yMesh: the width of the leaf at the corresponding point, in percent of the leaf width.
    :return: the meshedLeaflet function
    :note: default values are to be set in __wralea__.py, not here !
    """
    if yMesh is None:
        yMesh = [0.92, 0.98, 0.666, 0.0]
    if xMesh is None:
        xMesh = [0.25, 0.5, 0.75, 1]

    # write the node code here.
    def meshedLeaflet(points, turtle=None):
        """compute leaflet geometry from 4 points"""

        # if the list of points is not a complete leaf
        # we have to return without pushing the turtle ;
        # We could display a red sphere to make the miss very visible, as well
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
        # the opening angle is computed from the arccos (lateral vectors of the leaflet)
        #
        Axis = points[2] - points[0]
        axisLength = norm(Axis)
        Axis.normalize()

        # leftmost leaflet
        # normal Axis
        side = points[3] - points[0]
        sideLength = norm(side)
        side.normalize()
        normAxis = computeUpAxis(Axis, side)
        if abs(norm(normAxis)) < 0.001:
            print("Z.bug= %s" % points[0][2])  # dbg

        # 2nd : compute the width of this half leaflet (sideLength * sin(angle))
        lateralG = Axis ^ side  # to detect closed leflets and display them differently
        halfWidth = sideLength * norm(lateralG)
        lateralG.normalize()

        # jessica's code for building the mesh
        ls_pts = [Vector3(0.0, 0.0, 0.0)]
        for i in range(len(xMesh)):
            ls_pts.append(Vector3(xMesh[i], 0, 0))
            ls_pts.append(Vector3(xMesh[i], yMesh[i], 0))
        # ls_pts.append(Vector3(1.,0.,0.))
        # we build triangles C O U N T E R Clockwise
        # jessica's code avec triangulation automatique
        ls_ind = []
        for i in range(2, len(ls_pts)):
            if i % 2:
                ls_ind.append(pgl.Index3(i - 2, i, i - 1))
            elif not i == 2:
                ls_ind.append(pgl.Index3(i - 1, i, i - 2))
            else:  # i==2
                ls_ind.append(pgl.Index3(i - 2, i - 1, i))
        # ls_ind=[pgl.Index3(0,2,1),pgl.Index3(1,2,3),pgl.Index3(2,4,3),pgl.Index3(3,4,5),pgl.Index3(4,6,5),pgl.Index3(5,6,7)]
        triangleSet = pgl.TriangleSet(pgl.Point3Array(ls_pts), pgl.Index3Array(ls_ind))

        geom = triangleSet
        geom = pgl.Scaled((axisLength, halfWidth, 1), geom)
        # setHead sets the turtle such as the xy plane is displayed by it side
        turtle.setHead(normAxis, Axis)

        # 4 testing : display normal vector for this half-leaflet
        # displayNormalVector(turtle,points,0)

        # Rightmost half-leaflet
        side = points[1] - points[0]
        sideLength = norm(side)
        side.normalize()
        normAxis = computeUpAxis(side, Axis)

        lateralD = Axis ^ side  # to detect closed leflets
        lateralD.normalize()

        # anglOuverture=np.arccos(dot(lateralG,lateralD))
        # seuil= deg2rad*90 # was 120 #
        # if anglOuverture < seuil :
        #    myColors.setTurtleAnthocyan(turtle)
        # we draw the half-leaflet now that we comuted it's color
        turtle.customGeometry(geom, 1)

        #  compute the width of the right half leaflet
        halfWidth = sideLength * norm(side ^ Axis)

        # we change the sign of the y coordinates of the mesh
        for meshPoint in ls_pts:
            meshPoint[1] *= -1.0
        # As the Y coordinate has changed its sign, we build
        # automatically the triangles C C W again.
        ls_ind = []
        for i in range(2, len(ls_pts)):
            if i % 2:
                ls_ind.append(pgl.Index3(i - 2, i - 1, i))
            elif not i == 2:
                ls_ind.append(pgl.Index3(i - 1, i - 2, i))
            else:  # i==2
                ls_ind.append(pgl.Index3(i - 2, i, i - 1))

        triangleSet = pgl.TriangleSet(pgl.Point3Array(ls_pts), pgl.Index3Array(ls_ind))
        geom = triangleSet
        geom = pgl.Scaled((axisLength, halfWidth, 1), geom)
        # setHead() see previously
        turtle.setHead(normAxis, Axis)
        turtle.customGeometry(geom, 1)

        # 4 testing : display normal vector for this half-leaflet
        # displayNormalVector(turtle,points,0)

        turtle.pop()  # against 1st push()

    # return outputs
    return meshedLeaflet


# endef computeLeafletFrom4pts(xMesh=..., yMesh=...)


class ComputeLeafletFrom4pts(Node):
    def __init__(self):
        Node.__init__(self)
        self.add_input(name="xMesh", interface=ISequence)
        self.add_input(name="yMesh", interface=ISequence)
        self.add_output(name="compute_leaf", interface=IFunction)

    def __call__(self, inputs):
        xMesh = self.get_input("xMesh")
        yMesh = self.get_input("yMesh")
        return computeLeafletFrom4pts(xMesh, yMesh)


# end ComputeLeafletFrom4pts   (computeLeafletFrom4pts  wrapper)


#########################################
def rawLeaflet(points, turtle=None):
    """computes a leaflet geometry from 4 points

    :param points: a set of coordinates of 4 points that are supposed to be the edge of the leaflet, turning anticlockwise.
    :param turtle: an openalea.plantgl.all::PglTurtle object to draw objects onto
    """
    turtle.push()
    turtle.startPolygon()
    for pt in points[1:]:
        turtle.lineTo(pt)
    turtle.lineTo(points[0])
    turtle.stopPolygon()
    turtle.pop()


# endef rawleaflet


########################################
def polygonLeaflet():
    """
    default function to draw up a leaflet

    :return: a function that draws a raw leaflet.
    """
    # compute_leaf = None ;
    return rawLeaflet


# end polygonLeaflet


class PolygonLeaflet(Node):
    def __init__(self):
        Node.__init__(self)
        self.add_output(name="compute_leaf", interface=IFunction)

    def __call__(self, inputs):
        return polygonLeaflet()


# endpolygonLeaflet


class drawLeaves(Node):
    """:return: a list of the leaves drawing functions"""

    def __init__(self):
        Node.__init__(self)
        self.add_output(name="leavesComputers", interface=ISequence)

    def __call__(self, inputs):
        return noThing, rawLeaflet, computeLeafletFrom4pts()


# end drawLeaves


######################################## FLOWER
def bezierPatchFlower(controlpointmatrix=None, ustride=5, vstride=5, colorFunc=None):
    """
    This is a function that returns a bpFlower function  with in its closure :

    - the control points matrix, as a list of lists, which defines a mesh (it can be seen as a 2D set with an altitude for each point) :

        - every inner list contains a set of control points that defines a bezier curve in a direction of the mesh
        - all the N-th points of the inner lists defines the N-th bezier curve in the other direction of the mesh

    - the u and v strides
    - the coloring function

    :param controlpointmatrix: a list of lists of points of type openalea.mtg.plantframe::Vector4
    :param ustride: the number of points to us to discretize the surface along the 1st direction
    :param vstride: the number of points to us to discretize the surface along the 2nd direction
    :param colorFunc: a function that sets the color of the turtle
    """
    # write the node code here.
    lControlpointmatrix = controlpointmatrix

    if controlpointmatrix is None:
        # the return value of ctrlpointMatrix() yields an error. Why ?
        # lControlpointmatrix = ctrlpointMatrix()
        lControlpointmatrix = [
            [Vector4(0, -0.2, 0, 1), Vector4(0, 0.2, 0, 1)],
            [Vector4(0.28, -0.38, 0.13, 1), Vector4(0.28, 0.38, 0.13, 1)],
            [Vector4(0.56, -0.56, 0.17, 1), Vector4(0.56, 0.56, 0.17, 1)],
            [Vector4(0.86, -0.7, 0.21, 1), Vector4(0.86, 0.7, 0.5, 1)],
            [Vector4(1, -0.25, 1, 1), Vector4(1, 0.25, 1, 1)],
        ]
    myColorFunc = colorFunc
    if colorFunc is None:
        myColorFunc = myColors.setTurtlePink  # custom

    def bpFlower(pointsnDiameters, turtle=None, dummy0=None, dummy1=None):
        """computes a flower from two points and the diameters associated to
        the flower.
        @param points : list of pairs[Vector3, scalar] resp. (position;diameter)
        """
        luStride = ustride
        lvStride = vstride
        if luStride < 5:
            luStride = 5
        if lvStride < 5:
            lvStride = 5
        # ustride=5
        # vstride=5
        # pointsNdiamters is : [[base_pos, base_diam], [None,None], [top_pos, top_diam], [...]]
        basePos = pointsnDiameters[0][
            0
        ]  # TypeError: '_ProxyNode' object does not support indexing
        topPos = pointsnDiameters[2][0]
        # pedDiam=pointsnDiameters[0][1]
        flowerRay = (
            pointsnDiameters[2][1] if pointsnDiameters[2][1] else pointsnDiameters[0][1]
        )
        flowerRay *= 0.5
        flowerHeight = norm(topPos - basePos)
        baseRay = max(flowerRay * 0.2, flowerHeight * 0.2)  # arbitrarily
        deltaRay = flowerRay - baseRay
        petalLength = np.sqrt(flowerHeight * flowerHeight + deltaRay * deltaRay)

        # we build the generic patch
        petalMesh = pgl.BezierPatch(lControlpointmatrix, luStride, lvStride)
        # patch is scaled according to the global flower dimensions
        petalMesh = pgl.Scaled(
            Vector3(petalLength, max(baseRay, flowerRay) * 1.1, baseRay), petalMesh
        )
        #
        rad5eTour = np.pi / 2.5  # a fifth of a tour

        # compute the pitch angle (flower opening)
        if deltaRay > 0:  # opened flower
            openingAngle = np.arctan(flowerHeight / (deltaRay))
        elif deltaRay < 0:  # flower not opened yet
            openingAngle = np.pi * 0.5 + np.arctan((-deltaRay) / flowerHeight)
        else:  # say half opened
            openingAngle = np.pi * 0.5

        ovary = pgl.Sphere(baseRay, luStride)

        turtle.push()  # we draw now

        #  orient the turtle
        flowerAxis = topPos - basePos
        faceTo(turtle, flowerAxis)
        # turtle.setColor(4) # kind of yellow-green
        turtle.customGeometry(ovary, 1)  #

        myColorFunc(turtle)

        for iIndex in range(0, 5):
            # closing the flower :
            petal = pgl.AxisRotated((0, 1, 0), -openingAngle, petalMesh)
            # twisting a bit to limit collisions [Todo in the patch]
            # NOTWIST 4 test petal=AxisRotated((1,0,0),openingAngle*0.05,petal)
            petal = pgl.AxisRotated(
                (1, 0, 0), openingAngle * 0.055, petal
            )  # HALFTWIST 4 test
            angle = iIndex * rad5eTour
            petal = pgl.AxisRotated((0, 0, 1), angle, petal)
            petal = pgl.Translated(
                Vector3(
                    baseRay * np.cos(angle) * 0.8, baseRay * np.sin(angle) * 0.8, 0
                ),
                petal,
            )
            turtle.customGeometry(petal, 1)  # flowerHeight) #

        turtle.pop()

    return bpFlower


# endef bezierPatchFlower(controlpointmatrix=None,ustride=5,vstride=5,colorFunc=None)


class BezierPatchFlower(Node):
    ## This function sets up the BezierPatchFlower node within OpenAlea
    def __init__(self):
        Node.__init__(self)
        self.add_input(name="controlpointmatrix", interface=ISequence, value=None)
        self.add_input(name="ustride", interface=IInt)
        self.add_input(name="vstride", interface=IInt)
        self.add_input(name="colorFunc", interface=IFunction, value=None)
        self.add_output(name="compute_flower", interface=IFunction)

    def __call__(self, inputs):
        controlpointmatrix = self.get_input("controlpointmatrix")
        ustride = self.get_input("ustride")
        vstride = self.get_input("vstride")
        colorFunc = self.get_input("colorFunc")

        return bezierPatchFlower(controlpointmatrix, ustride, vstride, colorFunc)


# end BezierPatchFlower   (bezierPatchFlower wrapper)

################################## GENERIC _FLOWER_


def getValuesFromSepals(lSepales, mainAxis):
    """
    We compute the angles between the sepals and the axis of the organ, and the length of the sepals.

      - a list containing the angle of the most opened sepal and the less opened sepal
      - a list containing respectively the length of the sepals
      - the front direction to orient the turtle's mark

    :param lSepales: a list of 3D points representing a sepal
    :param mainAxis: a Vector3 that contains the main direction of the organ
    :return: the lists of : (directions, dimensions) of sepals and the Front direction
    """
    angles = []
    lengthes = []
    if lSepales:
        # testSepales=[]
        # avant-der (pointe) - premier (insertion rachis)
        vein = lSepales[0][-2] - lSepales[0][0]
        side = cross(mainAxis, vein)
        side.normalize()
        Front = cross(side, mainAxis)
        Front.normalize()

        for sepale in lSepales:
            vein = sepale[-2] - sepale[0]
            veinlength = norm(vein)
            vein.normalize()

            # one of both (debug)
            sine = norm(cross(mainAxis, vein))
            cosine = dot(mainAxis, vein)

            angle = np.arctan2(sine, cosine)
            angles.append(angle / deg2rad)
            lengthes.append(veinlength)

        return angles, lengthes, Front
    else:
        return [0], [30]


# end getValuesFromSepals


def notation2flowerAngles(stade, PcStade):
    """
    Computes flower angles (**in degrees**) from stage notations, i.e :
      - the sepal angles list:
          - the most opend sepal
          - the less opened sepal
      - the petal angles list:
          - the most opend petal
          - the less opened petal

    :param stade: a stage of flowering in "BFV ... FF"
    :param PcStade: the percent of evolution within the stage "stade"
    :return: a list of two lists containing the angles described above
    :bugs: the fruits are not at their right place.
    TODO : read from a .json dict a relationship established
    from the notations at the manip date
    (~/modeleChambre/documentation/PlantesDigit_Stades.xlsx)
    """
    return [0, 0], [0, 0]


# end notation2flowerAngles


def flowerParameters(points, stade=None, PcStade=0, lSepales=None, flowerDiameter=None):
    """Computes a set of parameters to draw flowerbuds, that is:

      - the head direction of the flower (the local vertical in some sort)
      - the height of this organ
      - Radius : the direction that the bud would be looking to if it was an elf (a local x vector)
      - lSepalAngles : the opening angles of the sepals if any
      - lSepalDims : the length of the sepals  if any
      - lPetalAngles : the opening angles of petals (if any)
      - lPetalDims : the dimension of petals (if any)

    :param points: a list of MTG nodes we get information from
    :param stade: todo : extract directly from points
    :param PcStade: todo : extract directly from points
    :param lSepales: list of 4 Vector3 points representing 0, 1 or 2 sepals
    :return: (Heading, height, Radius, lSepalAngles, lSepalDims, lPetalAngles, lPetalDims)

    """

    if lSepales is None:
        lSepales = []
    Heading = Vector4(0, 0, 1, 1)
    height = 0
    Radius = Vector4(0, 1, 0, 1)
    lSepalAngles = []
    lSepalDims = []
    lRealSepalsAzimuts = []  # digitized sepals angles
    lPetalAngles = []
    lPetalDims = []

    # we extract the positions of distant points
    ped = position(points[0])
    top = position(points[-1])  # Vu haut1 avec Sabine, en fait haut2

    # we compute the heading and size of the bud
    (Heading, height) = computeHeading([ped, top])

    # we check for sepals and compute their angles if any,
    if lSepales:
        (lSepalAngles, lSepalDims, Radius) = getValuesFromSepals(lSepales, Heading)
        lRealSepalsAzimuts = getSepalsAzimuts(lSepales, Heading, Radius)
    else:
        # if no sepals, we guess the radius
        Radius = computeFacingFromUp(Heading)

    # mimick an opening bud if only one sepal is opened :
    if len(lSepalAngles) == 1:
        if flowerDiameter:
            lSepalAngles.append(lSepalAngles[0])
        else:
            lSepalAngles.append(0)
        lSepalDims.append(lSepalDims[0])  # so that the length is the same for all

    if flowerDiameter:
        if flowerDiameter > 0:  # real flower
            flowerRay = flowerDiameter * 0.5

            # we compute the angle(s)
            lPetalAngles.append(np.arctan2(flowerRay, height))
            # lPetalDims.append(height / np.cos(lPetalAngles[0]))
            lPetalDims.append(np.sqrt(height * height + flowerRay * flowerRay))

            lPetalAngles[0] /= deg2rad
            lPetalAngles.append(lPetalAngles[0] * 0.8)
            lPetalDims.append(lPetalDims[0])

        else:  # faded flower
            lPetalAngles[:] = []
            lPetalAngles.append(180)
            lPetalAngles.append(180)

    elif lSepalAngles:
        budTime = rose_time.invertInnerSepalAngle(min([i for i in lSepalAngles]))
        lPetalAngles.append(rose_time.outerPetalAngle(budTime))
        lPetalAngles.append(rose_time.innerPetalAngle(budTime))
        lPetalDims.append(height)
        lPetalDims.append(height)
    elif stade:  # may check for only BVF and CPV here (SR ?)
        lSepalAngles, lDummyDims = notation2flowerAngles(stade, PcStade)

    # check petal angles from sepal ones

    return (
        Heading,
        height,
        Radius,
        lSepalAngles,
        lSepalDims,
        lPetalAngles,
        lPetalDims,
        lRealSepalsAzimuts,
    )


# end flowerParameters


# def fruitParameters(points, stade=None, PcStade=0, lSepales=[]):
#    """ returns a serie of parameters to draw fruits
#        Obsolete ; use flowerParameters instead
#    """
#    Heading = Vector4(0,0,1,1)
#    height=0
#    Radius = Vector4(0,1,0,1)
#    lSepalAngles= []
#    lSepalDims = []
#    lPetalAngles = []
#    lPetalDims = []
#
#    # we extract the positions of distant points
#    ped=position(points[0])
#    top=position(points[-1])
#
#    # we compute the heading and size of the bud
#    (Heading,height) = computeHeading([ped, top])
#
#    # we check for sepals and compute their angles if any,
#    if lSepales :
#        (lSepalAngles,lSepalDims,Radius) = getValuesFromSepals(lSepales, Heading)
#    else :
#        Radius=computeFacingFromUp(Heading)
#        # if no sepals, we check for "stade" notations
#
#        if stade: # may check for only SR, FO and FF here
#            lSepalAngles,lDummyDims = notation2flowerAngles(stade, PcStade)
#
#    # we get the diameter
#    flowerRay=  mtg.property('Diameter')[top]*0.5 # spyder doesn't know about mtg
#    # we compute the angle(s)
#    lPetalAngles[0]= np.arctan2(height,flowerRay)
#    lPetalDims[0]=height / np.cos(lPetalAngles[0])
#
#    lPetalAngles[0] /= deg2rad
#    lPetalAngles.apend(lPetalAngles[0]*0.8)
#    lPetalDims.append(lPetalDims[0])
#
#    return(Heading, height, Radius, lSepalAngles, lSepalDims,
#     lPetalAngles, lPetalDims)
## end fruitParameters


def floralOrgan(
    Heading,
    height,
    Radius,
    lSepalAngles=None,
    lSepalDims=None,
    lPetalAngles=None,
    lPetalDims=None,
    turtle=None,
    lNoSepals=None,
):
    """
    A function to draw floral organs with observed angles or observed stages of evolution in [BFV, CPV, SR, FO, FF], i.e :

    - Visible Flower Bud
    - Visible Petal's Color
    - Refecting Sepals
    - Opened Flower
    - Faded Flower

    :param Heading: a list of 3 Vector3
    :param height: the height of the organ
    :param Radius: the  radius  of the organ
    :param lSepalAngles: the angles of the most and the less opened sepal, taken between the Heading direction and the axle of the sepal
    :param lSepalDims: the dimensions of opened sepals
    :param lPetalAngles: the angles of the most and the less opened petal, taken between the Heading direction and the axle of the petal
    :param lpetalDims: the dimensions of opened petals
    :param turtle: the turtle to draw onto.
    :param lNoSepals: azimuths of real sepals (already drawn, so not to be created)
    :todo: add a param with the direction of existing sepals in the local mark, if any
    """

    # from openalea.mtg.plantframe import Vector4 as V4
    if lNoSepals is None:
        lNoSepals = []
    if lPetalDims is None:
        lPetalDims = []
    if lPetalAngles is None:
        lPetalAngles = []
    if lSepalDims is None:
        lSepalDims = []
    if lSepalAngles is None:
        lSepalAngles = []
    from openalea.plantgl.math import Vector4 as V4

    numSepals = 5.0  # number of sepals
    numPetals = 10.0  # number of petals

    sepalmatrix2 = [
        [V4(0, -0.0, 0.0, 1), V4(0, 0, -0, 1), V4(0, 0.0, 0.0, 1)],
        [V4(-0.2, -0.16, 0.0, 1), V4(-0.25, 0, 0.0, 1), V4(-0.2, 0.16, 0.0, 1)],
        [V4(-0.2, -0.12, 0.2, 1), V4(-0.25, 0, 0.2, 1), V4(-0.2, 0.12, 0.2, 1)],
        [V4(0.0, -0.05, 0.4, 1), V4(-0.1, 0, 0.4, 1), V4(0.0, 0.05, 0.4, 1)],
        [V4(0.0, -0.0, 1.0, 1), V4(0.0, 0, 1.0, 1), V4(0.0, 0.0, 1.0, 1)],
    ]

    petalmatrix2 = [
        [
            V4(0.0, 0.0, 0.0, 1),
            V4(-0.0, 0.0, 0.0, 1),
            V4(-0.0, 0, 0.0, 1),
            V4(-0.0, -0.0, 0.0, 1),
            V4(0.0, -0.0, 0.0, 1),
        ],
        [
            V4(0.0, 0.12, 0.1, 1),
            V4(-0.15, 0.1, 0.1, 1),
            V4(-0.25, 0, 0.1, 1),
            V4(-0.15, -0.1, 0.1, 1),
            V4(0.0, -0.12, 0.1, 1),
        ],
        [
            V4(0.0, 0.25, 0.2, 1),
            V4(-0.0, 0.17, 0.2, 1),
            V4(-0.2, 0, 0.2, 1),
            V4(-0.1, -0.17, 0.2, 1),
            V4(0.0, -0.25, 0.1, 1),
        ],
        [
            V4(0.06, 0.4, 0.6, 1),
            V4(0.05, 0.27, 0.6, 1),
            V4(0.05, 0, 0.6, 1),
            V4(0.05, -0.27, 0.6, 1),
            V4(0.045, -0.4, 0.6, 1),
        ],
        [
            V4(0.04, 0.35, 0.75, 1),
            V4(0.05, 0.25, 1.0, 1),
            V4(0.04, 0, 0.95, 1),
            V4(0.04, -0.25, 1.0, 1),
            V4(0.03, -0.35, 0.75, 1),
        ],
    ]

    def TransformSepal(sepalMatrix, angleExt, angleInt, numero=0):
        """this procedure will curve the sepal according to the stage"""
        """ We assume that sepalMatrix contains a vertical "impulse" profile 
        i.e the  z draw a _||_
        we rotate the 3rd point and followings around the origin and the y axis, 
        by a value of 2pi/3 * stage 
        :param sepalMatrix: a matrix of Vector4 points
        :param angleExt: the angle of the outer sepal
        :param angleInt: the angle of the inner sepal
        :param numero: the number of the sepal, that defines their position around the main axis
        :warning: the 1st point is supposed to be at [0,0,0] 
        """

        newSepalMatrix = [[]]
        # the opening angle of each sepal is computed accordingly to
        # the observations on a rose bud.
        # see fitting curves in ~/manips/rose/boutons/chronogramme.ods
        # convert degrees to radians
        firstSepalAngle = angleExt * deg2rad
        lastSepalAngle = angleInt * deg2rad

        # rotate around the main axis proportionally to the sepal number :
        angle = (
            firstSepalAngle + (lastSepalAngle - firstSepalAngle) * numero / numSepals
        )
        (sina, cosa) = getSiCo(angle)

        # we copy sepalMatrix
        for coords in sepalMatrix:
            newCoord = []
            for point in coords:
                newCoord.append(point)
            newSepalMatrix.append(newCoord)

        ################ we rotate the last groups of points
        # by unstacking and restacking the matrix
        # we get the points of sepalMatrix
        # from the forelast line (what did I mean ?)
        lignes = [newSepalMatrix.pop(), newSepalMatrix.pop()]
        lignes.reverse()
        # we rotate these points
        for points in lignes:
            newPoints = []
            for point in points:
                newx = point[0] * cosa - point[2] * sina
                newz = point[0] * sina + point[2] * cosa
                newPoint = V4(newx, point[1], newz, point[3])
                newPoints.append(newPoint)
            newSepalMatrix.append(newPoints)

        newSepalMatrix.remove([])
        return newSepalMatrix

    # end TransformSepal

    def TransformPetal(petalMatrix, angleExt, angleInt, numero=0):
        """this procedure will curve the sepal according to the stage
         We suppose that sepalMatrix contains a vertical crenel-like profile of a sepal  :
        i.e. the  z form a _||_
        we rotate the 3rd point and followings around the origin and the y-axis,
        by a value of 2pi/3 * stage
        :param sepalMatrix: a matrix of Vector4 points
        :param angleExt: the angle of the outer sepal
        :param angleInt: the angle of the inner sepal
        :param numero: the number of the sepal, that defines their position around the main axis
        :warning: the 1st point is supposed to be at [0,0,0]
        :return: a new petal matrix
        """

        newPetalMatrix = [[]]

        # the opening angle of each crown of petals is computed accordingly to
        # the observations on a rose bud.
        # see fitting curves in $ROSEDIR/doc/user/chronogramme.ods

        # fit by estimated MEAN values
        angle = angleInt
        if index / int(numSepals) < 1:
            angle = angleExt
        petalFactor = angle / 90.0
        angle *= deg2rad

        # angle according to the number of the petal "crown" :
        facteur = petalFactor
        (sina, cosa) = getSiCo(angle)
        anglePlus = angle * 1.2
        (sinPlus, cosPlus) = getSiCo(anglePlus)  # to wave the petal

        # facteur = min(max(angle/0.2, 0.2),1)
        facteur = np.sqrt(facteur)

        for line in petalMatrix:
            newLine = []
            for point in line:
                newLine.append(point)
            newPetalMatrix.append(newLine)
        newPetalMatrix.remove([])  # python
        ################
        # we rotate the last groups of points in order to open the flower
        # N O T E Visually, petals bend more than sepal for large angles,
        # so we must limit the angle below 90°.
        lignes = []
        for numRang in range(2):
            ligne = newPetalMatrix.pop()
            if numRang % 2:
                (sinus, cosinus) = (sinPlus, cosPlus)
            else:
                (sinus, cosinus) = (sina, cosa)
            newPoints = []
            for point in ligne:
                newx = point[0] * cosinus - point[2] * sinus
                newz = point[0] * sinus + point[2] * cosinus
                newPoint = V4(newx, point[1] * facteur, newz, point[3])
                newPoints.append(newPoint)
            lignes.append(newPoints)

        lignes.reverse()
        for points in lignes:
            newPetalMatrix.append(points)

        return newPetalMatrix

    # end TransformPetal

    # P R O C E S S I N G
    turtle.push()
    turtle.setHead(Heading, Radius)
    # this is empirical. It tends to make too small ovaries for wide opened flowers
    taille = height / 10.0
    # The longer the petals, the bigger the ovary
    if lPetalDims:
        taille = max(height, lPetalDims[0]) / 10.0
    taille_fruit = taille * 2.0  # was 2.5

    # ready to draw
    # we prolongate the ped along the heading direction :
    turtle.push()
    myColors.setTurtlePed(turtle)
    turtle.oLineRel(Heading * taille_fruit)
    # myColors.setTurtleOrange(turtle)
    # turtle.setColor(4)

    ############################ O V A R Y   |   F R U I T
    anglePetExt = anglePetInt = 0
    if lPetalAngles:
        anglePetExt = lPetalAngles[0]
        anglePetInt = lPetalAngles[-1]
    receptacle = pgl.Sphere(1.0)
    if anglePetExt > 90.0 and anglePetExt == anglePetInt:  # Faded flower
        myColors.setTurtleFruit(turtle)
        receptacle = pgl.Scaled(
            Vector3(taille_fruit * 1.333, taille_fruit * 1.333, taille_fruit),
            receptacle,
        )
        # receptacle= pgl.Translated(0, 0, -taille*0.5, receptacle)

    else:
        myColors.setTurtleReceptacle(turtle)
        receptacle = pgl.Scaled(Vector3(taille, taille, taille), receptacle)
        receptacle = pgl.Translated(0, 0, -taille * 0.5, receptacle)

    turtle.customGeometry(receptacle, 1)

    turtle.pop()

    ############################ S E P A L S
    ustride = 10  # the U resolution of the patch (along z)
    vstride = 8  # the V resolution of the patch (around the axle)
    angle72 = np.pi / 2.5  # the 1/5th of a tour

    myColors.setTurtleSepal(turtle)
    angleSepInt = angleSepExt = 0  # the outer /inner sepal angles
    if lSepalAngles:
        angleSepExt = lSepalAngles[0]
        angleSepInt = lSepalAngles[-1]

    groupe = pgl.Group([])
    thisHeight = height
    heightInc = 0
    if lSepalDims:
        thisHeight = lSepalDims[0]
        heightInc = (lSepalDims[0] - lSepalDims[-1]) / (numSepals - 1)
    for index in range(0, int(numSepals)):
        rotationAngle = angle72 * index * 2  #
        # turtle.setColor(index)
        # has this sepal been digitized ?
        Go = True
        # if lNoSepals:
        #    for az in lNoSepals:
        #        if inSector(rotationAngle,az, angle72*.5) :
        #            Go = False
        #            lNoSepals.remove(az)

        # Digitized sepals will not be drawn ; instead we draw the created ones
        # as they fit better with the created sepals
        if Go:  # we draw "replacement" sepal
            sepalMatrix = TransformSepal(sepalmatrix2, angleSepExt, angleSepInt, index)
            thisSepal = pgl.BezierPatch(sepalMatrix, ustride, vstride)
            thisSepal = pgl.Scaled(
                Vector3(thisHeight, thisHeight, thisHeight), thisSepal
            )
            newSepal = pgl.AxisRotated((0, 0, 1), rotationAngle + np.pi, thisSepal)  #
            groupe.geometryList.append(newSepal)

        thisHeight -= heightInc

    # DBG
    if groupe.geometryList:
        groupe = pgl.Translated(Vector3(0, 0, taille * 1.86), groupe)
        turtle.customGeometry(groupe, 1)

    # stage zero : No petal to build (invisible...)
    if angleSepExt <= 0.001:
        turtle.pop()
        return

    # check for FF stage
    # WARNING : digitization errors may lead to this case
    if anglePetExt == anglePetInt and anglePetExt > 80.0:
        turtle.pop()
        return

    ############################ P E T A L S
    angleRepartition = angle72 * 2.1
    myColors.setTurtlePetal(turtle)

    thisLength = lPetalDims[0]
    thisInc = (lPetalDims[0] - lPetalDims[-1]) / (numPetals - 1)
    for index in range(int(numPetals)):
        petalMatrix = TransformPetal(petalmatrix2, anglePetExt, anglePetInt, index)
        petal = pgl.BezierPatch(petalMatrix, ustride, vstride)
        petal = pgl.Scaled(Vector3(thisLength, thisLength, thisLength), petal)
        thisLength -= thisInc
        thisAngle = angleRepartition * index
        (thisSin, thisCos) = getSiCo(thisAngle)
        thisPetal = pgl.AxisRotated((0, 0, 1), thisAngle, petal)  # orientation
        thisPetal = pgl.Translated(
            -0.33 * taille * thisCos, -0.33 * taille * thisSin, taille * 2, thisPetal
        )  # placement # was : taille*2.
        turtle.customGeometry(thisPetal, 1)

    turtle.pop()


# endef floralOrgan(Heading, height, Radius, lSepalAngles=[],...)


def getSepalsAzimuts(lSepales, Heading, Radius):
    """We compute the azimuth in the local coordinate system of the sepals that has been digitized.

    The sepal axles coordinates are projected on the local "horizontal" plane, then
    we compute the angle they do with the local x-axis.
    To compute the projection V' of a vector V on the local horizontal plane,
    we compute its projection H' it onto the vertical axis H,  then we substract H' from V


    :param lSepales: the list of sepals described by 4 points
    :param Heading: the Up (or local z) direction of the floral organ.
    :param Radius: the Front (or local x) direction of the floral organ.
    :return: the list of angles.
    """
    angles = [0]  # 1st angle is null by construction (checked)

    # if there are 5 digitized sepals, we assume that they are correct
    if len(lSepales) == 5:
        for a in range(73, 360, 72):
            angles.append(a * np.pi / 180.0)
    else:
        for sepale in lSepales[1:]:
            sepalAxle = sepale[-2] - sepale[0]
            sepalAxle.normalize()

            hPrime = Heading * dot(sepalAxle, Heading)
            sepalAxle = sepalAxle - hPrime
            sepalAxle.normalize()

            sinAngle = norm(cross(Radius, sepalAxle))
            cosAngle = dot(Radius, sepalAxle)
            angle = np.arctan2(sinAngle, cosAngle)
            # put it all in the same tour
            if angle < 0:
                angle += 2 * np.pi
            angles.append(angle)
    return angles


# end getSepalsAzimuts


def drawFloralOrgan(colorFunc=None):
    """A function to return the function that draws floral organs

    :param colorFunc: the index of the color to use for the flower
    """
    myColorFunc = colorFunc
    if myColorFunc is None:
        myColorFunc = myColors.setTurtlePink  # custom
    return floralOrgan


# endef drawFloralOrgan(colorFunc=None)


class FloralOrgan(Node):
    """FIXME : inside implementation not to be shown"""

    def __init__(self):
        Node.__init__(self)
        self.add_input(name="colorFunc", interface=IFunction, value=None)
        self.add_output(name="compute_floralOrgan", interface=IFunction)

    def __call__(self, inputs):
        colorFunc = self.get_input("colorFunc")
        return drawFloralOrgan(colorFunc)


# end FloralOrgan (drawFloralOrgan  wrapper)


######################################## CONE FLOWER
def coneFlower(colorFunc=None):
    """We define here a function (rawFlower) that draws up a raw flower.

    :return: the function rawFlower
    """
    # write the node code here.
    myColorFunc = colorFunc
    if colorFunc is None:
        myColorFunc = myColors.setTurtlePink  # custom

    def rawFlower(pointsnDiameters, turtle=None, oneMore="yes", noWay="really"):
        """computes a flower from 2 pairs [position, diameter]"""
        #
        turtle.push()
        #
        myColorFunc(turtle)

        newProp = pointsnDiameters[0].properties()
        newCoord = [newProp["XX"], newProp["YY"], newProp["ZZ"]]
        turtle.oLineTo(newCoord)
        Diameter = pointsnDiameters[0].properties()["Diameter"] * 10
        newProp = pointsnDiameters[-1].properties()
        newCoord = [newProp["XX"], newProp["YY"], newProp["ZZ"]]
        turtle.oLineTo(newCoord)

        turtle.setWidth(Diameter * 0.5)
        turtle.pop()
        # end rawFlower

    # return outputs
    return rawFlower


# end coneFlower


class RawFlower(Node):
    def __init__(self):
        Node.__init__(self)
        self.add_input(name="colorFunc", interface=IFunction, value=None)
        self.add_output(name="compute_flower", interface=IFunction)

    def __call__(self, inputs):
        colorFunc = self.get_input("colorFunc")
        return coneFlower(colorFunc)


# end RawFlower   (coneFlower wrapper)


######################################## Fruit


def simpleFruit(colorFunc=None):
    """We define here a function "rawFruit" to draw up a raw fruit

    :param colorFunc: a function that sets the color of the turtle
    :return: the rawFruit function
    """
    # write the node code here.
    myColorFunc = colorFunc
    if colorFunc is None:
        myColorFunc = myColors.setTurtleFruit  # custom

    def rawFruit(points, turtle=None):  # arity is 4
        """
        Computes a fruit from a pair or positions
        This is experimental code for debugging
        """
        turtle.push()
        #  Looks like points are (end, begining...)
        point = points[1]
        # turtle.oLineTo(points[0]) #[0]) F A I L S because points[0] is a "ProxyNode"

        point0 = Vector3(
            [
                point.properties()["XX"],
                point.properties()["YY"],
                point.properties()["ZZ"],
            ]
        )
        point = points[0]
        point1 = Vector3(
            [
                point.properties()["XX"],
                point.properties()["YY"],
                point.properties()["ZZ"],
            ]
        )

        botPt = point0
        topPt = point1
        fruit_center = topPt * 0.4 + botPt * 0.6
        turtle.oLineTo(fruit_center)

        myColorFunc(turtle)

        fruitAxis = Vector3(topPt - botPt)  # should be typed such, anyway
        # digit point is on top of etamins
        # etamins are not represented
        fruitSize = norm(fruitAxis)  #
        ## we must orient the turtle before to draw
        ## this makes better fitting of the sphere and the paraboloid
        faceTo(turtle, fruitAxis)
        fruit = pgl.Scaled(
            Vector3(fruitSize * 0.6, fruitSize * 0.6, fruitSize * 0.4), pgl.Sphere()
        )
        turtle.customGeometry(fruit, 1)

        turtle.pop()
        # end rawFruit

    # return outputs
    return rawFruit


# end simpleFruit


class RawFruit(Node):
    def __init__(self):
        Node.__init__(self)
        self.add_input(name="colorFunc", interface=IFunction, value=None)
        self.add_output(name="compute_flower", interface=IFunction)

    def __call__(self, inputs):
        colorFunc = self.get_input("colorFunc")
        return simpleFruit(colorFunc)


# end RawFruit  (simpleFruit  wrapper)


########################################


def noThing(points, turtle=None, dummy=None, noWay="really"):
    """A function that makes nothing

    :param points: unused
    :param turtle: unused
    """
    pass


# endef noThing(points, turtle=None, dummy=None)


def makeNoOrgan():
    """
    makes nothing, so we can see details that are hidden otherwise.

    :returns: the function noThing that makes no change to the turtle.
    """
    # write the node code here.
    # return outputs
    return noThing


# end makeNoOrgan()


class NoOrgan(Node):
    def __init__(self):
        Node.__init__(self)
        self.add_output(name="compute_nothing", interface=IFunction)

    def __call__(self, inputs):
        return makeNoOrgan()


# end NoOrgan  (makeNoOrgan   wrapper)

########################################

## a raw control point matrix for testing bezier patches
ctpm = [
    [Vector4(0, -0.2, 0, 1), Vector4(0, 0.2, 0, 1)],
    [Vector4(0.28, -0.38, 0.13, 1), Vector4(0.28, 0.38, 0.13, 1)],
    [Vector4(0.56, -0.56, 0.17, 1), Vector4(0.56, 0.56, 0.17, 1)],
    [Vector4(0.86, -0.7, 0.21, 1), Vector4(0.86, 0.7, 0.5, 1)],
    [Vector4(1, -0.25, 1, 1), Vector4(1, 0.25, 1, 1)],
]


def ctrlpointMatrix():
    """We define here a control point matrix for a bezier
    patch with 2 columns and 7 rows that draws a raw petal.

    :returns: the control point matrix
    """
    # ctpm = None;
    # write the node code here.
    # did I mean "global" ?
    ctpm = [
        [Vector4(0, -0.40, 0, 1), Vector4(0, 0.4, 0, 1)],
        [Vector4(0.28, -0.45, 0.08, 1), Vector4(0.28, 0.45, 0.08, 1)],
        [Vector4(0.56, -0.45, 0.31, 1), Vector4(0.56, 0.45, 0.31, 1)],
        [Vector4(0.86, -0.45, 0.73, 1), Vector4(0.86, 0.45, 0.75, 1)],
        [Vector4(0.95, -0.5, 0.9, 1), Vector4(0.96, 0.5, 0.9, 1)],
        [Vector4(0.98, -0.45, 0.96, 1), Vector4(0.98, 0.45, 0.96, 1)],
        [Vector4(1, -0.10, 1, 1), Vector4(1, 0.10, 1, 1)],
    ]
    # return outputs
    return (ctpm,)


# end ctrlpointMatrix


class ControlPointsMatrix(Node):
    def __init__(self):
        Node.__init__(self)
        self.add_output(name="ctpm", interface=IData)

    def __call__(self, inputs):
        return ctrlpointMatrix()


# end ControlPointsMatrix   (ctrlpointMatrix  wrapper)


def petalMatrix():
    """
    We define here a control points matrix with 3 columns and 9 rows for a bezier patch to draw a petal.

    :returns: the control points matrix
    """
    # from openalea.mtg.plantframe import Vector4 as V4
    from openalea.plantgl.math import Vector4 as V4

    # code
    ctpm = [
        [V4(0, -0.12, 0.0, 1), V4(0, 0, -0, 1), V4(0, 0.12, 0.0, 1)],
        [V4(0.14, -0.25, -0.2, 1), V4(0.14, 0, -0.25, 1), V4(0.13, 0.25, -0.2, 1)],
        [V4(0.28, -0.25, 0.35, 1), V4(0.28, 0, 0.2, 1), V4(0.28, 0.25, 0.35, 1)],
        [V4(0.42, -0.25, 0.55, 1), V4(0.42, 0, 0.3, 1), V4(0.42, 0.25, 0.55, 1)],
        [V4(0.56, -0.30, 0.6, 1), V4(0.56, 0, 0.15, 1), V4(0.56, 0.3, 0.6, 1)],
        [V4(0.7, -0.33, 0.6, 1), V4(0.7, 0, 0.1, 1), V4(0.7, 0.48, 0.33, 1)],
        [V4(0.84, -0.42, 0.75, 1), V4(0.84, 0, 0.4, 1), V4(0.84, 0.42, 0.75, 1)],
        [V4(0.97, -0.38, 0.8, 1), V4(0.97, 0, 0.5, 1), V4(0.97, 0.38, 0.8, 1)],
        [V4(0.95, -0.1, 0.95, 1), V4(1, 0, 1, 1), V4(0.95, 0.1, 0.95, 1)],
    ]
    # return outputs
    return (ctpm,)


# endef petalMatrix()


class PetalMatrix(Node):
    def __init__(self):
        Node.__init__(self)
        self.add_output(name="ctpm", interface=IData)

    def __call__(self, inputs):
        return petalMatrix()


# end PetalMatrix  (petalMatrix  wrapper)


########################################
def position(n):
    """We compute the position of an MTG node in a openalea.mtg.plantframe::Vector3

    :param n: the MTG node
    :returns: the position
    """
    return Vector3(n.XX, n.YY, n.ZZ)


# endef position(n)

# lSepalStore=[]
rangFoliole = 0  # pour utiliser l'allometrie par rang
dicAllometrie = {}


########################################
def numRang2folId(rank):
    dicRang = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E"}
    vraiRang = rank / 2
    if vraiRang not in list(dicRang.keys()):
        vraiRang = 4  # si folioles > E
    return dicRang[vraiRang]


########################################
def vertexVisitor(
    leaf_factory=None,
    bud_factory=None,
    sepal_factory=None,
    flower_factory=None,
    fruit_factory=None,
    knop_factory=None,
    stipuLe_factory=None,
):
    """We define here a function (visitor) that is used visit MTG nodes.

    :param leaf_factory: the function that draws the leaves
    :param bud_factory: the function that draws the buds
    :param sepal_factory: the function that draws the sepals
    :param flower_factory: the function that draws the flowers
    :param fruit_factory: the function that draws the fruits
    :param knop_factory: the function that draws the knops
    :return: the visitor function
    :todo: check the arity of all the versions of bud_factory
    """
    # from openalea.mtg.MTG import components
    # from openalea.mtg.aml import MTG as omam
    from openalea.mtg import MTG as omm

    # write the node code here.
    lSepalStore = []

    if leaf_factory is None:
        # pass
        leaf_factory = rawLeaflet
    # tests
    # leaf_factory=computeLeafletFrom4pts([0,0.5,1],[0,1,0])
    if bud_factory is None:
        bud_factory = rawBud()
    if sepal_factory is None:
        # pass
        sepal_factory = polygonLeaflet()  # rawLeaflet test aussi
    if flower_factory is None:
        flower_factory = coneFlower()  # bug when flower_factory is None
    if fruit_factory is None:
        fruit_factory = (
            simpleFruit()
        )  # bug "'tuple' object is not callable" if fruit_factory is None
    if knop_factory is None:
        knop_factory = None
    if stipuLe_factory is None:  # prevent from 'tuple' object bug
        stipuLe_factory = None

    def visitor(
        g,
        v,
        turtle,
        leaf_computer=leaf_factory,
        bud_computer=bud_factory,
        sepal_computer=sepal_factory,
        flower_computer=flower_factory,
        fruit_computer=fruit_factory,
        knop_factory=knop_factory,
        stipuLe_factory=stipuLe_factory,
    ):
        """
        a function that analyses the code of a vertex then takes decisions about the ways to display it
        """
        global rangFoliole
        # global dicAllometrie

        # import openalea.rose
        from openalea.rose import data

        # p = re.sub("rose", "share", openalea.rose.__path__[0])
        p = data.mtg_dir()

        dicAllometrie = {}
        if os.path.isdir(p):
            ficJson = p / "allometrieFolioles.json"
            if os.path.isfile(ficJson):
                with open(ficJson, "r") as fjs:
                    dicAllometrie = json.load(fjs)
            else:
                print("No file %s" % ficJson)
        else:
            dicAllometrie = {}
            print("""No dir %s" !""" % (p))

        n = g.node(v)
        pt = position(n)
        symbol = n.label[0]
        turtle.setId(v)
        currentColor = turtle.getColor()

        if symbol in ["E", "R"]:  # internode, rachis
            if n.Diameter is None:
                logging.error(
                    "ERROR: vertex %d (name: %s, line around %d)"
                    % (v, n.label, n._line)
                )
                n.Diameter = 0.75

            turtle.oLineTo(pt)
            turtle.setWidth(n.Diameter / 2.0)
            if symbol == "R":
                rangFoliole = len(omm.Descendants(g, v)) / 4

        elif n.label == "K1":  # knop
            if knop_factory is not None:
                # we draw a leaf axil bud
                points = [position(n)]
                while n.nb_children() == 1:
                    n = list(n.children())[0]
                    points.append(position(n))
                knop_factory(points, turtle)

        elif n.label == "L1":  # stipule
            if stipuLe_factory is not None:
                # we draw a stipule as an occultor for the bud
                points = [position(n)]
                while n.nb_children() == 1:
                    n = list(n.children())[0]
                    points.append(position(n))
                stipuLe_factory(points, turtle)

        elif n.label == "F1" or n.label == "Y1":  # leaflets
            if n.label == "Y1":  # young leaflets
                myColors.setTurtleAnthocyan(turtle)
            else:
                myColors.setTurtleLeaf(turtle)  #

            points = [position(n.parent()), pt]
            while n.nb_children() == 1:
                n = list(n.children())[0]
                points.append(position(n))

            lesX, lesY = dicAllometrie[numRang2folId(rangFoliole)]
            leaf_computer = computeLeafletFrom4pts(lesX, lesY)

            leaf_computer(points, turtle)

        elif n.label == "S1":  # sepal
            points = [position(n.parent()), pt]
            while n.nb_children() == 1:
                n = list(n.children())[0]
                points.append(position(n))
            myColors.setTurtleSepal(turtle)

            # lesX, lesY = dicAllometrie['S']
            # sepal_computer=computeLeafletFrom4pts(lesX,lesY)
            # sepal_computer(points, turtle)
            lSepalStore.append(points)

        elif n.label == "B1":  # flower Button
            points = [position(n.parent()), position(n)]

            # CPL
            parent = n.parent()
            pointsnDiameter = [
                [position(parent), parent.Diameter],
                [None, None],
                [position(n), n.Diameter],
            ]

            while n.nb_children() == 1:
                n = list(n.children())[0]
                points.append(position(n))
            bud_computer(pointsnDiameter, turtle, lSepalStore)

            # process digitized sepals
            turtle.setColor(4)  # apple green
            while lSepalStore:
                lSepalStore.pop()
                # sepal_computer(lSepalStore.pop(),turtle)

        elif n.label == "O1":  # flOwer
            turtle.setColor(4)  # apple green

            points = [position(n.parent()), position(n)]
            parent = n.parent()
            pointsnDiameter = [
                [position(parent), parent.Diameter],
                [None, None],
                [position(n), n.Diameter],
            ]
            flower_computer(pointsnDiameter, turtle, lSepalStore, n.Diameter)

            # process digitized sepals (if any)
            # turtle.setColor(len(lSepalStore)) # apple green
            turtle.setColor(4)  # apple green
            while lSepalStore:
                lSepalStore.pop()
            #    sepal_computer(lSepalStore.pop(),turtle)

        elif n.label == "C1":  # fruit (Cynorrodon)
            turtle.setColor(4)  # apple green
            # process sepals
            points = [n.parent(), n]
            # CPL
            parent = n.parent()
            pointsnDiameter = [
                [position(parent), parent.Diameter],
                [None, None],
                [position(n), n.Diameter],
            ]

            # fruit_computer(points, turtle, lSepalStore, -1)
            fruit_computer(pointsnDiameter, turtle, lSepalStore, -1)
            while lSepalStore:
                lSepalStore.pop()
                # sepal_computer(lSepalStore.pop(),turtle)

        elif n.label == "T1":  # Terminator
            # The turtle is supposed to be at the top of the previous vertex
            turtle.stopGC()  # because of <T1,bugged in donneesMSD
            myColors.setTurtleAnthocyan(turtle)
            turtle.startGC()
            turtle.oLineTo(pt)
            turtle.setWidth(0.01)

        elif symbol == "H":  # hidden vertex
            pass

        turtle.setColor(currentColor)

    # end visitor

    # return outputs
    return visitor


# endef vertexVisitor(leaf_factory=None, bud_factory=None, ...)


def mesh(geometry):
    """
    :param geometry: an PlantFrame geometry
    :return: the meshed (triangulated) geometry"""
    tessel = pgl.Tesselator()
    geometry.apply(tessel)
    mesh_ = tessel.triangulation
    return mesh_


# end mesh


def canline(ind, label, p):
    """
    Write a triangle in the can formalism (version 01)
    :param ind: geometry.indexList, i.e la liste des index adressant les points 3D
    :param label: the label of the triangle
    :param p: geometry.pointList, i.e la liste des points 3D constituant le polygone
    :return: a can 02 line
    """
    return "p 2 %s 9 3 %s" % (str(label), " ".join(str(x) for i in ind for x in p[i]))


# end canline


def can02line(dateDigit, typeOrg, numPlante, numOrg):
    """
    :param dateDigit: the day number
    :param typeOrg: the type of organ
    :param numPlante: the plant number
    :param numOrg:  the Id of the organ
    :return: a can02 line heading fields
    :note: all these fields will be read as integers by Sec2
    """
    return "%s %s %s %s " % (dateDigit, typeOrg, numPlante, numOrg)


# end can02line

# global variables whose values remains unchanged between successive calls of vertexVisitor4CAN02
numeroPlante = 0  # the plant number, to detect when a new plant is processed
numApp = 0  # the number of callings within a plant (debug purposes)
# orgNum = 1     # the organ Id
sOn = []  # ?? todo : unerstand y # None         # the stack of nodes that carry a branch
oldOrdre = 0  # did we branch or debranch ?


########################################
def vertexVisitor4CAN02(
    leaf_factory=None,
    bud_factory=None,
    sepal_factory=None,
    flower_factory=None,
    fruit_factory=None,
    knop_factory=None,
    stipuLe_factory=None,
    pathToOrgIds=None,
):
    """We define here a function (visitor) that is used visit MTG nodes.

    :param leaf_factory: the function that draws the leaves
    :param bud_factory: the function that draws the buds
    :param sepal_factory: the function that draws the sepals
    :param flower_factory: the function that draws the flowers
    :param fruit_factory: the function that draws the fruits
    :param knop_factory: the function that draws the knops
    :param canFacts: data to build the CAN02 files
    :return: the visitor function
    :todo: check the arity of all the versions of bud_factory
    """
    # write the node code here.
    lSepalStore = []

    if leaf_factory is None:
        leaf_factory = rawLeaflet
    if bud_factory is None:
        bud_factory = rawBud
    if sepal_factory is None:
        sepal_factory = polygonLeaflet()  # rawLeaflet
    if flower_factory is None:
        flower_factory = coneFlower()  # bug when flower_factory is None
    if fruit_factory is None:
        fruit_factory = (
            simpleFruit()
        )  # bug "'tuple' object is not callable" if fruit_factory is None
    if knop_factory is None:
        knop_factory = noThing
    if stipuLe_factory is None:
        stipuLe_factory = noThing
    if pathToOrgIds is None:
        return None

    from openalea.mtg import MTG as omm
    import json
    import re
    import alinea.rose

    pkg = alinea.rose.__path__

    for path in pkg:
        if re.search("rose/rose$", path):
            p = re.sub("rose$", "share/CAN", path)

            with open("%s/%s.json" % (p, "symbOrganId"), "r") as f:
                symbolOrganIdict = json.load(f)
            with open("%s/%s.json" % (p, "coulOrganes"), "r") as f:
                coulOrganesIdict = json.load(f)
            p = re.sub("rose$", "share/MTG", path)
            with open("%s/%s.json" % (p, "allometrieFolioles"), "r") as f:
                dicAllometrie = json.load(f)

    def orgNumFromStack(stack):
        """
        Computing the organ number from the stack of nodes that bear the node :
        stack[-1] is the current node ; stack[-2] is the last branching node (lbn), &.so
        local node has a weight of 1 ; lbn has a weigh of 1000, &.so
        """
        retVal = 0
        if stack:
            factor = 1
            localStack = stack[0:3]
            while localStack:
                retVal += localStack.pop() * factor
                factor *= 1000
        else:
            return 1
        return retVal

    # fin orgNumFromStack

    def visitor(
        g,
        v,
        turtle,
        leaf_computer=leaf_factory,
        bud_computer=bud_factory,
        sepal_computer=sepal_factory,
        flower_computer=flower_factory,
        fruit_computer=fruit_factory,
        knop_factory=knop_factory,
        stipuLe_factory=stipuLe_factory,
        canFacts=None,
        symbolOrganIdict=symbolOrganIdict,
        coulOrganIdict=coulOrganesIdict,
    ):
        """
        a function that analyses the code of a vertex then
        takes decisions about the ways to display it.
        if canFacts is a python dict, it will write CAN02 file accordingly to
        Sec2/Sources/Canopy/Organ.hpp's codification.
        """
        if canFacts is None:
            canFacts = {}
        from openalea.mtg import algo

        global rangFoliole

        # A 2nd turtle to duplicate the local geometry, so we still
        # know the organ number when writing it into the CAN file
        maTortue = pgl.PglTurtle()
        maTortue.move(turtle.getPosition())
        maTortue.startGC()
        maTortue.setWidth(turtle.getWidth())

        n = g.node(v)
        pt = position(n)
        symbol = n.label[0]

        turtle.setId(v)
        maTortue.setId(v)

        currentColor = turtle.getColor()

        global numeroPlante  # we test the plant number to deal with  numApp
        global numApp  # dbg: the number of times we called this fuction within a plant

        plantNum = None
        global oldOrdre  # keep the order between 2 calls
        global sOn  # keep the stack of node number between 2 calls
        # global anglOuverture

        orgType = 666
        if symbolOrganIdict:
            orgType = symbolOrganIdict[symbol]

        if canFacts:
            plantNum = g.properties()["plantNum"]

        if symbol in ["E", "R"]:
            if n.Diameter is None:
                logging.error(
                    "ERROR: vertex %d (name: %s, line around %d)"
                    % (v, n.label, n._line)
                )
                n.Diameter = 0.75
            if symbol == "R":
                rangFoliole = len(omm.Descendants(g, v)) / 4

            if symbol == "E":
                # orgType=2 # Sec2/Sources/Canopy/CANReader.cpp
                # To deal with branching :
                numNode = int(n.label[1:])
                ordre = algo.order(g, v)  # vplants doc 0.8 p.83
                if ordre - oldOrdre > 0:
                    sOn.append(numNode)
                elif ordre - oldOrdre < 0:
                    sOn.pop()
                    sOn[-1] = numNode
                else:
                    if sOn:
                        sOn[-1] = numNode
                    else:
                        sOn.append(numNode)
                oldOrdre = ordre

            turtle.oLineTo(pt)
            turtle.setWidth(n.Diameter / 2.0)
            maTortue.oLineTo(pt)
            maTortue.setWidth(n.Diameter / 2.0)

        elif n.label == "K1":
            if knop_factory is not None:
                points = [position(n)]
                while n.nb_children() == 1:
                    n = list(n.children())[0]
                    points.append(position(n))
                knop_factory(points, maTortue)
                knop_factory(points, turtle)

        elif n.label == "L1":
            if stipuLe_factory is not None:
                # orgType=12 # stipule
                # we draw a stipule as a partial occultor for the bud
                points = [position(n)]
                while n.nb_children() == 1:
                    n = list(n.children())[0]
                    points.append(position(n))
                stipuLe_factory(
                    points,
                    maTortue,
                )
                stipuLe_factory(points, turtle)

        elif n.label == "F1" or n.label == "Y1":
            if n.label == "Y1":  # young leaflets
                # 'ttention, ce n'est que visuel dans OA
                myColors.setTurtleAnthocyan(turtle)
                myColors.setTurtleAnthocyan(maTortue)
            else:
                myColors.setTurtleLeaf(turtle)
                myColors.setTurtleLeaf(maTortue)  #

            points = [position(n.parent()), pt]
            while n.nb_children() == 1:
                n = list(n.children())[0]
                points.append(position(n))

            lesX, lesY = dicAllometrie[numRang2folId(rangFoliole)]
            leaf_computer = computeLeafletFrom4pts(lesX, lesY)

            leaf_computer(points, turtle)
            leaf_computer(points, maTortue)
            # Now sec2 takes into account optical propertiesof the organ type
            orgType = symbolOrganIdict[n.label[0]]

        elif n.label == "S1":
            # orgType=6 # sepal
            points = [position(n.parent()), pt]
            while n.nb_children() == 1:
                n = list(n.children())[0]
                points.append(position(n))
            lSepalStore.append(points)
            myColors.setTurtleSepal(maTortue)
            sepal_computer(points, maTortue)
            myColors.setTurtleSepal(turtle)
            sepal_computer(points, turtle)

        elif n.label == "B1":
            # orgType=7 # flower button
            myColors.setTurtleButton(maTortue)
            myColors.setTurtleButton(turtle)
            points = [n.parent(), n]
            while n.nb_children() == 1:
                n = list(n.children())[0]
                points.append(n)
            bud_computer(points, turtle, lSepalStore)
            bud_computer(points, maTortue, lSepalStore)

            # process digitized sepals
            # turtle.setColor(4) # fluo apple green
            # maTortue.setColor(4)
            while lSepalStore:
                lSepalStore.pop()
                # sepal_computer(lSepalStore[-1],maTortue)
                # sepal_computer(lSepalStore.pop(),turtle)

        elif n.label == "O1":
            # orgType=8 # fleur
            #            turtle.setColor(4) #fluo apple green
            #            maTortue.setColor(4)

            points = [n.parent(), n]
            flower_computer(points, turtle, lSepalStore, n.Diameter)
            flower_computer(points, maTortue, lSepalStore, n.Diameter)

            # process digitized sepals (if any)
            # turtle.setColor(4) # fluo apple green
            # maTortue.setColor(4) #
            while lSepalStore:
                lSepalStore.pop()
                # sepal_computer(lSepalStore[-1],maTortue)
                # sepal_computer(lSepalStore.pop(),turtle)

        elif n.label == "C1":
            # orgType=9 # fruit or cynorrhodon
            # turtle.setColor(4) # fluo apple green
            # maTortue.setColor(4) #
            points = [n.parent(), n]
            fruit_computer(points, turtle, lSepalStore, -1)
            fruit_computer(points, maTortue, lSepalStore, -1)
            # turtle.setColor(4) # fluo apple green
            # maTortue.setColor(4) #
            while lSepalStore:
                lSepalStore.pop()
                # sepal_computer(lSepalStore[-1],maTortue)
                # sepal_computer(lSepalStore.pop(),turtle)

            # process terminator
        elif n.label == "T1":
            # orgType=10 # terminator
            # The turtle is supposed to be at the top of the previous vertex
            turtle.setColor(2)  # green
            # turtle.startGC()
            turtle.oLineTo(pt)
            turtle.setWidth(0.01)

            maTortue.setColor(2)  # fluo apple green
            maTortue.oLineTo(pt)
            maTortue.setWidth(0.01)

        # tODO : pass ou continue ?
        elif symbol == "H":  # hidden vertex
            pass
        elif symbol == "J":  # peduncle
            pass
        # A  CAN02 file may contain several plants, but we don't use this here
        elif symbol == "P":
            pass

        turtle.setColor(currentColor)
        maTortue.setColor(currentColor)

        # code CAN02
        if not numeroPlante == plantNum:
            # tracking the number of calls (debug)
            numApp = 1
            numeroPlante = plantNum
            sOn = []

        orgNum = orgNumFromStack(sOn)

        if canFacts:
            numApp += 1
            # out = []
            # TODO : modifier en laissant orgType vide "%%s"
            debutLigne = can02line(canFacts["dateDigit"], "%s", plantNum, orgNum)

            maTortue.stopGC()
            maScene = maTortue.getScene()
            for obj in range(len(maScene)):
                geometry = mesh(maScene[obj])
                p = geometry.pointList
                index = geometry.indexList
                numTri = 1
                # TODO : calculer orgType d'apres la couleur et le dico de
                # couleur qui associera couleur:orgType
                # Cf. rose_file::scene2Can01()
                for ind in index:
                    if symbol in "B O C".split():
                        # compute orgType
                        # from maScene[obj].appearance.diffuseColor()
                        # laCouleur=str(maScene[obj].appearance.diffuseColor())
                        laCouleur = re.sub(
                            "Color3", "", str(maScene[obj].appearance.diffuseColor())
                        )

                        if laCouleur in list(coulOrganIdict.keys()):
                            orgType = coulOrganIdict[laCouleur]
                        else:
                            print("symbol: %s : %s" % (symbol, laCouleur))

                    canFacts["canStream"].write(
                        "%s %d %s\n"
                        % (
                            debutLigne % orgType,
                            numTri,
                            "  ".join("%8.3f" % x for i in ind for x in p[i]),
                        )
                    )
                    numTri += 1
        else:
            print(("canFacts: %s" % canFacts))

    # end visitor

    # return outputs
    return visitor


# end vertexVisitor4CAN02(leaf_factory=None, bud_factory=None, ...)


class VertexVisitor(Node):
    def __init__(self):
        Node.__init__(self)
        self.add_input(name="leaf_factory", interface=IFunction)
        self.add_input(name="bud_factory", interface=IFunction)
        self.add_input(name="sepal_factory", interface=IFunction)
        self.add_input(name="flower_factory", interface=IFunction)
        self.add_input(name="fruit_factory", interface=IFunction)
        self.add_input(name="knop_factory", interface=IFunction)
        self.add_input(name="stipuLe_factory", interface=IFunction)
        self.add_output(name="VertexVisitor", interface=IFunction)

    def __call__(self, inputs):
        leaf_factory = self.get_input("leaf_factory")
        bud_factory = self.get_input("bud_factory")
        sepal_factory = self.get_input("sepal_factory")
        flower_factory = self.get_input("flower_factory")
        fruit_factory = self.get_input("fruit_factory")
        knop_factory = self.get_input("knop_factory")
        stipuLe_factory = self.get_input("stipuLe_factory")
        return vertexVisitor(
            leaf_factory,
            bud_factory,
            sepal_factory,
            flower_factory,
            fruit_factory,
            knop_factory,
            stipuLe_factory,
        )


# end class VertexVisitor   (wrapper for vertexVisitor)


class VertexVisitor4CAN02(Node):
    def __init__(self):
        Node.__init__(self)
        self.add_input(name="leaf_factory", interface=IFunction)
        self.add_input(name="bud_factory", interface=IFunction)
        self.add_input(name="sepal_factory", interface=IFunction)
        self.add_input(name="flower_factory", interface=IFunction)
        self.add_input(name="fruit_factory", interface=IFunction)
        self.add_input(name="knop_factory", interface=IFunction)
        self.add_input(name="stipuLe_factory", interface=IFunction)
        self.add_input(name="canFacts", interface=IDict)
        self.add_output(name="VertexVisitor", interface=IFunction)

    def __call__(self, inputs):
        leaf_factory = self.get_input("leaf_factory")
        bud_factory = self.get_input("bud_factory")
        sepal_factory = self.get_input("sepal_factory")
        flower_factory = self.get_input("flower_factory")
        fruit_factory = self.get_input("fruit_factory")
        knop_factory = self.get_input("knop_factory")
        stipuLe_factory = self.get_input("stipuLe_factory")
        canFacts = self.get_input("canFacts")
        return vertexVisitor4CAN02(
            leaf_factory,
            bud_factory,
            sepal_factory,
            flower_factory,
            fruit_factory,
            knop_factory,
            stipuLe_factory,
            canFacts,
        )


# end class VertexVisitor4CAN02  (wrapper for vertexVisitor4CAN02)


#### Copied from mtg.turtle ###
def traverse_with_turtle(g, vid, visitor, turtle=None):
    """
    This function is called from within TurtleFrame. It explores the part
    of an MTG tree being under the node number "vid".
    It walks through that sub-MTG using the pre_order2_with_filter algorithm.

    :param g: the MTG object we are working on
    :param vid: the vertex ID inside the MTG
    :param visitor: the function that visits the nodes of the sub-MTG
    :see: openalea/mtg/traversal.py
    :note: this function was inspired by OpenAlea.Mtg-0.9.5-py2.6.egg/openalea/mtg/turtle.py
    """
    if turtle is None:
        turtle = pgl.PglTurtle()

    def push_turtle(v):
        if g.edge_type(v) == "+":
            turtle.push()
            if g.class_name(v) == "R":
                """
                The generalized cylinders may seem flattened horizontally
                or vertically when they draw a new rachis.
                So we turn the turtle towards the leaf before to draw it.
                """
                import numpy.linalg as npl

                pp = position(g.node(v).parent())
                tmp = int(g.node(v).parent().index())

                ps = None
                while tmp is not None:
                    if g.class_name(tmp) == "E":
                        ps = position(g.node(tmp))
                        break
                    children = g.node(tmp).children()
                    if len(children) == 0:
                        break
                    tmp = int(g.node(tmp).children()[0].index())

                if ps is not None:
                    rachis = position(g.node(v)) - pp
                    rachis = rachis / npl.norm(rachis)
                    tige = ps - pp

                    travers = tige ^ rachis
                    travers = travers / npl.norm(travers)
                    # that's the point :
                    turtle.stopGC()
                    turtle.setHead(travers, rachis)
                    turtle.startGC()

            turtle.setId(v)
        return True

    def pop_turtle(v):
        if g.edge_type(v) == "+":
            # turtle.stopGC()
            turtle.pop()

    turtle.push()

    turtle.startGC()
    visitor(g, vid, turtle)
    for v in pre_order2_with_filter(g, vid, None, push_turtle, pop_turtle):
        if v == vid:
            continue
        visitor(g, v, turtle)
    turtle.stopGC()
    turtle.pop()
    return turtle.getScene()


# endef traverse_with_turtle(g, vid, visitor, turtle=None)


#### Copied from traverse_with_turtle() ###
def traverse_with_turtle4CAN02(g, vid, visitor, turtle=None, canFacts=None):
    """
    This function is called from within TurtleFrame. It explores the part
    of an MTG tree being under the node number "vid".
    It walks through that sub-MTG using the pre_order2_with_filter algorithm.

    :param g: the MTG object we are working on
    :param vid: the vertex ID inside the MTG
    :param visitor: the function that visits the nodes of the sub-MTG
    :see: openalea/mtg/traversal.py
    :note: this function was derived from OpenAlea.Mtg-0.9.5-py2.6.egg/openalea/mtg/turtle.py
    """
    if canFacts is None:
        canFacts = {}
    if turtle is None:
        turtle = pgl.PglTurtle()

    def push_turtle(v):
        if g.edge_type(v) == "+":
            turtle.push()
            # turtle.startGC()
            turtle.setId(v)
        return True

    def pop_turtle(v):
        if g.edge_type(v) == "+":
            # turtle.stopGC()
            turtle.pop()

    turtle.push()
    turtle.startGC()

    visitor(g, vid, turtle, canFacts=canFacts)
    turtle.stopGC()
    for v in pre_order2_with_filter(g, vid, None, push_turtle, pop_turtle):
        if v == vid:
            continue
        turtle.startGC()
        visitor(g, v, turtle, canFacts=canFacts)
        turtle.stopGC()
    turtle.pop()
    return turtle.getScene()


# endef traverse_with_turtle4CAN02(g, vid, visitor, turtle=None, canFacts=[])


######################################################
def TurtleFrame(g, visitor):
    """The function that sets the turtle up and calls the function traverse_with_turtle
    that walks through the MTG tree, with  "visitor" as a parameter.

    :param g: an MTG object to explore.
    :param visitor: the function to be called at every node of the "g" MTG.
    :calls: pgl.PglTurtle that makes a brand-new turtle.
    :calls: the traverse_with_turtle function, with the turtle as an argument
    :return: the scene collected by the turtle during the walkthrough.
    """
    debug = False  # True
    n = g.max_scale()
    turtle = pgl.PglTurtle()
    ## we want to change the default color
    ## let's wait to have scanned some photographs to set this
    # setTurtleStrand(turtle)

    for plant_id in g.vertices(scale=1):
        plant_node = g.node(plant_id)
        if debug:
            print("plant_node = %s" % plant_id)
        # moved the "position" function away
        origin = pgl.Vector3(plant_node.XX, plant_node.YY, plant_node.ZZ)
        turtle.move(origin)
        # vid =  g.component_roots_at_scale(plant_id, scale=n).next() # does not run
        tmp = iter(g.component_roots_at_scale(plant_id, scale=n))
        vid = next(tmp)

        traverse_with_turtle(g, vid, visitor, turtle)
    return turtle.getScene()


# endef TurtleFrame(g, visitor)


######################################################
def TurtleFrame4CAN02(g, visitor, plantFacts):
    """The function that sets the turtle up and calls the function traverse_with_turtle
    that walks through the MTG tree, with  "visitor" as a parameter.

    :param g: an MTG object to explore.
    :param visitor: the function to be called at every node of the "g" MTG.
    :calls: pgl.PglTurtle that makes a brand new turtle.
    :calls: the traverse_with_turtle function, with the turtle as an argument
    :return: the scene collected by the turtle during the walkthrough.
    """
    debug = False  # True
    n = g.max_scale()
    turtle = pgl.PglTurtle()

    for plant_id in g.vertices(scale=1):
        plant_node = g.node(plant_id)
        if debug:
            print("plant_node = %s" % plant_id)
        origin = pgl.Vector3(plant_node.XX, plant_node.YY, plant_node.ZZ)
        turtle.move(origin)
        tmp = iter(g.component_roots_at_scale(plant_id, scale=n))
        vid = next(tmp)

        traverse_with_turtle4CAN02(g, vid, visitor, turtle, plantFacts)
    return turtle.getScene()


# endef TurtleFrame4CAN02(g, visitor)


def reconstructWithTurtle(mtg, visitor, powerParam):
    """Builds a scene from an MTG object using a vertex visitor
    function and a number to help compute the diameter of the nodes of the trunk.

    :param mtg: an MTG object
    :param visitor: The visitor function  walks through the nodes of the MTG and checks for the symbols of the nodes to call the display function that fits this organ
    :param powerParam: The numerical exponent helps to compute the diameters where they have not been measured, using a pipe model.
    :calls: the TurtleFrame function
    :return: the 3D scene that was collected by TurtleFrame during the walk through the MTG.
    :todo: Add some constant in the arguments
    """
    # Compute the radius with pipe model
    diameter = mtg.property("Diameter")
    for v in mtg:
        if mtg.class_name(v) == "R":
            diameter[v] = 0.75
        elif mtg.class_name(v) == "B":
            diameter[mtg.parent(v)] = 1.75
        elif mtg.class_name(v) in ["O", "C"]:
            diameter[mtg.parent(v)] = 2.0

    drf = DressingData(
        LeafClass=["F", "S"],
        FlowerClass="O",
        FruitClass="C",
        MinTopDiameter=dict(E=0.5),
    )  # {'E':0.5}) #dict(E=0.5))
    pf = PlantFrame(
        mtg, TopDiameter="Diameter", DressingData=drf, Exclude="F S T O B C".split()
    )

    mtg.properties()["Diameter"] = pf.algo_diameter(power=powerParam)

    theScene = TurtleFrame(mtg, visitor)
    # return outputs
    return (theScene,)


# end reconstructWithTurtle(mtg, visitor, powerParam)


def buildCanPath(path):
    """we comute the path to write CAN files in"""
    if path is None or path == "":
        retPath = os.getenv("TEMP")
        if retPath is None:
            retPath = "/tmp"
    elif re.search("/MTG/", path):
        # we want to avoid errors when we associate filenames/experiments
        retPath = re.sub("/MTG/", "/CAN/", path)
    else:
        retPath = path
    if not os.path.exists(retPath):
        os.makedirs(retPath)

    return retPath


# end buildCanPath


def clearCanPath(path):
    """we clear all the *.can file within the directory "path" """
    import glob
    import os

    for can in glob.glob("%s/*.can" % buildCanPath(path)):
        os.unlink(can)


# end clearCanPath()


def openCanFile(path, plantPath, plantName):
    """
    we open a file whose name is built whether the path is absolute or relative
    and with plantName.can as its basename
    """
    realPath = buildCanPath(path)
    retVal = open("%s/%s.can" % (realPath, plantName), "w")
    retVal.write("CAN02\n")
    retVal.write(
        "#dateDigit\ttypeOrgane\tnumPlante\tnumOrgane\tnumTri\tx1 y1 z1\tx2 y2 z2\tx3 y3 z3\n"
    )
    # retVal.write("#Debugging\n");
    return retVal


# end openCanFile


def writeCanFile(fOut, numTri, organNum, organType, plantNum, jour=1, geometrie=None):
    """
    We  write a line of data.
    This is test stuff ; i.e.  to be called out of plantFrame
    """
    if geometrie is None:
        geometrie = []
    fOut.write(
        "%d %d %d %d %d %s\n" % (jour, organType, plantNum, organNum, numTri, geometrie)
    )


# end writeCanFile


def dateDigit(dirName, plantnum):
    """
    we return the date when this computation was made
    :TODO: we want to compute the number of the day when the digitization was made,
     this data could become deductible from the dirname if the associated knowledge
    By importing json & loadin the dict everytime, this code should be quite inefficient in C
    Getting the dict (at least it's name) as an input of the node could be an option

    """
    # import time
    # return time.strftime('%Y%m%d',time.localtime())
    import json
    import re

    #    from openalea.core.pkgmanager import PackageManager
    #    pm = PackageManager()
    #    pkg = pm.get_wralea_path()
    import alinea.rose

    p = re.sub("rose$", "share", alinea.rose.__path__[0])
    #    pkg.append(p)
    #    p=''
    #    for path in pkg :
    #        if re.search("rose-master/rose$", path) :
    #            p=path
    if p:
        with open("%s/CAN/datesPrelevements.json" % p, "r") as f:
            dicoPrel = json.load(f)

    chemin = dirName.split("/")
    manip = chemin[-2]
    prel = chemin[-1]
    return int(dicoPrel[manip][prel][str(plantnum % 2000)])


# end dateDigit


def reconstructionsWithTurtle(mtgs, visitor, powerParam, canFilesOutPath):
    """Builds a list of scenes from a list of MTG object using a vertex visitor
    function and a number to help compute the diameter of the nodes of the trunk.

    :param mtgs: a list of MTG objects
    :param visitor: The visitor function  walks through the nodes of the MTG and checks for the symbols of the nodes to call the display function that fits this organ
    :param powerParam: The numerical exponent helps to compute the diameters where they have not been measured, using a pipe model.
    :param canFilesOutPath: a path to write can files to, either absolute, relative or empty.
        If absolute, can files are written there,
        If relative, it plugs into the dirname of the MTG file,
        If empty, no can files are generated.
    :calls: the TurtleFrame function
    :return: the 3D scene that was collected by TurtleFrame during the walk through the MTG.
    :todo: Add some constant in the arguments
    """
    # Compute the radius with pipe model

    theScenes = []
    makeCan = False
    # canPath=''
    fOut = None
    canFacts = {}
    # dateDigit= None

    if not canFilesOutPath == "":
        makeCan = True
        clearCanPath(canFilesOutPath)

    for mtg in mtgs:
        # if we have to write a can file, we'll do it organ by organ in each MTG
        if makeCan:
            # check if we can get two interesting properties
            if "dirName" in mtg.properties() and "plantNum" in mtg.properties():
                fOut = openCanFile(
                    canFilesOutPath,
                    mtg.properties()["dirName"],
                    mtg.properties()["plantNum"],
                )
                canFacts["canStream"] = fOut
                canFacts["dateDigit"] = dateDigit(
                    mtg.properties()["dirName"], mtg.properties()["plantNum"]
                )

        diameter = mtg.property("Diameter")
        for v in mtg:
            if mtg.class_name(v) == "R":
                diameter[v] = 0.75
            elif mtg.class_name(v) == "B":
                diameter[mtg.parent(v)] = 1.75
            elif mtg.class_name(v) in ["O", "C"]:
                diameter[mtg.parent(v)] = 2.0

        drf = DressingData(
            LeafClass=["F", "S"],
            FlowerClass="O",
            FruitClass="C",
            MinTopDiameter=dict(E=0.5),
        )
        pf = PlantFrame(
            mtg, TopDiameter="Diameter", DressingData=drf, Exclude="F S T O B C".split()
        )
        mtg.properties()["Diameter"] = pf.algo_diameter(power=powerParam)

        theScene = TurtleFrame4CAN02(mtg, visitor, canFacts)
        theScenes.append(theScene)

        if fOut:
            fOut.close()

    # return outputs
    return (theScenes,)


# end reconstructionsWithTurtle(mtgs, visitor, powerParam)


class ReconstructWithTurtle(Node):
    def __init__(self):
        Node.__init__(self)
        self.add_input(name="g", interface=IData)
        self.add_input(name="Visitor", interface=IFunction)
        self.add_input(name="powerParam", value=2.2, interface=IFloat)
        self.add_output(name="TheScene", interface=IData)

    def __call__(self, inputs):
        g = self.get_input("g")
        Visitor = self.get_input("Visitor")
        powerParam = self.get_input("powerParam")
        return reconstructWithTurtle(g, Visitor, powerParam)


# end ReconstructWithTurtle   (reconstructionsWithTurtle  wrapper)


class ReconstructionsWithTurtle(Node):
    def __init__(self):
        Node.__init__(self)
        self.add_input(name="MTGs", interface=ISequence)
        self.add_input(name="Visitor", interface=IFunction)
        self.add_input(name="powerParam", value=2.2, interface=IFloat)
        self.add_input(name="canFilesOutPath", value="", interface=IStr)
        self.add_output(name="TheScenes", interface=ISequence)

    def __call__(self, inputs):
        MTGs = self.get_input("MTGs")
        Visitor = self.get_input("Visitor")
        powerParam = self.get_input("powerParam")
        canFilesOutPath = self.get_input("canFilesOutPath")
        return reconstructionsWithTurtle(MTGs, Visitor, powerParam, canFilesOutPath)


# end ReconstructionsWithTurtle   (reconstructionsWithTurtle  wrapper)


def scene_union(somescenes=None):
    """glue MTGs' scenes together in a big scene"""
    if somescenes is None:
        somescenes = []
    # write the node code here.
    if isinstance(somescenes, list):
        if len(somescenes) >= 2:
            thescene = somescenes[0] + somescenes[1]
            for somescene in somescenes[2:]:
                thescene = thescene + somescene
        else:
            thescene = somescenes[0]
    else:  # we take a risk to return something not being an MTG
        thescene = somescenes

    # return outputs
    return (thescene,)


# end scene_union(somescenes)


class Scene_union(Node):
    def __init__(self):
        Node.__init__(self)
        self.add_input(name="somescenes", interface=ISequence)
        self.add_output(name="ascene", interface=IData)

    def __call__(self, inputs):
        someScenes = self.get_input("somescenes")
        return scene_union(someScenes)


# end Scene_union      (scene_union  wrapper)
