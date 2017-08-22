import numpy as np
from numpy.linalg import norm
import itertools
import diagram ; reload(diagram)

modelfile = 'model2.py'
from runmodel import get_param_file
paramfile = get_param_file(modelfile)

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



def simu(params, attname, conditions=cross_conditions()):
    from runmodel import runmodel
    targetcontents = []
    for auxin, sugar, gr24, bap in conditions:
            resvalues = runmodel(auxin, sugar, gr24, bap, attname, params, modelfile)
            if type(attname) == str:
                res = resvalues[attname]
                targetcontents.append(res)
            else:
                res = resvalues[attname[-1]]
                targetcontents.append(res)
    return targetcontents


def get_param_init(paramnames):
    namespace = {}
    execfile(paramfile, namespace)
    return np.array([namespace[p] for p in paramnames])


def optimize(func, initvalue):
    from scipy.optimize import least_squares
    result = least_squares(func,initvalue, ftol=1e-5)
    return result.x, result.status > 0

def evalsimu(target, attname, conditions):
    def evaluator(params):
        values = simu(params,attname,conditions)
        res =  (target - values)/target
        print params,':',norm(res)
        return res
    return evaluator

from params_generate import *

######  CK #########

cktargets = np.array([0.75, 0.97, 1., 1.1, 0.51, 0.59, 0.58, 0.59, 0.23, 0.36, 0.46, 0.51])
ckconditions = cross_conditions([0, 1, 2.5], [0.1, 0.5, 1 , 2.5])

def optimize_ck(generate = True):
    paramnames = get_param_names('CK',paramfile)
    print paramnames
    ckevalsimu = evalsimu(cktargets,'ck',ckconditions)
    #ckevalsimu = evalsimu(cktargets,'ck')
    ckinit = get_param_init(paramnames)
    print 'Ck Init :',ckinit
    result, ok = optimize(ckevalsimu,ckinit)
    print dict(zip(paramnames, result))
    diagram.generate_fig_ck(cktargets, ckconditions,'ck', result)
    if ok and generate: 
        update_param_file(paramfile,dict(zip(paramnames, result)))
	

######  SL #########

sltargets = (0.4, 1.)
sltargets = np.array([sltargets[0],sltargets[0],sltargets[1],sltargets[1]])
slconditions = cross_conditions([0,2.5],[1 , 2.5])

def optimize_sl(generate = True):
    paramnames = get_param_names('SL',paramfile)
    slevalsimu = evalsimu(sltargets,'sl',slconditions)
    slinit = get_param_init(paramnames)
    result, ok = optimize(slevalsimu,slinit)
    diagram.generate_fig_sl(sltargets, slconditions, 'sl', result)
    if ok and generate: 
        update_param_file(paramfile,dict(zip(paramnames, result)))

######  SL signal #########

slsignaltargets = np.array([0.1,0.06,0.28,0.14])
slsignalconditions = cross_conditions([0,2.5],[1 , 2.5])

def optimize_slsignal(generate = True):
    paramnames = get_param_names('SLsignal',paramfile)
    slpevalsimu = evalsimu(slsignaltargets,'slsignal',slsignalconditions)
    slpinit = get_param_init(paramnames)
    result, ok = optimize(slpevalsimu,slpinit)
    diagram.generate_fig_slsignal(slsignaltargets, slsignalconditions,'slsignal', result)
    if ok and generate: 
        update_param_file(paramfile,dict(zip(paramnames, result)))

######  BRC1 #########

brc1targets = np.array([1.,  0.8, 3.11, 1.5])
brc1conditions = cross_conditions([0,2.5],[1 , 2.5])


def optimize_brc1(generate = True, brc1targets = brc1targets, conditions = brc1conditions, randomseed = False):
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
        print 'ok :',ok
        val = norm(brc1evalsimu(result))
        if bestresult is None or bestresult[1] > val: bestresult = (result, val)
    result = bestresult[0]

    diagram.generate_fig_brc1(brc1targets, conditions, 'brc1', result)
    if generate: 
        update_param_file(paramfile,dict(zip(paramnames, result)))

sugarlevels = [0.1, 0.5, 1 ,  2.5]
auxinlevels = [0,   1,   2.5]

measureddurations =  [[3.2 , 2.7, 1, 0.9],
                      [None, 5.8, 3.5, 2.1],
                      [None, None, None, 3.1]]


interpolateddurations = [[None ,  None, None, None],
                         [10.2, None, None, None],
                         [54, 15.5, None, None]]


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


################ Extra BAP and GR24 experiment
baplevel = 0.2

bapconditions = [[0.5, 2.5, 0, baplevel], [1,2.5,0,baplevel]]
bapdurations = [5.6, 2.8]
bapbrc1levels = map(brc1_law, bapdurations)

gr24level = 0.1
gr24conditions = [[0.5, 0, gr24level,0], [1,1,gr24level,0]]
gr24durations = [10, 4]
gr24brc1levels = map(brc1_law, gr24durations) 

######### Full optimization of Brc1 ########

def optimize_brc1_full(generate = True, randomseed = False):
        brc1targets, conditions = estimate_brc1_from_duration()
        brc1targets += bapbrc1levels + gr24brc1levels
        conditions += bapconditions + gr24conditions
        print len(brc1targets), brc1targets
        print len(conditions), conditions
        optimize_brc1(generate, brc1targets, conditions, randomseed)



######### TOTAL ########
## obsolete

def optimize_all(generate = True):
    import diagram
    paramnames =  get_all_param_names(['CK','SL','SLsignal','BRC1'],paramfile) 
    print paramnames
    targets = sum([[cktargets[i],sltargets[i],slsignaltargets[i],brc1targets[i]] for i in xrange(len(cktargets))],[])
    print targets
    allevalsimu = evalsimu(np.array(targets),['ck','sl','slsignal','brc1'],conditions)
    allinit = get_param_init(paramnames)
    result, ok = optimize(allevalsimu,allinit)
    if ok and generate: 
        update_param_file(paramfile,dict(zip(paramnames, result)))
    diagram.generate_fig_compound()


#########  MAIN ########

def main_optimize():
    import sys
    generate = False
    if len(sys.argv) > 1:
        data = sys.argv[1]
        func = 'optimize_'+data
        if len(sys.argv) > 2:
            generate = eval(sys.argv[2])
            assert generate in [False,True]
        globals()[func](generate)
    else:
        optimize_brc1_full(generate)

if __name__ == '__main__':
    import sys
    #test_gr24()
    main_optimize()
    #estimate_brc1_from_duration()
    #estimate_brc1_duration_law()
