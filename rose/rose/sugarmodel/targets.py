import itertools
import numpy as np

def isiterable(obj):
    try:
        iter(obj)
        return True
    except:
        return False

def tolist(obj):
    if isiterable(obj) : return obj
    else : return [obj]

def cross_conditions(auxinslevels = [0,2.5], sugarlevels = [0, 1 , 2.5], gr24levels = 0, baplevels = 0):
    return list(itertools.product(tolist(auxinslevels),tolist(sugarlevels), tolist(gr24levels), tolist(baplevels)))



######  CK #########

cktargets = np.array([0.75, 0.97, 1., 1.1, 0.51, 0.59, 0.58, 0.59, 0.23, 0.36, 0.46, 0.51])
ckconditions = cross_conditions([0, 1, 2.5], [0.1, 0.5, 1 , 2.5])


######  SL #########

sltargets = (0.4, 1.)
sltargets = np.array([sltargets[0],sltargets[0],sltargets[1],sltargets[1]])
slconditions = cross_conditions([0,2.5],[1 , 2.5])

######  SL signal #########

slsignaltargets = np.array([0.1,0.06,0.28,0.14])
slsignalconditions = cross_conditions([0,2.5],[1 , 2.5])

######  BRC1 #########

brc1targets = np.array([1.,  0.8, 3.11, 1.5])
brc1conditions = cross_conditions([0,2.5],[1 , 2.5])

sugarlevels = [0.1, 0.5, 1 ,  2.5]
auxinlevels = [0,   1,   2.5]

measureddurations =  [[3.2 , 2.7, 1, 0.9],
                      [None, 5.8, 3.5, 2.1],
                      [None, None, None, 3.1]]


interpolateddurations = [[None ,  None, None, None],
                         [10.2, None, None, None],
                         [54, 15.5, None, None]]


completedurations =  [[measureddurations[i][j] if not measureddurations[i][j] is None else interpolateddurations[i][j] for j in xrange(len(measureddurations[i])) ] for i in xrange(len(measureddurations)) ]


from model2 import brc1_law


def estimate_brc1_from_duration(includebrc1measure = True,  
                                includemeasuredduration = True, 
                                includeinterpolation = True,
                                gr24 = 0, bap = 0):
    if includebrc1measure:
        valres  = list(brc1targets)
        condres = list(brc1conditions)
    else:
        valres  = []
        condres = []

    if includeinterpolation and includemeasuredduration :
        ldurations = completedurations 
    elif includeinterpolation:
        ldurations = interpolateddurations 
    elif includemeasuredduration:
        ldurations = measureddurations 

    if includeinterpolation or includemeasuredduration :
        for aux,sug in itertools.product(enumerate(auxinlevels), enumerate(sugarlevels)):
            auxi, auxval = aux
            sugi, sugval = sug
            duration = ldurations[auxi][sugi]
            brc1 = brc1_law(duration)
            if not brc1 is None: 
                valres.append(brc1)
                condres.append((auxval,sugval,gr24,bap))
    return valres, condres

################ Brc1 Duration relation

def estimate_brc1_duration_law():
    import numpy as np
    import matplotlib.pyplot as plt

    delays = dict()
    for aux,sug in itertools.product(enumerate(auxinlevels), enumerate(sugarlevels)):
        auxi, auxval = aux
        sugi, sugval = sug
        duration = measureddurations[auxi][sugi]
        if not duration is None:
            delays[(auxval,sugval)] = duration
    measureddelay = []
    measuredbrc1  = []
    consideredcond = []
    for i, cond in enumerate(brc1conditions):
        if cond in delays:
            consideredcond.append(cond)
            measureddelay.append(delays[cond])
            measuredbrc1.append(brc1targets[i])

    print measureddelay
    print measuredbrc1
    print consideredcond


    from scipy.stats import linregress
    slope, intercept, r_value, p_value, std_err = linregress(measureddelay, measuredbrc1)
    print 'slope', slope
    print 'intercept', intercept

    x = np.array(measureddelay)
    plt.plot(measureddelay, measuredbrc1,'ro',color=(1,0,0))
    plt.plot( x, slope*x+intercept, '-k', label = ('$y=%.4f x '+('+ ' if intercept > 0 else '') +'%.4f, r^2=%.4f$') % (slope, intercept, r_value)) 
    plt.margins(0.2)
    plt.legend(loc=2)
    plt.ylabel('Burst delay')
    plt.xlabel('BRC1 level')
    plt.show() 

################ Extra BAP and GR24 experiment

baplevel = 10

bapconditions = [(0.5, 2.5, 0, baplevel), (1,2.5,0,baplevel)]
bapdurations = [5.6, 2.8]
bapbrc1levels = map(brc1_law, bapdurations)

gr24level = 10
gr24conditions = [(0.5, 0, gr24level,0), (1,1,gr24level,0)]
gr24durations = [15, 4]
gr24brc1levels = map(brc1_law, gr24durations) 

