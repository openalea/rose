from vplants.plantgl.all import *

def PlantPositionning(scene,plantID,plant_pos):
    '''
    Position a plant according to its coordinates 
    '''
    pos=[]
    plantIDsplit=plantID.partition('-')
    num=int(plantIDsplit[2])
    pos=plant_pos[plantIDsplit[0]][num-1]
    #pos=plant_pos[plantIDsplit[0]]
    out_scene=scene
    # write the node code here.
    if len(scene)!=0:
        for s in xrange(len(scene)):
            #out_scene.add=Shape(Translated(pos,scene[s].geometry),scene[s].appearance)
            out_scene[s].geometry=Translated(pos,scene[s].geometry)
    # return outputs
    return out_scene
