import openalea
import openalea.plantgl.all as pgl
#import sphere
def position(n):
    """ returns the position of the node in a Vector3 data """
    return openalea.plantgl.all.Vector3(n.XX, n.YY, n.ZZ)
    
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

def VertexVisitor(leaf_factory=None):
    '''    function to visit MTG nodes
    '''
    # write the node code here.   
    visitor = None; 


    if leaf_factory is None:
        leaf_factory=compute_leaflet

    def visitor(g, v, turtle, leaf_computer=leaf_factory):
        n = g.node(v)
        pt = position(n)
        symbol = n.label[0]
        turtle.setId(v)

        if symbol in ['E', 'R']:
            if n.Diameter is None:
                print 'ERROR: vertex %d (name: %s, line around %d)'%(v,n.label,n._line)
                n.Diameter = 0.75

            if n.edge_type() == '+'  or not n.parent():
                turtle.setWidth(n.Diameter / 2.)
                #pass

            turtle.oLineTo(pt)
            turtle.setWidth(n.Diameter / 2.)

        elif n.label in [ 'F1', 'S1' ]:
            if symbol == 'F':
                turtle.incColor()
            else :
                turtle.setColor(4)
            
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
            radiusOfBud=(pt-oldPt)*0.5
            radius = pgl.norm(radiusOfBud)*1.1
            geometry= pgl.Translated(radiusOfBud, pgl.Sphere(radius))
            #return pgl.Translated(distance, pgl.Sphere(radius))
            #geom = leaf_factory(points)
            turtle.customGeometry(geometry, 1)
            turtle.pop()
        elif n.label == "O1" :
            turtle.push()
            turtle.stopGC()
            turtle.startGC()	    
            turtle.setColor(3) # red
            # CPL
            turtle.setWidth(n.parent().Diameter*.5)   
            turtle.lineTo(pt)
            turtle.setWidth(n.Diameter*.5)   
            turtle.pop()

        elif symbol == "T":
            if n.label == "T1":
                turtle.stopGC()
                turtle.incColor()
                turtle.startGC()
                turtle.move(pt)

#X                 oldPt=turtle.getPosition()
#X                 radiusOfBud=(pt-oldPt)*0.5
#X                 turtle.oLineTo(oldPt+radiusOfBud)
#X                 turtle.stopGC()
#X                 turtle.incColor()
#X                 turtle.startGC()
#X                 #turtle.setWidth(2.5)
                #turtle.setWidth(n.parent().Diameter/2.)

            if n.label == "T2":
                turtle.lineTo(pt)
                turtle.setWidth(0.01)	    
                turtle.decColor()


    # return outputs
    return visitor,
