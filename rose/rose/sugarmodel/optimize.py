import numpy as np
from numpy.linalg import norm
import itertools

modelfile = 'model2.py'
paramfile = 'params10_init.py'

conditions = list(itertools.product([0,2.5],[0, 1 , 2.5]))

def simu(params, attname, conditions=conditions, withgr24 = False):
    from openalea.lpy import Lsystem
    targetcontents = []
    for auxin, sugar in conditions:
            if type(attname) == str: entry = attname.upper()
            else : entry = 'ALL'
            namespace = { entry : tuple(params)} 
            execfile(modelfile, namespace)
            eval_model = namespace['eval_model']
            sl, ck, brc1 = eval_model(auxin, sugar, gr24 = (0 if not withgr24 else 10.))
            resvalues = { 'sl' : sl , 'ck' : ck, 'brc1' : brc1 }
            if type(attname) == str:
                res = resvalues[attname]
                targetcontents.append(res)
            else:
                for att in attname:
                    res = resvalues[att]
                    targetcontents.append(res)
    return targetcontents


def get_param_init(paramnames):
    namespace = {}
    execfile(paramfile, namespace)
    return np.array([namespace[p] for p in paramnames])


def optimize(func, initvalue):
    from scipy.optimize import leastsq
    return leastsq(func,initvalue, ftol=1e-5)

def evalsimu(target, attname, conditions=conditions):
    withgr24optim = False
    if withgr24optim:
        simugr24a = conditions.index((1,0.5))    
        simugr24b = conditions.index((1,1))
    def evaluator(params):
        values = simu(params,attname,conditions)
        res =  (target - values)/target
        if withgr24optim:
            vgr24 = simu(params, attname, [conditions[simugr24a], conditions[simugr24b]], True)
            nres1 = 1.7  - (vgr24[0]/res[simugr24a])
            nres2 = 1.4  - (vgr24[1]/res[simugr24b])
            res = list(res)
            res += [nres1, nres2]
            res = np.array(res)
            print (vgr24[0], res[simugr24a], vgr24[0]/res[simugr24a])
            print (vgr24[1], res[simugr24b], vgr24[1]/res[simugr24b])
            print params,':',norm(res),res[-2:]
        else : 
            print params,':',norm(res)
        return res
    return evaluator

from params_generate import *

######  CK #########

cktargets = np.array([0.75, 0.97, 1., 1.1, 0.51, 0.59, 0.58, 0.59, 0.23, 0.36, 0.46, 0.51])
ckconditions = list(itertools.product([0, 1, 2.5],[0.1, 0.5, 1 , 2.5]))

def optimize_ck(generate = True):
    import diagram
    paramnames = get_param_names('CK',paramfile)
    ckevalsimu = evalsimu(cktargets,'ck',ckconditions)
    #ckevalsimu = evalsimu(cktargets,'ck')
    ckinit = get_param_init(paramnames)
    print 'Ck Init :',ckinit
    result, ok = optimize(ckevalsimu,ckinit)
    if generate: 
        update_param_file(paramfile,dict(zip(paramnames, result)))
        diagram.generate_fig_ck(cktargets)
	

######  SL #########

sltargets = (0.1, 1.)
sltargets = np.array([sltargets[0],sltargets[0],sltargets[1],sltargets[1]])
slconditions = list(itertools.product([0,2.5],[1 , 2.5]))

def optimize_sl(generate = True):
    import diagram
    paramnames = get_param_names('SL',paramfile)
    slevalsimu = evalsimu(sltargets,'sl',slconditions)
    slinit = get_param_init(paramnames)
    result, ok = optimize(slevalsimu,slinit)
    if generate: 
        update_param_file(paramfile,dict(zip(paramnames, result)))
        diagram.generate_fig_sl(sltargets)


######  BRC1 #########

brc1targets = np.array([1.,  0.8, 3.11, 1.5])
brc1conditions = list(itertools.product([0,2.5],[1 , 2.5]))


def optimize_brc1(generate = True, brc1targets = brc1targets, conditions = brc1conditions, randomseed = False):
    import diagram; reload(diagram)
    from random import uniform
    paramnames =  get_param_names('BRC1',paramfile)
    print paramnames
    brc1evalsimu = evalsimu(np.array(brc1targets),'brc1',conditions)
    if randomseed:
        brc1inits = [[uniform(0,100) if '_k_' in p else uniform(0,1)  for p in paramnames] for n in xrange(20)]
    else:
        brc1init = get_param_init(paramnames)
        brc1inits = [brc1init]
    bestresult = None
    for brc1init in brc1inits:
        print brc1init
        result, ok = optimize(brc1evalsimu,brc1init)
        val = norm(brc1evalsimu(result))
        if bestresult is None or bestresult[1] > val: bestresult = (result, val)
    result = bestresult[0]
    if generate: 
        update_param_file(paramfile,dict(zip(paramnames, result)))
        diagram.generate_fig_brc1()

sugarlevels = [0.1, 0.5, 1 ,  2.5]
auxinlevels = [0,   1,   2.5]

measureddurations =  [[3.2 , 2.7, 1, 0.9],
                      [None, 5.8, 3.5, 2.1],
                      [None, None, None, 3.1]]

interpolateddurations = [[None ,  None, None, None],
                         [14, None, None, None],
                         [40, 14, None, None]]


completedurations =  [[measureddurations[i][j] if not measureddurations[i][j] is None else interpolateddurations[i][j] for j in xrange(len(measureddurations[i])) ] for i in xrange(len(measureddurations)) ]

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



from model2 import brc1_law


def estimate_brc1_from_duration(includebrc1measure = True,  
                                includemeasuredduration = True, 
                                includeinterpolation = True):
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
                condres.append((auxval,sugval))
    return valres, condres


######### TOTAL ########
## obsolete

def optimize_all(generate = True):
    import diagram
    paramnames =  get_all_param_names(['CK','SL','BRC1'],paramfile) 
    print paramnames
    targets = sum([[cktargets[i],sltargets[i],brc1targets[i]] for i in xrange(len(cktargets))],[])
    print targets
    allevalsimu = evalsimu(np.array(targets),['ck','sl','brc1'],conditions)
    allinit = get_param_init(paramnames)
    result, ok = optimize(allevalsimu,allinit)
    if generate: 
        update_param_file(paramfile,dict(zip(paramnames, result)))
        diagram.generate_fig_compound()


#########  MAIN ########

def main_optimize():
    import sys
    if len(sys.argv) > 1:
        data = sys.argv[1]
        func = 'optimize_'+data
        globals()[func]()
    else:
        brc1targets, conditions = estimate_brc1_from_duration()
        print len(brc1targets), brc1targets
        print len(conditions), conditions
        optimize_brc1(True, brc1targets, conditions, False)

if __name__ == '__main__':
    import sys
    #test_gr24()
    main_optimize()
    #estimate_brc1_from_duration()
    #estimate_brc1_duration_law()
