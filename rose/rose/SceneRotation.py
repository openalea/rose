from vplants.plantgl.all import *
from math import radians

def SceneRotation(scene):
    '''    
    Rotate from 180 degrees a complete scene
    '''
    # write the node code here.
    if len(scene)!=0:
        for i in range(len(scene)):
            sc=scene[i].geometry
            v=Vector3(1,0,0)
            sc_rot=AxisRotated(v,3.14,sc)
            ##sc_rot2=AxisRotated(Vector3(0,0,1),radians(288.0),sc_rot)
            scene[i].geometry=sc_rot

    # return outputs
    return scene
