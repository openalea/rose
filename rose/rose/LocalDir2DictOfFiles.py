import os

def LocalDir2DictOfFiles(listoffiles):
    '''    makes a dict of names: complete_path from a dirname and a name filter
    '''
    dictoffiles = {} ; 
    # write the node code here.
    # downloads files from a web server in temp. files, then return the dictionnary that associates temp files and filenames.
    for fichier in listoffiles:
        
        dictoffiles[os.path.basename(fichier)] = fichier

    # return outputs
    return dictoffiles,
