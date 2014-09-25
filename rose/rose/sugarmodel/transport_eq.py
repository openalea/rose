

class SimuParameters:
  innate_polarity = True
  ACTIVATION = False
  with_auxin_max_level = True
    
  default_active_transport_coef = 0.5 # T
  diffusion_coef = 0.1 # D
  
  # axin synthesis and degradation coefficient
  default_auxin_synth_coef = 0.5 # \rho (c_i)
  default_auxin_degrad_coef = 0.1 # v (a)
  
  default_pin_synth_coeff = 0.0 # rho_0
  pin_degrad_coeff = 10  # \mu
    
  # parameter of the flux feedback function
  h_coef = 7.5 # rho_i->j in the paper
  # non linear exponent of the flux feedback function
  n = 3
  # hill saturation coef
  K = 1.3
  
  default_sugar = 0
  default_ck = 0
  default_ck_synth_coef = 0
  default_ck_degrad_coef =0
  ck_diffusion_coef = 0.2
  
  default_sl = 0
  default_sl_synth_coef = 0
  default_sl_degrad_coef = 0
  sl_diffusion_coef = 0.2
  
  default_pin_sl_interaction = 0
  
  dt = 0.05
  
  DEGRADATION = True
  DIFFUSION   = True

  ck_auxin_interaction = 0
  ck_sugar_interaction = 0
  
  # strigolactone coeficient
  sl_auxin_interaction = 0
  sl_sugar_interaction = 0
  
  auxin_sugar_interaction = 0


P = SimuParameters()

def set_simu_parameters(params):
  global P
  P = params


from openalea.lpy import ParameterSet

class OrganParameter(ParameterSet):
  def __init__(self, **kwd):
#    """ State variable of a compartment.
#    
#    Parameters
#    ==========
#      - auxin : auxin concentration
#      - sugar : sugar concentration
#      - pin: PIN concentration in the organ not affected to the membranes
#      - pin_up = 0, # PIN surfacic concentration on upward membrane
#      - pin_down =0, # PIN surfacic concentration on downard membrane
#      pin_lat=0 # PIN surfacic concentration on lateral membrane
#      flux_up = 0 # flux coming from upward membrane (positive if entering the cell)
#      flux_down =0, # flux coming from downard membrane
#      flux_lat=0 # flux coming from lateral membrane
#    """
#    
    ParameterSet.__init__(self, **kwd)
    
    # auxin and sugar concentration
    self.setdefault(auxin=0, sugar=P.default_sugar)
    self.setdefault(auxin_sugar_interaction = P.auxin_sugar_interaction)
    # topological situation
    self.setdefault(first = False, order = 0)
    # pin concentration
    # PIN surfacic concentration on the upward, downward and lateral membrane
    self.setdefault(pin_up=0, pin_down=0,  pin_lat=0)
    self.setdefault(active_transport_coef = P.default_active_transport_coef)
    
    self.setdefault(pin_synth_coeff = P.default_pin_synth_coeff)
    
    # flux coming from the upward, downward and lateral membrane (negative if entering the cell)
    self.setdefault(flux_up=0, flux_down=0, flux_lat=0)
    # auxin coeficient
    self.setdefault(auxin_synth_coef  = P.default_auxin_synth_coef, 
                    auxin_decay_coef = P.default_auxin_decay_coef,
                    auxin_target_concentration = self.auxin)
    # cytokinin coeficient
    self.setdefault(ck = P.default_ck,
                    ck_synth_coef = P.default_ck_synth_coef,
                    ck_decay_coef = P.default_ck_decay_coef,
                    ck_auxin_interaction = P.ck_auxin_interaction,
                    ck_sugar_interaction = P.ck_sugar_interaction)
    # strigolactone coeficient
    self.setdefault(sl = P.default_sl,
                    sl_synth_coef = P.default_sl_synth_coef,
                    sl_decay_coef= P.default_sl_decay_coef,
                    sl_auxin_interaction = P.sl_auxin_interaction,
                    sl_sugar_interaction = P.sl_sugar_interaction)
                    
    self.setdefault(pin_sl_interaction=P.default_pin_sl_interaction,
                    pin_sugar_interaction=P.pin_sugar_interaction)

class ApexParameter(OrganParameter):
  def __init__(self, **kwd):
    OrganParameter.__init__(self, **kwd)
    self.setdefault(active=False)



def h(flux) :
  if flux < 0.:  return 0.

  fluxn = abs(flux) ** P.n
  return  (fluxn / (P.K**P.n + fluxn))



def fluxij(ci, cj, 
           pinij, pinji,  
           active_transport_coef_i, active_transport_coef_j):
    
    return (pinij * active_transport_coef_i * ci - pinji * active_transport_coef_j *cj) +  P.diffusion_coef * (ci-cj)



def dfluxij(fluxij, pi, pj, verbose = False):
  
  selfenhancingterm = pi.active_transport_coef * pi.auxin * P.h_coef * h(fluxij)
  
  degradationterm = - P.pin_decay_coeff * fluxij
  
  diffusionterm1 =  pi.pin_synth_coeff * pi.active_transport_coef * pi.auxin  
  diffusionterm1 -= pj.pin_synth_coeff * pj.active_transport_coef * pj.auxin 
  
  diffusionterm2 =  (P.pin_decay_coeff * P.diffusion_coef * (pi.auxin - pj.auxin)) 
  
  if verbose : print diffusionterm1, diffusionterm2
  diffusionterm = diffusionterm1 + diffusionterm2
  
  result = 0
  if fluxij > 0.:
     result =  selfenhancingterm 
  if P.DEGRADATION:
     result += degradationterm 
  if P.DIFFUSION:
     result += diffusionterm
  return result

def basediffusion(propname, p, pu, pd, pl, diffusioncoef):
    prop = getattr(p,propname)
    deltaprop = 0
    if pu: deltaprop += (getattr(pu,propname)-prop)
    if pd: deltaprop += (getattr(pd,propname)-prop)
    if pl: deltaprop += (getattr(pl,propname)-prop)
    
    dp = deltaprop*diffusioncoef + getattr(p,propname+'_synth_coef') - getattr(p,propname+'_decay_coef')*prop
    return dp 

def process_transport(p, pu = None, pd = None, pl = None, verbose = False):
  if not pl is None: 
    if len(pl) == 0: pl = None
    else: pl = pl[0]
  
  a = p.auxin
  fu, fd, fl  = p.flux_up, p.flux_down, p.flux_lat
  pinu, pind, pinl = p.pin_up , p.pin_down, p.pin_lat
  pinsum = pinu+ pind+ pinl
  
  if pu: au =  pu.auxin
  if pd: ad =  pd.auxin
  if pl: al = pl.auxin
    
  p = p.copy()
  
  # fluxs are counted negativelly when they get into p
  net_flux = 0
  if pu:
    p.flux_up = fluxij(a, au, p.pin_up, pu.pin_down, p.active_transport_coef, pu.active_transport_coef)
    net_flux += p.flux_up 
  
  if pd:
    if pd.order < p.order:   pdpin = pd.pin_lat
    else:                    pdpin = pd.pin_up
    
    p.flux_down = fluxij(a,ad,p.pin_down, pdpin, p.active_transport_coef, pd.active_transport_coef)
    net_flux +=  p.flux_down

  if pl:
    p.flux_lat = fluxij(a,al,p.pin_lat,pl.pin_down,p.active_transport_coef,pl.active_transport_coef)                
    net_flux += p.flux_lat
  
  if verbose : print p.flux_up, p.flux_down, p.flux_lat
  
  # rate of change of auxin
  ra = 0
  
  # auxin synthesis
  if not P.with_auxin_max_level:
      ra = p.auxin_synth_coef 
  else:
      diffauxin = p.auxin_target_concentration - a
      ra = p.auxin_synth_coef * (diffauxin if diffauxin > 0 else 0)  # auxin synthesis
  
  ra += - p.auxin_decay_coef * a # auxin degradation
  ra -= net_flux # sum phi_ji sij / vi
  
  ra += p.auxin_sugar_interaction * a * p.sugar
  
  p.auxin += ra*P.dt 
  
  #assert 0. <= p.auxin <= 10. 
  # dPiu/dt, dPid/dt => rpinu, rpind
  
  # pin concentration.
  net_rpin = 0
  if pu:
    rpinu = p.pin_synth_coeff - P.pin_decay_coeff * p.pin_up  - p.pin_sl_interaction*(p.pin_up*p.sl)
    if not P.innate_polarity:
      hu = P.h_coef * h(fu)
      rpinu += hu
    rpinu -= p.pin_sl_interaction * p.pin_up * p.sl
    rpinu += p.pin_sugar_interaction * p.pin_up * p.sugar
    p.pin_up += rpinu*P.dt
    net_rpin += rpinu
  
  if pd:
    hd = P.h_coef * h(fd)
    rpind = hd + p.pin_synth_coeff - P.pin_decay_coeff*p.pin_down   - p.pin_sl_interaction*(p.pin_down*p.sl)
    p.pin_down += rpind*P.dt
    rpind -= p.pin_sl_interaction * p.pin_down * p.sl
    rpind += p.pin_sugar_interaction * p.pin_down * p.sugar
    net_rpin += rpind
    
  if pl:
    rpinl =  p.pin_synth_coeff - P.pin_decay_coeff*p.pin_lat   - p.pin_sl_interaction*(p.pin_lat*p.sl)
    if not P.innate_polarity:
      hl = P.h_coef * h(fl)
      rpinl += hl
    rpinl -= p.pin_sl_interaction * p.pin_lat * p.sl
    rpinl += p.pin_sugar_interaction * p.pin_lat * p.sugar
    p.pin_lat += rpinl*P.dt
    net_rpin += rpinl
  
  
  # citokinin
  dck = basediffusion('ck', p, pu, pd, pl, P.ck_diffusion_coef)
  dck -= p.ck_auxin_interaction * p.ck * a
  dck += p.ck_sugar_interaction * p.ck * p.sugar
  p.ck = dck*P.dt
  
  #strigolactone
  dsl = basediffusion('sl', p, pu, pd, pl, P.sl_diffusion_coef)
  dsl += p.sl_auxin_interaction * p.sl * a
  dsl -= p.sl_sugar_interaction * p.sl * p.sugar
  p.sl = dsl*P.dt
  
  # brc1
  if hasattr(p,'brc1'):
    brc1 = p.brc1
    dbrc1 = - p.ck_brc1_interaction *(brc1*p.ck) + p.sl_brc1_interaction *(brc1*p.sl) - p.brc1_decay_coef*brc1 + p.brc1_synth_coef
    p.brc1 += dbrc1*P.dt
  
  # growth
  if hasattr(p,'g'):
    g = p.g
    dg = p.ck_g_interaction * (p.ck*g) - p.brc1_g_interaction *(p.brc1*g) + p.auxflux_g_interaction *(g * net_flux) + p.auxin_g_interaction *(p.auxin*g) - p.g_decay *g
    p.g += dg*P.dt
  
  return p

