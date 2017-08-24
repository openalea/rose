

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
                result += var+'= {'+var.strip()+'}\n'
            else:
                result += l                
        else: result += l
    return result

def generate_paramfile(params, param_file):
    content = generate_template(param_file)
    content = content.format(**params)
    return content

def update_param_file(paramfile, newvalues = {}):
    from datetime import datetime
    from os.path import join, exists
    from os import makedirs
    import shutil

    backupdir = 'backup'

    w,v = {},{}
    execfile(paramfile,w,v)
    v.update(newvalues)
    content = generate_paramfile(v, paramfile)

    print 'Write parameters in file',repr(paramfile)
    if not exists(backupdir) : makedirs (backupdir)
    shutil.copy(paramfile,join(backupdir, paramfile+'-'+datetime.now().strftime('%d-%m-%y_%H-%M-%S')))
    f = file(paramfile,'w')
    f.write(content)


def get_parameters(paramtags, paramfile):
    # New way of defining parameters
    from defaultparameters import is_defaultparameters_function

    w,v = {},{}
    execfile(paramfile,w,v)
    if paramtags in v and is_defaultparameters_function(v[paramtags]):
        return v[paramtags].values

    # old ways
    def contains(l, pattern):
        try:
            idx = l.index(pattern)
            return l[idx-1] in ' \t\n' and l[idx+len(paramtags)] in ' \t\n' 
        except ValueError,e:
            return False

    f = file(paramfile)
    paramnames = None
    for l in f:
        if contains(l, paramtags ):
            paramnames = map(lambda x:x.strip(), l.split('=')[0].split(','))
            break
 
    namespace = {}
    execfile(paramfile, namespace)
    
    return dict([(p,namespace[p]) for p in paramnames])

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
