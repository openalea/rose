#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-
from openalea.mtg.plantframe import *

def revolutiontestinonefile():
    '''    test the load of uninode files
    '''
    out1 = None; 
    # write the node code here.

    # write the node code here.
    pts=[Vector2(0.1, 0.00),
         Vector2(0.50, 0.06),
         Vector2(0.40, 0.14),
         Vector2(0.60, 0.18),
         Vector2(1.00, 0.30),
         Vector2(0.90, 0.42),
         Vector2(0.50, 0.60),
         Vector2(0.30, 0.84),
         Vector2(0.00, 1.00)]
    #print points
    pa=Point2Array(pts)
    pl=Polyline2D(pa)
    out1=Revolution(pl)


    # return outputs
    return out1,
