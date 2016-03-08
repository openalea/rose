
if not 'GR24' in globals():
  GR24 = 0

if not 'BAP' in globals():
  BAP = 0

if 'ALL' in globals():
  CK = ALL[:5]
  SL = ALL[5:8]
  BRC1 = ALL[8:]

if 'BRC1'in globals():
  BRC1 = [abs(v) for v in BRC1]


paramfile = 'params10_init.py'

execfile(paramfile,globals(),locals())
ck_sugar_exp = 2
ck_auxin_exp = 2
ck_ckdecay_exp = 2

brc1_sugar_coef = 1
brc1_ck_coef = 2
brc1_sl_coef = 2

import params_generate; reload(params_generate)
from params_generate import param_order


params = param_order(paramfile)
for p in params:
  if globals()[p] < 0 : globals()[p] = abs(globals()[p])
  if globals()[p] > 1000 : globals()[p] = 1000
  if 'decay' in p and globals()[p] > 0.99 : globals()[p] = 0.99

from math import *


def sl_plateau(auxin):
    return (sl_base_synth_coef + sl_auxin_synth_coef*auxin) / sl_base_decay_coef


def ck_plateau(auxin, sugar):
    return pow( (ck_base_synth_coef + ck_sugar_synth_coef * (pow(sugar, ck_sugar_exp) / 
        (ck_sugar_k_synth_coef + pow(sugar, ck_sugar_exp) ) ) ) * (1./(ck_auxin_k_synth_coef + pow(auxin, ck_auxin_exp ) )) * (1./ck_base_decay_coef), 1./ ck_ckdecay_exp )



def brc1_plateau(ck, sl, sugar, gr24, bap):
    powsl = pow(sl+gr24, brc1_sl_coef)
    powck = pow(ck+bap, brc1_ck_coef)
    
    res =  brc1_slck_synthcoef 
    res *= (powsl / (brc1_sl_k_synth_coef + brc1_sugar_k_synth_coef * powsl * pow(sugar,brc1_sugar_coef)))  # Stimulation by sl
    res *= (brc1_ck_k1_synth_coef + brc1_ck_synth_coef*powck)/(brc1_ck_k2_synth_coef + powck)                   # Inhibition by ck
    res += brc1_base_synth_coef
    res /= brc1_base_decay_coef
    return res

    ## Attempt : 
    # mbrc1_sl_k_synth_coef = brc1_sl_k_synth_coef * (1 + pow(sugar,brc1_sugar_coef)/ brc1_sugar_k_synth_coef)
    # res *= (powsl / (mbrc1_sl_k_synth_coef + powsl ))  # Stimulation by sl

    #res /=  (brc1_sugar_k_synth_coef + brc1_sugar_synth_coef * pow(sugar,brc1_sugar_coef))          # Inhibition by sugar

def eval_model(auxin, sugar, gr24 = 0, bap = 0):
    sl = sl_plateau(auxin)
    ck = ck_plateau(auxin, sugar)
    brc1 = brc1_plateau(ck, sl, sugar, gr24, bap)
    #print auxin, sugar, '-->' , sl, ck, brc1
    return sl, ck, brc1
