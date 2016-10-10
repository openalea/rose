

ck_init  = 0
if 'CK' in globals():
  ck_base_synth_coef, ck_sugar_synth_coef, ck_sugar_k_synth_coef, ck_auxin_k_synth_coef, ck_base_decay_coef    = CK
else:
  ck_base_synth_coef    = 0.735
  ck_sugar_synth_coef   = 0.236
  ck_sugar_k_synth_coef = 0.015
  ck_auxin_k_synth_coef = 0.73
  ck_base_decay_coef    = 1

sl_init  = 0
if 'SP' in globals():
  sl_auxin_synth_coef, sl_base_synth_coef, sl_base_decay_coef  = SL
else:
  sl_auxin_synth_coef = 0.1
  sl_base_synth_coef  = 0.3
  sl_base_decay_coef  = 1.0


init_brc1 = 0
if 'BRC1' in globals():
  brc1_base_synth_coef, brc1_slck_synthcoef, brc1_sugar_k_synth_coef, brc1_sl_k_synth_coef, brc1_ck_k1_synth_coef,brc1_ck_k2_synth_coef,brc1_ck_synth_coef, brc1_base_decay_coef  = BRC1
else:
  brc1_base_synth_coef    = 0.22
  brc1_slck_synthcoef     = 1.4906671569
  brc1_sugar_k_synth_coef = 0.728873984321
  brc1_sl_k_synth_coef    = 0.179806097238
  brc1_ck_synth_coef      = 0.01
  brc1_ck_k1_synth_coef   = 17.278879128
  brc1_ck_k2_synth_coef   = 4.66442560191
  brc1_base_decay_coef    = 0.523651612781


