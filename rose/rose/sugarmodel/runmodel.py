
def get_param_file(modelfile):
    lnamespace = {}
    execfile(modelfile, lnamespace)
    paramfile = lnamespace['paramfile']
    return paramfile

modelfile = 'model2.py'

def runmodel(auxin, sugar, gr24, bap, paramfamily = None, values = None, modelfile = modelfile):

    # prepare the values for the paramfamily
    if not (paramfamily is None or values is None ) :
        if type(paramfamily) == str: 
            entry = paramfamily.upper()
            namespace = { entry : tuple(values)} 
        else : 
            cidx = 0
            namespace = {}
            for entry in paramfamily:
                entry = entry.upper()
                nbpar = len(get_param_names(entry, get_param_file(modelfile)))
                namespace.update({ entry : tuple(values[cidx:cidx+nbpar])})
                cidx += nbpar
    else:
        namespace = {}

    # Execution of the model
    execfile(modelfile, namespace)
    eval_model = namespace['eval_model']
    sl, ck, cksignal, slsignal, brc1 = eval_model(auxin, sugar, gr24, bap)

    # retrieval of the values as a dict
    resvalues = { 'sl' : sl , 'ck' : ck, 'cksignal': cksignal, 'slsignal': slsignal, 'brc1' : brc1 }
    return resvalues