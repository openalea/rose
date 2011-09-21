#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import re
import urllib

def httpDir2DictOfFiles(url, listoffilenames=[]):
    # downloads files from a web server in temp. files, then return the dictionnary that associates temp files and filenames.
    dictoffiles = {}
    htmlfile=""
    # write the node code here.
    (htmlfile, h) = urllib.urlretrieve ( url +"/", None, urllib.reporthook)
    htmlfile. = htmlfile.split("\n")
    for ligne in htmlfile:
    #print "ligne= %s" % ligne
    if re.search (filtre, ligne):
        filename=re.sub("<li><a href=\"","",ligne)
        filename=re.sub("\">.*</a></li>$","", filename)
        #print "(filtre, ligne) = (%s,%s)" % (filtre, ligne)
        listoffiles += [filename]

    for fichier in listoffiles:
        #url=urllib.URLopener(open_http)

        #objet=url.open_file(webserver +"/"+ fichier)

        fn, h = urllib.urlretrieve(url +"/"+ fichier, None, urllib.reporthook)
        #print "(fn,h) =  (%s, %s)" % (fn,h)
        dictoffiles[fichier] = fn
        
    # return outputs
    return dictoffiles,
