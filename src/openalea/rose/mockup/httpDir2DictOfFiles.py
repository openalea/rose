#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
#
# $Id$
#
import re

from urllib import request, reporthook


def httpDir2DictOfFiles(url, filtre=".mtg"):
    # downloads files from a web server in temp. files, then return the dictionary that associates temp files and filenames.
    dictoffiles = {}
    listoffiles = []
    # write the node code here.
    (htmlFileName, h) = request.urlretrieve(url + "/", None, reporthook)
    htmlfile = open(htmlFileName, "r")
    htmlfileContent = htmlfile.read()
    htmlfileContent = htmlfileContent.split("\n")
    for ligne in htmlfileContent:
        if re.search(filtre, ligne):
            filename = re.sub('<li><a href="', "", ligne)
            filename = re.sub('">.*</a></li>$', "", filename)
            listoffiles += [filename]
    htmlfile.close()
    for fichier in listoffiles:
        fn, h = request.urlretrieve(url + "/" + fichier, None, reporthook)
        dictoffiles[fichier] = fn

    # return outputs
    return (dictoffiles,)
