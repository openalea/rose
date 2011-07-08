import openalea
import openalea.plantgl.all as pgl
#import sphere
def position(n):
    """ returns the position of the node in a Vector3 data """
    return openalea.plantgl.all.Vector3(n.XX, n.YY, n.ZZ)
    
def VertexVisitor(leaf_factory):
    '''    function to visit MTG nodes
    '''
    # write the node code here.   
    visitor = None; 
    def compute_leaflet(points, turtle):
	""" default function to draw up a leaflet 
             NOTE : without the turtle.push() and turtle.pop(),
	     it hangs the viewer up with a message to the father shell :
	     *** glibc detected *** /usr/bin/python: double free or corruption (out): 0x0000000004bfebd0 ***
	     """
	turtle.push()
        turtle.startPolygon()
        for pt in points[1:]:
            turtle.lineTo(pt)
        turtle.lineTo(points[0])
        turtle.stopPolygon()
	turtle.pop()
    if leaf_factory is None:
        leaf_factory=compute_leaflet
    def visitor(g, v, turtle, leaf_computer=leaf_factory):
        n = g.node(v)
        pt = position(n)
        symbol = n.label[0]
        turtle.setWidth(2.5)
        if symbol in ['E', 'R']:
            #if n.edge_type() == '+' :
            #    turtle.startGC()

            turtle.setId(v)
	    if symbol == "E":
                turtle.setWidth(2.5)
	    elif symbol == "R":                
                turtle.setWidth(0.75)
	    turtle.lineTo(pt)

        elif n.label =='F1':
            turtle.setId(v)
            turtle.incColor()
            points = [position(n.parent()), pt]
            while n.nb_children() == 1:
                n = list(n.children())[0]
                points.append(position(n))
            leaf_computer(points,turtle)
	    
	elif n.label == "B1" :
	    # 4 testing
            turtle.push()
            #turtle.incColor()
            turtle.setColor(4) # apple green
            oldPt=turtle.getPosition()
            rayOfBud=(pt-oldPt)*0.5
            radius = pgl.norm(rayOfBud)*1.1
            geometry= pgl.Translated(rayOfBud, pgl.Sphere(radius))
            #return pgl.Translated(distance, pgl.Sphere(radius))
            #geom = leaf_factory(points)
            turtle.customGeometry(geometry, 1)
            turtle.pop()
	elif n.label == "O1" :
            turtle.push()
            turtle.stopGC()
            turtle.startGC()	    
            turtle.setColor(3) # red
	    turtle.lineTo(pt)
            turtle.setWidth(n.Diameter*.5)   
            turtle.pop()

        elif symbol == "T":
	    if n.label == "T1":
                turtle.lineTo(pt)
                turtle.stopGC()
		turtle.incColor()
                turtle.startGC()
                turtle.setWidth(2.5)

	    if n.label == "T2":
                turtle.lineTo(pt)
                turtle.setWidth(0.01)	    


    # return outputs
    return visitor,
