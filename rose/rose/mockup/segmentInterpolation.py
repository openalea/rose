#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-


def bySegments(x, Xmin, Xmax, Ymin, Ymax):
    """ computes a value for a function defined by segments :
    Xmin, Xmax, Ymin, Ymax.

    Pre conditions :

      - Xmin < Xmax

    Post conditions:
      - x < Xmin : return Ymin
      - x > Xmax : return Ymax
      - else :
      - K= (Ymax-Ymin) / (Xmax - Xmin)
      - return Ymin + K * (x-Xmin)

    :param x: the x value 
    :param Xmin: the low value of the x range
    :param Xmax: the high value of the x range
    :param Ymin: the low value of the y range
    :param Ymax: the high value of the y range
    :return: the interpolated y value
    """
    #print "Xmin, Xmax, Ymin, Ymax = %f, %f, %f, %f" %(Xmin, Xmax, Ymin, Ymax)
    if (Xmax <= Xmin) or (Ymin == Ymax):
        raise ValueError
    if x <= Xmin:
        return Ymin
    elif x >= Xmax:
        return Ymax
    K=  (Ymax - Ymin) / float(Xmax - Xmin)
    return Ymin + K * (x-Xmin)

def invBySegments(y, Xmin, Xmax, Ymin, Ymax): 
    """ computes the reverse function of bySegments :
    preconditions : Ymin != Ymax
     
    :param y: the y value 
    :param Xmin: the low value of the x range
    :param Xmax: the high value of the x range
    :param Ymin: the low value of the y range
    :param Ymax: the high value of the y range
    :return: the  interpolated x value
    :warning: we only process positive slopes.
"""
    if Ymin == Ymax:
        raise ValueError
    if y < Ymin :
        return Xmin
    elif y > Ymax:
        return Xmax
    K=(Xmax - Xmin)/float(Ymax-Ymin)
    return Xmin + K * (y-Ymin)


def checkIfIn (left,right, value):
    """ 
    Ensure that "value" meets the following conditions :

    - if left <= right : 
        - value will be inside [left - right]
    - else : 
        - value will be outside ]right - left[ 

   :param left: a limit that is allowed to be lower than "value"
   :param right: a limit that is allowed to be higher than "value"
   :param value: the value to be checked
   :return: either "value" if it passes the test, or left, or right, depending wether is closest to "value"
   :note: the result is assigned a forced value when calling checkIfIn (guard,guard, value)
   """
    if left <= right: # we want to include
        if value < left:
            value=left
        elif value > right:
            value=right
    else: # we want to exclude
        if value < (left+right)/2.: # is value lower than the mean of the interval ?
            if value > right:       # is value inside the interval ?
                value = right       # if so : value is set to the lower border  
        elif value < left :         # else : is value inside the interval ?
            value = left            # if so : value is set to the higher border
    #print "value=%s" % value
    return value


def test():
    minX=1
    maxX=10
    minY=12
    maxY=14

    factor=100

    if minX <  maxX:
      thisX = minX
      thatX = maxX
    else:
      thisX = maxX
      thatX = minX

    #direct
    for x in range(int(thisX*factor),int(thatX*factor)):
      y=x/float(factor)
      print "%f %f" % (y,bySegments(y,minX, maxX, minY,maxY))
    print

    #inverse
    for x in range(int(maxY*factor),int(minY*factor),-1):
      y=x/float(factor)
      print "%f %f" % (y,invBySegments(y,minX, maxX, minY, maxY))

    print
    # reciprocity
    for x in range(int(thisX*factor),int(thatX*factor)):
      y=x/float(factor)
      print "%f %f" % (y,invBySegments(bySegments(y,minX, maxX, minY,maxY),minX, maxX, minY,maxY))

# e.g. inside gnuplot (plot "< bySegments.py" w l)
if __name__ == "__main__":
    test()
