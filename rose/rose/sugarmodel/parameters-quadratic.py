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
      sl_base_synth_coef  = 0.396, 0, 1000
      sl_base_decay_coef  = 0.99, 0, 0.99


@defaultparameters
def I():
      ckresponse_ck_k1_synth_coef     = 368.349294272, 0, 1000
      slresponse_sugar_k1_synth_coef  = 1.64757277011,  0, 1000
      slresponse_sugar_k2_synth_coef  = 3.16768039884,  0, 1000
      I_base_synth_coef               = 0.817618509982, 0, 1000
      I_slck_synthcoef                = 0.00605564966771,  0, 1000
      I_base_decay_coef               = 0.986266847403, 0, 0.99


