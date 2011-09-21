#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
import re
import urllib
def httpDir2DictOfFiles(url, filtre='') :
    # downloads files from a web server in temp. files, then return the dictionnary that associates temp files and filenames.
    dictoffiles = {}
    listoffiles=[]
    htmlfile=""
    # write the node code here.
    (htmlFileName, h) = urllib.urlretrieve ( url +"/", None, urllib.reporthook)
    htmlfile=open(htmlFileName,"r")
    htmlfileContent=htmlfile.read()
    htmlfileContent = htmlfileContent.split("\n")
    for ligne in htmlfileContent:
        print "ligne= %s" % ligne
        if re.search (filtre, ligne):
            filename=re.sub("<li><a href=\"","",ligne)
            filename=re.sub("\">.*</a></li>$","", filename)
            #print "(filtre, ligne) = (%s,%s)" % (filtre, ligne)
            listoffiles += [filename]
    htmlfile.close()
    for fichier in listoffiles:
        #url=urllib.URLopener(open_http)

        #objet=url.open_file(webserver +"/"+ fichier)

        fn, h = urllib.urlretrieve(url +"/"+ fichier, None, urllib.reporthook)
        #print "(fn,h) =  (%s, %s)" % (fn,h)
        dictoffiles[fichier] = fn
        
    # return outputs
    return dictoffiles,
