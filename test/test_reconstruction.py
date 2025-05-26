from openalea.rose import data
from openalea.plantgl.all import Scene

from openalea.rose.mockup import rose
from openalea.rose.mockup.rose_geometry import (
    vertexVisitor, reconstructWithTurtle,
    computeLeafletFrom4pts,
    bezierPatchFlower, petalMatrix,
    computeKnop4pts, drawStipule3pts
)

def get_one_expe():
    manips_dir = data.manip_dir()
    m_dir = (manips_dir[0])
    m_name = m_dir.name
    print(f'{m_name} : {m_dir}')
    expes = data.experiments(m_dir)
    exp = expes[0]
    return exp

def get_one_set_expe():
    manips_dir = data.manip_dir()
    m_dir = (manips_dir[0])
    m_name = m_dir.name
    print(f'{m_name} : {m_dir}')
    expes = data.experiments(m_dir)
    return expes

def get_all_expe():
    names = data.manips()

    exps = []
    for name in names:
        exps.extend(data.experiments(name))
    return exps

def grid(dir):
    assert((dir/'grid.txt').is_file())
    return dir/'grid.txt'

def origin(dir):
    assert((dir/'origin.txt').is_file())
    return dir/'origin.txt'

def test_one():
    dir = get_one_expe()
    return myMTG(dir)

def myMTG(dir):
    grid_fn = grid(dir)
    origin_fn = origin(dir)

    dictofindices, gridSpecs = rose.getGrid(grid_fn)
    #print(f'Grid : {dictofindices}, {gridSpecs}')
    _origin = rose.getOrigin(origin_fn)
    #print(f'Origins : {_origin}')

    plantlist = dictofindices
    existingmtglist, = rose.localDir2DictOfFiles([str(fn) for fn in dir.glob('*.mtg')])
    excludelist=[] 
    gridDef = gridSpecs
    _origin=_origin
    DoFill=True 
    DoRotate=True
   
    dictOfPositions, _ = rose.cropGeneration_2011(
        plantlist=plantlist,
        existingmtglist=existingmtglist,
        excludelist=excludelist,
        gridDef=gridDef,
        origin=_origin,
        DoFill=DoFill,
        DoRotate=DoRotate)
    
    listofmtgs, = rose.files2MTGs(dictOfPositions)

    mtg_union, = rose.mTG_union(listofmtgs)

    return mtg_union


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

def run_all():
    expes = get_all_expe()
    gs = [myMTG(d) for d in expes]
    scenes = [reconstruct(g) for g in gs]
    return scenes

def bug1():
    expes = get_all_expe()
    d = expes[10]
    g=myMTG(d)
    scene = reconstruct(g)
    return scene

def environment(idx=0):
    expes = get_all_expe()
    d = expes[idx]
    g=myMTG(d)
    scene = reconstruct(g)
    chamber = Scene(str(data.phytotron()))
    scene.add(chamber)
    return scene

def save_gltf(scene, filename):
    from openalea.scenemanagement.convert import GLTFScene
    gltf = GLTFScene(scene)
    gltf.run()
    gltf.to_gltf(filename)

def save_environment():
    env = Scene(data.environments()[0])
    scene = Scene(env)
    save_gltf(scene, "chamber.glb")

def save_expe(index):
    expes = get_all_expe()
    d = expes[index]
    g=myMTG(d)
    scene = reconstruct(g)
    save_gltf(scene, f"rose_{index}.glb")
