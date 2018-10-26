#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# $Id$
#
# imports globaux
import os,re

from openalea.core.external import Node, ISequence, IStr# *

myViewer="xv"

class RunXV(Node):
    def __init__(self):
        Node.__init__(self)
        self.add_input( name = 'iFileName', interface=IStr)
        self.add_output(name = 'oFileName', interface = IStr)
    def __call__( self, inputs ):
        fName = self.get_input( 'iFileName' )
        commande="%s %s &" % (myViewer, fName)
        os.system (commande)
        return fName

def decode_liste(codes=[], colonnes=[]):
    retVal=[]
    clefs=["M1","M2","M3", "C1","C2","FORT","FAIB"]
    manips=["Manip1","Manip2","Manip3", "C1","C2", "PARfort","PARfaible"]
    prelevements=["P1","P2","P3"]
    dictOfDirs={}
    listOfPlants=[]

    #print "Entrée: \"%s\"" % codes

    map(lambda k, v: dictOfDirs.update({k: v}), clefs, manips)
    col_manip=0
    col_plante=2
    if colonnes :
        if len(colonnes == 2):
            col_manip = colonnes[0]
            col_plante = colonnes[1]
        else:
            print "decode_liste() : Attention : préciser deux colonnes ou rien"

    for ligne in codes:
        #print "ligne : \"%s\"" % ligne
        if ligne:
            manip=ligne[col_manip]
            plante_ID=ligne[col_plante]
            outDir=""
            for cle in clefs :
                if re.search(cle, manip):
                    outDir += "%s_" % dictOfDirs[cle]
            outDir=re.sub("_$","/", outDir) # le dernier souligné
            for prelev in prelevements:
                if re.search(prelev, manip):
                    outDir += "%s/" % prelev
            #print "DIR : \"%s\"" % result
            # le répertoire devrait être reconstitué
            if not outDir == "" :
                plante=re.sub("^([0-9]+)_.*","\\1", plante_ID)
                # print "Plante : %s" % plante
                result= "%s%s"% (outDir, plante)
                #result += "%s" % plante
                if not result in listOfPlants:
                    listOfPlants.append(result)
                    retVal.append(result)

    return retVal
# decode_list

class Decode_liste(Node):
    def __init__(self):
        Node.__init__(self)
        self.add_input( name = 'list_of_codes', interface=ISequence)
        self.add_input(name= 'colonnes', interface = ISequence, value=[])
        self.add_output(name = 'list_of_plants', interface = ISequence)
    def __call__( self, inputs ):
        codes= self.get_input('list_of_codes')
        plantes=decode_liste(codes)
        return plantes

if __name__ == "__main__":

    # This is a test :
    # in the openalea environment, i.e with the (openalea) prompt,
    # typing "python ./rose_process.py [-(t|h)]" runs.
    # It means that openalea.core.* imports are successful,
    # so that we can do many things within the conda environment.
    
    import sys
    testTag=[ '-t', '--test']
    helpTag=[ '-h', '--help']

    helpString=""" Test du module %s
     Syntaxe :
       %%s [-h] [-t]
       alias :
      -t in %s : effectue des tests internes
      -h in %s : affiche ce message
      """ % (sys.argv[0], testTag, helpTag)

    def testFunc():
         return False

    def Help(code, msg):
         print "%s" % msg
         sys.exit(code)
         
    import unittest
    class TestSimple(unittest.TestCase):
        def setUp(self):
            pass
        def tearDown(self):
            pass
        def test01_testFunc(self):
            self.assertFalse(testFunc())

    for arg in sys.argv[1:]:
        if  arg in testTag:
            sys.argv.remove(arg)
            unittest.main()
        elif arg in helpTag:
            Help(0, helpString)
        else:
            print """Argument "%s" non reconnu :  S T O P  !""" % arg
            Help(-1, helpString)

    # anyway :
    unittest.main()
