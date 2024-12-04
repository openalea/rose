from openalea.deploy.shared_data import shared_data
import openalea.rose

def data():
    rose_dir = shared_data(openalea.rose)
    if rose_dir is None:
        rose_dir = shared_data(openalea.rose, share_path='../../../share')

    return rose_dir

def mtg_dir():
    p = data()

    mtg_dir = next(p.glob('MTG'))
    return mtg_dir

def manip_dir():
    mtg_d = mtg_dir()
    return [p for p in mtg_d.glob('*') if p.is_dir()]

def manips():
    return [p.name for p in manip_dir()]

def experiments(manip):
    return list((mtg_dir()/manip).glob('*'))


