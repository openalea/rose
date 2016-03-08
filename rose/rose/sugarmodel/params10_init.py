

ck_init  = 0
if 'CK' in globals():
  ck_base_synth_coef, ck_sugar_synth_coef, ck_sugar_k_synth_coef, ck_auxin_k_synth_coef, ck_base_decay_coef    = CK
else:
  ck_base_synth_coef    = 0.0320929759286
  ck_sugar_synth_coef   = 0.0837621770959
  ck_sugar_k_synth_coef = 3.79615340561e-09
  ck_auxin_k_synth_coef = 1.16767779717
  ck_base_decay_coef    = 0.0274843284672

sl_init  = 0
if 'SP' in globals():
  sl_auxin_synth_coef, sl_base_synth_coef, sl_base_decay_coef  = SL
else:
  sl_auxin_synth_coef = 0.02
  sl_base_synth_coef  = 0.1
  sl_base_decay_coef  = 0.1


init_brc1 = 0
if 'BRC1' in globals():
  brc1_base_synth_coef, brc1_slck_synthcoef, brc1_sugar_k_synth_coef, brc1_sl_k_synth_coef, brc1_ck_k1_synth_coef,brc1_ck_k2_synth_coef,brc1_ck_synth_coef, brc1_base_decay_coef  = BRC1
else:
  brc1_base_synth_coef    = 0.419668980571
  brc1_slck_synthcoef     = 4685.25205023
  brc1_sugar_k_synth_coef = -444.698872429 # gamma2
  brc1_sl_k_synth_coef    = 198.538575094 # k4
  brc1_ck_synth_coef      = 4.8289814571e-06 # gamma3
  brc1_ck_k1_synth_coef   = -1.55053204493
  brc1_ck_k2_synth_coef   = 0.426675637302
  brc1_base_decay_coef    = 11.454382799


