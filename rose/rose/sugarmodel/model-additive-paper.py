

# The optimizable parameters are defined in this file
paramfile = 'parameters-additive.py'
execfile(paramfile, globals(),locals())

from math import *

def sl_plateau(auxin):
    return ( k2 +pow(auxin,2) / (beta0+pow(auxin,2)) ) / beta2

def ck_plateau(auxin, sugar):
    return ( alpha2 * (pow(sugar, 2) / (k1 + pow(sugar, 2) ) )  + (alpha0/(1+alpha1*auxin) ) ) / alpha3 

def ckresponse(ck):
    return (k3+pow(ck,2))/pow(ck,2)

def sugaresponse(sugar):
    return sigma1 + sigma2*pow(sugar,2)

def slresponse(sl,sugar):
    return  pow(sl, 2) / (1 + sugaresponse(sugar)*pow(sl, 2) ) 

def I_plateau(eck,esl):
    return ( delta0 + delta1*esl + delta2*eck )/delta3

def eval_model(auxin, sugar, gr24 = 0, bap = 0):
    """ Main function of the model """
    sl = sl_plateau(auxin)+gr24
    ck = ck_plateau(auxin, sugar)+bap

    Sck = ckresponse(ck)
    Ssl = slresponse(sl, sugar)

    I = I_plateau(Sck,Ssl)
    return sl, ck, Sck, Ssl, I




