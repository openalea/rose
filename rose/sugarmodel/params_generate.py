"""
    Method to regenerate a parameter file with updated values.
"""

def isfloatortuple(txt):
    if '#' in txt:
        txt = txt[:txt.index('#')]
    if ',' in txt:
        return min(map(isfloatortuple, txt.split(','))) == True
    else:
        try:
            float(txt.strip())
            return True
        except ValueError, ve:
            return False

def generate_template(param_file):
    f = file(param_file,'r')
    result = ''
    for l in f:
        if '=' in l and l[0] == ' ':
            lsplit = l.split('=')
            var = lsplit[0]
            value = lsplit[1]
            if isfloatortuple(value):
                if ',' in value:
                    nvalues = value.split(',')
                    result += var+'= {'+var.strip()+'},'+','.join(nvalues[1:])
                else:
                    result += var+'= {'+var.strip()+'}\n'
            else:
                result += l                
        else: result += l
    return result

def generate_paramfile(params, param_file):
    content = generate_template(param_file)
    print content
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
    print content

    print 'Write parameters in file',repr(paramfile)
    if not exists(backupdir) : makedirs (backupdir)
    shutil.copy(paramfile,join(backupdir, paramfile+'-'+datetime.now().strftime('%d-%m-%y_%H-%M-%S')))
    f = file(paramfile,'w')
    f.write(content)


def get_parameters(paramtags, paramfile):
    # New way of defining parameters
    from defaultparameters import is_defaultparameters_function, get_defaultparameters

    w,v = {},{}
    execfile(paramfile,w,v)
    if paramtags in v and is_defaultparameters_function(v[paramtags]):
        return get_defaultparameters(v[paramtags])

