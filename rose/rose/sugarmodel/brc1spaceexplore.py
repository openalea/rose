import numpy as np
from numpy.linalg import norm

lsysfile = 'rosebudJan15-model1-v0.lpy'

def simu(brc1):
    from openalea.lpy import Lsystem
    targetcontents = []
    for auxin in [0,2.5]:
        for sugar in [0, 1 , 2.5]:
            simu = Lsystem(lsysfile, {'AUXIN': auxin, 'SUGAR' : sugar, 'BRC1' : brc1} )
            ls = simu.iterate()
            res = ls[-1].p.brc1
            targetcontents.append(res)
    return targetcontents


targets = np.array([1.,  0.5, 0.4, 2.9, 2.1, 1])


def optimize():
    def evalsimu(params):
        res =  targets - simu(params)
        print params,':',norm(res)
        return res

    from scipy.optimize import leastsq

    return leastsq(evalsimu,[4.2,  7.6, 7.2, 2.7])

if __name__ == '__main__': 
    print optimize()