#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import re

def httpFileList(htmlfile, filtre):
    '''    gets web directory listing
    '''
    listoffiles = [] ; 
    # write the node code here.
    htmlfile=htmlfile.split("\n")
    for ligne in htmlfile:
        #print "ligne= %s" % ligne
        if re.search (filtre, ligne):
            filename=re.sub("<li><a href=\"","",ligne)
            filename=re.sub("\">.*</a></li>$","", filename)
            #print "(filtre, ligne) = (%s,%s)" % (filtre, ligne)
            listoffiles += [filename]

    # return outputs
    return listoffiles,
