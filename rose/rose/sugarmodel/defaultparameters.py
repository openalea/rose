
def get_caller_frame():
    import inspect
    return inspect.getouterframes(inspect.currentframe())[2][0]
   
class LocalsRetriever:
    def __init__(self, func):
        self.mylocals = {}
        self.depth = 0
        self.func = func

    def _mytracer(self, frame, event, arg):
        #print frame, event, arg
        if event == 'call':
            self.depth += 1
            if self.depth == 1:
                return self._mytracer
        elif event == 'return':
            self.depth -= 1
            self.mylocals.update(frame.f_locals)
        elif event == 'line':
            pass
        elif event == 'exception':
            pass
        else:
            pass

    def __call__(self, *args, **kwds):
        import sys
        sys.settrace(self._mytracer)
        res = None
        try:
            res = self.func(*args, **kwds)
        finally:
            sys.settrace(None)
        return self.mylocals, res


_dfattrname = 'paramsvalues'

def defaultparameters(function):
    """ 
    A decorator to define in a simple way default values of parameters.

    This decorator retrieve all the local variables of a function and insert them
    in the global namespace if they do not already exist after the function definition.

    Example:

    @defaultparameters
    def myparams():
        a = 1
        b = 2

    c  = a * b

    """
    params, res = LocalsRetriever(function)()
    for pname, pvalue in params.items():
        if type(pvalue) == tuple:
            get_caller_frame().f_locals.setdefault(pname, pvalue[0])
        else:
            get_caller_frame().f_locals.setdefault(pname, pvalue)
    map(get_caller_frame().f_locals.setdefault, params.keys(), params.values())
    setattr(function,_dfattrname,params)
    return function


def is_defaultparameters_function(function):
    import inspect
    return inspect.isfunction(function) and hasattr(function,_dfattrname)

def get_defaultparameters_functions(namespace):
    return dict([(fname, fvalue) for fname,fvalue in namespace.items() if is_defaultparameters_function(fvalue)])

def get_defaultparameters(namespace):
    # if a function is passed here
    if is_defaultparameters_function(namespace) : 
        return getattr(namespace,_dfattrname)
    
    # if a namespace is given here
    dpfunctions = get_defaultparameters_functions(namespace)
    results = {}
    for func in dpfunctions.values():
        results.update(getattr(func,_dfattrname))
    return results

def get_redefinedparameters(namespace):
    defparameters = get_defaultparameters(namespace)
    return dict([(pname, pvalue) for pname, pvalue in defparameters.items() if pvalue != namespace[pname]])

def get_parameters(namespace):
    defparameters = get_defaultparameters(namespace)
    return dict([(pname, namespace[pname]) for pname in defparameters.keys()])



__all__ = ['defaultparameters', 'is_defaultparameters_function', 'get_defaultparameters_functions', 'get_defaultparameters', 'get_redefinedparameters']