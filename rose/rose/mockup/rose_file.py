#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-
"""
.. module rose_geometry 
.. moduleauthor:: H. Autret <hautret@angers.inra.fr>
"""
# for csv
from openalea.core.external import * 
import openalea.core.logger  as ocl
import csv


def readCsv(fileName, delimiter=','):
    """ we read the csv file, then we return a list of splited lines """
    retList=[]
    fIn=open(fileName,"U")
    if not fIn:
        ocl.error("%s : no such file" %filename ) 
        return retList
    else :
        csvIn=csv.reader(fIn,delimiter=delimiter)
        for ligne in csvIn:
            retList.append(ligne)
        fIn.close()

    return retList
# end readCsv

class ReadCsv(Node):
    def __init__(self):
        Node.__init__(self)
        self.add_input(name= 'fileName', interface = IStr, value=None) 
        self.add_input(name= 'delimiter', interface = IStr, value=",") 
        self.add_output( name = retList, interface = ISequence )

    def __call__( self, inputs ):
        return readCsv

# for scene2can10
import openalea.plantgl.all as pgl
import os
from openalea.core.pkgmanager import PackageManager
from os.path import join

def mesh(geometry):
    #d = pgl.Tesselator()
    #geometry.apply(d)
    #return d.result
    tessel = pgl.Tesselator()
    geometry.apply(tessel)
    mesh_ = tessel.triangulation
    return mesh_

def canline(ind, label,p):
    return "p 2 %s 9 3 %s"%(str(label), ' '.join(str(x) for i in ind for x in p[i]))

def scene2Can01 (maScene, fileName):
    # copied from alinea.topvine
    out = []
    for obj in range (len(maScene)):
        geometry = mesh(maScene[obj])
        label = maScene[obj].geometry.getName()
        label = "007" #maScene[obj].geometry.getName()
        p = geometry.pointList
        index = geometry.indexList
        for ind in index:
            out.append(canline(ind, label,p))

    o = open(fileName, 'w')#stockage dans un fichier can persistant
    o.write("CAN01\n")
    #print "len(out) = %s" % len(out)
    for i in range(len(out)):
        o.write(out[i]+"\n")

    o.close()
    return maScene

class Scene2Can01(Node):
    def __init__(self):
        Node.__init__(self)
        self.add_input(name= 'maScene', interface = None, value=None) 
        self.add_input(name= 'fileName', interface = IStr, value="can01.can") 
        self.add_output( name = 'maScene', interface = None )

    def __call__( self, inputs ):
        return scene2Can01
