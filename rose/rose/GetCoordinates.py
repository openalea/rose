def GetCoordinates(plant, crop_coord):
    '''
    Return the coordinates of the plant selected
    '''
    plant_coord = None; 
    # write the node code here.
    # read the file and create a dictionnary
    coords_file = open(crop_coord, 'r')
    coords_dict={}
    for line in coords_file:
        plt=line.split()[0]
        x,y,z=line.split()[1:]
        coords_dict.setdefault(plt,[]).append((float(x),float(y),float(z)))
        
    plant_coord=coords_dict[plant]
    
    # return outputs
    return plant_coord
