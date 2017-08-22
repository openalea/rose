

ck_init  = 0
if 'CK' in globals():
  ck_auxin_synth_coef, ck_auxin_k_synth_coef, ck_sugar_synth_coef, ck_sugar_k_synth_coef, ck_base_decay_coef    = CK
else:
  ck_auxin_synth_coef    = 0.790012936748
  ck_auxin_k_synth_coef = 0.959667760808
  ck_sugar_synth_coef   = 0.245915750382
  ck_sugar_k_synth_coef = 0.19089274493
  ck_base_decay_coef    = 1.0

sl_init  = 0
if 'SL' in globals():
  sl_auxin_synth_coef, sl_base_synth_coef, sl_base_decay_coef  = SL
else:
  sl_auxin_synth_coef = 4.27188552189
  sl_base_synth_coef  = 0.396
  sl_base_decay_coef  = 1.01869268311


init_brc1 = 0
if 'BRC1' in globals():
  cksignal_ck_k1_synth_coef, slsignal_sugar_k1_synth_coef, slsignal_sugar_k2_synth_coef, brc1_base_synth_coef,brc1_slck_synthcoef,brc1_base_decay_coef  = BRC1
else:
  cksignal_ck_k1_synth_coef   = 0.553888258685
  slsignal_sugar_k1_synth_coef  = 35.295883754
  slsignal_sugar_k2_synth_coef = 9.95857429924
  brc1_base_synth_coef    = 0.623182402342
  brc1_slck_synthcoef     = -14.4105803451
  brc1_base_decay_coef    = 1.01140263087


