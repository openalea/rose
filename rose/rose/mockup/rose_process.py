#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

# imports globaux
import os,re,sys

# imports du projet
import process
day=process.dayTime()

helpString=""" On fait ci et ça
Syntaxe :
  %%s [-h] [-t]
  alias : 
 -t in %s : effectue des tests internes
 -h in %s : affiche ce message
 """ % (process.testTag, process.helpTag)

# remove
readDummy=False
dummyTag=""

def faitCeci():
    return False

from openalea.core.external import * 
from openalea.core.logger  import *
import os
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

    print "Entrée: \"%s\"" % codes
    
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
                    # preparer les répertoires de stockage pour les can
                    #os.system("mkdir -p can/%s" % outDir) 
        
    
    return retVal


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
    import unittest
    class TestSimple(unittest.TestCase):
        def setUp(self):
            pass
        def tearDown(self):
            pass
        def test01_faitCeci(self):
            self.assertFalse(faitCeci)

    for arg in sys.argv[1:]:
        if readDummy:
            dummy=arg
            readDummy=False
        elif arg in process.testTag:
            sys.argv.remove(arg)        
            unittest.main()
        elif arg in process.helpTag:
            process.Help(0, helpString)
        else:
            print """Argument "%s" non reconnu :  S T O P  !""" % arg
            process.Help(-1, helpString)
