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
