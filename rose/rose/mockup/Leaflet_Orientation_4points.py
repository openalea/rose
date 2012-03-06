from openalea.plantgl.all import *
from openalea.mtg.aml import MTG
from openalea.mtg.dresser import dressing_data_from_file
from math import sqrt

#def ortho_transfo(vector1,vector2):
#    """ Compute a transfo that transform a Z vector in two vector. """
#    #axes = Vector3.OX, Vector3.OY, Vector3.OZ
#    vector1 = vector1.normed() # returns a plantGL viewer error when vector = 0 ie when length is null
#    vector2 = vector2.normed() 
#    #main_vector = axes[vector.getMaxAbsCoord()]
#    X = vector2 ^ vector1
#    Y = vector1 ^ X
#    return X,Y

def orthoL(A,B,C):
    vector1=B-A
    vector2=C-A
    vector3=dot(vector2,vector1)/(norm(vector1)*norm(vector1))*vector1
    D=vector3+A
    Lgvect=B-A
    lgvect=C-D
    return Lgvect.normed(),lgvect.normed()

def transformation2(geometry, pt_base, pt_top, side,width):
    """ Transform a fixed geometry.
    Using two points and a diameter
    """
    length = norm(pt_top-pt_base)
    scale = (length, width, 1)
    #scale = (1, width, length)
    #scale = (1, width, length)

    translation = pt_base
    X, Y = orthoL(pt_base,pt_top,side)
    #geom_movecenter=Translated((-1,0,0),geometry)
    geom = Scaled(scale, geometry)
    #geomrot=AxisRotated(Vector3(0,1,0),90,geom)
    
    #geom = Oriented(X, Y, geom)
    geom = Oriented(X, Y, geom)
    geom = Translated(translation, geom)
    return geom

def Leaflet_Orientation_4points(mtg, mesh):
    '''    
    '''
    scene = Scene()
    # A correspond  la partie droite de la foliole quand on regarde de la base vers la pointe de la foliole
    geom=mesh
    #geomB=mesh[1]
    #drf_p=dressing_data_from_file(mesh)
    g=mtg
    
    if g=={'index': 0, 'complex': None, 'scale': 0, 'vid': 0, 'label': ''}:
        scene=scene
    else:
        list_s=[]
        # List of stipules id
        x=g.properties()['XX']
        y= g.properties()['YY']
        z= g.properties()['ZZ']
        for i in range(len(g)):
            if g.class_name(i)=='F':
                list_s.append(i)
        for fol in list_s:
            if g.index(fol)=='1':
                base=Vector3(x[g.parent(fol)]/10,y[g.parent(fol)]/10,z[g.parent(fol)]/10)-Vector3(x[1]/10.,y[1]/10.,0.)
                side1=Vector3(x[fol]/10,y[fol]/10,z[fol]/10)-Vector3(x[1]/10.,y[1]/10.,0.)
            elif g.index(fol)=='2':
                top=Vector3(x[fol]/10,y[fol]/10,z[fol]/10)-Vector3(x[1]/10.,y[1]/10.,0.)
            else:
                side2=Vector3(x[fol]/10,y[fol]/10,z[fol]/10)-Vector3(x[1]/10.,y[1]/10.,0.)
                #length=sqrt( (top[0]-base[0])*(top[0]-base[0]) + (top[1]-base[1])*(top[1]-base[1]) + (top[2]-base[2])*(top[2]-base[2]) )
                width=norm(side2-side1)/2. # la division par 2 n'est pas trs prcise
                #symbol=drf_p.symbols[drf_p.classes['R']]
                geomtransfo=transformation2(geom,base,top,side1,width)
                color = (44,195,48)
                geom_shp=Shape(geomtransfo, Material(color),fol)
                scene.add(geom_shp)
                geomtransfo=transformation2(geom,base,top,side2,width)
                geom_shp=Shape(geomtransfo, Material(color),fol)
                scene.add(geom_shp)
    # return outputs
    return scene
