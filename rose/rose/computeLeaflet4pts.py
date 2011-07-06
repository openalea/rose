import openalea.plantgl.all as pgl

def computeLeaflet4pts():
    '''    compute leaflet geometry from 4 points
    '''
    compute_leaf = None ; 
    # write the node code here.
    def compute_leaf(points, turtle=None):
        '''    compute leaflet geometry from 4 points
        '''
        geometry = None; 
	
        # example node code here : displays spheres
        barycenter = sum(points, pgl.Vector3())/len(points)
        distance = barycenter-points[0]
        radius = pgl.norm(distance)/10.
        geometry= pgl.Translated(distance, pgl.Sphere(radius))
        turtle.customGeometry(geometry, 1)

    # return outputs
    return compute_leaf,
