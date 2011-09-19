from openalea.mtg.aml import MTG
from openalea.mtg.algo import union

def MTG_union(mtgsin):
    '''    make the union of MTGs
    '''
    mtgout = None; 
    # write the node code here.
    # print "len(mtgsin)=%d" % len(mtgsin)
    if isinstance (mtgsin, list):
        if len(mtgsin) >= 2 :
            mtgout = union(mtgsin[0],mtgsin[1])
            for MtgIn in mtgsin[2:]:
                mtgout = union(mtgout,MtgIn)
        else:
            mtgout = mtgsin[0]
    else : # we take the a risk to return something not being an MTG
        mtgout = mtgsin

    # return outputs
    return mtgout,
