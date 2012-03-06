#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import os
import re
import subprocess
import sys



dicManips={"M1":["M1-PARfort","M1-PARfaible"], "M2":["M2-PARfort","M2-PARfaible"],"M3":["M3-PARfF"]}

dicDirs={"M1-PARfort":"Manip1_C1_PARfort","M1-PARfaible":"Manip1_C2_PARfaible","M2-PARfort":"Manip2_C1_PARfort","M2-PARfaible":"Manip2_C2_PARfaible","M3-PARfF":"Manip3_C1C2_PARfF"}

dicPrel={"M1-PARfort":3,"M1-PARfaible":3,"M2-PARfort":2,"M2-PARfaible":2,"M3-PARfF":3}

def InstallGrids(ROOT):
    #print "Todo !"
    sCommande = "ls *.fake" 
    FakesProc=subprocess.Popen(sCommande, stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    FakesOnes=FakesProc.stdout.read()
    FakesOnes=FakesOnes.split("\n")
    FakesOnes.remove("")
    sCommande = "ls 2011-M*.txt" 
    RealsProc=subprocess.Popen(sCommande, stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    TrueOnes=RealsProc.stdout.read()
    TrueOnes=TrueOnes.split("\n")
    TrueOnes.remove("")
    positions="positions.txt"
    origine="origin.txt"
    for manip in dicManips.keys():
        print "manip %s" %manip
        #if re.search(manip, TrueFile):
        for sousManip in dicManips[manip]:
            print "sousManip %s" % sousManip
            #if re.search (sousManip,TrueFile):
            for prel in range(1,dicPrel[sousManip]+1):
                print "prel P%d" % prel 
                fullPath="%s/%s/P%d" % \
                    (ROOT,dicDirs[sousManip], prel)
                #for TrueFile in TrueOnes:
                Target="2011-%s-P%d.txt" % (sousManip, prel) 
                if Target in TrueOnes :
                    print " ---------- Got one!"
                    sCommande = "cp %s %s/%s" % (Target, fullPath, positions )
                    #print sCommande
                    #os.system(sCommande)
                    
                else:
                    print " ---------- Nope..."
                    FakeFile="2011-%s-P%d.fake" % (sousManip, prel)
                    sCommande = "cp %s %s/%s" % \
                        (FakeFile ,fullPath ,positions )
                print sCommande
                os.system(sCommande)
                # Origine
                # TODO : find out what is the origin for Manip3_C1C2
                # and set up this code properly
                if re.search("C1",fullPath):
                    sCommande = "cp C1_origine.txt %s/%s" %(fullPath , origine)
                else:
                    sCommande = "cp C2_origine.txt %s/%s"%(fullPath , origine)
                print sCommande
                os.system(sCommande)
                   
                #continue
                            
                                
    
    

def max (listofnumbers):
    res=-9999
    for item in listofnumbers:
        item = int(item.rsplit(".")[0])
        if res < item :
            res = item
    return res

def processLiveness(process):    
    from os import waitpid, P_NOWAIT, WIFEXITED, WEXITSTATUS, WIFSIGNALED, WTERMSIG
    from errno import ECHILD
    try:
       pid, status = waitpid(process.pid, P_NOWAIT)
       if pid:
         if WIFSIGNALED(status):
            print "Processus tue par le signal %s" % WTERMSIG(status)
         elif WIFEXITED(status):
            print "Processus termine: code %s" % WEXITSTATUS(status)
         #else:
         #   print "Processus termine"
       else:
         print "Processus toujours actif"   
    except OSError, err:
       if err.errno == ECHILD:
          print "Processus mort"
       else:
          print "Erreur inconnue"


def makeFakeGrids(ROOT):
    # We list the files by here
    sCommande = "ls *.txt" 
    FichiersExistants=subprocess.Popen(sCommande, stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    ListeExistants=FichiersExistants.stdout.read()
    ListeExistants=ListeExistants.split("\n")
    ListeExistants.remove("")
    processLiveness(FichiersExistants) # for fun

    for manip in sorted(dicManips.keys()):
        for sousManip in dicManips[manip] :
            print "%s::%s : %s/%s" % (manip, sousManip,ROOT,dicDirs[sousManip])
            for prel in range(1,dicPrel[sousManip]+1):
                print "P%d" % prel
                os.system("ls %s/%s/P%d|wc -l" %(ROOT,dicDirs[sousManip],prel))
                sCommande = "cd %s/%s/P%d ; ls *.mtg" % (ROOT,dicDirs[sousManip],prel)
                Fichiers=subprocess.Popen(sCommande, stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
                Liste=Fichiers.stdout.read()
                Liste=Liste.split("\n")
                Liste.remove("")
                
                OutFileName="2011-%s-P%d" % (sousManip,prel)
                if "%s.txt" % OutFileName in ListeExistants:
                    continue
                else :
                    OutFileName = "%s.fake" % OutFileName
                fOut=open(OutFileName,"w")
                indexListe=0
                indexBrut=0
                #fakeNumPlante=max(Liste)+1
                fakeNumPlante=9999
                for y in range(0,6):
                    for x in range(0,13):
                        numPlante=fakeNumPlante
                        if indexListe < len(Liste):
                            if indexBrut %2 == 0 :
                                numPlante=Liste[indexListe].rsplit(".")[0]
                                indexListe +=1
                        indexBrut += 1
                        #fakeNumPlante += 1
                        fOut.write("%s\t%d\t%d\n" % (numPlante, x,y))
                #fOut.write("\n")
                fOut.close()

def test():
    print "nothing done !"
    return

def work(ROOT):
    print "working !"
    makeFakeGrids(ROOT)
    InstallGrids(ROOT)

if __name__ == "__main__" :
    #test()
    ROOT="/mnt/echange/samba/MTG"
    if len(sys.argv) > 1:
        ROOT=sys.argv[1]
    work(ROOT)
