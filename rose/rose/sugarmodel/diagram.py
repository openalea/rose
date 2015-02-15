import numpy as np
import matplotlib.pyplot as plt
from openalea.lpy import Lsystem

lsysfile = 'rosebudJan15-model1-v0.lpy'



def generate_fig(target = 'ck', title = 'CK'):
   generate_fig_func(lambda res : getattr(res,target),title)
   
def generate_fig_func(func, title):
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

    ax.legend( (rects1[0], rects2[0]), ('NAA 0', 'NAA 2.5') )
    plt.show()


def generate_fig_ck():
    generate_fig()

def generate_fig_sl():
    generate_fig('sl','SL')

def generate_fig_slp():
    generate_fig('slp','SLp')

def generate_fig_brc1():
    generate_fig('brc1','BRC1')


if __name__ == '__main__':
    generate_fig_brc1()