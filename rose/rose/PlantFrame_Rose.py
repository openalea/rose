from openalea.mtg.aml import MTG
from openalea.mtg.dresser import dressing_data_from_file
from openalea.mtg.plantframe import PlantFrame, compute_axes, build_scene
from vplants.plantgl.all import *
from math import radians
import numpy

def transformation1(geometry, pt_base, pt_top, diameter):
    """ Transform a fixed geometry.
    Using two points and a diameter
    """
    length = norm(pt_top-pt_base)
    scale = Vector3(diameter, diameter, length)

    translation = pt_base
    X, Y = ortho_transfo(pt_top-pt_base)

    geom = Scaled(scale, geometry)
    
    geom = Oriented(X, Y, geom)
    geom = Translated(translation, geom)
    return geom
    
def ortho_transfo(vector):
    """ Compute a transfo that transform a Z vector into vector. """
    axes = Vector3.OX, Vector3.OY, Vector3.OZ
    vector = vector.normed() # returns a plantGL viewer error when vector = 0 ie when length is null
    main_vector = axes[vector.getMaxAbsCoord()]
    X = main_vector ^ vector
    Y = vector ^ X
    return X,Y

def PlantFrame_Rose(mtg_file, drf_p):
    ''' 
    Author : C.Pradal, R.Barillot, adapted by J. Bertheloot
    Utility :Compute a plantframe for rose internodes by using a dressing file with predefined geometric symbols.
    '''

    scene=Scene()

    if mtg_file=={'index': 0, 'complex': None, 'scale': 0, 'vid': 0, 'label': ''}:
        scene=scene

    else:
        #gp = mtg_file
        drf_p = dressing_data_from_file(drf_p)
    
    # Basis from each plant
    #trunks = list(gp.vertices(scale=2))
    
    # Input Point Coordinates
        x= mtg_file.properties()['XX']
        y= mtg_file.properties()['YY']
        z= mtg_file.properties()['ZZ']

        #diam = mtg_file.property('TopDiameter')

        def internode_shape(vid):

            # Class name of the vertex
            klass = mtg_file.class_name(vid)

            # Vertex of the parent
            pid = mtg_file.parent(vid) if mtg_file.parent(vid) is not None else mtg_file.complex(vid)

            while pid not in x:
                pid = mtg_file.complex(pid)

            # Bottom and top coordinates of vid

            # Calculated so as to have the base of the plant at x=0, y=0 
            bot = Vector3(x[pid], y[pid], z[pid])-Vector3(x[1],y[1],0.)
            top = Vector3(x[vid], y[vid], z[vid])-Vector3(x[1],y[1],0.)
            #d = diam.get(vid,20)/100.
            d=0.25 if klass=="E" else 0.10

            # Assigns symbols from drf
            symbol = None
            if klass in drf_p.classes:
                symbol = drf_p.symbols[drf_p.classes[klass]]

            geom = transformation1(symbol, bot, top, d)

            color = (0,255,0) if klass == 'R' else (44,195,48)

            return Shape(geom, Material(color),vid)

        # Creates scene
        scene = Scene([internode_shape(vid) for vid in mtg_file.vertices(scale=mtg_file.max_scale()) if mtg_file.class_name(vid) in ['E','R'] ])

    # Add a tag to identify pea shape in final scene
    #for shp in scene:
    #   shp.setName(str(shp.name)+'_P')
    return scene, mtg_file
