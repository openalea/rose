import numpy as np
from numpy.linalg import norm
import os
from targets import *

def simu(params, attname, conditions=cross_conditions()):
    from runmodel import runmodel
    targetcontents = []
    for auxin, sugar, gr24, bap in conditions:
            resvalues = runmodel(auxin, sugar, gr24, bap, params)
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

reallyrandom = True

def get_attempt_dir(tag, paramfile):
    from os.path import exists, join
    from os import makedirs
    mdir = join('randomseed' if reallyrandom else 'randomseedreg',os.path.splitext(os.path.basename(paramfile))[0],tag)
    if not exists(mdir) : makedirs(mdir)
    return mdir

def read_attempt(tag, i, paramfile):
    from cPickle import load        
    from os.path import exists, join
    f = join(get_attempt_dir(tag, paramfile),str(i)+'.pkl')
    if exists(f):    
        stream = file(f,'rb')
        return load( stream)[1:]


def save_attempt(tag, i, val, param, paramfile):
    from cPickle import dump
    from os.path import join
    f = join(get_attempt_dir(tag, paramfile),str(i)+'.pkl')
    stream = file(f,'wb')
    dump( (i,val, param), stream)


def process(params, saving = True):
    tag, conditions, targets, paramfile, i, paraminit = params

    parameters = get_parameters(tag, paramfile)
    myevalsimu = evalsimu(tag, parameters.keys(), targets, conditions)

    val = None
    res = None
    if saving : 
        res = read_attempt(tag, i, paramfile)

    if res :
        val, result = res
        print 'Seed ',i, 'Val', val, 'Params', result
        ok = True
    if val is None:
        print 'Start from', paraminit
        result, ok = optimize(myevalsimu, paraminit, param_bounds(parameters))
        result, ok = optimize(myevalsimu, result, param_bounds(parameters))
        val = norm(myevalsimu(result))
        if ok and saving: 
            save_attempt(tag, i, val, result, paramfile)
    return result, val


def generate_paraminits(tag, parameters, randomseedenabled, seeds):
    from math import ceil
    from itertools import product
    paraminits = [ param_values(parameters) ]
    if randomseedenabled:
        from random import uniform, seed
        if reallyrandom:
            if type(seeds) == int: seeds = xrange(1,seeds)
            elif 0 in seeds: seeds.remove(0)
            for n in seeds:
                seed(n)
                paraminits.append([uniform(pmin,pmax)  for pname, (pvalue, pmin, pmax) in parameters.items()])
        else:
            dim = len(parameters)
            nbvalperparam = ceil(pow(seeds,1./dim))
            paraminits = list(product(*[np.linspace(pmin,pmax,nbvalperparam) for pname, (pvalue, pmin, pmax) in parameters.items()]))
    return paraminits        

def optimize_group(generate, tag, conditions, targets, randomseedenabled = False, seeds = 1000, view = True, parallel = True):
    from runmodel import modelfile, paramfile
    print seeds
    print 'Model :',repr(modelfile),'with parameters',repr(paramfile),'on', tag
    parameters = get_parameters(tag, paramfile)

    paraminits = generate_paraminits(tag, parameters, randomseedenabled, seeds)

    initialval = norm(evalsimu(tag, parameters.keys(), targets, conditions)(param_values(parameters)))

    if not randomseedenabled:
        results = []
        for i, paraminit in enumerate(paraminits):
            result, val  = process((tag, conditions, targets, paramfile, i, paraminit), saving = False)
            results.append((result, val))
    else:
        from multiprocessing import Pool, cpu_count
        n = cpu_count()-1
        p = Pool(n)
        results = p.map(process, [(tag, conditions, targets, paramfile, i, paraminit) for i, paraminit in enumerate(paraminits)])
    
    bestresult, bestval = min(results, key=lambda x : x[1])

    namedresult = dict(zip(parameters.keys(), bestresult))

    import diagram ; reload(diagram)

    improvement = abs(initialval - bestval) > 1e-5
    if improvement :
        print 'Improve solution : ', initialval, ' --> ', bestval
        if view : diagram.generate_fig(tag, targetvalues = targets, conditions = conditions, values = namedresult)
        if generate: 
            update_param_file(paramfile, namedresult)
    else:
        print 'No improvement found'
        if view : diagram.generate_fig(tag, targetvalues = targets, conditions = conditions)


######  CK #########

def optimize_CK(generate = True, randomseedenabled = False, seeds = 1000, view = True):
    optimize_group(generate, 'CK', ckconditions, cktargets, randomseedenabled, seeds, view = view)
	

######  SL #########

def optimize_SL(generate = True, randomseedenabled = False, seeds = 100, view = True):
    optimize_group(generate,  'SL', slconditions, sltargets, randomseedenabled, seeds, view = view)

######  I #########

def optimize_I_simple(generate = True, targets = Itargets, conditions = Iconditions, randomseedenabled = False, seeds = 1000, view = True):
    optimize_group(generate, 'I', conditions, targets, randomseedenabled, seeds=seeds, view = view)


######### Full optimization of I ########

def optimize_I(generate = True, randomseedenabled = False, seeds = 1000, view = False):
        Itargets, conditions = estimate_I_from_duration()
        Itargets += bapIlevels + gr24Ilevels
        conditions += bapconditions + gr24conditions
        #print len(brc1targets), brc1targets
        #print len(conditions), conditions
        optimize_I_simple(generate, Itargets, conditions, randomseedenabled, seeds=seeds, view = view)


####### Estimate volumes ############

def read_attempts(tag):
    from runmodel import modelfile, paramfile
    from os.path import exists, join, splitext
    import glob
    print 'Model :',repr(modelfile),'with parameters',repr(paramfile),'on', tag
    parameters = get_parameters(tag, paramfile)
    mdir = get_attempt_dir(tag, paramfile)
    files = glob.glob(join(mdir,'*.pkl'))
    files = [splitext(f[len(mdir)+1:])[0] for f in files]
    seeds = map(int, files)
    seeds.sort()

    paraminits = generate_paraminits(tag, parameters, True, seeds)
    results = [ read_attempt(tag, i, paramfile) for i in seeds]
    values = [r[0] if len(r) == 2 else r[1] for r in results]
    params = [r[1] if len(r) == 2 else r[2] for r in results]
    return parameters, params, values, seeds

def filter_attempts(tag, parameters, params, values, seeds):
    maxerror = {'I':0.7,'CK':0.4}.get(tag,None)
    if not maxerror is None : 
        nbvalues = len(values)
        filtering = [i for i,v in enumerate(values) if v <= maxerror]
        params = [params[i] for i in filtering]
        values = [values[i] for i in filtering]
        seeds = [seeds[i] for i in filtering]
        print 'Remove',nbvalues - len(values),'values'
    return parameters, params, values, seeds

def estimate_volumes_CK(): estimate_volumes('CK')
def estimate_volumes_SL(): estimate_volumes('SL')
def estimate_volumes_I():  estimate_volumes('I')

def estimate_variability(tag):
    parameters, params, values, seeds = read_attempts(tag)
    parameters, params, values, seeds = filter_attempts(tag, parameters, params, values, seeds)
    output = file('optimalsolution.csv','w')
    output.write('\t'.join(parameters.keys())+'\t\t\Error\n')
    for p,v in zip(params, values):
        output.write('\t'.join(map(str,p))+'\t:\t'+str(v)+'\n')

    params = np.array(params)
    for i in xrange(len(parameters.keys())):
        print parameters.keys()[i] + '\t'+str(np.mean(params[:,i]))+' +- '+str(np.std(params[:,i]))+'\t'
    print 
    print 'Error:', str(np.mean(values))+' +- '+str(np.std(values))+'  '+str(min(values))+'  '+str(max(values))
    plot_variability(tag)


def plot_variability(tag):
    import matplotlib.pyplot as plot
    from math import ceil
    parameters, params, values, seeds = read_attempts(tag)
    parameters, params, values, seeds = filter_attempts(tag, parameters, params, values, seeds)
    nbcol = 3
    nbrow = ceil((len(parameters)+1)/float(nbcol))
    for i,parname in enumerate(parameters.keys()):
        axes = plot.subplot(nbrow,nbcol,i+1)
        data = [param[i] for param in params]
        plot.hist(data)
        axes.set_xlabel(parname)
    axes = plot.subplot(nbrow,nbcol,len(parameters)+1)
    plot.hist(values)
    axes.set_xlabel('Error')
    plot.show()



#########  MAIN ########

def print_help():
    print 'help of script optimize.py'
    print '-h : this help'
    print '-m : set the model to optimize'
    print '-r : with random seed'
    print '-v : characterize random seed'
    print '-w : characterize variability of random seed'
    print 'CK,SL,I,ALL : optimize the parameters of the specified compound'
    print 'default : optimize I with all conditions (including burst delay inference)'

def main_optimize():
    #estimate_volumes_CK()
    #exit()
    import sys
    generate = True
    randomseedenabled = False
    target = 'optimize_'
    def targetfunc(tag):
        if target == 'optimize_':
            func = target+tag
            def mfunc(view = True): 
                return globals()[func](generate, randomseedenabled, view=view)
        else:
            def mfunc(view = True): 
                return globals()[target](tag)
        return mfunc

    if len(sys.argv) > 1:
        i = 1
        done = False
        while  i < len(sys.argv) and not done:
            current = sys.argv[i].upper()
            print current
            if current == '-H':
                print_help()
            elif current == '-M':
                from runmodel import set_model
                set_model(sys.argv[i+1])
                i += 1
            elif current == '-R':
                randomseedenabled = True
            elif current == '-W':
                target = 'estimate_variability'
            elif current == 'ALL':
                targetfunc('CK')(view = False)
                targetfunc('SL')(view = False)
                targetfunc('I')(view = False)
                done = True
            elif target+current in globals() or target in globals():
                targetfunc(current)()
                done = True
            else:
                print 'Unknow option : ', sys.argv[i]
                print_help()
                done = True
            i += 1
        if not done:
            targetfunc('I')()
    else: 
        optimize_I(generate, randomseedenabled)


if __name__ == '__main__':
    #test_volume()
    main_optimize()

