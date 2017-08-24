
def get_param_file(modelfile):
    lnamespace = {}
    execfile(modelfile, lnamespace)
    paramfile = lnamespace['paramfile']
    return paramfile

#modelfile = 'model2.py'
modelfile = 'model2_sugarOnBRC1Only.py'
paramfile = get_param_file(modelfile)


def runmodel(auxin, sugar, gr24 = 0, bap = 0, values = None, modelfile = modelfile):
    
    namespace = {}
    if not values is None : namespace.update(values)

    # Execution of the model
    execfile(modelfile, namespace)
    eval_model = namespace['eval_model']
    sl, ck, cksignal, slsignal, brc1 = eval_model(auxin, sugar, gr24, bap)

    # retrieval of the values as a dict
    resvalues = { 'sl' : sl , 'ck' : ck, 'cksignal': cksignal, 'slsignal': slsignal, 'brc1' : brc1 }
    return resvalues