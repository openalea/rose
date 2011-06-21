def computeLeaflet4pts():
    '''    compute leaflet geometry from 4 points
    '''
    computeleaflet4pts = None; 
    # write the node code here.
    def compute_leaf(points, turtle=None):
        '''    compute leaflet geometry from 4 points
        '''
        geometry = None; 
        # write the node code here.
        barycenter = sum(points, pgl.Vector3())/len(points)
        distance = barycenter-points[0]
        radius = pgl.norm(distance)/10.
        geometry= pgl.Translated(distance, pgl.Sphere(radius))
        return pgl.Translated(distance, pgl.Sphere(radius))

    # return outputs
    return computeleaflet4pts,
