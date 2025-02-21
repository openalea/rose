#! /usr/bin/env python
# -*- coding: iso-8859-1 -*-

import os


def GetLocalFiles(filesInPath=None):
    """Create a dictionary from the list of available files"""
    if filesInPath is None:
        filesInPath = []
    dictoffilenames = {}
    # write the node code here.
    # filesInPath=filesInPath.split("\n")
    filesInPath = filesInPath
    for fichier in filesInPath:
        nomFich = os.path.basename(fichier)
        dictoffilenames[nomFich] = fichier
    # return outputs
    return (dictoffilenames,)
