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
      k3  = 999.998122581, 0, 1000      
      k4  = 1.43459297626, 0, 1000      
      c3  = 0.122744157084, 0, 1000     
      a3  = 1.57033749145,  0, 1000     
      a4  = 279.498689669,  0, 1000  
      a5  = 1.17350080058,  0, 1000  
      b4  = 2.42641642596,  0, 1000  
      d3  = 0.988089269883, 0, 0.99  



