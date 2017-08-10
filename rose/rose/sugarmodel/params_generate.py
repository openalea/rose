

def param_order(param_file):
    f = file(param_file,'r')
    result = []
    for l in f:
        if '=' in l and l[0] == ' ' and (not ',' in l):
            lsplit = l.split('=')
            var = lsplit[0].strip()
            value = lsplit[1]
            if isfloat(value):
                result.append(var)
    return result

def isfloat(txt):
    try:
        float(txt.strip())
        return True
    except ValueError, ve:
        return False

def generate_template(param_file):
    f = file(param_file,'r')
    result = ''
    for l in f:
        if '=' in l and l[0] == ' ' and (not ',' in l):
            lsplit = l.split('=')
            var = lsplit[0]
            value = lsplit[1]
            if isfloat(value):
                result += var+'= {}\n'
            else:
                result += l                
        else: result += l
    return result


def generate_params(params, param_file):
    paramnames = param_order(param_file)
    pvalues = []
    for p in paramnames:
        pvalues.append(params[p])
        del params[p]



    content = generate_template(param_file)
    #content = file(template,'r').read()
    #print content
    content = content.format(*pvalues)
    #for k,v in params.items():
    #    content += str(k)+' = '+str(v)+'\n'
    return content

def update_param_file(paramfile, newvalues = {}):
    from datetime import datetime
    w,v = {},{}
    execfile(paramfile,w,v)
    v.update(newvalues)
    content = generate_params(v, paramfile)
    import shutil
    shutil.copy(paramfile,paramfile+'-'+datetime.now().strftime('%d-%m-%y_%H-%M-%S'))
    print 'Write parameters in file',repr(paramfile)
    f = file(paramfile,'w')
    f.write(content)

def get_param_names(paramtags, paramfile):
    def contains(l, pattern):
        try:
            idx = l.index(pattern)
            return l[idx-1] in ' \t\n' and l[idx+len(paramtags)] in ' \t\n' 
        except ValueError,e:
            return False

    f = file(paramfile)
    for l in f:
        if contains(l,paramtags ):
            return map(lambda x:x.strip(), l.split('=')[0].split(','))

def get_all_param_names(paramtags,paramfile):
    def contains(l, pattern):
        try:
            idx = l.index(pattern)
            return l[idx-1] in ' \t\n' and l[idx+len(pattern)] in ' \t\n' 
        except ValueError,e:
            return False

    f = file(paramfile)
    results = []
    for l in f:
        for tag in paramtags:
            if contains(l,tag ):
                results += map(lambda x:x.strip(), l.split('=')[0].split(','))
    return results
