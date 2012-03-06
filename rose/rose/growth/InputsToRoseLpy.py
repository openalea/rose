import csv

def InputsToRoseLpy(inputsperphyto, inputsperplant, cType, plantnum):
    '''  Convert the growRose input tables into a dictionnary  
    '''
    inputsdict = {}
   
    # write the node code here.

    
    #inputsperplant=csv.reader(open("D:/SurSamba/ModelKO/dataSabine/Inputs/inputsperplant.csv",'r'),delimiter=',')
    #inputsperplant=csv.reader(open("D:/SurSamba/ModelKO/dataSabine/Inputs/inputsperplant2plt.csv",'r'),delimiter=',')
    inputsperplant=csv.reader(open(inputsperplant,'r'),delimiter=',') 
    #inputsperplant=csv.DictReader(open("D:/SurSamba/ModelKO/dataSabine/Inputs/inputsperplant.csv",'r'),delimiter=',')  
    #inputsperphyto=csv.reader(open("D:/SurSamba/ModelKO/dataSabine/Inputs/inputsperphyto2plt.csv",'r'),delimiter=',')
    inputsperphyto=csv.reader(open(inputsperphyto,'r'),delimiter=',')

    inputsperplant.next()
    for row in inputsperplant:
        #print int(row[0].split(';')[0])
        #plt.append(int(row[0].split(';')[0]))
        #nphy.append(int(row[0].split(';')[1]))
        if plantnum==None:
            inputsdict.setdefault('plt',[]).append(int(row[0].split(';')[0]))
            inputsdict.setdefault('nphy',[]).append(int(row[0].split(';')[1]))
            inputsdict.setdefault('ddEM',[]).append(float(row[0].split(';')[2]))
        else:
            if int(row[0].split(';')[0])==plantnum:
                inputsdict.setdefault('plt',[]).append(int(row[0].split(';')[0]))
                inputsdict.setdefault('nphy',[]).append(int(row[0].split(';')[1]))
                inputsdict.setdefault('ddEM',[]).append(float(row[0].split(';')[2]))
    
    
    phyto={}
    apf={}
    lmaxen={}
    lmaxfola={}
    inputsperphyto.next()
    for line in inputsperphyto:
        p=int(line[0].split(';')[0])
        if plantnum==None:
            #print p
            # pour que cela fonctionne, j'ai mis des 0 pour lfola pour les feuilles inexistantes (feuille virtuelle du dernier entre-neoud ou stipule)
            phyto.setdefault(p,[]).append(int(line[0].split(';')[1]))
            apf.setdefault(p,[]).append(float(line[0].split(';')[5]))
            lmaxen.setdefault(p,[]).append(float(line[0].split(';')[3]))
            lmaxfola.setdefault(p,[]).append(float(line[0].split(';')[4]))
        else:
            if p==plantnum:
                #inputsdict.setdefault('Phyto',[]).append(int(line[0].split(';')[1]))
                #inputsdict.setdefault('ApF',[]).append(float(line[0].split(';')[5]))
                #inputsdict.setdefault('LmaxEN',[]).append(float(line[0].split(';')[3]))
                #inputsdict.setdefault('LmaxfolA',[]).append(float(line[0].split(';')[4]))
                phyto.setdefault(p,[]).append(int(line[0].split(';')[1]))
                apf.setdefault(p,[]).append(float(line[0].split(';')[5]))
                lmaxen.setdefault(p,[]).append(float(line[0].split(';')[3]))
                lmaxfola.setdefault(p,[]).append(float(line[0].split(';')[4]))

    for p in inputsdict['plt']:
        #print tuple(apf[p])
        # prendre le nombre de phytos max dans fichier ech plante et verifier si on a le bon compte !
        inputsdict.setdefault('Phyto',[]).append(tuple(phyto[p]))
        inputsdict.setdefault('ApF',[]).append(tuple(apf[p]))
        inputsdict.setdefault('LmaxEN',[]).append(tuple(lmaxen[p]))
        inputsdict.setdefault('LmaxfolA',[]).append(tuple(lmaxfola[p]))

    inputsdict['cUnit']=cType
    
    if plantnum==None:
        inputsdict['nplants']=len(inputsdict['plt'])
    else:
        inputsdict['nplants']=1
    
    # return outputs
    return inputsdict,
