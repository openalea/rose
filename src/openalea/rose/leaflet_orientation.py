from openalea.mtg.aml import *
from math import cos,sin,radians,atan
from openalea.mtg.aml import MTG
from openalea.mtg.plantframe.dresser import dressing_data_from_file
import random
from openalea.plantgl.all import *
import time
import os
import re



def Opening(note):
    op=0
    if note==1.0:
        op=180
    elif note==0.9:
        op=40
    elif note==0.8:
        op=90
    elif note==0.7:
        op=40
    else:
        op=0
    return op

#def CoordToAngle(a,b):
  #  if a>0. and b>=0.:
   #     theta=atan(b/a)
    #elif a>0. and b<0.:
     #   theta=atan(b/a)+2*3.1416
    #elif a<0.:
     #   theta=atan(b/a)+3.1416
    #elif a==0. and b>=0.:
     #   theta=3.1416/2
    #elif a==0. and b<0.:
     #   theta=3*3.1416/2
    #return theta

def CoordToAngle(a,b):
    theta=0.
    if a>0. :
        theta=atan(b/a)
    elif a<0. and b>=0.:
        theta=atan(b/a)+3.1416
    elif a<0. and b<0.:
        theta=atan(b/a)-3.1416
    elif a==0. and b>=0.:
        theta=3.1416/2
    elif a==0. and b<0.:
        theta=-3.1416/2
    return theta

def Conv2Euler(vect):
    aa=CoordToAngle(vect[0],vect[1])+3.1416
    if vect[2]<0:
        coef=-1
    else:
        coef=1
    vecttp=(vect[0],vect[1])
    if abs(vecttp[0])>abs(vecttp[1]):
        ang=CoordToAngle(vect[0],vect[2])
        if vect[0]<0:
            bb=coef*(3.1416+ang)
        else:
            bb=ang
    else:
        ang=CoordToAngle(vect[1],vect[2])
        if vect[1]<0.:
            bb=coef*(3.1416+ang)
        else:
            bb=ang
    return Vector3(aa,bb,0.)

def leaflet_orientation(mtg,geom_file,mesh):
    '''
    Author: J.Bertheloot - 2010    
    '''
    g=mtg
    if mesh==None:
        scene_phyto = Scene(geom_file)
        geom = scene_phyto[0].geometry
        geom.radius=0.5
    else:
        geom=mesh

    scene=Scene()

    if g=={'index': 0, 'complex': None, 'scale': 0, 'vid': 0, 'label': ''}:
        scene=scene
    else:
        list_s=[]
        # List of stipules id
        for i in range(len(g)):
            if g.class_name(i)=='F':
                list_s.append(i)
        if len(list_s)>0:
            # Transforms stipule geoms according to mtg
            for fol in list_s:
                # Scaling
                length = float(g.property('Length')[fol])/10.0
                if mesh==None:
                    geom_movecenter=Translated((-0.5,0,0),geom)
                else:
                    geom_movecenter=Translated((-1,0,0),geom)
                geom_scal = Scaled((length,length*0.30,1),geom_movecenter)

                # Rotation according to Euler angles according to the opening degree of the leaflet
                opening_note=g.property('Ouverture')[fol]
                opening=Opening(opening_note)
                #print opening
                #opening=radians(90)

                if g.property('AA')=={}:
                    ##rot=g.property('Rotation')[1]
                    topRachisID=g.parent(fol)
                    baseRachisID=g.parent(topRachisID)
                    if g.nb_children(topRachisID)>1:
                        for i in g.children(topRachisID):
                            baseRachisID=i
                    topRachis=Vector3(g.property('XX')[topRachisID],g.property('YY')[topRachisID],g.property('ZZ')[topRachisID])
                    baseRachis=Vector3(g.property('XX')[baseRachisID],g.property('YY')[baseRachisID],g.property('ZZ')[baseRachisID])
                    vector=topRachis-baseRachis
                    vector=vector.normed()
                    ortho=Vector3(0,0,1)^vector
                    #print ortho, Conv2Euler(ortho)*180/3.1416
                    #print geom_scal.scale
                    #print vector[1]
                
                    if int(g.property('FolID')[fol])!=1:
                        if int((g.property('FolID')[fol]-int(g.property('FolID')[fol]))*10)==1:
                            #print "1" 
                            #print ortho,vector
                            #geom_eulrot1 = EulerRotated(Conv2Euler(ortho)[0]+3.1416,Conv2Euler(ortho)[1],Conv2Euler(ortho)[2]-3.14/2+radians(opening)/2, geom_scal)
                            #geom_eulrot2 = EulerRotated(Conv2Euler(ortho)[0]+3.1416,Conv2Euler(ortho)[1],Conv2Euler(ortho)[2]-3.14/2-radians(opening)/2, geom_scal)
                            geom_eulrot1 = EulerRotated(Conv2Euler(ortho)[0],0.,0.-3.14/2+radians(opening)/2, geom_scal)
                            geom_eulrot2 = EulerRotated(Conv2Euler(ortho)[0],0.,0.-3.14/2-radians(opening)/2, geom_scal)
                        else:
                            #print "2"
                            #ortho2=Vector3(-ortho[0],-ortho[1],0.)
                            #print ortho2,vector
                            #geom_eulrot1 = EulerRotated(Conv2Euler(ortho)[0]+3.1416*2,Conv2Euler(ortho)[1],Conv2Euler(ortho)[2]-3.14/2+radians(opening)/2, geom_scal)
                            #geom_eulrot2 = EulerRotated(Conv2Euler(ortho)[0]+3.1416*2,Conv2Euler(ortho)[1],Conv2Euler(ortho)[2]-3.14/2-radians(opening)/2, geom_scal)
                            geom_eulrot1 = EulerRotated(Conv2Euler(ortho)[0]+3.1416,0.,0.-3.14/2+radians(opening)/2, geom_scal)
                            geom_eulrot2 = EulerRotated(Conv2Euler(ortho)[0]+3.1416,0.,0.-3.14/2-radians(opening)/2, geom_scal)
                    else:
                        #print "a",Conv2Euler(vector)*180/3.1416
                        geom_eulrot1 = EulerRotated(Conv2Euler(vector)[0],Conv2Euler(vector)[1],0.-3.14/2+radians(opening)/2, geom_scal)
                        geom_eulrot2 = EulerRotated(Conv2Euler(vector)[0],Conv2Euler(vector)[1],0.-3.14/2-radians(opening)/2, geom_scal)
                else:
                    geom_eulrot1 = EulerRotated(radians(int(g.property('AA')[fol])), radians(int(g.property('BB')[fol])),radians(int(g.property('CC')[fol]))-3.14/2+radians(opening)/2, geom_scal)
                    geom_eulrot2 = EulerRotated(radians(int(g.property('AA')[fol])), radians(int(g.property('BB')[fol])),radians(int(g.property('CC')[fol]))-3.14/2-radians(opening)/2, geom_scal)
                    #print geom_scal.scale
        
                # Translation so as to have the base of the plant at x=0, y=0
                pid=g.parent(fol)
                x=g.property('XX')[pid]
                x0=g.property('XX')[1]
                y=g.property('YY')[pid]
                y0=g.property('YY')[1]
                z=g.property('ZZ')[pid]
                trans = Vector3(x,y,z)-Vector3(x0,y0,0)
                geom_trans1 = Translated(trans, geom_eulrot1)
                geom_trans2 = Translated(trans, geom_eulrot2)

                # Identification
                col = Material(Color3(44,195,48))# peut etre ameliore ac une texture
                geom_shp1 = Shape (geom_trans1,col,fol)
                geom_shp2 = Shape (geom_trans2,col,fol)
        
                # Creates scene
                scene.add(geom_shp1)
                scene.add(geom_shp2)
            
    return scene
