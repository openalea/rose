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

######  SL response #########

#slresponsetargets = np.array([0.1,0.06,0.28,0.14])
#slresponseconditions = cross_conditions([0,2.5],[1 , 2.5])

######  I #########

Itargets = np.array([1.,  0.8, 3.11, 1.5])
Iconditions = cross_conditions([0,2.5],[1 , 2.5])

sugarlevels = [0.1, 0.5, 1 ,  2.5]
auxinlevels = [0,   1,   2.5]

measureddurations =  [[3.2 , 2.7, 1, 0.9],
                      [None, 5.8, 3.5, 2.1],
                      [None, None, None, 3.1]]


interpolateddurations = [[None ,  None, None, None],
                         [10.2, None, None, None],
                         [54, 15.5, None, None]]


completedurations =  [[measureddurations[i][j] if not measureddurations[i][j] is None else interpolateddurations[i][j] for j in xrange(len(measureddurations[i])) ] for i in xrange(len(measureddurations)) ]


from model import I_law


def estimate_I_from_duration(includeImeasure = True,  
                             includemeasuredduration = True, 
                             includeinterpolation = True,
                                gr24 = 0, bap = 0):
    if includeImeasure:
        valres  = list(Itargets)
        condres = list(Iconditions)
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
            I = I_law(duration)
            if not I is None: 
                valres.append(I)
                condres.append((auxval,sugval,gr24,bap))
    return valres, condres

################ I Duration relation

def estimate_I_duration_law():
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
    measuredI  = []
    consideredcond = []
    for i, cond in enumerate(Iconditions):
        if cond in delays:
            consideredcond.append(cond)
            measureddelay.append(delays[cond])
            measuredI.append(Itargets[i])

    print measureddelay
    print measuredI
    print consideredcond


    from scipy.stats import linregress
    slope, intercept, r_value, p_value, std_err = linregress(measureddelay, measuredI)
    print 'slope', slope
    print 'intercept', intercept

    x = np.array(measureddelay)
    plt.plot(measureddelay, measuredI,'ro',color=(1,0,0))
    plt.plot( x, slope*x+intercept, '-k', label = ('$y=%.4f x '+('+ ' if intercept > 0 else '') +'%.4f, r^2=%.4f$') % (slope, intercept, r_value)) 
    plt.margins(0.2)
    plt.legend(loc=2)
    plt.ylabel('Burst d elay')
    plt.xlabel('I level')
    plt.show() 

################ Extra BAP and GR24 experiment

baplevel = 0.25 # CK

            # auxin, sugar, gr24, bap
bapconditions = [(2.5, 0.5,  0, baplevel), (2.5, 1, 0, baplevel)]
bapdurations = [5.6, 2.8]
bapIlevels = map(I_law, bapdurations)

gr24level = 2 # SL
gr24conditions = [(1, 0.5, gr24level, 0), (1, 1, gr24level, 0)]
gr24durations = [15, 4]
gr24Ilevels = map(I_law, gr24durations) 

