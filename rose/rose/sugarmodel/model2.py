
if 'ALL' in globals():
  CK = ALL[:5]
  SL = ALL[5:8]
  CKsignal = ALL[8:9]
  SLsignal = ALL[9:11]
  BRC1 = ALL[11:]

if 'BRC1'in globals():
  BRC1 = [abs(v) for v in BRC1]


paramfile = 'params10_init.py'

execfile(paramfile,globals(),locals())

sl_auxin_exp = 2
ck_sugar_exp = 2
ck_auxin_exp = 1
cksignal_ck_exp = 3
slsignal_sl_exp = 2
slsignal_sugar_exp = 2


import params_generate; reload(params_generate)
from params_generate import param_order


params = param_order(paramfile)
for p in params:
  if globals()[p] < 0 : globals()[p] = abs(globals()[p])
  if globals()[p] > 1000 : globals()[p] = 1000
  if 'decay' in p and globals()[p] > 0.99 : globals()[p] = 0.99

from math import *


def sl_plateau(auxin):
    return ( sl_base_synth_coef +pow(auxin,sl_auxin_exp) / (sl_auxin_synth_coef+pow(auxin,sl_auxin_exp)) ) / sl_base_decay_coef


def ck_plateau(auxin, sugar):
    return ( ck_sugar_synth_coef * (pow(sugar, ck_sugar_exp) / 
        (ck_sugar_k_synth_coef + pow(sugar, ck_sugar_exp) ) )  + (ck_auxin_synth_coef/(1+ck_auxin_k_synth_coef*pow(auxin, ck_auxin_exp)) ) ) * (1./ck_base_decay_coef)

def cksignal(ck,bap):
    return (pow(ck,cksignal_ck_exp)/(cksignal_ck_k1_synth_coef+pow(ck,cksignal_ck_exp)) )

def slsignal(sl,sugar,gr24):
    powsl = pow(sl+gr24, slsignal_sl_exp)  
    powsugar = pow(sugar,slsignal_sugar_exp)
    return ( ( powsl / (1 + (slsignal_sugar_k1_synth_coef+slsignal_sugar_k2_synth_coef*powsugar)*powsl ) ) )

def brc1_plateau(eck,esl):
    return ( brc1_base_synth_coef + brc1_slck_synthcoef*esl/eck )/brc1_base_decay_coef

def eval_model(auxin, sugar, gr24 = 0, bap = 0):
    sl = sl_plateau(auxin)+gr24
    ck = ck_plateau(auxin, sugar)+bap
    Sck = cksignal(ck,bap)
    Ssl = slsignal(sl,sugar,gr24)
    brc1 = brc1_plateau(Sck,Ssl)
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


