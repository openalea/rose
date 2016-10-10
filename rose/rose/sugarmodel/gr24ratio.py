def ratio(k, sl):
    return (k * 100 + sl) / (k * 50 + sl)


execfile('params10_init.py')

import model2; reload(model2)
from model2 import brc1_plateau, eval_model
from numpy import arange
from math import *


def bratio(sugar, gr24 = 1.4):
    ck = 0.4
    sl = 0.2
    a = brc1_plateau(ck, sl, sugar, gr24, 0)
    b = brc1_plateau(ck, sl, sugar, 0, 0)
    return a / b, a, b

def bratioofratio(gr24 = 1.4): 
    return bratio(0.5, gr24)[0] / bratio(1, gr24)[0]

def test_gr24():
    g = 0.2
    print g, bratioofratio(g), bratio(0.5,g), bratio(1,g)



def gr24simu(attname, condition, gr24value = 0, bapvalue = 0):
    from openalea.lpy import Lsystem
    targetcontents = []
    for auxin, sugar in conditions:
            namespace = { } 
            execfile(modelfile, namespace)
            eval_model = namespace['eval_model']
            sl, ck, brc1 = eval_model(auxin, sugar, gr24value, bapvalue)
            resvalues = { 'sl' : sl , 'ck' : ck, 'brc1' : brc1 }
            if type(attname) == str:
                res = resvalues[attname]
                targetcontents.append(res)
            else:
                for att in attname:
                    res = resvalues[att]
                    targetcontents.append(res)
    return targetcontents



def plot_brc1_gr24():
    import matplotlib.pyplot as plt
    delta = 0.01
    sugar = list(arange(0.1, 3,0.01))
    possugar0_5 = [i for i,v in enumerate(sugar) if abs(v-0.5) < delta/2][0]
    possugar1 = [i for i,v in enumerate(sugar) if abs(v-1.0) < delta/2][0]

    ck = 0.4
    sl = 0.2
    gr24ev = lambda gr24 : map(lambda x : eval_model(1, x, gr24=gr24)[2], sugar )
    gr24ref = gr24ev(0)
    vmax = 0
    for gr24 in arange(0,1.1,0.1):
        gr24v = gr24ev(gr24) 
        vmax = max(vmax,max(gr24v))
        plt.plot(sugar, gr24v , label=str(gr24)+' '+str(round(gr24v[possugar0_5]/gr24ref[possugar0_5],2))+' '+str(round(gr24v[possugar1]/gr24ref[possugar1],2)))
    plt.legend()
    plt.plot([0.5,0.5],[0,ceil(vmax)],'r')
    plt.plot([1,1],[0,ceil(vmax)],'r')
    plt.show()

from model2 import brc1_threshold
def plot_brc1_bap():
    import matplotlib.pyplot as plt
    delta = 0.01
    sugar = list(arange(0.1, 3,0.01))
    possugar0_5 = [i for i,v in enumerate(sugar) if abs(v-0.5) < delta/2][0]
    possugar1 = [i for i,v in enumerate(sugar) if abs(v-1.0) < delta/2][0]

    ck = 0.4
    sl = 0.2
    bapev = lambda bapv : map(lambda x : eval_model(2.5, x, bap=bapv)[2], sugar )
    bapref = bapev(0)
    vmax = 0
    for bap in arange(0,10.1,1):
        bapv = bapev(bap) 
        vmax = max(vmax,max(bapv))
        plt.plot(sugar, bapv , label=str(bap))
    plt.legend()
    plt.plot([0.5,0.5],[0,ceil(vmax)],'r')
    plt.plot([1,1],[0,ceil(vmax)],'r')
    plt.plot([0,max(sugar)],[brc1_threshold,brc1_threshold],'g', label='Threshold')
    plt.show()


from model2 import burst_delay_law
def compare_bap_desinhibition():
    sugar = 1
    bap   = 0.2 # 1.3 # 1.5
    gr24  = 0.2
    auxin = 1 # 2.5
    for sugar in [0.5,1]:
        sl, ck, brc1a = eval_model(auxin = 0,   sugar = sugar)
        sl, ck, brc1b = eval_model(auxin = auxin, sugar = sugar)
        sl, ck, brc1c = eval_model(auxin = auxin, sugar = sugar, bap = bap)
        sl, ck, brc1d = eval_model(auxin = auxin, sugar = sugar, bap = bap, gr24 = gr24)
        sl, ck, brc1e = eval_model(auxin = auxin, sugar = sugar, gr24 = gr24)
        print 'Suc'+str(sugar*100),':',brc1a, '+NAA'+str(auxin)+':', brc1b, '+BAP'+str(bap)+':',brc1c, '+GR24'+str(gr24)+':', brc1d, '++GR24'+str(gr24)+':',brc1e
        print 'Suc'+str(sugar*100),':',burst_delay_law(brc1a), '+NAA'+str(auxin)+':', burst_delay_law(brc1b), '+BAP'+str(bap)+':',burst_delay_law(brc1c), '+GR24'+str(gr24)+':', burst_delay_law(brc1d), '++GR24'+str(gr24)+':',burst_delay_law(brc1e)

if __name__ == '__main__':
    #test_gr24()
    compare_bap_desinhibition()
    #plot_brc1_gr24()
    #plot_brc1_bap()
