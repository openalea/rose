

# The optimizable parameters are defined in this file
paramfile = 'parameters-cubic.py'
execfile(paramfile, globals(),locals())

sl_auxin_exp = 2
ck_sugar_exp = 2
ck_auxin_exp = 1
ckresponse_ck_exp = 3
slresponse_sl_exp = 2
slresponse_sugar_exp = 2


from math import *


def sl_plateau(auxin):
    return ( sl_base_synth_coef +pow(auxin,sl_auxin_exp) / (sl_auxin_synth_coef+pow(auxin,sl_auxin_exp)) ) / sl_base_decay_coef


def ck_plateau(auxin, sugar):
    return (( ck_sugar_synth_coef * (pow(sugar, ck_sugar_exp) / (ck_sugar_k_synth_coef + pow(sugar, ck_sugar_exp) ) )  
             + (ck_auxin_synth_coef/(1+ck_auxin_k_synth_coef*pow(auxin, ck_auxin_exp)) ) ) 
             / ck_base_decay_coef )

def ckresponse(ck):
    return (pow(ck,ckresponse_ck_exp)/(ckresponse_ck_k1_synth_coef+pow(ck,ckresponse_ck_exp)) )

def slresponse(sl,sugar):
    powsl = pow(sl, slresponse_sl_exp)  
    powsugar = pow(sugar,slresponse_sugar_exp)
    return ( ( powsl / (1 + (slresponse_sugar_k1_synth_coef+slresponse_sugar_k2_synth_coef*powsugar)*powsl ) ) )

def I_plateau(eck,esl):
    return ( I_base_synth_coef + I_slck_synthcoef*esl/eck )/I_base_decay_coef

def eval_model(auxin, sugar, gr24 = 0, bap = 0):
    """ Main function of the model """
    sl = sl_plateau(auxin)+gr24
    ck = ck_plateau(auxin, sugar)+bap
    Sck = ckresponse(ck)
    Ssl = slresponse(sl, sugar)
    I = I_plateau(Sck,Ssl)
    return sl, ck, Sck, Ssl, I


#### Not optimized but part of the model

I_threshold = 3.
slope = 0.281857451404
intercept = 0.630237580994

def burst_delay_law(I):
    if I < I_threshold : return  (I - intercept)/ slope 
    return None

def I_law(duration):
    if not duration is None : return  duration * slope + intercept 
    return None


