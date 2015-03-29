

# to have slower burst
ck_init  = 0
if 'CK' in globals():
  ck_base_synth_coef, ck_sugar_synth_coef, ck_sugar_k_synth_coef, ck_auxin_k_synth_coef, ck_base_decay_coef    = CK
else:
  ck_base_synth_coef    = 0.01 
  ck_sugar_synth_coef   = 0.04 
  ck_sugar_k_synth_coef = 0.41  
  ck_auxin_k_synth_coef = 0.52
  ck_base_decay_coef    = 0.02

sl_init  = 0
if 'SP' in globals():
  sl_auxin_synth_coef, sl_base_synth_coef, sl_base_decay_coef = SL
else:
  sl_auxin_synth_coef = 0.02
  sl_base_synth_coef  = 0.1
  sl_base_decay_coef  = 0.1


slp_init = 0
if 'SLP' in globals():
  slp_sugar_synth_coef, slp_sugar_k_synth_coef, slp_decay_coef = SLP
else:
  slp_sugar_synth_coef   = 0.03
  slp_sugar_k_synth_coef = 0.8
  slp_decay_coef         = 0.037



init_brc1 = 0
if 'BRC1' in globals():
  brc1_base_synth_coef, brc1_slp_synth_coef, brc1_ck_synth_coef, brc1_ck_k_synth_coef, brc1_base_decay_coef = BRC1
else:
  brc1_base_synth_coef = 0.1
  brc1_slp_synth_coef  = 0.45
  brc1_ck_synth_coef   = 0.6/4
  brc1_ck_k_synth_coef = 0.5
  brc1_base_decay_coef = 1

