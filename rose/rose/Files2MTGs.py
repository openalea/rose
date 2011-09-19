#!/usr/bin/env python
# coding: iso-8859-15 -*-

## Creates a list of MTG object from a dict of MTG files associated to a list of coordinates 
from openalea.mtg.aml import MTG
import math

def Files2MTGs(cropdict, ToRotate=True):
    '''    reads MTG files, then 
    - places them both onto their coordinates, 
    - uses them again to fill up empty spaces, with a random rotation angle.
    @param cropdict : a dictionary built with 
    - MTG files names as keys,
    - shift of the real plant as 1st value for each key
    - shift and rotation as further values, if any
    #return a list of MTG objects that were build from the dict
    '''
    listofmtgs = []; 
    # write the node code here.

    def BaseOfPlant(nodeOfMTG):
        """ returns the coordinates of the anchorage of the plant in the XY plane"""
        return (nodeOfMTG.XX, nodeOfMTG.YY)

    def PositionIt(noeud, orx, ory, rotc, rots, shiftx, shifty, shiftz, doRotate):
        """ positions the node "noeud"
        the node gets
        - moved to the origin point as (orx, ory)
        - rotated around this point by the values (rot cos, rot sin) 
        - moved along the "shift" vector
        @param noeud the MTG node
        @param orx origin.x
        @param ory origin.y
        @param rotc cosine of the rotation angle
        @param rots sine of the rotation angle
        @param shiftx the x displacement to apply onto "noeud"
        @param shifty the y displacement to apply onto "noeud"
        @param shiftz the z displacement to apply onto "noeud"

        Note : the parameters are scalars rather than structures in order to speed up the process.
        """
        x0=noeud.XX - orx
        y0=noeud.YY - ory
        if doRotate :
            x1 = x0*rotc - y0*rots
            y1 = y0*rotc + x0*rots
        else:
            x1 = x0
            y1 = y0
        noeud.XX = x1 + shiftx
        noeud.YY = y1 + shifty
        noeud.ZZ += shiftz

     # creates output list (to be improved with rotates and shifts)
    for plante in cropdict.keys():
        for shiftRot in cropdict[plante]:
            
            #print shift

            # get prepared for rotations
            shift=shiftRot[0]
            sx=shift[0]
            sy=shift[1]
            sz=shift[2]

            angle=shiftRot[1]
            #angle= 1. # DBG 1 rad.
            (rc,rs)=(math.cos(angle), math.sin(angle))

            # load the MTG
            mtg=MTG(plante)

            noeud = mtg.node(1)      # the anchorage of the plant
            (ox,oy)= BaseOfPlant(noeud)
            
            PositionIt(noeud, ox, oy, rc, rs, sx, sy, sz, ToRotate)
            #if ToRotate :
            #    RotateIt(noeud, cosa, sina)
            #ShiftIt(noeud, shiftRot[0])
            for vtx in mtg.vertices(scale=2): # the rest of the plant
                noeud = mtg.node(vtx)
                #if ToRotate :
                #    RotateIt(noeud, cosa, sina)
                #ShiftIt(noeud, shiftRot[0])
                PositionIt(noeud, ox, oy, rc, rs, sx, sy, sz, ToRotate)
            listofmtgs += [mtg] 

   # return outputs
    return listofmtgs,
