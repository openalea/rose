paramfile = 'parameters_sugarOnBRC1Only.py'

execfile(paramfile,globals(),locals())

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
    return ( ck_sugar_synth_coef * (pow(sugar, ck_sugar_exp) / 
        (ck_sugar_k_synth_coef + pow(sugar, ck_sugar_exp) ) )  + (ck_auxin_synth_coef/(1+ck_auxin_k_synth_coef*pow(auxin, ck_auxin_exp)) ) ) * (1./ck_base_decay_coef)

def ckresponse(ck,bap):
    return (pow(ck,ckresponse_ck_exp)/(ckresponse_ck_k1_synth_coef+pow(ck,ckresponse_ck_exp)) )

def slresponse(sl,gr24):
    powsl = pow(sl+gr24, slresponse_sl_exp)  
    return ( ( powsl / (slresponse_sugar_k1_synth_coef+powsl ) ) )

def brc1_plateau(eck,esl,sugar):
    return ( brc1_base_synth_coef + brc1_slck_synthcoef * 1/(brc1_sugar_base_synthcoef+sugar*sugar/(brc1_sugar_k_synthcoef+sugar*sugar)) * esl/eck )/brc1_base_decay_coef

def eval_model(auxin, sugar, gr24 = 0, bap = 0):
    sl = sl_plateau(auxin)+gr24
    ck = ck_plateau(auxin, sugar)+bap
    Sck = ckresponse(ck,bap)
    Ssl = slresponse(sl,gr24)
    brc1 = brc1_plateau(Sck,Ssl,sugar)
    #print auxin, sugar, '-->' , sl, ck, brc1
    return sl, ck, Sck, Ssl, brc1


#### Not optimized !!! But part of the model

brc1_threshold = 3.
slope = 0.281857451404
intercept = 0.630237580994

def burst_delay_law(brc1):
    if brc1 < brc1_threshold : return  (brc1 - intercept)/ slope 
    return 0

def brc1_law(duration):
    if not duration is None : return  duration * slope + intercept # (duration - intercept)/ slope 
    return None


