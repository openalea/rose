import matplotlib
#matplotlib.use('Qt4Agg')
import numpy as np
import matplotlib.pyplot as plt
from runmodel import runmodel
from targets import *
from model_general import burst_delay_law, I_threshold
import targets as tg

   
def generate_fig(title, targetvalues = None, conditions = None, values = None):

    auxinvalues = [0, 1, 2.5]
    sugarvalues = [0.1, 0.5, 1 , 2.5]

    width = 0.2       # the width of the bars
    ind = np.arange(len(sugarvalues))  # the x locations for the groups
    

    def myplot( values = None):
        Simus = []
        ax = plt.gca()

        print "Auxin\tSugar\tGR24\tBAP\t:\t"+title
        for auxin in auxinvalues:
            Simus.append(list())
            for sugar in sugarvalues:
                resvalues = runmodel(auxin, sugar, gr24 = 0, bap = 0, values = values)
                Simus[-1].append(resvalues[title])
                print auxin, '\t', sugar, '\t', 0, '\t', 0, '\t', ':', '\t', resvalues[title]


        rects1 = ax.bar(ind, Simus[0], width, color=[0.2,0.2,0.2])
        color = 0.2 + 0.6 / 2.5
        rects2 = ax.bar(ind+width, Simus[1], width, color=[color,color,color])
        rects3 = ax.bar(ind+2*width, Simus[2], width, color=[0.8,0.8,0.8])

        i = 0
        for auxin, sugar, gr24, bap in  bapconditions:
                resvalues = runmodel(auxin, sugar, gr24, bap, values)
                resvalue  =  resvalues[title]
                color = 0.2 + 0.6 * auxin / 2.5
                rectsi = ax.bar([len(sugarvalues)+width*i], [resvalue], width, color=[color,color,color])
                i += 1
                print auxin,'\t',  sugar, '\t',  gr24, '\t', bap, '\t', ':', '\t', resvalues[title]


        i = 0
        for auxin, sugar, gr24, bap in  gr24conditions:
                resvalues = runmodel(auxin, sugar, gr24, bap, values)
                resvalue  =  resvalues[title]
                #print resvalue
                color = 0.2 + 0.6 * auxin / 2.5
                rectsi = ax.bar([len(sugarvalues)+1+width*i], [resvalue], width, color=[color,color,color])
                i += 1
                print auxin, '\t', sugar, '\t', gr24, '\t', bap, '\t', ':', '\t', resvalues[title]
               
               

        # add some text for labels, title and axes ticks
        ax.set_ylabel(title)
        ax.set_title(title)
        ax.set_xticks(np.arange(len(sugarvalues)+2)+width)
        ax.set_xticklabels( ('10', '50', '100', '250', 'BAP/50-100','GR24/50-100') )
        ax.set_xlabel('Sugar')

        if not targetvalues is None and not conditions is None:
            # il faudrait faire quelque chose de plus generique
            ptargetindices = []
            ptargetvalues  = []
            for target, (auxc, sugarc, gr24c, bapc) in zip(targetvalues, conditions):
                if gr24c == 0 and bapc == 0:
                    pos = ind[sugarvalues.index(sugarc)] + width * auxinvalues.index(auxc)
                    ptargetindices.append(pos)
                    ptargetvalues.append(target)
                else:
                    if gr24c > 0:
                        if (auxc, sugarc, gr24c, bapc) in gr24conditions:
                            pos = len(sugarvalues)+1 + width * gr24conditions.index((auxc, sugarc, gr24c, bapc))
                            ptargetindices.append(pos)
                            ptargetvalues.append(target)
                    elif bapc > 0:
                        if (auxc, sugarc, gr24c, bapc) in bapconditions:
                            pos = len(sugarvalues) + width * bapconditions.index((auxc, sugarc, gr24c, bapc))
                            ptargetindices.append(pos)
                            ptargetvalues.append(target)

            ax.plot(ptargetindices,ptargetvalues,'ro',color=[0,1,0], label = 'Target')
        
        ax.legend( (rects1[0], rects2[0], rects3[0]), ('NAA 0', 'NAA 1', 'NAA 2.5') )

        if title == 'I':
            N = len(sugarvalues)+2
            ax.plot([0,N],[I_threshold,I_threshold])
            ax.axis([0,N,0,17])

    if values is None  :   
        fig, ax = plt.subplots()
        myplot()
    else:
        #fig, axes = plt.subplots(1, 2)
        plt.subplot(211)
        myplot()
        plt.subplot(212)
        myplot( values)


    plt.show()




Zero4None = lambda x : x if not x is None else 0

def generate_fig_compounds(paramset = ['SL','CK', 'CKRESPONSE', 'SLRESPONSE', 'I','burst'], 
                       auxincontents = [0.,1.,2.5], sugarcontents = [0.1, 0.5, 1. , 2.5], 
                       legendpos = (2, 1), 
                       func = {'burst' : lambda res : Zero4None(burst_delay_law(res['I']))}, 
                       title = {'burst' : 'T', 'CKRESPONSE' : 'CK response', 'SLRESPONSE' : 'SL response'} , 
                       targets = {'SL' : tg.sltargets, 
                                  'CK' : tg.cktargets,
                                  'I' : tg.Itargets }): 

    N = len(sugarcontents)
    M = len(auxincontents)
    width = 1/float(N+1)       # the width of the bars
    ind = np.arange(N)  # the x locations for the groups

    targetindices_ck=None
    for i in auxincontents:
        v = i + 0.5
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
        v = i + 0.5
        if targetindices is None : targetindices = stcind+v*width
        else : targetindices = np.concatenate((targetindices,stcind+v*width))
    

    targetcontents = dict([(pname, []) for pname in paramset])
    for auxin in auxincontents:
        for pname in paramset:
            targetcontents[pname].append(list())
        for sugar in sugarcontents:
            resvalues = runmodel(auxin, sugar)
            for pname in paramset:
                if func.has_key(pname) : getval = func[pname]
                else : getval = lambda r :  r[pname]
                targetcontents[pname][-1].append(getval(resvalues))

    #print 'Simulation:',targetcontents

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
        irow = int(iparam//nbcol)
        icol = int(iparam%nbcol)
        ax = axes[irow][icol]
        i = 0.5
        rects = []
        for target,color in zip(targetcontents[pname], colors):
            rects.append(ax.bar(ind+i*width, target, width, color=[color,color,color]))
            i += 1

        if pname == 'I':
                tcolors = [[0,0,0],[0,0.4,0],[0,1,0]]
                i = 0
                for tval, tcond in  [tg.estimate_I_from_duration(False, False, True),    # interpolationduration # white
                                     tg.estimate_I_from_duration(False, True,  False),   # measuredduration # dark green
                                     tg.estimate_I_from_duration(True,  False, False)]:  # Imeasure      # green
                    tind = [ (auxincontents.index(aux) + 0.5) * width +  sugarcontents.index(sug) for aux,sug,gr24,bap in tcond ]
                    ax.plot(tind,tval,'ro',color=tcolors[i], label = 'Target')
                    i += 1

        elif targets.has_key(pname):
            if type(targets[pname]) == dict:
                tval, tcond = targets[pname]
                tind = [ (auxincontents.index(aux) + 0.5) * width +  sugarcontents.index(sug) for aux,sug,gr24,bap in tcond ]
                ax.plot(tind,tval,'ro',color=[0,1,0], label = 'Target')
            else:
                if pname=='CK':
                    ax.plot(targetindices_ck,targets[pname],'ro',color=[0,1,0], label = 'Target')
                else:
                    ax.plot(targetindices,targets[pname],'ro',color=[0,1,0], label = 'Target')
                
        
        if pname == 'I':
            ax.plot([0,N],[I_threshold,I_threshold])
            ax.axis([0,N,0,17])


        # add some text for labels, title and axes tic
        ax.set_ylabel(title.get(pname,pname))
        ax.set_xticks(ind+width*(0.5+len(auxincontents)/2))

        ax.set_xticklabels( ['Manitol' if sugar == 0 else str(sugar*100)+' mM' for sugar in sugarcontents] )

    plt.legend( rects, [str(aux)+' $\mu$M NAA' for aux in auxincontents] ,bbox_to_anchor=legendpos)
    mngr = plt.get_current_fig_manager()
    try:
        mngr.window.setGeometry(1000,100,800,800)
    except:
        pass
    plt.show()


def fig_CK():   generate_fig('CK', cktargets,  ckconditions)
def fig_SL():   generate_fig('SL', sltargets,  slconditions)
def fig_I():  
    Itargets, Iconditions = estimate_I_from_duration()
    Itargets += bapIlevels + gr24Ilevels
    Iconditions += bapconditions + gr24conditions
    generate_fig('I', Itargets,  Iconditions)

def fig_ALL():  generate_fig_compounds()

def print_values(auxinvalues, sugarvalues, gr24values, bapvalues):
    print "Auxin\tSugar\tGR24\tBAP\t:",
    init = True


    for auxin, sugar, gr24, bap in  cross_conditions(auxinvalues, sugarvalues, gr24values, bapvalues):
        resvalues = runmodel(auxin, sugar, gr24 = gr24, bap = bap)
        if init:
            print '\t'.join(resvalues.keys()),'\tBurst Delay'
            init = False
        print auxin, '\t', sugar, '\t', gr24, '\t', bap, '\t', ':', '\t'.join(map(str,resvalues.values())),'\t',burst_delay_law(resvalues['I'])




def print_help():
    print 'help of script diagram.py'
    print '-h : this help'
    print '-t : print a table of resulting values of simulations for different conditions'
    print '-m : set the model to plot'
    print 'ck,sl,I,ALL : plot the values of the specified compound'
    print 'default : plot a composed diagram of the different compounds'

from numpy import arange

def main():
    import sys
    if len(sys.argv) > 1:
        i = 1
        shouldplot = False
        while  i < len(sys.argv):
            if sys.argv[i] == '-t':
                print_values(arange(0,2.6,0.1), arange(0.1,2.6,0.1), [0, gr24level], [0, baplevel])
                shouldplot = False
            elif sys.argv[i] == '-h':
                print_help()
                return
            elif sys.argv[i] == '-m':
                from runmodel import set_model
                set_model(sys.argv[i+1])
                i += 1
                shouldplot = True
            elif 'fig_'+sys.argv[i] in globals():
                data = sys.argv[i].upper()
                func = 'fig_'+data
                globals()[func]()
                shouldplot = False
            else:
                print 'Unknow option : ', sys.argv[i]
                print_help()
            i += 1
            if shouldplot:
                generate_fig_compounds()
    else:   
        generate_fig_compounds()

if __name__ == '__main__':
    main()