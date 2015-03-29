import numpy as np
import matplotlib.pyplot as plt
from openalea.lpy import Lsystem

lsysfile = 'rosebudJan15-model1-v1.lpy'



def generate_fig(target = 'ck', title = 'CK', targetvalues = None):
   generate_fig_func(lambda res : getattr(res,target),title,targetvalues=targetvalues)
   
def generate_fig_func(func, title, targetvalues = None):
    N = 3
    width = 0.35       # the width of the bars
    ind = np.arange(N)  # the x locations for the groups

    targetcontents = []
    for auxin in [0,2.5]:
        targetcontents.append(list())
        for sugar in [0, 1 , 2.5]:
            simu = Lsystem(lsysfile, {'AUXIN': auxin, 'SUGAR' : sugar} )
            ls = simu.iterate()
            res = ls[-1].p
            targetcontents[-1].append(func(res))

    fig, ax = plt.subplots()
    rects1 = ax.bar(ind, targetcontents[0], width, color=[0,0,0])
    rects2 = ax.bar(ind+width, targetcontents[1], width, color=[0.6,0.6,0.6])

    # add some text for labels, title and axes ticks
    ax.set_ylabel('Simulated relative '+title+' content')
    ax.set_title(title)
    ax.set_xticks(ind+width)
    ax.set_xticklabels( ('Manitol', '1', '2.5') )

    if not targetvalues is None:
        indices = np.concatenate((ind+width/2,ind+3*width/2))
        ax.plot(indices,targetvalues,'ro',color=[0,1,0], label = 'Target')

    ax.legend( (rects1[0], rects2[0]), ('NAA 0', 'NAA 2.5') )
    plt.show()


def generate_fig2(target = 'ck', title = 'CK'):
   generate_fig_func2(lambda res : getattr(res,target),title)
   
def generate_fig_func2(func, title,legendpos = (1.07, 1)):
    auxincontents = [0,1,2.5,5]
    sugarcontents = [0.1, 0.5, 1 , 2.5]

    N = len(sugarcontents)
    M = len(auxincontents)
    width = 1/float(N+1)       # the width of the bars
    ind = np.arange(N)  # the x locations for the groups

    targetcontents = []
    for auxin in auxincontents:
        targetcontents.append(list())
        for sugar in sugarcontents:
            simu = Lsystem(lsysfile, {'AUXIN': auxin, 'SUGAR' : sugar} )
            ls = simu.iterate()
            res = ls[-1].p
            targetcontents[-1].append(func(res))

    print targetcontents
    dc = 0.8/(M-1)
    colors = [0.9]+[0.9-i*dc for i in xrange(1,M-1)]+[0.1]
    fig, ax = plt.subplots()
    i = 0.5
    rects = []
    for target,color in zip(targetcontents, colors):
        rects.append(ax.bar(ind+i*width, target, width, color=[color,color,color]))
        i += 1

    # add some text for labels, title and axes ticks
    ax.set_ylabel('Simulated relative '+title+' content')
    ax.set_title(title)
    ax.set_xticks(ind+width*(0.5+len(auxincontents)/2))

    ax.set_xticklabels( ['Manitol' if sugar == 0 else str(sugar*100)+' mM' for sugar in sugarcontents] )

    ax.legend( rects, [str(aux)+' $\mu$M NAA' for aux in auxincontents] ,bbox_to_anchor=legendpos )
    plt.show()


from cellproliferation import burst_delay_law
import optimize 
#def generate_fig_func3(paramset = ['ck','sl','slp','brc1'], auxincontents = [0,1,2.5,5], sugarcontents = [0.1, 0.5, 1 , 2.5], legendpos = (1.07, 1)):
def generate_fig_func3(paramset = ['sl','slp','ck','brc1','burst'], 
                       # auxincontents = [0,1,2.5,5], sugarcontents = [0.1, 0.5, 1 , 2.5], 
                       auxincontents = [0,2.5], sugarcontents = [0.0, 1 , 2.5], 
                       legendpos = (2, 1), 
                       func = {'burst' : lambda res : burst_delay_law(res.brc1)}, 
                       title = {'burst' : 'burst delay'} , 
                       targets = {'sl' : optimize.sltargets, 'slp' : optimize.slptargets, 'ck' : optimize.cktargets, 'brc1' : optimize.brc1targets}):

    N = len(sugarcontents)
    M = len(auxincontents)
    width = 1/float(N+1)       # the width of the bars
    ind = np.arange(N)  # the x locations for the groups

    targetcontents = dict([(pname, []) for pname in paramset])
    for auxin in auxincontents:
        for pname in paramset:
            targetcontents[pname].append(list())
        for sugar in sugarcontents:
            simu = Lsystem(lsysfile, {'AUXIN': auxin, 'SUGAR' : sugar} )
            ls = simu.iterate()
            res = ls[-1].p
            for pname in paramset:
                if func.has_key(pname) : getval = func[pname]
                else : getval = lambda r :  getattr(r,pname)
                targetcontents[pname][-1].append(getval(res))

    print targetcontents
    dc = 0.8/(M-1)
    colors = [0.9]+[0.9-i*dc for i in xrange(1,M-1)]+[0.1]
    nbparam = len(paramset)

    from math import sqrt
    nbrow = round(sqrt(nbparam))
    nbcol = nbrow
    if nbrow * (nbcol -1) > nbparam: nbcol -= 1
    elif nbrow * nbcol  < nbparam: nbrow += 1

    for iparam, pname in enumerate(paramset):
        ax = plt.subplot(nbrow, nbcol,iparam+1)
        i = 0.5
        rects = []
        for target,color in zip(targetcontents[pname], colors):
            rects.append(ax.bar(ind+i*width, target, width, color=[color,color,color]))
            i += 1

        if targets.has_key(pname):
            indices = np.concatenate((ind+width,ind+2*width))
            ax.plot(indices,targets[pname],'ro',color=[0,1,0], label = 'Target')

        # add some text for labels, title and axes tic
        ax.set_ylabel(title.get(pname,'Simulated relative '+pname+' contents'))
        ax.set_xticks(ind+width*(0.5+len(auxincontents)/2))

        ax.set_xticklabels( ['Manitol' if sugar == 0 else str(sugar*100)+' mM' for sugar in sugarcontents] )

    plt.legend( rects, [str(aux)+' $\mu$M NAA' for aux in auxincontents] ,bbox_to_anchor=legendpos)
    plt.show()


import optimize

def generate_fig_ck(targetvalues = None):
    if targetvalues is None:
        targetvalues = optimize.cktargets
    generate_fig('ck', 'CK', targetvalues = targetvalues)

def generate_fig_sl(targetvalues = None):
    if targetvalues is None:
        targetvalues = optimize.sltargets
    generate_fig('sl','SL', targetvalues = targetvalues)

def generate_fig_slp(targetvalues = None):
    if targetvalues is None:
        targetvalues = optimize.slptargets
    generate_fig('slp','SLp', targetvalues = targetvalues)

def generate_fig_brc1(targetvalues = None):
    if targetvalues is None:
        targetvalues = optimize.brc1targets
    generate_fig('brc1','BRC1', targetvalues = targetvalues)


def generate_fig_comp():
    auxincontents = [0,1,2.5,5]
    sugarcontents = [0.1, 0.5, 1 , 2.5]

    N = len(sugarcontents)
    width = 1/float(N+1)       # the width of the bars
    ind = np.arange(N)  # the x locations for the groups

    brc1levels = [[1.0108692768952487, 0.6722887068218482, 0.45498203294721207, 0.2762034309804555], 
                  [1.629482933567273, 1.0740412960652266, 0.7400141770201679, 0.49290843510338356], 
                  [2.6868882741803595, 2.0299595484866377, 1.5408027394180974, 1.182167415167441], 
                  [3.323413276025248, 2.924482859726581, 2.4539200431896204, 2.038817303128552]]

    durations =  [[3 , 2, 1.5, 1],
                  [None, 6, 3, 2],
                  [None, None, 9, 3.5],
                  [None, None, None, 7]]


    colors = [[1,1,1],[2/3.,2/3.,2/3.],[1/3.,1/3.,1/3.],[0,0,0]]
    fig, ax = plt.subplots()
    i = 0.5
    rects = []
    for target,color in zip(brc1levels, colors):

        rects.append(ax.bar(ind+i*width, target, width, color=color))
        i += 1

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
        #generate_fig_func3()
        generate_fig2('brc1','BRC1')
