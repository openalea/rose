from defaultparameters import *

# defining parameters as paramname = value, lowerlimit, upperlimit

@defaultparameters
def CK():
      c1  = 0.790012936748, 0, 1000  # alpha0
      b1  = 0.959667760808, 0, 1000  # alpha1
      a1  = 0.245915750382, 0, 1000  # alpha2
      k1  = 0.19089274493, 0, 1000   # k1
      d1  = 0.99, 0, 0.99            # alpha3

@defaultparameters
def SL():
      c2  = 0.344791998158, 0, 1000     # beta0
      a2  = 24.8935838411, 0 , 1000
      k2  = 294.578518524, 0, 100000           # k2
      d2  = 0.861979995395, 0, 0.99              # beta2


@defaultparameters
def I():
      k3  = 999.999593567, 0, 1000       # k3
      u1  = 4.80118658782e-13,  0, 1000   # sigma1
      u2  = 7.09685104032,  0, 1000      # sigma2
      c3  = 0.332015464625, 0, 1000      # delta0
      a3  = 5.640106629,  0, 1000      # delta1
      a4  = 287.533204963,  0, 1000  # delta2
      d3  = 0.987995826276, 0, 0.99      # delta3


