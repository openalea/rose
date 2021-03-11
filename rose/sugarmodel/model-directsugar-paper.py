

# The optimizable parameters are defined in this file
paramfile = 'parameters-directsugar-paper.py'
execfile(paramfile, globals(),locals())

from math import *

def sl_plateau(auxin):
    return ( c2 + a2 * pow(auxin,2) / (k2 + pow(auxin,2)) ) / d2

def ck_plateau(auxin, sugar):
    return (  (c1/(1+b1*auxin) ) + a1 * (pow(sugar, 2) / (k1 + pow(sugar, 2) ) ) ) / d1 

def ckresponse(ck):
    return 1/(1+k3*pow(ck,2))

def sugarresponse(sugar):
    return 1 /(1 + k4*pow(sugar,2))

def slresponse(sl):
    return  pow(sl, 2) / (1 + b4*pow(sl, 2) ) 

def I_plateau(eck,esl,esug):
    return ( c3 + a3*esl + a4*eck + a5*esug) / d3

def eval_model(auxin, sugar, gr24 = 0, bap = 0):
    """ Main function of the model """
    sl = sl_plateau(auxin)+gr24
    ck = ck_plateau(auxin, sugar)+bap

    Sck = ckresponse(ck)
    Ssl = slresponse(sl)
    Ssug = sugarresponse(sugar)

    I = I_plateau(Sck,Ssl,Ssug)
    return sl, ck, Sck, Ssl, I




