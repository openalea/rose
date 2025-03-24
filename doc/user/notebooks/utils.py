from math import pi, radians
from openalea.plantgl.all import (Scene, Disc, Translated, Shape, Vector3
, Material, Color3, AxisRotated)

from openalea.rose import data
from openalea.rose.data import sensors
from openalea.rose.mockup import rose
from openalea.rose.mockup.rose_geometry import (
    vertexVisitor, reconstructWithTurtle,
    computeLeafletFrom4pts,
    bezierPatchFlower, petalMatrix,
    computeKnop4pts, drawStipule3pts
)

import pandas


def grid(dir):
    return dir/'grid.txt'

def origin(dir):
    return dir/'origin.txt'

def reconstruct(g):
    lx = [0, 0.2, 0.4, 0.6, 0.8, 1.]
    ly = [0, 0.86, 0.95, 0.81, 0.41, 0]

    leaf_factory = computeLeafletFrom4pts(lx, ly)
    sepal_factory = leaf_factory
    matrix, = petalMatrix()
    bud_factory = bezierPatchFlower(matrix,0,0)
    flower_factory = fruit_factory = bud_factory
    knop_factory = computeKnop4pts()
    stipule_factory = drawStipule3pts()

    visitor = vertexVisitor(leaf_factory=leaf_factory,
                            bud_factory=bud_factory,
                            sepal_factory=sepal_factory,
                            flower_factory=flower_factory,
                            fruit_factory=fruit_factory,
                            knop_factory=knop_factory,
                            stipuLe_factory=stipule_factory)
    scene, = reconstructWithTurtle(g, visitor, 2.1)
    return scene



def myMTG(dir):
    grid_fn = grid(dir)
    origin_fn = origin(dir)

    dictofindices, gridSpecs = rose.getGrid(grid_fn)
    # print(f'Grid : {dictofindices}, {gridSpecs}')
    _origin = rose.getOrigin(origin_fn)
    # print(f'Origins : {_origin}')

    plantlist = dictofindices
    existingmtglist, = rose.localDir2DictOfFiles(
        [str(fn) for fn in dir.glob('*.mtg')])
    excludelist = []
    gridDef = gridSpecs
    _origin = _origin
    DoFill = True
    DoRotate = True

    dictOfPositions, = rose.cropGeneration_2011(
        plantlist=plantlist,
        existingmtglist=existingmtglist,
        excludelist=excludelist,
        gridDef=gridDef,
        origin=_origin,
        DoFill=DoFill,
        DoRotate=DoRotate)

    # print(dictOfPositions)

    listofmtgs, = rose.files2MTGs(dictOfPositions)

    # print(listofmtgs)

    mtg_union, = rose.mTG_union(listofmtgs)

    return mtg_union

def get_all_expe():
    names = data.manips()

    exps = []
    for name in names:
        exps.extend(data.experiments(name))
    return exps

def environment():
    return Scene(data.environments()[0])

def experiment(idx=0):
    expes = get_all_expe()
    d = expes[idx]
    g=myMTG(d)
    scene = reconstruct(g)
    env = Scene(data.environments()[0])
    scene.add(env)
    return scene

def sensor_exp(idx=0):
    sen = sensors()[idx]
    sensor_scene = Scene()
    df = pandas.read_csv(sen)

    for _, row in df.iterrows():
        d = Shape(Disc(int(row["rayon_capteur"])))
        m = Material(Color3(150,0, 0))
        if "Orientation" in row.keys():
            if row["Orientation"] == "Sideward":
                m = Material(Color3(0,0, 150))
                orient = Vector3(1, 0, 0)
                d = Shape(AxisRotated(orient, radians(90), d.geometry))

        d = Shape(Translated(Vector3(int(row['X']), int(row['Y']), int(row['Z'])), d.geometry), m)
        sensor_scene.add(d)
    return sensor_scene
