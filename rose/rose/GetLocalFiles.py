import os

def GetLocalFiles(filesInPath):
    '''    Create a dictionnary from the list of available files 
    '''
    dictoffilenames = {}; 
    # write the node code here.
    for fichier in filesInPath:
        nomFich = os.path.basename(fichier)
        dictoffilenames[nomFich] = fichier
    # return outputs
    return dictoffilenames,
