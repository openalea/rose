import numpy as np
from numpy.linalg import norm

from runmodel import modelfile, paramfile
from targets import *

def simu(params, attname, conditions=cross_conditions()):
    from runmodel import runmodel
    targetcontents = []
    for auxin, sugar, gr24, bap in conditions:
            resvalues = runmodel(auxin, sugar, gr24, bap, params, modelfile)
            if type(attname) == str:
                res = resvalues[attname]
                targetcontents.append(res)
            else:
                res = resvalues[attname[-1]]
                targetcontents.append(res)
    return targetcontents


def optimize(func, initvalues, bounds = (-np.inf,np.inf)):
    from scipy.optimize import least_squares
    result = least_squares(func, initvalues, bounds=bounds, ftol=1e-5)
    return result.x, result.status > 0

def evalsimu(attname, paramnames, target, conditions):
    target = np.array(target)
    def evaluator(paramvalues):
        values = simu(dict(zip(paramnames,paramvalues)), attname, conditions)
        res =  (target - values)/target
        print paramvalues,':',norm(res)
        return res
    return evaluator

from params_generate import *

def param_bounds(parameters):
    resultinf = []
    resultsup = []
    for pname, pvalue in parameters.items():
        if type(pvalue) == tuple:
            assert len(pvalue) == 3
            resultinf.append(min(pvalue[1],pvalue[2]))
            resultsup.append(max(pvalue[1],pvalue[2]))
        else :
            resultinf.append(-np.inf)
            resultsup.append(np.inf)
    return (resultinf, resultsup)

def param_values(parameters):
    result = []
    for pname, pvalue in parameters.items():
        if type(pvalue) == tuple:
            assert len(pvalue) == 3
            result.append(pvalue[0])
        else :
            result.append(pvalue)
    return result

def optimize_group(generate, tag, functag, conditions, targets, randomseed = False):
    print 'Model :',repr(modelfile)
    parameters = get_parameters(functag, paramfile)
    myevalsimu = evalsimu(tag, parameters.keys(), targets, conditions)

    paraminits = [param_values(parameters)]
    if randomseed:
        from random import uniform
        paraminits += [[uniform(0,100) if '_k_' in p else uniform(0,1)  for p in parameters.keys()] for n in xrange(20)]

    initialval = norm(myevalsimu(param_values(parameters)))
    bestresult = None
    bestval = initialval

    for paraminit in paraminits:
        result, ok = optimize(myevalsimu, paraminit, param_bounds(parameters))
        val = norm(myevalsimu(result))

        if ok and bestresult is None or bestval > val: 
            bestresult, bestval = result, val

    namedresult = dict(zip(parameters.keys(), bestresult))

    import diagram ; reload(diagram)

    improvement = abs(initialval - bestval) > 1e-5
    if improvement :
        print 'Improve solution : ', initialval, ' --> ', bestval
        diagram.generate_fig(functag, targetvalues = targets, conditions = conditions, values = namedresult)
        if generate: 
            update_param_file(paramfile, namedresult)
    else:
        print 'No improvement found'
        diagram.generate_fig(functag, targetvalues = targets, conditions = conditions)


######  CK #########

def optimize_ck(generate = True, randomseed = False):
    optimize_group(generate, 'ck', 'CK', ckconditions, cktargets, randomseed)
	

######  SL #########

def optimize_sl(generate = True, randomseed = False):
    optimize_group(generate, 'sl', 'SL', slconditions, sltargets, randomseed)


######  SL response #########
#
#def optimize_slresponse(generate = True, randomseed = False):
#    optimize_group(generate, 'slresponse', 'SLResponse', slresponseconditions, slresponsetargets, randomseed)


######  BRC1 #########

def optimize_brc1(generate = True, brc1targets = brc1targets, conditions = brc1conditions, randomseed = False):
    optimize_group(generate, 'brc1', 'BRC1', conditions, brc1targets, randomseed)


######### Full optimization of Brc1 ########

def optimize_brc1_full(generate = True, randomseed = False):
        brc1targets, conditions = estimate_brc1_from_duration()
        brc1targets += bapbrc1levels + gr24brc1levels
        conditions += bapconditions + gr24conditions
        #print len(brc1targets), brc1targets
        #print len(conditions), conditions
        optimize_brc1(generate, brc1targets, conditions, randomseed)



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
