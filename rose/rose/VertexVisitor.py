import openalea
def position(n):
    """ returns the position of the node in a Vector3 data """
    return openalea.plantgl.all.Vector3(n.XX, n.YY, n.ZZ)
    
def VertexVisitor(leaf_factory):
    '''    function to visit MTG nodes
    '''
    # write the node code here.   
    visitor = None; 
    def compute_leaflet(points, turtle):
        turtle.startPolygon()
        for pt in points[1:]:
            turtle.lineTo(pt)
        turtle.lineTo(points[0])
        turtle.stopPolygon()
    if leaf_factory is None:
        leaf_factory=compute_leaflet
    def visitor(g, v, turtle, leaf_computer=leaf_factory):
        n = g.node(v)
        pt = position(n)
        symbol = n.label[0]
        if symbol in ['E', 'R']:
            #if n.edge_type() == '+' :
            #    turtle.startGC()
            turtle.setId(v)
            turtle.lineTo(pt)
        if n.label =='F1':
            turtle.setId(v)
            turtle.incColor()
            points = [position(n.parent()), pt]
            while n.nb_children() == 1:
                n = list(n.children())[0]
                points.append(position(n))
            leaf_computer(points,turtle)

    # return outputs
    return visitor,
