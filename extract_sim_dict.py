#!/usr/bin/env python3
#-*- coding: utf-8 -*-

#une fonction pour lire un corpus 
from collections import defaultdict, Counter
import pickle
import math
import time
def readLemmeEtCategorie(m):
    '''
    Cette fonction renvoie une liste des lemmes avec leurs catégorie morpho-syntaxique
    Args:
        m:une fichier
    Returns:
        une liste des tuples
        par exemple :      
        (('Quatre', 'D'), 1, ('blessé', 'N'))
    '''

    l=[]
    with open(m,"r") as f:
        lines = f.readlines() #chaque line est un list de string, donc lines est un list de list de string
        for line in lines:
            newline = line.split()
            if len(newline)!=0:
                l.append((newline[2],newline[3]))#une list de tuple

    list_dict=[] #list_dict est une liste de [(('futur', 'A'), -1, ('de', 'P+D'))] (comme un model)

    for i in range(len(l)):
        list_dict.append((l[i-1],1,l[i]))
        list_dict.append((l[i],-1,l[i-1]))

    return list_dict



def dict_tout_mot(list_dict):
    '''
    Cette fonction crée une dictionnaire des mots existant dans une fichier
    we can find out :
    1, the frequence of each w
    2, the frequence of each context (r,w') coresspondant with this w 

    Args:
        m:un liste des tuples

    returns:
        une dictionnaire de dictionnaires de type: 4 grand Catégorie(N,V,Adj,V):{(w,cat): {((-1/+1,(w',cat)):freq...]}}
        par exemple:
        "N":('Saudrupt', 'N'): Counter({(1, ('planeur', 'N')): 1})

    '''

    dict_nom=defaultdict(Counter)
    dict_verbe=defaultdict(Counter)
    dict_adj=defaultdict(Counter)
    dict_adv=defaultdict(Counter)

    dict_all={}

    for i in list_dict:
        if i[2][1] in ['N','A','V','ADV']: #la condition pour avoir que les contextes N,A,ADJ,ADV
            if i[0][1]=='N':        
                dict_nom[i[0]][i[1:]]+=1

            if i[0][1]=='V':
                dict_verbe[i[0]][i[1:]]+=1

            if i[0][1]=='A':
                dict_adj[i[0]][i[1:]]+=1           

            if i[0][1]=='ADV':
                dict_adv[i[0]][i[1:]]+=1

    dict_all['N']=dict_nom
    dict_all['V']=dict_verbe
    dict_all['A']=dict_adj
    dict_all['ADV']=dict_adv

    return dict_all

def get_treshold_freq(dictt):
    '''
    Args:
        dictt:Dict tout mot

    Returns:
        une dict des catégories morphosyntaxique et la fréquence limite des contexte comme leurs valeurs
    '''

    somme=0 
    nbr_contx=0
    treshold_N=0
    treshold_A=0
    treshold_V=0
    treshold_ADV=0

    Dict_treshold={}

    for k,v in dictt.items():
        if k=='N': #la frequence totale de tous les contextes appertenant à cette categorie morpho-syntx
            for i,j in v.items():
                for m,n in j.items():
                    nbr_contx+=1
                    somme+=n
            treshold_N=somme//nbr_contx #on garde comme la fréquence d'élimination 10% de la fréquence moyenne
            somme=0 
            nbr_contx=0

        if k=='V':
            for i,j in v.items():
                for m,n in j.items():
                    nbr_contx+=1
                    somme+=n
            treshold_V=somme//nbr_contx
            somme=0 
            nbr_contx=0

        if k=='A':
            for i,j in v.items():
                for m,n in j.items():
                    nbr_contx+=1
                    somme+=n
            treshold_A=somme//nbr_contx
            somme=0 
            nbr_contx=0

        if k=='ADV':
            for i,j in v.items():
                for m,n in j.items():
                    nbr_contx+=1
                    somme+=n
            treshold_ADV=somme//nbr_contx
            somme=0 
            nbr_contx=0

    Dict_treshold['N']=treshold_N
    Dict_treshold['V']=treshold_V
    Dict_treshold['A']=treshold_A
    Dict_treshold['ADV']=treshold_ADV

    return Dict_treshold

def get_list_delete(dict_mot,dict_treshold):
    """
    Cette fonction crée une liste des contextes qui vont etre enlévé de dict_tout_mot et les écrit sur un fichier csv
    Puis il 
    """
    list_delete_N=[]
    list_delete_V=[]
    list_delete_A=[]
    list_delete_ADV=[]
    dict_all={}
    dict_nom={}
    dict_verbe={}
    dict_adj={}
    dict_adv={} #on va créer une version de notre dictionnaire sans les contextes qui sont moins que le treshold

    for k,v in dict_mot.items():
        if k=='N':
            for i,j in v.items():
                dict_nom[i]={}
                for m in j.keys():
                    if j[m]<=dict_treshold['N']:
                        list_delete_N.append((m,j[m])) #enregistre les elts qui vont etre supprimé
                    else:
                        dict_nom[i][m]=j[m] #on prends pas les elts moins de treshold dans la nouvelle dict
                if dict_nom[i]=={}: #si apres la nettoyage du contexte le clé n'a aucun valeur, on le supprime également
                    del dict_nom[i]

        if k=='V':
            for i,j in v.items():
                dict_verbe[i]={}
                for m in j.keys():
                    if j[m]<=dict_treshold['V']:
                        list_delete_V.append((m,j[m]))
                    else:
                        dict_verbe[i][m]=j[m]
                if dict_verbe[i]=={}:
                    del dict_verbe[i]
        if k=='A':
            for i,j in v.items():
                dict_adj[i]={}
                for m in j.keys():
                    if j[m]<=dict_treshold['A']:
                        list_delete_A.append((m,j[m]))
                    else:
                        dict_adj[i][m]=j[m]
                if dict_adj[i]=={}:
                    del dict_adj[i]

        if k=='ADV':
            for i,j in v.items():
                dict_adv[i]={}
                for m in j.keys():
                    if j[m]<=dict_treshold['ADV']:
                        list_delete_ADV.append((m,j[m]))
                    else:
                        dict_adv[i][m]=j[m]
                if dict_adv[i]=={}:
                    del dict_adv[i]
    dict_all['N']=dict_nom
    dict_all['V']=dict_verbe
    dict_all['A']=dict_adj
    dict_all['ADV']=dict_adv


    filename='deleted_contx_cz.csv'
    with open(filename,'w') as f: #on enregistre les contextes qu'on va supprimer pour garder la trace
        for i in list(set(list_delete_N)):
                f.write("NOMS")
                f.write('\t')
                f.write(str(i))
                f.write('\n')
        for i in list(set(list_delete_V)):
                f.write("VERBES")
                f.write('\t')
                f.write(str(i))
                f.write('\n')
        for i in list(set(list_delete_A)):
                f.write("ADJECTIVES")
                f.write('\t')
                f.write(str(i))
                f.write('\n')
        for i in list(set(list_delete_ADV)):
                f.write("ADVERBES")
                f.write('\t')
                f.write(str(i))
                f.write('\n')

    f.close()

    return dict_all

def frequency_w(dictt,word):

    freq=0
    for k,v in dictt.items():
        if word in v.keys():
            for i,j in v[word].items():
                freq+=j
    return freq

def frequency_context(dictt):

    frequency_contx=Counter()
    for k,v in dictt.items():
        for i,j in v.items():
            for m,n in j.items():

                frequency_contx[m]+=n
    return frequency_contx


def cosine(l1,l2):
    return sum([i*j for i,j in zip(l1,l2)])/(math.sqrt(sum([i*i for i in l1]))* math.sqrt(sum([i*i for i in l2])))



def calcul_similarite(dictt,returnfile):
    """
    Cette fonction permet de faire un calcul de similarité entres les w qui se trouve dans une dictionnaire

    """

    sim_matrice={'N':{},'V':{},'A':{},'ADV':{}}
    List_common_w1=[]
    List_common_w2=[]
    dict_context=frequency_context(dictt)
    pm1=0
    pm2=0
    rel_freq1=0
    rel_freq2=0 
    for k,v in dictt.items():
        if k=="N":
            for w1,j in v.items():
                for w2,n in v.items():
                    if w1!=w2:
                        for i,s in j.items():
                            for l,m in n.items():
                                if i==l: #si les contextes sont communes
                                    pmi1=math.log(s/(frequency_w(dictt,w1)*dict_context.get(i)))
                                    pmi2=math.log(m/(frequency_w(dictt,w2)*dict_context.get(l)))
                                    #rel_freq1=s/frequency_w(dictt,w1)
                                    #rel_freq2=m/frequency_w(dictt,w2)
                                    List_common_w1.append(pmi1)
                                    List_common_w2.append(pmi2)
                
                    if len(List_common_w1)or len(List_common_w2)!=0:
                        try:
                            sim_matrice['N'][w1[0]].append((w2[0],cosine(List_common_w1,List_common_w2)))

                        except KeyError:
                            sim_matrice['N'][w1[0]]=[(w2[0],cosine(List_common_w1,List_common_w2))]
                    List_common_w1=[]
                    List_common_w2=[]

        if k=="V":
            for w1,j in v.items():
                for w2,n in v.items():
                    if w1!=w2:
                        for i,s in j.items():
                            for l,m in n.items():
                                if i==l:
                                    pmi1=math.log(s/(frequency_w(dictt,w1)*dict_context.get(i)))
                                    pmi2=math.log(m/(frequency_w(dictt,w2)*dict_context.get(l)))

                                    List_common_w1.append(pmi1)
                                    List_common_w2.append(pmi2)
                    if len(List_common_w1)or len(List_common_w2)!=0:
                        try:
                            sim_matrice['V'][w1[0]].append((w2[0],cosine(List_common_w1,List_common_w2)))

                        except KeyError:
                            sim_matrice['V'][w1[0]]=[(w2[0],cosine(List_common_w1,List_common_w2))]
                    List_common_w1=[]
                    List_common_w2=[]
        if k=="A":
            for w1,j in v.items():
                for w2,n in v.items():
                    if w1!=w2:
                        for i,s in j.items():
                            for l,m in n.items():
                                if i==l:
                                    pmi1=math.log(s/(frequency_w(dictt,w1)*dict_context.get(i)))
                                    pmi2=math.log(m/(frequency_w(dictt,w2)*dict_context.get(l)))
                                    List_common_w1.append(pmi1)
                                    List_common_w2.append(pmi2)
                    if len(List_common_w1)or len(List_common_w2)!=0:
                        try:
                            sim_matrice['A'][w1[0]].append((w2[0],cosine(List_common_w1,List_common_w2)))
                        except KeyError:
                            sim_matrice['A'][w1[0]]=[(w2[0],cosine(List_common_w1,List_common_w2))]
                    List_common_w1=[]
                    List_common_w2=[]
        if k=="ADV":
            for w1,j in v.items():
                for w2,n in v.items():
                    if w1!=w2:
                        for i,s in j.items():
                            for l,m in n.items():
                                if i==l:
                                    pmi1=math.log(s/(frequency_w(dictt,w1)*dict_context.get(i)))
                                    pmi2=math.log(m/(frequency_w(dictt,w2)*dict_context.get(l)))
                                    #rel_freq1=s/frequency_w(dictt,w1)
                                    #rel_freq2=m/frequency_w(dictt,w2)
                                    List_common_w1.append(pmi1)
                                    List_common_w2.append(pmi2)
                    if len(List_common_w1)or len(List_common_w2)!=0:
                        try:
                            sim_matrice['ADV'][w1[0]].append((w2[0],cosine(List_common_w1,List_common_w2)))

                        except KeyError:
                            sim_matrice['ADV'][w1[0]]=[(w2[0],cosine(List_common_w1,List_common_w2))]
                    List_common_w1=[]
                    List_common_w2=[]
    pickle_out = open(returnfile,'wb')
    pickle.dump(sim_matrice, pickle_out)
    pickle_out.close()
    print(sim_matrice)
#TESTS              

m = "EP.tcs.melt.utf8.split-cz.outmalt"


dictt=dict_tout_mot(readLemmeEtCategorie(m))
cleaned_dict=get_list_delete(dictt,get_treshold_freq(dictt))
debut = time.time()
calcul_similarite(cleaned_dict,'cz_similarity_dict.pickle')
fin = time.time()
print(fin - debut)



