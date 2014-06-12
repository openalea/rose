

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
  
  dt = 0.05
  
  DEGRADATION = True
  DIFFUSION   = True


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
    self.setdefault(auxin=0, sugar=0)
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
                    auxin_degrad_coef = P.default_auxin_degrad_coef,
                    auxin_target_concentration = self.auxin)



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


#
def dfluxij(fluxij, pi, pj, verbose = False):
  
  selfenhancingterm = pi.active_transport_coef * pi.auxin * P.h_coef * h(fluxij)
  
  degradationterm = - P.pin_degrad_coeff * fluxij
  
  diffusionterm1 =  pi.pin_synth_coeff * pi.active_transport_coef * pi.auxin  
  diffusionterm1 -= pj.pin_synth_coeff * pj.active_transport_coef * pj.auxin 
  
  diffusionterm2 =  (P.pin_degrad_coeff * P.diffusion_coef * (pi.auxin - pj.auxin)) 
  
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



def process_transport(p, pu = None, pd = None, pl = None, verbose = False):
  if not pl is None: 
    if len(pl) == 0: pl = None
    else: pl = pl[0]
  
  a = p.auxin
  fu, fd, fl  = p.flux_up, p.flux_down, p.flux_lat
  pinu, pind, pinl = p.pin_up , p.pin_down, p.pin_lat
  
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
  
  ra += - p.auxin_degrad_coef * a # auxin degradation
  ra -= net_flux # sum phi_ji sij / vi
  
  p.auxin += ra*P.dt 
  
  #assert 0. <= p.auxin <= 10. 
  # dPiu/dt, dPid/dt => rpinu, rpind
  
  # pin concentration.
  net_rpin = 0
  if pu:
    rpinu = p.pin_synth_coeff - P.pin_degrad_coeff * p.pin_up 
    if not P.innate_polarity:
      hu = P.h_coef * h(fu)
      rpinu += hu
    p.pin_up += rpinu*P.dt
    net_rpin += rpinu
  
  if pd:
    hd = P.h_coef * h(fd)
    rpind = hd + p.pin_synth_coeff - P.pin_degrad_coeff*p.pin_down 
    p.pin_down += rpind*P.dt
    net_rpin += rpind
    
  if pl:
    rpinl =  p.pin_synth_coeff - P.pin_degrad_coeff*p.pin_lat
    if not P.innate_polarity:
      hl = P.h_coef * h(fl)
      rpinl += hl
    p.pin_lat += rpinl*P.dt
    net_rpin += rpinl
  
  return p

