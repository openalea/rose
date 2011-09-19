#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import re
import urllib

def httpDir2DictOfFiles(url, listoffilenames=[]):
    '''    downloads files from a web server in temp. files, then return the dictionnary that associates temp files and filenames.
    '''
    dictoffiles = {}; 
    # write the node code here.
    
    for fichier in listoffilenames:
        #url=urllib.URLopener(open_http)

        #objet=url.open_file(webserver +"/"+ fichier)

        fn, h = urllib.urlretrieve(url +"/"+ fichier, None, urllib.reporthook)
        #print "(fn,h) =  (%s, %s)" % (fn,h)
        dictoffiles[fichier] = fn
        
    # return outputs
    return dictoffiles,
