import os
import random

def CropGeneration(txtfile, Plt_Not_Use, filling=True, crop_width=90.0, crop_length=200.0, spacing=15.0):
    '''    
    '''
    # Create a dictionnary whose keys are plants ID and values are lists of plant positions
    coords_file = open(txtfile, 'r')
    dico={}
    for line in coords_file:
        plt=line.split()[0]
        x,y,z=line.split()[1:]
        dico.setdefault(plt,[]).append([float(x),float(y),float(z)])
    coords_file.close()

    # initialization of the output plants
    plants=[]

    # Create a copy of the first dictionnary in the right form
    dico_copy={}
    for k in dico:
        dico_copy[k]=dico[k][0]

    # If we want to fill the crop digitized with plants chosen randomly,
    if filling ==True:
        # creation of a list of plant positions in the complete crop
        pos_list=[]
        nplts_x=int(crop_length/spacing)
        nplts_y=int(crop_width/spacing)
        z=0.
        for px in range(1,nplts_x+1):
            x=px*spacing
            for py in range(1,nplts_y+1):
                y=py*spacing-spacing/2
                pos_list.append([x,y,z])
        # identification of the missing plants, attribution of a plant ID, and dictionnary filling with the random plants
        keys = list(dico_copy)
        keys.remove(Plt_Not_Use)

        points = set(dico_copy.values())
        for p in pos_list:
            if p not in points:
                pltID = random.sample(keys,1)
                pltID = ''.join(pltID)
                dico[pltID].append(p)
        
    IDplants=[]
    for key in dico:
        for i in range(len(dico[key])):
            ID=key+'-'+str(i+1)
            IDplants.append(ID)

    return dico,IDplants

