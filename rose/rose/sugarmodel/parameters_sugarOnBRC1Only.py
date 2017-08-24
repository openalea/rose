from defaultparameters import *



@defaultparameters
def CK():
      ck_auxin_synth_coef   = 0.790015255143, 0, 1000 
      ck_auxin_k_synth_coef = 0.9596872476, 0, 1000 
      ck_sugar_synth_coef   = 0.245916756979, 0, 1000 
      ck_sugar_k_synth_coef = 0.190883693373, 0, 1000 
      ck_base_decay_coef    = 0.99, 0, 0.99


@defaultparameters
def SL():
      sl_auxin_synth_coef = 4.27188552293, 0, 1000 
      sl_base_synth_coef  = 0.395999999962, 0, 1000 
      sl_base_decay_coef  = 0.989999999902, 0, 0.99


@defaultparameters
def BRC1():
      ckresponse_ck_k1_synth_coef     = 0.180618026978, 0, 1000 
      slresponse_sugar_k1_synth_coef  = 0.22462147474, 0, 1000 
      brc1_base_synth_coef            = 0.626214062313, 0, 1000 
      brc1_slck_synthcoef             = 0.355306677632, 0, 1000 
      brc1_sugar_base_synthcoef       = 0.233994896088, 0, 1000 
      brc1_sugar_k_synthcoef          = 3.60939359009, 0, 1000 
      brc1_base_decay_coef            = 0.989989367875, 0, 0.99


