def PlantPositions(txtfile):
    '''    
    '''
    # write the node code here.
    coords_file = open(txtfile, 'r')
    dico={}
    for line in coords_file:
        plt=line.split()[0]
        x,y,z=line.split()[1:]
        dico.setdefault(plt,[]).append([float(x),float(y),float(z)])
    plts=dico.keys()
    coords_file.close()

    return dico,plts
