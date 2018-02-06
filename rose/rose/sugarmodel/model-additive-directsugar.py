

# The optimizable parameters are defined in this file
paramfile = 'parameters-additive-directsugar.py'
execfile(paramfile, globals(),locals())

sl_auxin_exp = 2
ck_sugar_exp = 2
ck_auxin_exp = 1
ckresponse_ck_exp = 2
slresponse_sl_exp = 2
sugarresponse_sugar_exp = 2


from math import *


def sl_plateau(auxin):
    return ( sl_base_synth_coef +pow(auxin,sl_auxin_exp) / (sl_auxin_synth_coef+pow(auxin,sl_auxin_exp)) ) / sl_base_decay_coef


def ck_plateau(auxin, sugar):
    return (( ck_sugar_synth_coef * (pow(sugar, ck_sugar_exp) / (ck_sugar_k_synth_coef + pow(sugar, ck_sugar_exp) ) )  
             + (ck_auxin_synth_coef/(1+ck_auxin_k_synth_coef*pow(auxin, ck_auxin_exp)) ) ) 
             / ck_base_decay_coef )

def ckresponse(ck):
    powck = pow(ck,ckresponse_ck_exp)
    return ((ckresponse_ck_k1_synth_coef+powck)/powck )

def slresponse(sl):
    powsl = pow(sl, slresponse_sl_exp)  
    return  ( powsl / (1 + slresponse_k1_synth_coef*powsl ) ) 

def sugarresponse(sugar):
    powsugar = pow(sugar, sugarresponse_sugar_exp)  
    return (  (sugarresponse_k1_synth_coef + powsugar ) / powsugar) 

def I_plateau(eck, esl, esug):
    return ( I_base_synth_coef + I_sl_synthcoef*esl + I_ck_synthcoef*eck  + I_sugar_synthcoef*esug )/I_base_decay_coef

def eval_model(auxin, sugar, gr24 = 0, bap = 0):
    """ Main function of the model """
    sl = sl_plateau(auxin)+gr24
    ck = ck_plateau(auxin, sugar)+bap

    Sck = ckresponse(ck)
    Ssl = slresponse(sl)
    Ssugar = sugarresponse(sugar)

    I = I_plateau(Sck,Ssl,Ssugar)
    return sl, ck, Sck, Ssl, I




