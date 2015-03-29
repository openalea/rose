import numpy as np
from numpy.linalg import norm

lsysfile = 'rosebudJan15-model1-v1.lpy'

def simu(params,attname):
    from openalea.lpy import Lsystem
    targetcontents = []
    for auxin in [0,2.5]:
        for sugar in [0, 1 , 2.5]:
            simu = Lsystem(lsysfile, {'AUXIN': auxin, 'SUGAR' : sugar, attname.upper() : tuple(params)} )
            ls = simu.iterate()
            res = getattr(ls[-1].p,attname)
            targetcontents.append(res)
    return targetcontents

def get_param_init(paramnames):
    from openalea.lpy import Lsystem
    simu = Lsystem(lsysfile)
    return np.array([getattr(simu,p) for p in paramnames])


def optimize(func, initvalue):
    from scipy.optimize import leastsq
    return leastsq(func,initvalue)

def evalsimu(target, attname):
    def evaluator(params):
        res =  target - simu(params,attname)
        print params,':',norm(res)
        return res
    return evaluator

######  CK #########

cktargets = np.array([1., 1.9, 2.1, 0.25, 0.5, 0.6])
def optimize_ck():
    ckevalsimu = evalsimu(cktargets,'ck')
    ckinit = get_param_init(['ck_base_synth_coef', 'ck_sugar_k_synth_coef', 'ck_auxin_k_synth_coef', 'ck_base_decay_coef'])
    return optimize(ckevalsimu,ckinit)

######  SL #########

sltargets = (1., 1.1,)

def optimize_sl():
    slevalsimu = evalsimu(np.array([sltargets[0],sltargets[0],sltargets[0],sltargets[1],sltargets[1],sltargets[1]]),'sl')
    slinit = get_param_init(['sl_auxin_synth_coef', 'sl_base_synth_coef', 'sl_base_decay_coef'])
    return optimize(slpevalsimu,slpinit)

######  SLP #########

slptargets = np.array([1., 0.5, 0.2, 1.1, 0.6, 0.3])

def optimize_slp():
    slpevalsimu = evalsimu(slptargets,'slp')
    slpinit = get_param_init(['slp_sugar_synth_coef', 'slp_sugar_k_synth_coef', 'slp_decay_coef'])
    return optimize(slpevalsimu,slpinit)

######  BRC1 #########

brc1targets = np.array([1.,  0.5, 0.4, 2.9, 2.1, 1])
brc1init1 = [7.6, 4.2,  4.2, 1,  2.7]
brc1optim = [0.0007, 0.0034, 0.0027, 0.19, 0.0036]
brc1init  = [0.1,  0.45,  0.6,  0.25,  1]

def optimize_brc1():
    brc1evalsimu = evalsimu(brc1targets,'brc1')
    brc1init = get_param_init(['brc1_base_synth_coef', 'brc1_slp_synth_coef', 'brc1_ck_synth_coef', 'brc1_ck_k_synth_coef','brc1_base_decay_coef'])
    return optimize(brc1evalsimu,brc1init)


#########  MAIN ########


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        data = sys.argv[1]
        func = 'optimize_'+data
        globals()[func]()
    else:
        optimize_brc1()