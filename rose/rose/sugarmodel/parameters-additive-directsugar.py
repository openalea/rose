from defaultparameters import *

# defining parameters as paramname = value, lowerlimit, upperlimit

@defaultparameters
def CK():
      ck_auxin_synth_coef   = 0.790012936748, 0, 1000 
      ck_auxin_k_synth_coef = 0.959667760808, 0, 1000
      ck_sugar_synth_coef   = 0.245915750382, 0, 1000
      ck_sugar_k_synth_coef = 0.19089274493, 0, 1000
      ck_base_decay_coef    = 0.99, 0, 0.99

@defaultparameters
def SL():
      sl_auxin_synth_coef = 4.27188552189, 0, 1000
      sl_base_synth_coef  = 0.396, 0, 100000
      sl_base_decay_coef  = 0.99, 0, 0.99


@defaultparameters
def I():
      ckresponse_ck_k1_synth_coef     = 728.06384382, 0, 1000
      slresponse_k1_synth_coef  = 1.69523600756,  0, 1000
      sugarresponse_k1_synth_coef  = 13.6121341329,  0, 1000
      I_base_synth_coef               = 0.47815219768, 0, 1000
      I_sl_synthcoef                  = 1.57627594649,  0, 1000
      I_ck_synthcoef                  = 0.000324965113006,  0, 1000
      I_sugar_synthcoef               = 0.000548257616108,  0, 1000
      I_base_decay_coef               = 0.989963624887, 0, 0.99


