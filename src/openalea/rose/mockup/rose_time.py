#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# $Id$
#

import re


def bySegments(x, Xmin, Xmax, Ymin, Ymax):
    # cloud be placed somewhere else, but used only here, so it remains here.
    """computes a value for a function defined by segments :
    Xmin, Xmax, Ymin, Ymax.

    Pre-conditions :

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
    if (Xmax <= Xmin) or (Ymin == Ymax):
        raise ValueError
    if x <= Xmin:
        return Ymin
    elif x >= Xmax:
        return Ymax
    K = (Ymax - Ymin) / float(Xmax - Xmin)
    return Ymin + K * (x - Xmin)


def invBySegments(y, Xmin, Xmax, Ymin, Ymax):
    # cloud be placed somewhere else, but used only here, so it remains here.
    """computes the reverse function of bySegments :
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
    if y < Ymin:
        return Xmin
    elif y > Ymax:
        return Xmax
    K = (Xmax - Xmin) / float(Ymax - Ymin)
    return Xmin + K * (y - Ymin)


def checkIfIn(left, right, value):
    # cloud be placed somewhere else, but used only here, so it remains here.
    """
     Ensure that "value" meets the following conditions :

     - if left <= right :
         - value will be inside [left - right]
     - else :
         - value will be outside ]right - left[

    :param left: a limit that is allowed to be lower than "value"
    :param right: a limit that is allowed to be higher than "value"
    :param value: the value to be checked
    :return: either "value" if it passes the test, or left, or right, depending on whether is closest to "value"
    :note: the result is assigned a forced value when calling checkIfIn (guard,guard, value)
    """
    if left <= right:  # we want to include
        if value < left:
            value = left
        elif value > right:
            value = right
    else:  # we want to exclude
        if (
            value < (left + right) / 2.0
        ):  # is value lower than the mean of the interval ?
            if value > right:  # is value inside the interval ?
                value = right  # if so : value is set to the lower border
        elif value < left:  # else : is value inside the interval ?
            value = left  # if so : value is set to the higher border
    return value


##########################  P A Y L O A D
# duration of the states (empiric data)
AngleMin = 0
SepalExtAngleMax = 120
SepalExtTimeMin = 0.0
SepalExtTimeMax = 0.1

SepalIntAngleMax = 110
SepalIntTimeMin = 0.0
SepalIntTimeMax = 0.3

PetalExtAngleMax = 90
PetalExtTimeMin = 0.2
PetalExtTimeMax = 0.9

PetalIntAngleMax = 80
PetalIntTimeMin = 0.4
PetalIntTimeMax = 0.9

# beginning of SR - start
plageCPV = invBySegments(
    SepalExtAngleMax * 0.8, SepalExtTimeMin, SepalExtTimeMax, AngleMin, SepalExtAngleMax
)
# Inside Petal angle that marks the beginning of FO
AnglePetaleIntDebutFO = 20
finSR = invBySegments(
    AnglePetaleIntDebutFO, PetalIntTimeMin, PetalIntTimeMax, AngleMin, PetalIntAngleMax
)
# duration of SR
plageSR = finSR - plageCPV  # plageSR=0.4
# remaining time
plageFO = 1 - finSR  # =0.52


def computeStage(stade, avancement):
    tauxAvancement = avancement / 100.0  # back to decimal value

    # re.search ("(?i)...) : case insensitive search
    if re.search("(?i)bfv", stade):
        return 0  # ( [0,0,0,0],[10])                 # bud not opened yet
    elif re.search("(?i)cpv", stade):
        time01 = plageCPV * tauxAvancement  # sepals are opening
    elif re.search("(?i)sr", stade):
        time01 = plageCPV + plageSR * tauxAvancement  # petals not yet opening
    elif re.search("(?i)fo", stade):
        time01 = plageCPV + plageSR + plageFO * tauxAvancement  # petals opening
    elif re.search("(?i)ff", stade):
        time01 = 1  # or 1.00 ?
    print("time01=%f" % time01)
    return time01


# parameters
# #	S+	S-	P+	P-
# X min	0	0	2	4
# Xmax	1	3	4	9
# Ymin	0	0	0	0
# Ymax	120	110	90	80
def outerSepalAngle(time01):
    return bySegments(time01, 0, 0.1, 0, 120)


def invertOuterSepalAngle(angle):
    return invBySegments(angle, 0, 0.1, 0, 120)


def innerSepalAngle(time01):
    return bySegments(time01, 0, 0.3, 0, 110)


def invertInnerSepalAngle(angle):
    return invBySegments(angle, 0, 0.3, 0, 110)


def outerPetalAngle(time01):
    return bySegments(time01, 0.2, 0.9, 0, 90)  # paramètres vus avec Jess


def invertOuterPetalAngle(angle):
    return invBySegments(angle, 0.2, 0.9, 0, 90)


def innerPetalAngle(time01):
    return bySegments(time01, 0.4, 0.9, 0, 80)  #  // vus avec Jess


def notation2flowerAngles(stade, avancement=0.0, sepalAngles=None, flowerAngles=None):
    """translate observations to flower time01
    @param stade : a state of flower devlt in [BVF, CPV, SR, FO, FF]
    @param avancement : step in the current stade (0 .. 100) percent
    @param sepalAngles : parameters to draw sepals if they have been
    caught up in the MTG : [length of sepal, angle/vertical]
    @param flowerAngles : parameters to draw sepals if they have been
    caught up in the MTG : [length of petal, angle/vertical]
    TODO : separer angles et dimensions
    """
    if sepalAngles is None:
        sepalAngles = []
    if flowerAngles is None:
        flowerAngles = []

    # TODO : déterminer une priorité des entrées pour éviter
    # les incohérences tq pétales + ouverts que sépales

    flowerHeight = 20
    petalExtAngle = None
    petalIntAngle = 0
    if flowerAngles is not None:
        if len(flowerAngles) > 0:
            flowerHeight = flowerAngles[0]  # length mm
            if len(flowerAngles) > 1:
                petalExtAngle = flowerAngles[1]  # angle degrees
                if len(flowerAngles) > 2:
                    petalExtAngle = flowerAngles[2]  # angle degrees

    sepalLength = flowerHeight  # TODO : petal length
    sepalExtAngle = None
    if sepalAngles is not None:
        if len(sepalAngles) > 0:
            sepalLength = sepalAngles[0]  # length mm
            if len(sepalAngles) > 1:
                sepalExtAngle = sepalAngles[1]  # angle degrees
                if len(sepalAngles) > 2:
                    sepalExtAngle = sepalAngles[2]  # angle degrees

    avancement = checkIfIn(0.0, 100.0, avancement)  # avancement must inside [0,100]
    time01 = computeStage(stade, avancement)

    if re.search("(?i)bfv", stade):
        return [], []
    elif re.search("(?i)(cpv)|(sr)|(fo)", stade):  # |fo to check continuity
        sepalExtAngle = outerSepalAngle(time01)
        sepalIntAngle = innerSepalAngle(time01)
        petalExtAngle = outerPetalAngle(time01)
        petalIntAngle = innerPetalAngle(time01)
        return [sepalLength, [sepalExtAngle, sepalIntAngle]], [
            flowerHeight,
            [petalExtAngle, petalIntAngle],
        ]
    elif re.search("(?i)ff", stade):
        return [], [0, [120, 120]]

    if sepalExtAngle is None:  # no measure for  sepal angles, so
        # we compute them both
        sepalExtAngle = outerSepalAngle(time01)
        sepalIntAngle = innerSepalAngle(time01)
    else:
        sepalIntAngle = sepalExtAngle * 0.8  # better idea :
        # this is the mean angle ; so :
        # -> compute it
        # then compute the ext and int angles such as e.g +- 10-20%

    petalFacts = [flowerHeight, [petalExtAngle, petalIntAngle]]
    sepalFacts = []
    if sepalLength is not None:
        sepalFacts.append(sepalLength)
        sepalFacts.append([sepalExtAngle, sepalIntAngle])

    # return outputs
    return sepalFacts, petalFacts


def test():
    minX = 1
    maxX = 10
    minY = 12
    maxY = 14

    factor = 100

    if minX < maxX:
        thisX = minX
        thatX = maxX
    else:
        thisX = maxX
        thatX = minX

    # direct
    for x in range(int(thisX * factor), int(thatX * factor)):
        y = x / float(factor)
        print("%f %f" % (y, bySegments(y, minX, maxX, minY, maxY)))

    # inverse
    for x in range(int(maxY * factor), int(minY * factor), -1):
        y = x / float(factor)
        print("%f %f" % (y, invBySegments(y, minX, maxX, minY, maxY)))

    # reciprocity
    for x in range(int(thisX * factor), int(thatX * factor)):
        y = x / float(factor)
        print(
            "%f %f"
            % (
                y,
                invBySegments(
                    bySegments(y, minX, maxX, minY, maxY), minX, maxX, minY, maxY
                ),
            )
        )


# e.g. inside gnuplot (plot "< bySegments.py" w l)
if __name__ == "__main__":
    test()
