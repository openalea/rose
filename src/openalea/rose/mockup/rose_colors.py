#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-
#
# $Id$
#
from openalea.core.external import Node, ISequence 

"""
We define stuff to implement new colors
"""

import openalea.plantgl.all as pgl

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
yellow=14
green=15
blue=16
purple=17
grey=18
white=19

# Next will be useful for organs
button=20
fruit=21
ped=22
petal=23
pink=24
receptacle=25
sepal=26
leaf=27

# others for fun or testing
perlGrey=28
brokenWhite=29
# KO
koPink=30
# Knop
anthocyan=31

def Anthocyan():
    return pgl.Color3(100, 50, 50)
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

# The following colors are hard coding the type of the organ
# TODO : si une des 3 valeurs dépasse 127, y a t-il mise à l'échelle ?
def Button():
    return pgl.Color3(70,130,10) #35,65,5) 
def Fruit():
    return pgl.Color3(255,127,0) 
def Leaf():
    return pgl.Color3(30,60,10) #30,60,10 ; test à 64,128,21
def Ped():
    return pgl.Color3(130,90,30) #65,45,15) 
def Receptacle():
    return pgl.Color3(59,130,36) #25,55,15) 
def Petal():
    return pgl.Color3(255,45,100) # 140,25,55) # 100,50,50
def Sepal():
    return pgl.Color3(65,130,21) #30,60,10)
    
def setTurtleButton(t):
    t.setColorAt(button, Button())
    t.setColor(button) 
def setTurtleFruit(t):
    t.setColorAt(fruit, Fruit())
    t.setColor(fruit) 
def setTurtleLeaf(t):
    t.setColorAt(leaf, Leaf())
    t.setColor(leaf) 
def setTurtlePed(t):
    t.setColorAt(ped, Ped())
    t.setColor(ped) 
def setTurtleReceptacle(t):
    t.setColorAt(receptacle, Receptacle())
    t.setColor(receptacle) 
def setTurtlePetal(t):
    t.setColorAt(petal, Petal())
    t.setColor(petal) 
def setTurtleSepal(t):
    t.setColorAt(sepal, Sepal())
    t.setColor(sepal) 
# end hard code

def setTurtleAnthocyan(t):
    t.setColorAt(anthocyan, Anthocyan())
    t.setColor(anthocyan) 
def setTurtleBlue(t):
    t.setColorAt(blue, Blue())
    t.setColor(blue) 

def setTurtleBrown(t):
    t.setColorAt(brown, Brown())
    t.setColor(brown) 

def setTurtleGreen(t):
    t.setColorAt(green, Green())
    t.setColor(green) 

def setTurtleKoPink(t):
    t.setColorAt(koPink, _KoPink())
    t.setColor(koPink) 


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

def setTurtleWhite(t):
    t.setColorAt(white,White())
    t.setColor(white) 
def setTurtleBrokenWhite(t):
    t.setColorAt(brokenWhite, BrokenWhite())
    t.setColor(brokenWhite) 

def setTurtleYellow(t):
    t.setColorAt(yellow,Yellow())
    t.setColor(yellow) 

class ColorFuncs(Node):
    def __init__(self):
        Node.__init__(self)
        self.add_output( name = 'colorFuncs', 
                         interface = ISequence )

    def __call__( self, inputs ):
        return (setTurtleButton, setTurtleFruit, 
                setTurtlePed, setTurtlePetal, 
                setTurtleReceptacle, setTurtleSepal, 
                setTurtleGreen,
                setTurtleBlue,
                setTurtlePink, setTurtlePurple,
                setTurtlePerlGrey, 
                setTurtleBrokenWhite,setTurtleWhite)
    
