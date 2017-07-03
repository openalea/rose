import matplotlib
matplotlib.use('Qt4Agg')
import numpy as np
import matplotlib.pyplot as plt
from openalea.lpy import Lsystem

#lsysfile = 'rosebudJune15v2-model1.lpy'
modelfile = 'model2.py'


def generate_fig(target = 'ck', title = 'CK', targetvalues = None):
   generate_fig_func(lambda res : getattr(res,target),title,targetvalues=targetvalues)
   
def generate_fig_func(func, title, targetvalues = None):

    import model2
    from model2 import ck_plateau, sl_plateau, cksignal, slsignal, brc1_plateau 

    N = 4
    width = 0.2       # the width of the bars
    ind = np.arange(N)  # the x locations for the groups

    Simus = []
    for auxin in [0,1,2.5]:
        Simus.append(list())
        for sugar in [0.1, 0.5, 1 , 2.5]:
            if title=='CK':
                simu = ck_plateau(auxin,sugar)
            else:
                if title=='SL':
                    simu = sl_plateau(auxin)
                else:
                    if title=='SLsignal':
                        sl = sl_plateau(auxin)
                        simu = slsignal(sl,sugar,0.)
                    else:
                        ck=ck_plateau(auxin,sugar)
                        sl=sl_plateau(auxin)
                        simu = brc1_plateau(ck,sl,sugar,0.,0.)
            Simus[-1].append(simu)

    fig, ax = plt.subplots()
    rects1 = ax.bar(ind, Simus[0], width, color=[0,0,0,0])
    rects2 = ax.bar(ind+width, Simus[1], width, color=[0.5,0.5,0.5,0.5])
    rects3 = ax.bar(ind+2*width, Simus[2], width, color=[1,1,1,1])

    # add some text for labels, title and axes ticks
    ax.set_ylabel('Simulated relative '+title+' content')
    ax.set_title(title)
    ax.set_xticks(ind+width)
    ax.set_xticklabels( ('10', '50', '100', '250') )

    if not targetvalues is None:
        # il faudrait faire quelque chose de plus generique
        if title=='CK':
            indices = np.concatenate((ind+width/2,ind+3*width/2,ind+5*width/2))
            ax.plot(indices,targetvalues,'ro',color=[0,1,0], label = 'Target')
        else:
            ind2=np.array([2,3])
            indices=np.concatenate((ind2+width/2,ind2+5*width/2))
            ax.plot(indices,targetvalues,'ro',color=[0,1,0], label = 'Target')
    
    ax.legend( (rects1[0], rects2[0], rects3[0]), ('NAA 0', 'NAA 1', 'NAA 2.5') )
    plt.show()





import model2; reload(model2) 
from model2 import burst_delay_law
import optimize 

def generate_fig_compound(paramset = ['sl','ck', 'Sck', 'Ssl', 'brc1','burst'], 
                       auxincontents = [0.,1.,2.5], sugarcontents = [0.1, 0.5, 1. , 2.5], 
                       legendpos = (2, 1), 
                       func = {'burst' : lambda res : burst_delay_law(res['brc1'])}, 
                       title = {'burst' : 'simulated burst delay'} , 
                       targets = {'sl' : optimize.sltargets, 
                                  'ck' : optimize.cktargets,
                                  'Ssl':optimize.slsignaltargets,
                                  'brc1' : optimize.brc1targets }): # estimate_brc1_from_duration(True)

    N = len(sugarcontents)
    M = len(auxincontents)
    width = 1/float(N+1)       # the width of the bars
    ind = np.arange(N)  # the x locations for the groups

    targetindices_ck=None
    for i in auxincontents:
        v = i + 1
        if targetindices_ck is None : targetindices_ck = ind+v*width
        else : targetindices_ck = np.concatenate((targetindices_ck,ind+v*width))
        
    
    auxintargetcontents = [0., 2.5] 
    sugartargetcontents = [1. , 2.5]

    stcind = []
    for st in sugartargetcontents:
        stcind.append(sugarcontents.index(st))
    stcind = np.array(stcind)

    atcind = []
    for at in auxintargetcontents:
        atcind.append(auxincontents.index(at))
    atcind = np.array(atcind)

    targetindices = None
    for i in atcind:
        v = i + 1
        if targetindices is None : targetindices = stcind+v*width
        else : targetindices = np.concatenate((targetindices,stcind+v*width))
    

    targetcontents = dict([(pname, []) for pname in paramset])
    for auxin in auxincontents:
        for pname in paramset:
            targetcontents[pname].append(list())
        for sugar in sugarcontents:
            namespace = { } 
            execfile(modelfile, namespace)
            eval_model = namespace['eval_model']
            sl, ck, Sck, Ssl, brc1 = eval_model(auxin, sugar)
            resvalues = { 'sl' : sl , 'ck' : ck, 'Sck': Sck, 'Ssl': Ssl, 'brc1' : brc1 }
            for pname in paramset:
                if func.has_key(pname) : getval = func[pname]
                else : getval = lambda r :  r[pname]
                targetcontents[pname][-1].append(getval(resvalues))

    print 'Simulation:',targetcontents

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

        if pname == 'brc1':
                import optimize; reload(optimize)
                from optimize import estimate_brc1_from_duration
                tcolors = [[1,1,1],[0,0.4,0],[0,1,0]]
                i = 0
                for tval, tcond in  [estimate_brc1_from_duration(False, False, True),    # interpolationduration # white
                                     estimate_brc1_from_duration(False, True,  False),   # measuredduration # dark green
                                     estimate_brc1_from_duration(True,  False, False)]:  # brc1measure      # green
                    tind = [ (auxincontents.index(aux) + 1) * width +  sugarcontents.index(sug) for aux,sug in tcond ]
                    ax.plot(tind,tval,'ro',color=tcolors[i], label = 'Target')
                    i += 1

        elif targets.has_key(pname):
            if type(targets[pname]) == dict:
                tval, tcond = targets[pname]
                tind = [ (auxincontents.index(aux) + 1) * width +  sugarcontents.index(sug) for aux,sug in tcond ]
                ax.plot(tind,tval,'ro',color=[0,1,0], label = 'Target')
            else:
                if pname=='ck':
                    ax.plot(targetindices_ck,targets[pname],'ro',color=[0,1,0], label = 'Target')
                else:
                    ax.plot(targetindices,targets[pname],'ro',color=[0,1,0], label = 'Target')
                
        
        if pname == 'brc1':
            from model2 import brc1_threshold
            ax.plot([0,N],[brc1_threshold,brc1_threshold])
            ax.axis([0,N,0,17])


        # add some text for labels, title and axes tic
        ax.set_ylabel(title.get(pname,'Simulated relative '+pname+' contents'))
        ax.set_xticks(ind+width*(0.5+len(auxincontents)/2))

        ax.set_xticklabels( ['Manitol' if sugar == 0 else str(sugar*100)+' mM' for sugar in sugarcontents] )

    plt.legend( rects, [str(aux)+' $\mu$M NAA' for aux in auxincontents] ,bbox_to_anchor=legendpos)
    mngr = plt.get_current_fig_manager()
    mngr.window.setGeometry(1000,100,800,800)
    plt.show()


#data=np.random.exponential(scale=180, size=10000)
#print ('el valor medio de la distribucion exponencial es: ')
#print np.average(data)
#plt.hist(data,bins=len(data)**0.5,normed=True, cumulative=True, facecolor='red', label='datos tamano paqutes acumulativa', alpha=0.5)
#plt.legend()
#plt.xlabel('algo')
#plt.ylabel('algo')
#plt.grid()
#plt.show()



import optimize

def generate_fig_ck(targetvalues = None):
    if targetvalues is None:
        targetvalues = optimize.cktargets
    generate_fig('ck', 'CK', targetvalues = targetvalues)

def generate_fig_sl(targetvalues = None):
    if targetvalues is None:
        targetvalues = optimize.sltargets
    generate_fig('sl','SL', targetvalues = targetvalues)

def generate_fig_slsignal(targetvalues = None):
    if targetvalues is None:
        targetvalues = optimize.slsignaltargets
    generate_fig('slsignal','SLsignal', targetvalues = targetvalues)

def generate_fig_brc1(targetvalues = None):
    if targetvalues is None:
        targetvalues = optimize.brc1targets
    generate_fig('brc1','BRC1', targetvalues = targetvalues)


    # add some text for labels, title and axes ticks
    ax.set_ylabel('Simulated relative BRC1 content')
    ax.set_title(('BRC1'))
    ax.set_xticks(ind+width*(0.5+len(auxincontents)/2))

    ax.set_xticklabels( ['Manitol' if sugar == 0 else str(sugar*100)+' mM' for sugar in sugarcontents] )

    ax.legend( rects, [str(aux)+' $\mu$M NAA' for aux in auxincontents] ,bbox_to_anchor=(1.07, 1) )
    plt.show()



if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        data = sys.argv[1]
        func = 'generate_fig_'+data
        globals()[func]()
    else:
        generate_fig_compound()

