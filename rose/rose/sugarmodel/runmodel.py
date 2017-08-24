
def get_param_file(modelfile):
    lnamespace = {}
    execfile(modelfile, lnamespace)
    paramfile = lnamespace['paramfile']
    return paramfile

modelfile = 'model.py'
#modelfile = 'model_sugarOnBRC1Only.py'
paramfile = get_param_file(modelfile)


def runmodel(auxin, sugar, gr24 = 0, bap = 0, values = None, modelfile = modelfile):
    
    namespace = {}
    if not values is None : namespace.update(values)

    # Execution of the model
    execfile(modelfile, namespace)
    eval_model = namespace['eval_model']
    sl, ck, ckresponse, slresponse, brc1 = eval_model(auxin, sugar, gr24, bap)

    # retrieval of the values as a dict
    resvalues = { 'sl' : sl , 'ck' : ck, 'ckresponse': ckresponse, 'slresponse': slresponse, 'brc1' : brc1 }
    return resvalues