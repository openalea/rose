
def param_order(template_file):
    f = file(template_file,'r')
    result = []
    for l in f:
        if '%f' in l:
            var = l.split('=')[0].strip()
            result.append(var)
    return result

def generate_params(params):
    template = 'params.py.template'
    paramnames = param_order(template)
    print params
    print paramnames
    pvalues = []
    for p in paramnames:
        pvalues.append(params[p])
        del params[p]
    content = file(template,'r').read()
    #print content
    print pvalues
    content = content % tuple(pvalues)
    #for k,v in params.items():
    #    content += str(k)+' = '+str(v)+'\n'
    return content

def update_param_file(paramfile, newvalues = {}):
    w,v = {},{}
    execfile(paramfile,w,v)
    v.update(newvalues)
    content = generate_params(v)
    import shutil
    shutil.copy(paramfile,paramfile+'~')
    print 'Write parameters in file',repr(paramfile)
    f = file(paramfile,'w')
    f.write(content)
