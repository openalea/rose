#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# $Id$
#
"""
.. module rose_file
.. moduleauthor:: H. Autret <herve.autret@inrae.fr>
"""

import os
import re
import json
import csv

# for csv
from openalea.core.external import Node, IBool, IInt, ISequence, IStr  # *
import openalea.core.logger as ocl

import openalea.plantgl.all as pgl


def getHomeDir():
    """
    On 2020/02/24, the packagedir and expand_user_dir stopped
    to run.
    """
    return os.getenv("HOME")


class GetHomeDir(Node):
    def __init__(self):
        self.add_output(name="homeDir", interface=IStr)

    def __call__(self):
        return getHomeDir


def readCsv(fileName, delimiter=",", ligne_debut=0):
    """we read the csv file, then we return a list of split lines"""
    retList = []
    fIn = open(fileName, "U")
    if not fIn:
        ocl.error("%s : no such file" % fileName)
        return retList
    else:
        csvIn = csv.reader(fIn, delimiter=delimiter)
        lu = 0
        for ligne in csvIn:
            if ligne:
                sortie = []
                if lu >= ligne_debut:
                    for item in ligne:
                        sortie.append(item)
                    retList.append(sortie)
            lu += 1
        fIn.close()
    return retList


# end readCsv


class ReadCsv(Node):
    def __init__(self):
        Node.__init__(self)
        self.add_input(name="fileName", interface=IStr, value=None)
        self.add_input(name="delimiter", interface=IStr, value=",")
        self.add_input(name="ligne_debut", interface=IInt, value=0)
        self.add_output(name="retList", interface=ISequence)

    def __call__(self, inputs):
        return readCsv


def readXls(fileName, numero_feuille=0, ligne_debut=0):
    """we used to read the "fileName" xls file, then we could return a list of split lines
    There is no more a xlrd module within openalea
    """
    import xlrd

    retList = []
    wb = xlrd.open_workbook(fileName)
    if not wb:
        ocl.error("%s : no such file" % fileName)
        return retList
    else:
        try:
            sh1 = wb.sheet_by_index(numero_feuille)
        except:
            print(
                "Le classeur %s n'a pas de feuille numéro %d"
                % (fileName, numero_feuille)
            )
            return retList
        #        rep=""
        #        plantID=""
        for rx in range(sh1.nrows):
            sortie = []
            if rx >= ligne_debut:
                for item in sh1.row(rx):
                    sortie.append(item.value)
                retList.append(sortie)

    return retList


# end readXls


class ReadXls(Node):
    def __init__(self):
        Node.__init__(self)
        self.add_input(name="fileName", interface=IStr, value=None)
        self.add_input(name="sheet_number", interface=IInt, value=0)
        self.add_input(name="ligne_debut", interface=IInt, value=0)
        self.add_output(name="retList", interface=ISequence)

    def __call__(self, inputs):
        return readXls


# end Class readXls

# for scene2can01


def mesh(geometry):
    # d = pgl.Tesselator()
    # geometry.apply(d)
    # return d.result
    tessel = pgl.Tesselator()
    geometry.apply(tessel)
    mesh_ = tessel.triangulation
    return mesh_


def canline(ind, couleur, p):
    return "p 2 007 0x%02X%02X%02X 3 %s" % (
        couleur.red,
        couleur.green,
        couleur.blue,
        " ".join(str(x) for i in ind for x in p[i]),
    )


def scene2Can01(maScene, fileName, makeDir=False):
    # inspired from alinea.topvine
    out = []
    for obj in range(len(maScene)):
        couleur = maScene[obj].appearance.diffuseColor()
        geometry = mesh(maScene[obj])
        p = geometry.pointList
        index = geometry.indexList
        for ind in index:
            out.append(canline(ind, couleur, p))

    if makeDir:
        chemin = os.path.dirname(fileName)
        if not os.path.isdir(chemin):
            os.system("mkdir -p %s" % chemin)

    o = open(fileName, "w")  # storage in a persistent can file
    o.write("CAN01\n")
    for i in range(len(out)):
        o.write(out[i] + "\n")

    o.close()
    return maScene


class Scene2Can01(Node):
    def __init__(self):
        Node.__init__(self)
        self.add_input(name="maScene", interface=None, value=None)
        self.add_input(name="fileName", interface=IStr, value="can01.can")
        self.add_input(name="makeDir", interface=IBool, value=False)
        self.add_output(name="maScene", interface=None)

    def __call__(self, inputs):
        return scene2Can01


def intSort(listeOfStrings):
    """returns a numerically sorted list of string'd numbers"""
    resN = []  # tmp list for nums
    resS = []  # tmp list for strings
    for elt in listeOfStrings:
        try:
            tmpNum = int(float(elt))
            resN.append(tmpNum)
        except:
            resS.append(elt)
            continue
    resN.sort()
    # tri de fichiers sur le numero dans "/PATHTO/numero.ext" :
    resS.sort(key=lambda v: int(v.rsplit("/", 1)[1].split(".")[0]))
    resNOut = ["%s" % elt for elt in resN]
    return resNOut + resS


class IntSort(Node):
    def __init__(self):
        Node.__init__(self)
        self.add_input(name="strList", interface=ISequence, value=[])
        self.add_output(name="sortedList", interface=ISequence, value=None)

    def __call__(self, inputs):
        listeFics = self.get_input("strList")
        return intSort(listeFics)


def tempPickleFile(filename):
    """returns a temp file name in a temp dir according to the os"""
    # write the node code here.
    if filename is None:
        filename = "tempfile.dat"
    import os

    tempDir = os.getenv("TEMP")
    if not tempDir:
        tempDir = "/tmp"
    picklefile = tempDir + os.sep + filename
    # return outputs
    return (picklefile,)


def jsonDump(data, file_path):
    # unfortunately, json says that an MTG is not serializable
    #
    f = open(file_path, "w")
    json.dump(data, f, indent=4)
    f.close()


# fin jsonDump


def jsonLoad(file_path):
    f = open(file_path, "r")
    data = json.load(f, indent=4)
    f.close()
    return data


# fin jsonLoad


def rootName(nom):
    """returns the numeric sequence at the beginning of the file name"""
    root = nom.rsplit("/", 1)[-1]
    root = root.split(".", 1)[0]
    root = re.sub("^([0-9]+).*", "\\1", root)
    return root


class RootName(Node):
    def __init__(self):
        Node.__init__(self)
        self.add_input(name="fileName", interface=IStr, value="")
        self.add_output(name="rootName", interface=IStr, value=None)

    def __call__(self, inputs):
        nomFic = self.get_input("fileName")
        return rootName(nomFic)


if __name__ == "__main__":
    import unittest

    class TestSimple(unittest.TestCase):
        def setUp(self):
            self.root = "toto"
            self.tupleInt = (
                "1",
                "2",
                "4",
                "9",
                "16",
                "25",
                "36",
                "49",
                "64",
                "81",
                "100",
            )
            pass

        def tearDown(self):
            pass

        def test01_rootName(self):
            nom = "titi/%s.txt" % self.root
            self.assertEqual(self.root, rootName(nom))

        def test02_intSort(self):
            import random

            l1 = list(self.tupleInt)
            random.shuffle(l1)
            liste = ["%s" % elt for elt in l1]
            random.shuffle(liste)
            # there is a one in (10!)² chance that the test result is due to chance
            self.assertEqual(self.tupleInt, tuple(intSort(liste)))

            t1 = tuple(l1)
            # it is no longer due to chance:
            self.assertNotEqual(t1, tuple(intSort(liste)))

    unittest.main()
