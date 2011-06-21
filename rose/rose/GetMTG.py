from openalea.mtg.aml import*

def GetMTG(dirname, IDplant):
    '''    generates a complete path to a file.
    the argument is in the form of "NUM[-N]", which means that
    we want to create an MTG object fom the NUM.mtg file.
    To achieve that, the filename is splitted against the"-" (dash) separator
    and the string ".mtg" is concatenated to it.
   
    '''
    # write the node code here.
    """ default argument must follows non-default arguments
    # so GetMTG(dirname='.', IDplant) is uncorrect
    # and there is no satisfying default IDplant """
    if dirname is None:
	    dirname = "."
    IDplantsplit=IDplant.partition('-')
    plant=IDplantsplit[0]
    mtg_file="%s/%s.mtg" % (dirname,plant)
    mtg=MTG(mtg_file)
    # return outputs
    return mtg
