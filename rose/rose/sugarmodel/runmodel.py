
def get_param_file(modelfile):
    lnamespace = {}
    execfile(modelfile, lnamespace)
    paramfile = lnamespace['paramfile']
    return paramfile

modelfile = 'model-additive.py'
#modelfile = 'model_sugarOnBRC1Only.py'
paramfile = get_param_file(modelfile)


def set_model(fname):
    global modelfile, paramfile
    modelfile = fname
    paramfile = get_param_file(modelfile)

def runmodel(auxin, sugar, gr24 = 0, bap = 0, values = None):
    
    namespace = {}
    if not values is None : namespace.update(values)

    # Execution of the model
    execfile(modelfile, namespace)
    eval_model = namespace['eval_model']
    sl, ck, ckresponse, slresponse, I = eval_model(auxin, sugar, gr24, bap)

    # retrieval of the values as a dict
    resvalues = { 'SL' : sl , 'CK' : ck, 'CKRESPONSE': ckresponse, 'SLRESPONSE': slresponse, 'I' : I }
    return resvalues