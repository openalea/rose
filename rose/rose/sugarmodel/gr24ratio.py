import matplotlib
matplotlib.use('Qt4Agg')
import matplotlib.pyplot as plt

def ratio(k, sl):
    return (k * 100 + sl) / (k * 50 + sl)


execfile('params10_init.py')

modelfile = 'model2.py'
#modelfile = 'model2_sugaronBRC1.py'
#modelfile = 'model2_SUConCK.py'
#modelfile = 'model2SUConCKsignal.py'
import model2; reload(model2)
from model2 import eval_model,burst_delay_law
from numpy import arange
from math import *
import numpy as np

## Effect of external GR24 on BRC1 and start of bud elongation; sensitivity to GR24
def bratio(sugar, auxin, gr24 = 0.2):
    brc1_0gr24 = eval_model(auxin, sugar)[4]
    delay_0gr24 = burst_delay_law(brc1_0gr24)
    brc1_gr24 = eval_model(auxin, sugar,gr24,0)[4]
    delay_gr24 = burst_delay_law(brc1_gr24)
    return brc1_gr24/brc1_0gr24, brc1_gr24, brc1_0gr24, delay_gr24, delay_0gr24

def bratioofratio(gr24 = 0.2): 
    return bratio(0.5,1, gr24)[0] / bratio(1,1, gr24)[0]

def test_gr24():
    g = 0.2
    print g, bratioofratio(g), bratio(0.5,1,g), bratio(1,1,g)

## draw several figures representing sl, ck, Esl, Eck, brc1, and delay as a function of vals1 and vals2 
def draw_func(vals1,vals2,targetcontents,
              paramset = ['sl','ck', 'Esl', 'Eck', 'brc1','burst'],
              title = {'burst' : 'simulated burst delay'},
              legendpos = (2, 1)):
    
    N = len(vals1)
    M = len(vals2)
    width = 1/float(N+1)       # the width of the bars
    ind = np.arange(N)  # the x locations for the groups
    
    dc = 0.8/(M-1)
    colors = [0.9]+[0.9-i*dc for i in xrange(1,M-1)]+[0.1]
    nbparam = len(paramset)

    from math import sqrt
    nbrow = round(sqrt(nbparam))
    nbcol = nbrow
    if nbrow * (nbcol -1) > nbparam: nbcol -= 1
    elif nbrow * nbcol  < nbparam: nbrow += 1

    #plt.close('all')
    fig, axes = plt.subplots(int(nbrow), int(nbcol))
    for iparam, pname in enumerate(paramset):
        # ax = plt.subplot(nbrow, nbcol,iparam+1)
        ax = axes[iparam//nbcol][iparam%nbcol]
        i = 0.5
        rects = []
        for target,color in zip(targetcontents[pname], colors):
            rects.append(ax.bar(ind+i*width, target, width, color=[color,color,color]))
            i += 1
    
        # add some text for labels, title and axes tic
        ax.set_ylabel(title.get(pname,'Simulated relative '+pname+' contents'))
        ax.set_xticks(ind+width*(0.5+len(vals2)/2))

        ax.set_xticklabels( [str(v) for v in vals1] )

    plt.legend( rects, [str(v) for v in vals2] ,bbox_to_anchor=legendpos)
    mngr = plt.get_current_fig_manager()
    mngr.window.setGeometry(1000,100,800,800)
    plt.show()


## simulation of CK effect as a function of different sl levels

def gr24_bap_simu(paramset = ['sl','ck', 'Esl', 'Eck', 'brc1','burst'], 
                       auxin = 2.5,
                       sugar = 1.,
                       bapcontents = [0.,0.1, 0.2, 0.3, 0.4, 0.5],gr24contents = [-0.4,0.,0.4,0.8,1.2],
                       func = {'burst' : lambda res : burst_delay_law(res['brc1'])}):
    targetcontents = dict([(pname, []) for pname in paramset])
    for gr24 in gr24contents:
        for pname in paramset:
            targetcontents[pname].append(list())
        for bap in bapcontents:
            namespace = { } 
            execfile(modelfile, namespace)
            eval_model = namespace['eval_model']
            sl, ck, Eck, Esl, brc1 = eval_model(auxin, sugar, gr24, bap)
            resvalues = { 'sl' : sl , 'ck' : ck, 'Esl': Esl, 'Eck': Eck, 'brc1' : brc1 }
            for pname in paramset:
                if func.has_key(pname) : getval = func[pname]
                else : getval = lambda r :  r[pname]
                targetcontents[pname][-1].append(getval(resvalues))

    print targetcontents

    draw_func(vals1=bapcontents,vals2=gr24contents,targetcontents=targetcontents)    
    

## simulation of CK effect as a function of different sugar levels
# wa can add at maximum 0.4 bap to avoid being above the maximum value of 1 of CKs

def suc_bap_simu(paramset = ['sl','ck', 'Esl', 'Eck', 'brc1','burst'],
                       bap = 0.2,
                       auxincontents = [x / 100.0 for x in range(0, 260, 10)],sugarcontents = [x / 100.0 for x in range(0, 260, 10)],
                       func = {'burst' : lambda res : burst_delay_law(res['brc1'])}):
    targetcontents = dict([(pname, []) for pname in paramset])
    for sugar in sugarcontents:
        for pname in paramset:
            targetcontents[pname].append(list())
        for auxin in auxincontents:
            namespace = { } 
            execfile(modelfile, namespace)
            eval_model = namespace['eval_model']
            sl, ck, Eck, Esl, brc1 = eval_model(auxin, sugar,0,bap)
            resvalues = { 'sl' : sl , 'ck' : ck, 'Esl': Esl, 'Eck': Eck, 'brc1' : brc1 }
            for pname in paramset:
                if func.has_key(pname) : getval = func[pname]
                else : getval = lambda r :  r[pname]
                targetcontents[pname][-1].append(getval(resvalues))

    fname=open("bap2_SLsignal.txt","w")
    datas=targetcontents["Esl"]
    s=-1
    for sugar in sugarcontents:
        s=s+1
        a=-1
        for auxin in auxincontents:
            a=a+1
            line = str(sugar) + ' ' + str(auxin) + ' ' + str(datas[s][a])
            print line
            fname.write(line + '\n')
    
    
    #print targetcontents

    #draw_func(vals1=auxincontents,vals2=sugarcontents,targetcontents=targetcontents)    
    


## simulation of gr24 effect as a function of differnt naa levels
def naa_gr24_simu(paramset = ['sl','ck', 'Esl', 'Eck', 'brc1','burst'], 
                       gr24 = 0.1,
                       sugarcontents =  [x / 100.0 for x in range(0, 260, 10)] ,auxincontents= [x / 100.0 for x in range(0, 260, 10)],
                       func = {'burst' : lambda res : burst_delay_law(res['brc1'])}):
    targetcontents = dict([(pname, []) for pname in paramset])
    for sugar in sugarcontents:
        for pname in paramset:
            targetcontents[pname].append(list())
        for auxin in auxincontents:
            namespace = { } 
            execfile(modelfile, namespace)
            eval_model = namespace['eval_model']
            sl, ck, Eck, Esl, brc1 = eval_model(auxin, sugar, gr24)
            resvalues = { 'sl' : sl , 'ck' : ck, 'Esl': Esl, 'Eck': Eck, 'brc1' : brc1 }
            for pname in paramset:
                if func.has_key(pname) : getval = func[pname]
                else : getval = lambda r :  r[pname]
                targetcontents[pname][-1].append(getval(resvalues))

    fname=open("sl1.txt","w")    
    datas=targetcontents["Esl"]
    s=-1
    for sugar in sugarcontents:
        s=s+1
        a=-1
        for auxin in auxincontents:
            a=a+1
            line = str(sugar) + ' ' + str(auxin) + ' ' + str(datas[s][a])
            print line
            fname.write(line + '\n')
            
    #print targetcontents

    #draw_func(vals1=gr24contents,vals2=auxincontents,targetcontents=targetcontents)    

## simulation of the impact of Eck on BRC1 for different Esl values
def Eck_Esl_simu(effectsnames=['Eck','Esl'], sugarcontents=[0.1,0.5,1.,2.5],naacontents=[0.,1.,2.5]):
    
    effects=dict([(name, []) for name in effectsnames]) 
    for sugar in sugarcontents:
        for name in effectsnames:
            effects[name].append(list())
        for naa in naacontents:
            namespace = { } 
            execfile(modelfile, namespace)
            eval_model = namespace['eval_model']
            sl, ck, Eck, Esl, brc1 = eval_model(naa, sugar)
            effects['Eck'][-1].append(Eck)
            effects['Esl'][-1].append(Esl)
    EslEckrange=dict([(name, []) for name in effectsnames]) 
    EslEckrange['Eck']=[0.02,0.1]
    EslEckrange['Esl']=[x for x in range(0,6,1)]
    
    from model2 import brc1_plateau
    simubrc1=[]
    for Eck in EslEckrange['Eck']:
        simubrc1.append([])
        for Esl in EslEckrange['Esl']:
            simubrc1[-1].append(brc1_plateau(Eck,Esl))
    
    print(simubrc1)
    
    
   


############ obsolete
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
    #compare_bap_desinhibition()
    #gr24_bap_simu()
    #suc_bap_simu()
    #naa_gr24_simu()
    #deriv_naa()
    #deriv_sucrose()
    Eck_Esl_simu()
    #plot_brc1_gr24()
    #plot_brc1_bap()
