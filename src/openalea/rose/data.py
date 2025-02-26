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
    
def geom_dir():
    p = data()
    geom_dir = next(p.glob('GEOM'))
    return geom_dir

def sensors_dir():
    p = data()
    sensor_dir = next(p.glob('SENSORS'))
    return sensor_dir

def sensors():
    sensor_dir = sensors_dir()
    env_dir = [p for p in sensor_dir.glob('*') if p.is_file()]
    return [str(sensor_dir / p.name) for p in env_dir]

def environments():
    geom_d = geom_dir()
    env_dir = [p for p in geom_d.glob('*') if p.is_file()]
    return [str(geom_d / p.name) for p in env_dir]

def manip_dir():
    mtg_d = mtg_dir()
    return [p for p in mtg_d.glob('*') if p.is_dir()]

def manips():
    return [p.name for p in manip_dir()]

def experiments(manip):
    return list((mtg_dir()/manip).glob('*'))
