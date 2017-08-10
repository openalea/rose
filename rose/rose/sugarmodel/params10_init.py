

ck_init  = 0
if 'CK' in globals():
  ck_auxin_synth_coef, ck_auxin_k_synth_coef, ck_sugar_synth_coef, ck_sugar_k_synth_coef, ck_base_decay_coef    = CK
else:
  ck_auxin_synth_coef    = 0.790015255143
  ck_auxin_k_synth_coef = 0.9596872476
  ck_sugar_synth_coef   = 0.245916756979
  ck_sugar_k_synth_coef = 0.190883693373
  ck_base_decay_coef    = 1.0

sl_init  = 0
if 'SL' in globals():
  sl_auxin_synth_coef, sl_base_synth_coef, sl_base_decay_coef  = SL
else:
  sl_auxin_synth_coef = 3.97552418348
  sl_base_synth_coef  = 0.407477073244
  sl_base_decay_coef  = 1.01869268311

cksignal_init  = 0
if 'CKsignal' in globals():
   cksignal_ck_k1_synth_coef   = CKsignal
else:
   cksignal_ck_k1_synth_coef   = 1.0

slsignal_init  = 0
if 'SLsignal' in globals():
  slsignal_sugar_k1_synth_coef, slsignal_sugar_k2_synth_coef  = SLsignal
else:
  slsignal_sugar_k1_synth_coef  = 0.4
  slsignal_sugar_k2_synth_coef = 3.08

init_brc1 = 0
if 'BRC1' in globals():
  brc1_base_synth_coef,brc1_slck_synthcoef,brc1_base_decay_coef  = BRC1
else:
  brc1_base_synth_coef    = 0.0935
  brc1_slck_synthcoef     = 0.1
  brc1_base_decay_coef    = 0.11


