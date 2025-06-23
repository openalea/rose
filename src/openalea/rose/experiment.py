import os
from math import radians

from openalea.mtg import MTG
from openalea.plantgl.all import (Scene, Disc, Translated, Shape, Vector3
, Material, Color3, AxisRotated, Frustum, Text)

from openalea.rose import data
from openalea.rose.data import sensors, expe2_dir
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

def reconstruct(g, positions):
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

    m = Material("brown", Color3(43, 29, 14))
    m2 = Material("substrat", Color3(25, 25, 25))
    for plant, position in positions.items():
        plant_name = os.path.basename(plant).split('.')[0]
        # Adding pot
        f = Shape(Frustum(20,80, 1.5, True, 12))
        pos = position[0][0]
        f = Shape(Translated(pos[0], pos[1], pos[2], f.geometry), m)
        scene.add(f)

        # Adding dirt
        d = Shape(Disc(30, 12))
        d = Shape(Translated(pos[0], pos[1], pos[2] + 80.5, d.geometry), m2)
        scene.add(d)

        # Adding Text
        t = Text(plant_name, Vector3(pos[0], pos[1], pos[2] + 40))
        scene.add(t)
    return scene


def reconstruct_to_pos(g, position, plant_id):
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

    for sh in scene:
        sh.geometry = Translated(Vector3(position["x"],
                                         position["y"],
                                         900), sh.geometry)

    m = Material("brown", Color3(43, 29, 14))
    m2 = Material("substrat", Color3(25, 25, 25))
    # Adding pot
    f = Shape(Frustum(20,80, 1.5, True, 12))
    f = Shape(Translated(position["x"], position["y"], 900, f.geometry), m)
    scene.add(f)

    # Adding dirt
    d = Shape(Disc(30, 12))
    d = Shape(Translated(position["x"], position["y"], 900 + 80.5, d.geometry), m2)
    scene.add(d)
    # Adding Text
    t = Text(plant_id, Vector3(position["x"], position["y"], 900 + 40))
    scene.add(t)
    return scene

def myMTG(dir, fill=True):
    grid_fn = grid(dir)
    origin_fn = origin(dir)

    dictofindices, gridSpecs = rose.getGrid(grid_fn)
    _origin = rose.getOrigin(origin_fn)

    plantlist = dictofindices
    name_list = [str(fn) for fn in dir.glob('*.mtg')]

    existingmtglist, = rose.localDir2DictOfFiles(name_list)

    excludelist = []
    gridDef = gridSpecs
    _origin = _origin
    DoFill = fill
    DoRotate = True

    dictOfPositions, positions = rose.cropGeneration_2011(
        plantlist=plantlist,
        existingmtglist=existingmtglist,
        excludelist=excludelist,
        gridDef=gridDef,
        origin=_origin,
        DoFill=DoFill,
        DoRotate=DoRotate)

    listofmtgs, = rose.files2MTGs(dictOfPositions)

    mtg_union, = rose.mTG_union(listofmtgs)

    return mtg_union, dictOfPositions

def get_all_manips():
    names = data.manips()

    exps = []
    for name in names:
        exps.extend(data.experiments(name))
    return exps

def environment():
    return Scene(data.environments()[0])

def save_gltf(scene, filename):
    from openalea.scenemanagement.convert import GLTFScene
    gltf = GLTFScene(scene)
    gltf.run()
    gltf.to_gltf(filename)

def manip_named(manip_name="", stage="", fill=False):
    expes = get_all_manips()
    expes = list(filter(lambda x: manip_name in str(x) and stage in str(x), expes))
    d = expes[0]
    g, positions=myMTG(d, fill)
    scene = reconstruct(g, positions)
    return scene

def experiment(idx=0, fill=True):
    expes = get_all_manips()
    d = expes[idx]
    g, positions=myMTG(d, fill)
    scene = reconstruct(g, positions)
    return scene

def experiment2(disposition=0):
    d = os.path.join(expe2_dir())
    pos_file = os.path.join(expe2_dir(), "emplacementEtOrientationPlantesExpe2.csv")
    scene = Scene()

    # Create grid here
    pos_grid = [
        {"x": 1200, "y": 545},
        {"x": 1050, "y": 620},
        {"x": 1350, "y": 620},
        {"x": 1200, "y": 695},
        {"x": 1050, "y": 770},
        {"x": 1350, "y": 770},
        {"x": 1200, "y": 845},
        {"x": 1050, "y": 920},
        {"x": 1350, "y": 920},
        {"x": 1200, "y": 995},
        {"x": 1050, "y": 1070},
        {"x": 1350, "y": 1070},
        {"x": 1200, "y": 1145},
        {"x": 1050, "y": 1220},
        {"x": 1350, "y": 1220},
        {"x": 1200, "y": 1295},
    ]

    df = pandas.read_csv(pos_file)
    positions = df[f'conf {int(disposition)}'].iloc[1:] # get right configuration
    directions = df[f'dir {int(disposition)}'].iloc[1:]

    for idx, plant_id in positions.items():
        direction = directions[idx]
        file = os.path.join(d, f"conf{direction}/{plant_id}-{direction}.mtg")
        g = MTG(file)
        scene.add(reconstruct_to_pos(g, pos_grid[idx-1], plant_id))

    return scene

def sensor_exp(idx=0):
    sen = sensors()[idx]
    sensor_scene = Scene()
    df = pandas.read_csv(sen)

    for i, row in df.iterrows():
        d = Shape(Disc(int(row["rayon_capteur"])))
        m = Material(Color3(150,0, 0))
        if "Orientation" in row.keys():
            if row["Orientation"] == "Sideward":
                m = Material(Color3(0,0, 150))
                orient = Vector3(1, 0, 0)
                d = Shape(AxisRotated(orient, radians(90), d.geometry))

        d = Shape(Translated(Vector3(int(row['X']), int(row['Y']), int(row['Z'])), d.geometry), m)
        d.name = f"sensor_{i}"
        sensor_scene.add(d)
    return sensor_scene
