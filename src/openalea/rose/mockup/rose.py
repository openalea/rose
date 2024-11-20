#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-
#
# $Id$
#
"""
.. module:: rose
   :platform: Unix, Windows
   :synopsis: A useful module indeed.

.. moduleauthor:: Andrew Carter <andrew@invalid.com>
"""

from openalea.mtg.aml import MTG
import numpy as np
import random
import re
import urllib.request, urllib.parse, urllib.error

from openalea.mtg.algo import union

from openalea.core.external import Node, IBool, IData, IDict, ISequence, IStr, ITuple3# *
#from openalea.core.logger  import logger


def cropGeneration_2011(plantlist={}, existingmtglist={}, excludelist=[], gridDef=[], origin=(0, 0, 800), DoFill=True, DoRotate=True):
    '''   :brief: Generates a dictionnary of filenames associated with one or more position and orientation.
    :param plantlist: 'the dispatching grid of the plant numbers on the table'
    :param existingmtglist: 'the dictionnary of the existing pairs <plant_number:filename>'
    :param excludelist: 'a list of plants not to use for filling (if any)'
    :param gridDef: 'the dimensions of the grid used for this experiment : nX, nY, sizeX, sizeY'
    :param origin: 'the 3D global coordinates of the local 0,0,0 position within the grid'
    :param DoFill: 'Should we fill empty places with existing data ?'
    :param DoRotate: 'Should or should we not rotate the plants used for filling'
    '''
    #plant_mtgs = []; 
    if gridDef :
        n_x = int(gridDef[0])
        n_y = int(gridDef[1])
        s_x = float(gridDef[2])
        s_y = float(gridDef[3])
    else:
        n_x=13
        n_y=6
        s_x=150.
        s_y=150.
        
    def Index2Coord(ix,iy=None):
        if isinstance (ix,list):
            if len(ix) > 1:
                iy=ix[1]
                ix=ix[0]
            else:
                print("cropGeneration_2011 : bad list of coordinates : %s"%ix)
                return(origin)
        if ix < 0 or iy < 0:
            print("cropGeneration_2011 : negative coordinates are not agreed.")
        elif ix > n_x or iy > n_y :
            print("cropGeneration_2011 : coordinates out of range.")
        else:
            return (ix*s_x + origin[0], iy*s_y + origin[1], origin[2])

        return origin
    # end index2coord

    # DEBUG
    #print "plantlist : %s" % plantlist
    print("len (plantlist) : %d" % len(plantlist)) 
    #tablelayout = []; 
    dictOfPositions={}
    mtgFiles={}

    # We extract plant numbers from filenames
    # and we build the mtgFiles dict as pairs of {plantNum:fileName}
    for plantFile in list(existingmtglist.keys()):
        mtgFiles[int(plantFile.rsplit(".",1)[0])]=existingmtglist[plantFile]

    #  list of initial positions.
    # It HAS to be completed before we can add up ancillary positions
    for plante in list(plantlist.keys()):
        if int(plante) in list(mtgFiles.keys()) :
            # we make a dict with file:[3D position, angle]
            dictOfPositions[mtgFiles[int(plante)]] = [[Index2Coord(plantlist[plante][0]),0.]]
    # if we want to fill up empty places with a random plant num
    if DoFill :
        listOfNums=[]
        # The list of plants whe have data about.
        for clef in  list(mtgFiles.keys()) :
            listOfNums += [clef]
        # there may be plants we do not want to use for filling.
        for noClef in excludelist:
            listOfNums.remove(noClef)

        # the length of the list of existing MTG files, for random choice
        randRange=len(listOfNums)-1
        # In the list of plant positions, we look for plants P not in the
        # existingmtglist. If so, we choose a random a replacement plant P'
        # in the existingmtglist, and we append the coordinates of P to the
        # list of coordinates of P'
        # We can process a missing plant with several coordinates
        # so we may have used dummy numbers for missing plants
        for plante in list(plantlist.keys()):
            # if we have no data for this plant
            if not int(plante) in list(mtgFiles.keys()) :
                listOfCoords=plantlist[plante]
                for coords in listOfCoords:
                    # get a random index number
                    randPlantNum = random.randint(0,randRange)
                    # get a plant from this index
                    randPlant = listOfNums[randPlantNum]
                    # we give a random rotation 
                    if DoRotate == True :
                        # random angle in one tour
                        randAngle = random.uniform(-1,1) * np.pi
                    else :
                        randAngle = 0

                    if mtgFiles[randPlant] in list(dictOfPositions.keys()):
                        dictOfPositions[mtgFiles[randPlant]] += [[Index2Coord(coords),randAngle]]
                    else:
                        # If extra MTGs are found in the directory, we may use them
                        dictOfPositions[mtgFiles[randPlant]] = [[Index2Coord(coords),randAngle]]

    # returns output
    return dictOfPositions,
# end cropGeneration_2011

###################################### ALEA WRAPPER
class CropGeneration_2011(Node):
    """ Yields the cropGeneration_2011(...) function  """
    def __init__(self):
        Node.__init__(self)
        self.add_input( name = 'plantlist',
                        interface = IDict)
        self.add_input( name = 'existingmtglist',
                        interface = IDict)
        self.add_input( name = 'excludelist',
                        interface = ISequence )
        self.add_input( name = 'gridDef',
                        interface = ISequence)
        self.add_input( name = 'origin',
                        interface =  ITuple3)
        self.add_input( name = 'DoFill',
                        interface = IBool )
        self.add_input( name = 'DoRotate',
                        interface = IBool)
        self.add_output(name='dictOfPositions', 
                        interface=IDict)
        #self.add_input( name = '',
        #interface = )
    def __call__( self, inputs ):
        plantlist= self.get_input( 'plantlist' )
        existingmtglist= self.get_input( 'existingmtglist' )
        excludelist= self.get_input( 'excludelist' )
        gridDef= self.get_input( 'gridDef' )
        origin= self.get_input( 'origin' )
        DoFill= self.get_input( 'DoFill' )
        DoRotate= self.get_input( 'DoRotate' )
        return cropGeneration_2011(plantlist, existingmtglist, excludelist, \
                                  gridDef, origin, DoFill, DoRotate)
# end CropGeneration_2011 (cropGeneration_2011 wrapper)

#################################################################
def files2MTGs(cropdict):
    '''  
    :brief: Creates a list of MTG object from a dict of {MTG files:list of coordinates} pairs.
    The procedure reads the MTG files, then places them both onto their coordinates, 
    Then it uses the files again to fill up empty spaces, with a random rotation angle.
    :param cropdict : a dictionary built with 
    - MTG files names as keys,
    - shift of the real plant as 1st value for each key
    - shift and rotation as further values, if any
    :return: a list of MTG objects that were build from the dict
    '''
    listofmtgs = []; 
    
    def BaseOfPlant(nodeOfMTG):
        """ returns the coordinates of the anchorage of the plant in the XY plane"""
        return (nodeOfMTG.XX, nodeOfMTG.YY)

    def PositionIt(noeud, orx, ory, rotc, rots, shiftx, shifty, shiftz):
        """ positions the node "noeud"
        the node gets
        - moved to the origin point as (orx, ory)
        - rotated around this point by the values (rot cos, rot sin) 
        - moved along the "shift" vector
        :param noeud: the MTG node
        :param orx: origin.x
        :param ory: origin.y
        :param rotc: cosine of the rotation angle
        :param rots: sine of the rotation angle
        :param shiftx: the x displacement to apply onto "noeud"
        :param shifty: the y displacement to apply onto "noeud"
        :param shiftz: the z displacement to apply onto "noeud"

        Note : the parameters are scalars rather than structures in order to speed up the process.
        """
        x0=noeud.XX - orx
        y0=noeud.YY - ory
        x1 = x0*rotc - y0*rots
        y1 = y0*rotc + x0*rots
        noeud.XX = x1 + shiftx
        noeud.YY = y1 + shifty
        noeud.ZZ += shiftz

    # creates output list (to be improved with rotates and shifts)
    for plante in list(cropdict.keys()):

        for shiftRot in cropdict[plante]:
            
            # get prepared for rotations
            shift=shiftRot[0]
            sx=shift[0]
            sy=shift[1]
            sz=shift[2]

            angle=shiftRot[1]
            #angle= 1. # DBG 1 rad.
            (rc,rs)=(np.cos(angle), np.sin(angle))

            # load the MTG
            mtg=MTG(plante)

            noeud = mtg.node(1)      # the anchorage of the plant
            (ox,oy)= BaseOfPlant(noeud)
            
            PositionIt(noeud, ox, oy, rc, rs, sx, sy, sz )
            for vtx in mtg.vertices(scale=2): # the rest of the plant
                noeud = mtg.node(vtx)
                PositionIt(noeud, ox, oy, rc, rs, sx, sy, sz )

            listofmtgs += [mtg]

    # return outputs
    return listofmtgs,
# end files2MTGs

class Files2MTGs(Node):
    def __init__(self):
        Node.__init__(self)
        self.add_input( name = 'cropdict', 
                        interface = IDict )
        self.add_output( name = 'listofmtgs', 
                         interface = ISequence )

    def __call__( self, inputs ):
        cropdict= self.get_input( 'cropdict' )
        return files2MTGs(cropdict)
# end class Files2MTGs  (files2MTGs wrapper)

    #################################################################
def files2MTGs4CAN2(cropdict):
    '''  
    :brief: Creates a list of MTG object from a dict of {MTG files:list of coordinates} pairs.
    The procedure reads the MTG files, then places them both onto their coordinates, 
    Then it uses the files again to fill up empty spaces, with a random rotation angle.
    :param cropdict : a dictionary built with 
    - MTG files names as keys,
    - shift of the real plant as 1st value for each key
    - shift and rotation as further values, if any
    :return: a list of MTG objects that were build from the dict
    '''
    listofmtgs = []; 

    import os # path.(base|dir)name
    
    def BaseOfPlant(nodeOfMTG):
        """ returns the coordinates of the anchorage of the plant in the XY plane"""
        return (nodeOfMTG.XX, nodeOfMTG.YY)

    def PositionIt(noeud, orx, ory, rotc, rots, shiftx, shifty, shiftz):
        """ positions the node "noeud"
        the node gets
        - moved to the origin point as (orx, ory)
        - rotated around this point by the values (rot cos, rot sin) 
        - moved along the "shift" vector
        :param noeud: the MTG node
        :param orx: origin.x
        :param ory: origin.y
        :param rotc: cosine of the rotation angle
        :param rots: sine of the rotation angle
        :param shiftx: the x displacement to apply onto "noeud"
        :param shifty: the y displacement to apply onto "noeud"
        :param shiftz: the z displacement to apply onto "noeud"

        Note : the parameters are scalars rather than structures in order to speed up the process.
        """
        x0=noeud.XX - orx
        y0=noeud.YY - ory
        x1 = x0*rotc - y0*rots
        y1 = y0*rotc + x0*rots
        noeud.XX = x1 + shiftx
        noeud.YY = y1 + shifty
        noeud.ZZ += shiftz

    # creates output list (to be improved with rotates and shifts)
    for plante in list(cropdict.keys()):

        index=0 # the 1st occurence is the plant we're interested in
        for shiftRot in cropdict[plante]:
            
            # get prepared for rotations
            shift=shiftRot[0]
            sx=shift[0]
            sy=shift[1]
            sz=shift[2]

            angle=shiftRot[1]
            #angle= 1. # DBG 1 rad.
            (rc,rs)=(np.cos(angle), np.sin(angle))

            # load the MTG
            mtg=MTG(plante)

            noeud = mtg.node(1)      # the anchorage of the plant
            (ox,oy)= BaseOfPlant(noeud)
            
            PositionIt(noeud, ox, oy, rc, rs, sx, sy, sz )
            for vtx in mtg.vertices(scale=2): # the rest of the plant
                noeud = mtg.node(vtx)
                PositionIt(noeud, ox, oy, rc, rs, sx, sy, sz )

            # the path to the can file
            mtg.properties()['dirName']=str(os.path.dirname(plante))

            # we mark up filling plants by giving them a number higher then 2000:
            # the plant number gets increased by 2000 * repetition_number
            # (the numbering was always lower than 2000 in the 2011 experiments)

            nom=os.path.basename(plante).split('.')[0].split('-')[0].split("_")[-1]
            plantNum=int(re.sub("[^0-9]*([0-9]+)$","\\1",nom))
            if index > 0 :
                plantNum += 2000*index
            mtg.properties()['plantNum']=plantNum
            
            listofmtgs += [mtg]
            index += 1 # Is there more than one repetition of this plant ?

    # return outputs
    return listofmtgs,
# end files2MTGs4CAN2

class Files2MTGs4CAN2(Node):
    def __init__(self):
        Node.__init__(self)
        self.add_input( name = 'cropdict', 
                        interface = IDict )
        self.add_output( name = 'listofmtgs', 
                         interface = ISequence )

    def __call__( self, inputs ):
        cropdict= self.get_input( 'cropdict' )
        return files2MTGs4CAN2(cropdict)
# end Files2MTGs4CAN2 (files2MTGs4CAN2 wrapper)

#################################################################
def getMTG(dirname, IDplant):
    '''    generates a complete path to a file.
    the argument is in the form of "NUM[-N]", which means that
    we want to create an MTG object fom the NUM.mtg file.
    To achieve that, the filename is splitted against the"-" (dash) separator
    and the string ".mtg" is concatenated to it.
   
    '''
    if dirname is None:
        dirname = "."
    IDplantsplit=IDplant.partition('-')
    plant=IDplantsplit[0]
    mtg_file="%s/%s.mtg" % (dirname,plant)
    mtg=MTG(mtg_file)
    # return outputs
    return mtg
# end getMTG

class GetMTG(Node):
    def __init__(self):
        Node.__init__(self)
        self.add_input( name = 'dirname',
                        interface=IStr)
        self.add_input( name = 'IDplant',
                        interface=IStr)
        self.add_output(name = 'mtg',
                        interface=IData)

    def __call__( self, inputs ):
        dirname= self.get_input( 'dirname' )
        IDplant= self.get_input( 'IDplant' )
        return getMTG(dirname,IDplant)
# end GetMTG  (getMTG wrapper)

#################################################################
def getOrigin(originFilename):
    ''' reads the 3D coordinates of the 1st plant (i.e the one 
    in the [0,0] position) from a file '''
    import csv
    origin=None
    origin_file = open(originFilename, 'r')
    originCsv = csv.reader(origin_file,delimiter=',')
    header=next(originCsv)
    if header == ['x','y','z']:
        origin = [ float(item) for item in next(originCsv)]
    return origin

class GetOrigin(Node):
    def __init__(self):
        Node.__init__(self)
        self.add_input( name = 'originFilename',
                        interface=IStr)
        self.add_output(name = 'originCoordinates',
                        interface=ISequence)

    def __call__( self, inputs ):
        originFilename= self.get_input( 'originFilename' )
        return getOrigin(originFilename)
#end GetOrigin

#################################################################
def getGrid(gridfilename):
    '''    Makes a dictionnary from file that contains plants indexes inside a 2D grid.
    '''
    dictofindices = None; 

    def getGridSpecs(coords_file):
        """ we read the 1st line of the file and return it as a list """
        ligne = coords_file.readline()
        ligne=ligne.split('\n')
        ligne=ligne[0].split('\t')
        return ligne
        
    # Create a dictionnary whose keys are plants ID and values are lists of plant positions
    # From J. Berhteloot's CropGeneration
    coords_file = open(gridfilename, 'r')
    dictofindices={}
    gridSpecs = getGridSpecs(coords_file)
    for line in coords_file:
        plt=line.split()[0]
        x,y=line.split()[1:]
        dictofindices.setdefault(plt,[]).append([int(x),int(y)])
    coords_file.close()

    # return outputs
    return dictofindices, gridSpecs

class GetGrid(Node):
    def __init__(self):
        Node.__init__(self)
        self.add_input( name = 'gridFileName',
                        interface=IStr)
        self.add_output(name = 'dictOfPlantNums',
                        interface=IDict)
        self.add_output(name = 'gridSpecs',
                        interface=ISequence)

    def __call__( self, inputs ):
        gridFileName= self.get_input( 'gridFileName' )
        (dico, liste)=getGrid(gridFileName)
        return (dico, liste)
#end GrifFile2dict

#################################################################
def httpDir2DictOfFiles(url, filtre='.mtg') :
    # downloads files from a web server in temp. files, then return the dictionnary that associates temp files and filenames.
    dictoffiles = {}
    listoffiles=[]
    htmlfile=""
    
    (htmlFileName, h) = urllib.request.urlretrieve ( url +"/", None, urllib.reporthook)
    htmlfile=open(htmlFileName,"r")
    htmlfileContent=htmlfile.read()
    htmlfileContent = htmlfileContent.split("\n")
    for ligne in htmlfileContent:
        #print "ligne= %s" % ligne
        if re.search (filtre, ligne):
            filename=re.sub("<li><a href=\"","",ligne)
            filename=re.sub("\">.*</a></li>$","", filename)
            #print "(filtre, ligne) = (%s,%s)" % (filtre, ligne)
            listoffiles += [filename]
    htmlfile.close()
    for fichier in listoffiles:
        #url=urllib.URLopener(open_http)

        #objet=url.open_file(webserver +"/"+ fichier)

        fn, h = urllib.request.urlretrieve(url +"/"+ fichier, None, urllib.reporthook)
        #print "(fn,h) =  (%s, %s)" % (fn,h)
        dictoffiles[fichier] = fn
        
    # return outputs
    return dictoffiles,
#end httpDir2DictOfFiles

class HttpDir2DictOfFiles(Node):
    def __init__(self):
        Node.__init__(self)
        self.add_input( name = 'url',
                        interface=IStr)
        self.add_input( name = 'filtre',
                        interface=IStr)
        self.add_output(name = 'dictoffiles',
                        interface=IData)

    def __call__( self, inputs ):
        url = self.get_input( 'url' )
        filtre= self.get_input( 'filtre' )
        return httpDir2DictOfFiles(url, filtre)
#end HttpDir2DictOfFiles (httpDir2DictOfFiles wrapper)

#################################################################
def localDir2DictOfFiles(listoffiles):
    '''    makes a dict of names: complete_path from a dirname and a name filter
    '''
    dictoffiles = {} ; 
    # downloads files from a web server in temp. files, then return the dictionnary that associates temp files and filenames.
    from os import path as oPath
    for fichier in listoffiles:
        
        dictoffiles[oPath.basename(fichier)] = fichier

    # return outputs
    return dictoffiles,

class LocalDir2DictOfFiles(Node):
    def __init__(self):
        Node.__init__(self)
        self.add_input( name = 'listoffiles',
                        interface=IStr)
        self.add_output(name = 'dictoffiles',
                        interface=IData)

    def __call__( self, inputs ):
        listoffiles= self.get_input( 'listoffiles' )
        return localDir2DictOfFiles(listoffiles)
# end LocalDir2DictOfFiles

#################################################################
def mTG_union(mtgsin):
    '''    make the union of MTGs
    '''
    mtgout = None; 

    # print "len(mtgsin)=%d" % len(mtgsin)
    if isinstance (mtgsin, list):
        if len(mtgsin) >= 2 :
            mtgout = union(mtgsin[0],mtgsin[1])
            for MtgIn in mtgsin[2:]:
                mtgout = union(mtgout,MtgIn)
        else:
            mtgout = mtgsin[0]
    else : # we take the a risk to return something not being an MTG
        mtgout = mtgsin

    # return outputs
    return mtgout,
# end mTG_union

class MTG_union(Node):
    def __init__(self):
        Node.__init__(self)
        self.add_input( name = 'mtgsin',
                        interface=ISequence)
        self.add_output(name = 'mtgout',
                        interface=IData)

    def __call__( self, inputs ):
        mtgsin= self.get_input( 'mtgsin' )
        return mTG_union(mtgsin)
#end MTG_union  (mTG_union wrapper)

