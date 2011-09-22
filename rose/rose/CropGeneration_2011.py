## Creates a dict of MTG files associated to a list of coordinates 
from openalea.mtg.aml import MTG
import random
def CropGeneration_2011(plantlist={}, existingmtglist={}, excludelist=[], n_x=13, n_y=6, s_x=150, s_y=150, origin=(0, 0, 800), DoFill=True, DoRotate=True):
    '''    Generates a dictionnary of filenames associated with one or more position and orientation.
    '''
    plant_mtgs = []; 
    # write the node code here.
    def Index2Coord(ix,iy=None):
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
    for plantFile in existingmtglist.keys():
        mtgFiles[int(plantFile.rsplit(".",1)[0])]=existingmtglist[plantFile]

    #  list of initial positions.
    # It HAS to be completed before we can add up ancillary positions
    for plante in plantlist.keys():
        if int(plante) in mtgFiles.keys() :
            # we make a dict with file:[3D position, angle]
            dictOfPositions[mtgFiles[int(plante)]] = [[Index2Coord(plantlist[plante][0]),0.]]
    # if we want to fill up empty places with a random plant num
    if DoFill :
        listOfNums=[]
        # The list of plants whe have data about.
        for clef in  mtgFiles.keys() :
            listOfNums += [clef]
        # there may be plants we do not want to use for filling.
        if len(excludelist) > 0:
            for noClef in excludelist:
                listOfNums.remove(noClef)

        # the length of the list of existing MTG files, for random choice
        randRange=len(listOfNums)-1
        # In the list of plant positions, we look for plants P not in the
        # existingmtglist. If so, we choose a random a replacement plant P'
        # in the existingmtglist, and we append the coordinates of P to the
        # list of coordinates of P'
        # We can process a missing plant with several coordinates
        # so we can use dummy numbers for missing plants
        for plante in plantlist.keys():
            # if we have no data for this plant
            if not int(plante) in mtgFiles.keys() :
                listOfCoords=plantlist[plante]
                for coords in listOfCoords:
                    # get a random index number
                    randPlantNum = random.randint(0,randRange)
                    # get a plant from this index
                    randPlant = listOfNums[randPlantNum]
                    # we give a random rotation by 1/4 of tour 
                    # say : -1/4, 0, 1/4, 1/2 tour
                    if DoRotate :
                        randAngle = random.randint(-1, 2) * 0.5 * 3.14159
                    else :
                        randAngle = 0
                    dictOfPositions[mtgFiles[randPlant]] += [[Index2Coord(coords),randAngle]]
                #print "plante %s <- %s" % (plante, randPlant)

    # returns output
    return dictOfPositions,
