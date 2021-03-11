from openalea.mtg.aml import*

def GetMTG(dirname, IDplant):
    '''    
    '''
    # write the node code here.
    IDplantsplit=IDplant.partition('-')
    plant=IDplantsplit[0]
    mtg_file=dirname+"/"+plant+".mtg"
    mtg=MTG(mtg_file)
    # return outputs
    return mtg
