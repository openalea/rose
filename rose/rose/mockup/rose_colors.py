#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

from openalea.core.external import * 
from openalea.core.logger  import *

# for Colors
import openalea.plantgl.all as pgl

from openalea.mtg.plantframe import *
""" there are 5 builtin colors in oa.mtg.plantframe :
    0 : kind of black
    1 : copper
    2 : green
    3 : red
    4 : sort of yellow
    So we add up colors from the electrical color code from 11 to 19,
      and next will be pastels.
    # we do neither define nor use all of these colors for now
    """
strand=1
brown=11
red=12
orange=13
yellow=14
green=15
blue=16
purple=17
grey=18
white=19
# Newt will be pastels useful for roses
lightGrey=20
lightBrown=21
pink=22
lightOrange=23
lightYellow=24
lightGreen=25
lightBlue=26
lightPurple=27
perlGrey=28
brokenWhite=29
# KO
koPink=30

def Blue():
    return pgl.Color3(80,80,255)
def LightBlue():
    return pgl.Color3(127,192,255) 
def Brown():
    return pgl.Color3(70,32,10) 
def LightBrown():
    return pgl.Color3(139,69,19) # from SaddleBrown in /usr/share/X11/rgb.txt
def Green():
    return pgl.Color3(80,255,80)   # flashy green
def LightGreen():
    return pgl.Color3(176,255,176)
def LightGrey():
    return pgl.Color3(192,192,192)
def _KoPink():
    return pgl.Color3(140, 25, 55) # from petal scans
def PerlGrey():
    return pgl.Color3(228,228,228)
def Orange():
    return pgl.Color3(255,127,0)
def LightOrange():
    return pgl.Color3(255,192,127)
def Purple():
    return pgl.Color3(255,80,255)
def LightPurple():
    return pgl.Color3(255,144,255)
def Pink():
    return pgl.Color3(255,192,203)
def Red():
    return pgl.Color3(255,32,32)
def Strand():
    return pgl.Color3(80,80,20) # set a realistic one
def White():
    return pgl.Color3(255,255,255)
def BrokenWhite():
    return pgl.Color3(240,240,240)
def Yellow():
    return pgl.Color3(240,240,16)
def LightYellow():
    return pgl.Color3(250,250,192)

def setTurtleBlue(t):
    t.setColorAt(blue, Blue())
    t.setColor(blue) 
def setTurtleLightBlue(t):
    t.setColorAt(lightBlue, LightBlue())
    t.setColor(lightBlue) 

def setTurtleBrown(t):
    t.setColorAt(brown, Brown())
    t.setColor(brown) 
def setTurtleLightBrown(t):
    t.setColorAt(lightBrown, LightBrown())
    t.setColor(lightBrown) 

def setTurtleGreen(t):
    t.setColorAt(green, Green())
    t.setColor(green) 
def setTurtleLightGreen(t):
    t.setColorAt(lightGreen, LightGreen())
    t.setColor(lightGreen) 

def setTurtleKoPink(t):
    t.setColorAt(koPink, _KoPink())
    t.setColor(koPink) 

def setTurtleOrange(t):
    t.setColorAt(orange, Orange())
    t.setColor(orange) 
def setTurtleLightOrange(t):
    t.setColorAt(lightOrange, LightOrange())
    t.setColor(lightOrange) 

def setTurtleLightGrey(t):
    t.setColorAt(lightGrey, LightGrey())
    t.setColor(lightGrey) 
def setTurtlePerlGrey(t):
    t.setColorAt(perlGrey, PerlGrey())
    t.setColor(perlGrey) 

def setTurtlePink(t):
    t.setColorAt(pink, Pink())
    t.setColor(pink) 
def setTurtleRed(t):
    t.setColorAt(red, Red())
    t.setColor(red) 
def setTurtleStrand(t):
    t.setColorAt(strand, Strand())
    t.setColor(strand) 

def setTurtlePurple(t):
    t.setColorAt(purple, Purple())
    t.setColor(purple) 
def setTurtleLightPurple(t):
    t.setColorAt(lightPurple, LightPurple())
    t.setColor(lightPurple) 

def setTurtleWhite(t):
    t.setColorAt(white,White())
    t.setColor(white) 
def setTurtleBrokenWhite(t):
    t.setColorAt(brokenWhite, BrokenWhite())
    t.setColor(brokenWhite) 

def setTurtleYellow(t):
    t.setColorAt(yellow,Yellow())
    t.setColor(yellow) 
def setTurtleLightYellow(t):
    t.setColorAt(lightYellow, LightYellow())
    t.setColor(lightYellow) 

class ColorFuncs(Node):
    def __init__(self):
        Node.__init__(self)
        self.add_output( name = 'colorFuncs', 
                         interface = ISequence )

    def __call__( self, inputs ):
        return (setTurtleBrown, setTurtleLightBrown, 
                setTurtleOrange, setTurtleLightOrange, 
                setTurtleYellow, setTurtleLightYellow,
                setTurtleGreen, setTurtleLightGreen,
                setTurtleBlue, setTurtleLightBlue, 
                setTurtlePink, setTurtlePurple, setTurtleLightPurple,
                setTurtleLightGrey, setTurtlePerlGrey, 
                setTurtleBrokenWhite,setTurtleWhite)
    
