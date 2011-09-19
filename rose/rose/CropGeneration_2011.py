#!/usr/bin/env python
# coding: iso-8859-15 -*-

## Creates a dict of MTG files associated to a list of coordinates 
from openalea.mtg.aml import MTG
import random

def CropGeneration_2011(plantlist={}, existingmtglist=[], excludelist=[], n_x=13, n_y=6, s_x=150, s_y=150, origin=(0, 0, 800), DoFill=True):
    '''    Generates a dictionnary of filenames associated with one or more position and orientation.
    '''
    plant_mtgs = []; 
    # write the node code here.

    def index2coord(ix,iy=None):
        if isinstance (ix,list):
            if len(ix) > 1:
                iy=ix[1]
                ix=ix[0]
            else:
                print "CropGeneration_2011 : bad list of coordinates : %s"%ix
                return(origin)
        if ix < 0 or iy < 0:
            print "CropGeneration_2011 : negative coordinates are not agreed."
        elif ix >= n_x or iy >= n_y :
            print "CropGeneration_2011 : coordinates out of range."
        else:
            return (ix*s_x + origin[0], iy*s_y + origin[1], origin[2])

        return origin
    # end index2coord

    tablelayout = []; 
    dictOfPositions={}
    mtgFiles={}

    # We extract plant numbers from filenames
    # and we build the mtgFiles dict as pairs of {plantNum:fileName}
    for plantFile in existingmtglist:
        plantNum=plantFile.rsplit("/",1)[1]
        mtgFiles[plantNum.rsplit(".",1)[0]]=plantFile

    inv_plantFile=dict((v,k) for k, v in mtgFiles.iteritems())

    #  list of initial positions.
    # It HAS to be completed before we can add up ancillary positions
    for plante in plantlist.keys():
        if plante in mtgFiles.keys() :
            #dictofindices.setdefault(plt,[]).append([int(x),int(y)])
            # we make a dict with file:[3D position, angle]
            dictOfPositions[mtgFiles[plante]] = [[index2coord(plantlist[plante][0]),0.]]

    # DEBUG : return output NOW return dictOfPositions,
    if DoFill :
    # the length of the list of existing MTG files, for further random choice
        randRange=len(existingmtglist)-1
        # list of ancillary positions
        for plante in plantlist.keys():
            if not plante in mtgFiles.keys() :
                if len(excludelist)>0:
                    randPlantNum=excludelist[0]
                    while randPlantNum in excludelist:
                        randPlantNum = random.randint(0,randRange)
                        randPlant = existingmtglist[randPlantNum]
                        # BEWARE of the type returned by the rev. dict inv_plantFile
                        randPlantNum = int(inv_plantFile[randPlant])
                else :
                    randPlant = existingmtglist[random.randint(0,randRange)]
                #randPlant=existingmtglist[randPlantNum]
                #print "randPlant = %s" % randPlant
                # angle aleatoire  parmi -1/4,0, 1/4, 1/2 tour
                randAngle = random.randint(-1, 2) * 0.5 * 3.14159
                dictOfPositions[randPlant] += [[index2coord(plantlist[plante][0]),randAngle]]

    # returns output
    return dictOfPositions,
