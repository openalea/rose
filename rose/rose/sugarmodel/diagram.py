import matplotlib
matplotlib.use('Qt4Agg')
import numpy as np
import matplotlib.pyplot as plt
from runmodel import runmodel
from targets import *

   
def generate_fig(title, targetvalues = None, conditions = None, values = None):

    auxinvalues = [0, 1, 2.5]
    sugarvalues = [0.1, 0.5, 1 , 2.5]

    width = 0.2       # the width of the bars
    ind = np.arange(len(sugarvalues))  # the x locations for the groups
    

    def myplot( values = None):
        Simus = []
        ax = plt.gca()

        print "Auxin\tSugar\tGR24\tBAP\t:"+title.lower()
        for auxin in auxinvalues:
            Simus.append(list())
            for sugar in sugarvalues:
                resvalues = runmodel(auxin, sugar, gr24 = 0, bap = 0, values = values)
                Simus[-1].append(resvalues[title.lower()])
                print auxin, '\t', sugar, '\t', 0, '\t', 0, '\t', ':', resvalues[title.lower()]


        rects1 = ax.bar(ind, Simus[0], width, color=[0.2,0.2,0.2])
        color = 0.2 + 0.6 / 2.5
        rects2 = ax.bar(ind+width, Simus[1], width, color=[color,color,color])
        rects3 = ax.bar(ind+2*width, Simus[2], width, color=[0.8,0.8,0.8])

        i = 0
        for auxin, sugar, gr24, bap in  bapconditions:
                resvalues = runmodel(auxin, sugar, gr24, bap, values)
                resvalue  =  resvalues[title.lower()]
                color = 0.2 + 0.6 * auxin / 2.5
                rectsi = ax.bar([len(sugarvalues)+width*i], [resvalue], width, color=[color,color,color])
                i += 1
                print auxin,'\t',  sugar, '\t',  gr24, '\t', bap, '\t', ':', resvalues[title.lower()]


        i = 0
        for auxin, sugar, gr24, bap in  gr24conditions:
                resvalues = runmodel(auxin, sugar, gr24, bap, values)
                resvalue  =  resvalues[title.lower()]
                #print resvalue
                color = 0.2 + 0.6 * auxin / 2.5
                rectsi = ax.bar([len(sugarvalues)+1+width*i], [resvalue], width, color=[color,color,color])
                i += 1
                print auxin, '\t', sugar, '\t', gr24, '\t', bap, '\t', ':', resvalues[title.lower()]
               
               

        # add some text for labels, title and axes ticks
        ax.set_ylabel('Simulated relative '+title+' content')
        ax.set_title(title)
        ax.set_xticks(np.arange(len(sugarvalues)+2)+width)
        ax.set_xticklabels( ('10', '50', '100', '250', '50-100','50-100') )

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



from model import burst_delay_law, brc1_threshold
import targets as tg

Zero4None = lambda x : x if not x is None else 0

def generate_fig_compound(paramset = ['sl','ck', 'ckresponse', 'slresponse', 'brc1','burst'], 
                       auxincontents = [0.,1.,2.5], sugarcontents = [0.1, 0.5, 1. , 2.5], 
                       legendpos = (2, 1), 
                       func = {'burst' : lambda res : Zero4None(burst_delay_law(res['brc1']))}, 
                       title = {'burst' : 'simulated burst delay'} , 
                       targets = {'sl' : tg.sltargets, 
                                  'ck' : tg.cktargets,
                                  'brc1' : tg.brc1targets }): 

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

        if pname == 'brc1':
                tcolors = [[0,0,0],[0,0.4,0],[0,1,0]]
                i = 0
                for tval, tcond in  [tg.estimate_brc1_from_duration(False, False, True),    # interpolationduration # white
                                     tg.estimate_brc1_from_duration(False, True,  False),   # measuredduration # dark green
                                     tg.estimate_brc1_from_duration(True,  False, False)]:  # brc1measure      # green
                    tind = [ (auxincontents.index(aux) + 0.5) * width +  sugarcontents.index(sug) for aux,sug,gr24,bap in tcond ]
                    ax.plot(tind,tval,'ro',color=tcolors[i], label = 'Target')
                    i += 1

        elif targets.has_key(pname):
            if type(targets[pname]) == dict:
                tval, tcond = targets[pname]
                tind = [ (auxincontents.index(aux) + 0.5) * width +  sugarcontents.index(sug) for aux,sug,gr24,bap in tcond ]
                ax.plot(tind,tval,'ro',color=[0,1,0], label = 'Target')
            else:
                if pname=='ck':
                    ax.plot(targetindices_ck,targets[pname],'ro',color=[0,1,0], label = 'Target')
                else:
                    ax.plot(targetindices,targets[pname],'ro',color=[0,1,0], label = 'Target')
                
        
        if pname == 'brc1':
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


def fig_ck():   generate_fig('CK', cktargets,  ckconditions)
def fig_sl():   generate_fig('SL', sltargets,  slconditions)
def fig_brc1():  
    brc1targets, brc1conditions = estimate_brc1_from_duration()
    brc1targets += bapbrc1levels + gr24brc1levels
    brc1conditions += bapconditions + gr24conditions
    generate_fig('BRC1', brc1targets,  brc1conditions)


def print_values(auxinvalues, sugarvalues, gr24values, bapvalues):
    print "Auxin\tSugar\tGR24\tBAP\t:",
    init = True


    for auxin, sugar, gr24, bap in  cross_conditions(auxinvalues, sugarvalues, gr24values, bapvalues):
        resvalues = runmodel(auxin, sugar, gr24 = 0, bap = 0)
        if init:
            print '\t'.join(resvalues.keys()),'\tBurst Delay'
            init = False
        print auxin, '\t', sugar, '\t', gr24, '\t', bap, '\t', ':', '\t'.join(map(str,resvalues.values())),'\t',burst_delay_law(resvalues['brc1'])


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == '-t':
        print_values([0,   1,   2.5], [0.1, 0.5, 1 ,  2.5], [0, gr24level], [0, baplevel])
    elif len(sys.argv) > 1:
        data = sys.argv[1]
        func = 'fig_'+data
        globals()[func]()
    else:   
        generate_fig_compound()

