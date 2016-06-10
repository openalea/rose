from numpy import arange, array
from numpy.linalg import norm
from model2 import burst_delay_law, brc1_law

def cell_number(nbcycle, proliferationratio, initialnumber):
    if proliferationratio > 1 : proliferationratio = 1
    if proliferationratio < 0 : proliferationratio = 0
    #print nbcycle,  pow(2,nbcycle) * pow(proliferationratio, (nbcycle*(nbcycle-1)/2.) ), sum([(1 - pow(proliferationratio,m-1)) * pow(2,m-1) * pow(proliferationratio,(m-1)*(m-2)/2.) for m in xrange(1,nbcycle) ])
    return int(initialnumber * ( pow(2,nbcycle) *  pow(proliferationratio, (nbcycle*(nbcycle-1)/2.) ) + sum([(1 - pow(proliferationratio,m-1)) * pow(2,m-1) * pow(proliferationratio,(m-1)*(m-2)/2.) for m in xrange(1,nbcycle+1) ])))/2

def plot_cell_number(nbcycle, proliferationratio, initialnumber):
    import matplotlib.pyplot as plt
    cycles  = range(1, nbcycle+1)
    
    nbcells = [cell_number(i, proliferationratio, initialnumber) for i in xrange(1,nbcycle+1)]
    plt.plot(cycles, nbcells)
    print proliferationratio, nbcells
    plt.show()

def plot_cell_number_range(nbcycle, initialnumber):
    import matplotlib.pyplot as plt
    cycles  = range(1, nbcycle+1)
    
    for proliferationratio in arange(0,0.90001,0.05):    
        nbcells = [cell_number(i, proliferationratio, initialnumber) for i in xrange(1,nbcycle+1)]
        plt.plot(cycles, nbcells)
        print proliferationratio, nbcells
    plt.show()



sugarlevels = [0.1, 0.5, 1 , 2.5]
auxinlevels = [0,1,2.5,5]
brc1levels = [[1.0108692768952487, 0.6722887068218482, 0.45498203294721207, 0.2762034309804555], 
              [1.629482933567273, 1.0740412960652266, 0.7400141770201679, 0.49290843510338356], 
              [2.6868882741803595, 2.0299595484866377, 1.5408027394180974, 1.182167415167441], 
              [3.323413276025248, 2.924482859726581, 2.4539200431896204, 2.038817303128552]]

brc1levels = [[0.9390915273757392, 0.8238670902467156, 0.6190966373948812, 0.3251975707377661], 
 [1.428089655068316, 1.250125945909101, 0.9285607232931054, 0.45489729554261354], 
 [2.9014103421558497, 2.629416140968695, 2.0658714867815857, 1.0304118607452986], 
 [4.058224735682963, 3.8927793059789857, 3.4955638754259204, 2.3034587241871343]]

durations =  [[3 , 2, 1.5, 1],
              [None, 6, 3, 2],
              [None, None, 9, 3.5],
              [None, None, None, 7]]


def generate_brc1_levels():
    global brc1levels
    from openalea.lpy import Lsystem
    lsysfile = 'rosebudJan15-model1-v1.lpy'
    targetcontents = []
    for auxin in auxinlevels:
        targetcontents.append(list())
        for sugar in sugarlevels:
            simu = Lsystem(lsysfile, {'AUXIN': auxin, 'SUGAR' : sugar} )
            ls = simu.iterate()
            res = ls[-1].p
            targetcontents[-1].append(res.brc1)
    brc1levels =  targetcontents
    print brc1levels    

import numpy as np
brc1targets = np.array([1.,  0.5, 0.4, 2.9, 2.1, 1.])
def generate_measured_brc1_levels():
    global brc1levels, sugarlevels, auxinlevels, durations
    #import optimize
    #t = optimize.brc1targets
    t = brc1targets
    brc1levels = [[t[0], t[1], t[2]  ],
                  [t[3], t[4], t[5]  ]]
    durations =  [[3 , 1.5, 1],
                  [None, 9, 3.5]]    
    sugarlevels = [0, 1 , 2.5]
    auxinlevels = [0,2.5]


def checkbrc1inhibitionlevel():
    mininhibition = max([max(b) for b in brc1levels])
    maxoccur      = min([min(b) for b in brc1levels])
    for brc1cond, durationcond in zip(brc1levels,durations):
        for brc1, duration in zip(brc1cond, durationcond):
            if duration is None :
                if mininhibition > brc1: mininhibition = brc1
            else: 
                if maxoccur < brc1: maxoccur = brc1
    print '*', maxoccur, mininhibition
    assert mininhibition > maxoccur


brc1targets =  [1.,  0.5,  0.4,  2.9,  2.1,  1]
days        =  [3,   2,     1,   15,  9,  4]
cellcycle   = 1
initialcellnb = 20
targetcellnb = 100
maxbrc1level = 1.6

def showbrc1durationrelation():
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy import stats

    nbauxcond = len(auxinlevels)
    nbsugcond = len(sugarlevels)
    brc1values, durationvalues = [[] for i in xrange(nbauxcond)],[[] for i in xrange(nbauxcond)]
    i = 0
    x,y = [],[]
    for brc1cond, durationcond in zip(brc1levels,durations):
        for brc1, duration in zip(brc1cond, durationcond):
            if not duration is None :
                brc1values[i].append(brc1)
                x.append(brc1)
                durationvalues[i].append(duration)
                y.append(duration)
        i += 1
    colors = [(1,0,0),(0,1,0),(0,0,1),(1,0,1)]
    for i in xrange(nbauxcond):
        print '-',brc1values[i],durationvalues[i]
        #plt.plot(brc1values[i],durationvalues[i],'ro',color=colors[3-i], label = str(int(sugarlevels[i]*100))+' mM sucrose')
        plt.plot(durationvalues[i],brc1values[i],'ro',color=colors[3-i], label = str(auxinlevels[i])+' $\mu$M NAA')
    print x
    print y
    x,y = y,x
    x = np.array(x)
    slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
    print slope, intercept, r_value, p_value, std_err   

    plt.plot( x, slope*x+intercept, '-k', label = ('$y=%.4f x '+('+ ' if intercept > 0 else '') +'%.4f, r^2=%.4f$') % (slope, intercept, r_value)) 
    plt.margins(0.2)
    plt.legend(loc=2)
    plt.xlabel('Burst delay')
    plt.ylabel('BRC1 level')
    plt.show()    

def estimate_param(param):
    a,b,c= param
    def f(x): return a + b * x + c * (x**2)
    result = []
    for brc1, bday in zip(brc1targets, days):
        proliferationratio = f(brc1)
        cell_nb = cell_number(int(bday / cellcycle), proliferationratio, initialcellnb)
        result.append(float(targetcellnb - cell_nb))
    return array(result)

def normed_estimate_param(param):
    res = norm(estimate_param(param))
    print param, res
    return res




def generate_burst_delay_fig():
    import diagram
    reload(diagram)
    from diagram import generate_fig_func2
    generate_fig_func2(lambda res : burst_delay_law(res.brc1),'Burst Delay',legendpos=(0.92,1.1))

if __name__ == '__main__':
    #generate_burst_delay_fig()
    #generate_brc1_levels()
    generate_measured_brc1_levels()
    #try:
    #    checkbrc1inhibitionlevel()
    #except:
    #    print 'No valid inhibition level'
    showbrc1durationrelation()
    #checkbrc1inhibitionlevel()
    # plot_cell_number_range(10,  10)
