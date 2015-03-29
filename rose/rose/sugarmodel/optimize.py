import numpy as np
from numpy.linalg import norm
import itertools

lsysfile = 'rosebudJan15-model1-v1.lpy'
paramfile = 'params_init.py'

conditions = itertools.product([0,2.5],[0, 1 , 2.5])

def simu(params,attname, conditions=conditions):
    from openalea.lpy import Lsystem
    targetcontents = []
    for auxin, sugar in conditions:
            simu = Lsystem(lsysfile, {'AUXIN': auxin, 'SUGAR' : sugar, attname.upper() : tuple(params)} )
            ls = simu.iterate()
            res = getattr(ls[-1].p,attname)
            targetcontents.append(res)
    return targetcontents

def get_param_names(paramtags,paramfile = paramfile):
    def contains(l, pattern):
        try:
            idx = l.index(pattern)
            return l[idx-1] in ' \t\n' and l[idx+len(paramtags)] in ' \t\n' 
        except ValueError,e:
            return False

    f = file(paramfile)
    for l in f:
        if contains(l,paramtags ):
            return map(lambda x:x.strip(), l.split('=')[0].split(','))

def get_param_init(paramnames):
    from openalea.lpy import Lsystem
    simu = Lsystem(lsysfile)
    return np.array([getattr(simu,p) for p in paramnames])


def optimize(func, initvalue):
    from scipy.optimize import leastsq
    return leastsq(func,initvalue)

def evalsimu(target, attname, conditions=conditions):
    def evaluator(params):
        res =  target - simu(params,attname,conditions)
        print params,':',norm(res)
        return res
    return evaluator

from params_generate import *
import diagram

######  CK #########

#cktargets = np.array([1., 1.3, 2.1, 0.25, 0.4, 0.6])
cktargets = np.array([1., 1.9, 2.1, 0.25, 0.5, 0.6])
def optimize_ck(generate = True):
    paramnames = get_param_names('CK') # ['ck_base_synth_coef', 'ck_sugar_k_synth_coef', 'ck_auxin_k_synth_coef', 'ck_base_decay_coef']
    ckevalsimu = evalsimu(cktargets,'ck')
    ckinit = get_param_init(paramnames)
    print ckinit
    result, ok = optimize(ckevalsimu,ckinit)
    if generate: 
        update_param_file(paramfile,dict(zip(paramnames, result)))
        diagram.generate_fig_ck(cktargets)

######  SL #########

sltargets = (1., 1.5)
sltargets = np.array([sltargets[0],sltargets[0],sltargets[0],sltargets[1],sltargets[1],sltargets[1]])

def optimize_sl(generate = True):
    paramnames = get_param_names('SL') # ['sl_auxin_synth_coef', 'sl_base_synth_coef', 'sl_base_decay_coef']
    slevalsimu = evalsimu(sltargets,'sl')
    slinit = get_param_init(paramnames)
    result, ok = optimize(slevalsimu,slinit)
    if generate: 
        update_param_file(paramfile,dict(zip(paramnames, result)))
        diagram.generate_fig_sl(sltargets)

######  SLP #########

slptargets = np.array([1., 0.5, 0.2, 1.1, 0.6, 0.3])

def optimize_slp(generate = True):
    paramnames = get_param_names('SLP') # ['slp_sugar_synth_coef', 'slp_sugar_k_synth_coef', 'slp_decay_coef']
    slpevalsimu = evalsimu(slptargets,'slp')
    slpinit = get_param_init(paramnames)
    result, ok = optimize(slpevalsimu,slpinit)
    if generate: 
        update_param_file(paramfile,dict(zip(paramnames, result)))
        diagram.generate_fig_slp(slptargets)

######  BRC1 #########

brc1targets = np.array([1.,  0.5, 0.4, 2.9, 2.1, 1])

def optimize_brc1(generate = True, brc1targets = brc1targets, conditions = conditions):
    paramnames =  get_param_names('BRC1') # ['brc1_base_synth_coef', 'brc1_slp_synth_coef', 'brc1_ck_synth_coef', 'brc1_ck_k_synth_coef','brc1_base_decay_coef']
    brc1evalsimu = evalsimu(np.array(brc1targets),'brc1',conditions)
    brc1init = get_param_init(paramnames)
    result, ok = optimize(brc1evalsimu,brc1init)
    if generate: 
        update_param_file(paramfile,dict(zip(paramnames, result)))
        diagram.generate_fig_brc1(brc1targets)

sugarlevels = [0.1, 0.5, 1 , 2.5]
auxinlevels = [0,1,2.5,5]
durations =  [[3 , 2, 1.5, 1],
              [None, 6, 3, 2],
              [None, None, 9, 3.5],
              [None, None, None, 7]]

def brc1_law(duration):
    slope = 4.6978021978
    intercept = -1.0978021978
    if not duration is None : return (duration - intercept)/ slope 
    return None


def estimate_brc1_from_duration():
    valres  = []
    condres = []
    for aux,sug in itertools.product(enumerate(auxinlevels), enumerate(sugarlevels)):
        auxi, auxval = aux
        sugi, sugval = sug
        duration = durations[sugi][auxi]
        brc1 = brc1_law(duration)
        if not brc1 is None: 
            valres.append(brc1)
            condres.append((auxval,sugval))
    return valres, condres


######### TOTAL ########

def optimize_all(generate = True):
    optimize_ck(generate)
    optimize_sl(generate)
    optimize_slp(generate)
    optimize_brc1(generate)


#########  MAIN ########


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        data = sys.argv[1]
        func = 'optimize_'+data
        globals()[func]()
    else:
        brc1targets, conditions = estimate_brc1_from_duration()
        print brc1targets
        print conditions
        optimize_brc1(True, brc1targets, conditions)