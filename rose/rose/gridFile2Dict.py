def gridFile2Dict(gridfilename):
    '''    Makse a dictionnary from file that contains plants indexes inside a 2D grid.
    '''
    dictofindices = None; 
    # write the node code here.
    # Create a dictionnary whose keys are plants ID and values are lists of plant positions
    # From J. Berhteloot's CropGeneration
    coords_file = open(gridfilename, 'r')
    dictofindices={}
    for line in coords_file:
        plt=line.split()[0]
        x,y=line.split()[1:]
        dictofindices.setdefault(plt,[]).append([int(x),int(y)])
    coords_file.close()

    # return outputs
    return dictofindices,
