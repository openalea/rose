from defaultparameters import *

# defining parameters as paramname = value, lowerlimit, upperlimit

@defaultparameters
def CK():
      ck_auxin_synth_coef   = 0.790012936748, 0, 100000 
      ck_auxin_k_synth_coef = 0.959667760808, 0, 100000
      ck_sugar_synth_coef   = 0.245915750382, 0, 100000
      ck_sugar_k_synth_coef = 0.19089274493, 0, 100000
      ck_base_decay_coef    = 0.99, 0, 0.99

@defaultparameters
def SL():
      sl_auxin_synth_coef = 4.27188552189, 0, 100000
      sl_base_synth_coef  = 0.396, 0, 100000
      sl_base_decay_coef  = 0.99, 0, 0.99


@defaultparameters
def I():
      ckresponse_ck_k1_synth_coef     = 803.421171174, 0, 100000
      slresponse_sugar_k1_synth_coef  = 6.6838489915e-14,  0, 100000
      slresponse_sugar_k2_synth_coef  = 6.18151629277,  0, 100000
      I_base_synth_coef               = 0.359995245808, 0, 100000
      I_sl_synthcoef                  = 5.02575901989,  0, 100000
      I_ck_synthcoef                  = 0.000339635986326,  0, 100000
      I_base_decay_coef               = 0.989244936889, 0, 0.99


