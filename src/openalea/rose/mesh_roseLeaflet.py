from openalea.plantgl.all import*


from math import radians

def mesh_roseLeaflet(x,y):
    '''    
    '''
    # list of points
    ls_ptA=[Vector3(0.,0.,0.)]
    for i in range(len(x)-1):
        ls_ptA.append(Vector3(x[i],y[i]/2,0))
        ls_ptA.append(Vector3(x[i],0,0))
    ls_ptA.append(Vector3(1.,0.,0.))
    # list of index    
    ls_indA=[Index3(0,1,2),Index3(1,3,2),Index3(2,3,4),Index3(3,5,4),Index3(4,5,6),Index3(5,7,6)]
    trianglesetA=TriangleSet(Point3Array(ls_ptA),Index3Array(ls_indA))


    return trianglesetA
