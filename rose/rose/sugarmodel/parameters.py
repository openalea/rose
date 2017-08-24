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
def BRC1():
      ckresponse_ck_k1_synth_coef     = 0.335227513165, 0, 1000
      slresponse_sugar_k1_synth_coef  = 5.27978524571,  0, 1000
      slresponse_sugar_k2_synth_coef  = 2.69224386227,  0, 1000
      brc1_base_synth_coef          = 0.649986436378, 0, 1000
      brc1_slck_synthcoef           = 4.34411430799,  0, 1000
      brc1_base_decay_coef          = 0.989670071812,  0, 0.99


