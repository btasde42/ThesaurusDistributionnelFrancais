#!/usr/bin/env python3
#-*- coding: utf-8 -*-

#une fonction pour lire un corpus 
from collections import defaultdict, Counter
import pandas as pd
from itertools import dropwhile
import math

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
    Cette fonction crée une liste des contextes ou w qui vont etre enlévé de dict_tout_mot
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


    filename='deleted_contx.csv'
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

'''
now we still have to do: 
1, a new dictionnary after deleting the very low frequency words
2, find out all the 3 parts of the frenquences
'''
"""
    def newlist_tout_mot(dict_tout):
        '''
        here we have to delete all the words that we think are not useful
        we can use the lists inf the function get_list_delete :
        1, we create an original liste ( actually we have already one: readlemme
        2, then we delete the words in the original list who occurs also in the delete list.

        so we can get the 3 types of the frenquences: f(w), f(r,w'), f(w,r,w')

        retuern:

        so in the end, it will still show like a list:
        still like readlemme
        ''' 

'''        
    def get_all_keys(dictt):
        '''
        Renvoie une liste de tuples où il y a les clés uniques et leur frequence
        '''
        dict_key=OrderedDict()

        for k,v in dictt.items():
            dict_key[k[0]]=dict_key.get(k[0],0)+1

        list_key=[]

        for i,j in dict_key.items():            
            list_key.append((i,j))

        return list_key
'''
"""

'''
then we have to caqlculate the PMI and Cosine

to calculate the PMI, first we should knwo 2 parts : 
pmi(x,y)=log(f(x,y)/(f(x)*f(y))) f(x,y)=f(w,(r,w')) f(x)=f(w) f(y)=f(r,w')
and here, we can say

'''
def frequency_w(l):
    '''
    here to calculate the frequency of each words, we still have to creat a dictionnary
    
    Arge:
        l=newlist_tout_mot(dict_tout) a liste of the words that we keep after deleting all the words that we don't need,

    Returns:
        a dictionnary, keys are the words, values are the frenquency
        for example :
        (('Quatre', 'D'):2))
    '''
    frequency={}

    frequency_N={}
    frequency_V={}
    frequency_A={}
    frequency_ADV={}

    frequency["N"]=frequency_N
    frequency["V"]=frequency_V
    frequency["A"]=frequency_A
    frequency["ADV"]=frequency_ADV

    for i in l:
        if i[0][1]=="N":
            frequency_N[i[0]]=frequency_N.get(i[0],0)+1

        if i[0][1]=="V":
            frequency_V[i[0]]=frequency_N.get(i[0],0)+1

        if i[0][1]=="A":
            frequency_A[i[0]]=frequency_A.get(i[0],0)+1

        if i[0][1]=="ADV":
            frequency_ADV[i[0]]=frequency_ADV.get(i[0],0)+1

    return frequency

def frequency_context(l):
    '''
    we have to calculate the frequence of the context as well
    contxet : (r,w')

    Arge:
        l, l=newlist_tout_mot(dict_tout) a liste of the words that we keep after deleting all the words that we don't need,

    Returns:
        a dictionnary, keys are the contexts, values are the frenquency
        for example :
        ((1,('Quatre', 'D')):2))
    '''
    frequency={}

    frequency_N={}
    frequency_V={}
    frequency_A={}
    frequency_ADV={}

    frequency["N"]=frequency_N
    frequency["V"]=frequency_V
    frequency["A"]=frequency_A
    frequency["ADV"]=frequency_ADV

    for i in l:
        if i[2][1]=="N":
            frequency_N[i[1:]]=frequency_N.get(i[1:],0)+1

        if i[2][1]=="V":
            frequency_V[i[1:]]=frequency_V.get(i[1:],0)+1

        if i[2][1]=="A":
            frequency_A[i[1:]]=frequency_A.get(i[1:],0)+1

        if i[2][1]=="ADV":
            frequency_ADV[i[1:]]=frequency_ADV.get(i[1:],0)+1

    return frequency

def frequency_w_et_context(l):
    '''
    here we have to calculate the repitation of the whole w, (r,w')

    '''
    frequency={}

    for i in l:
        frequency[i]=frequency.get(i,0)+1

    return frequency


def pmi(l):
    
    allpmi={}

    allpmi_N={}
    allpmi_V={}
    allpmi_A={}
    allpmi_ADV={}

    allpmi["N"]=allpmi_N
    allpmi["V"]=allpmi_V
    allpmi["A"]=allpmi_A
    allpmi["ADV"]=allpmi_ADV

    f1=frequency_w_et_context(l) #here f1 is actually a dictionnary
    f2=frequency_w(l)
    f3=frequency_context(l)


    for k in f1:
        if (k[0][1]=="N") and (k[0]in f2["N"]) and (k[1:]in f3["N"])  :
            allpmi_N[k[0][0]]=math.log(f1[k]/(f2["N"][k[0]]*f3["N"][k[1:]]))

        if (k[0][1]=="V") and (k[0]in f2["V"]) and (k[1:]in f3["V"]):
            allpmi_V[k[0][0]]=math.log(f1[k]/(f2["V"][k[0]]*f3["V"][k[1:]]))

        if (k[0][1]=="A") and (k[0]in f2["A"]) and (k[1:]in f3["A"]):
            allpmi_A[k[0][0]]=math.log(f1[k]/(f2["A"][k[0]]*f3["A"][k[1:]]))
        
        if (k[0][1]=="ADV") and (k[0]in f2["ADV"]) and (k[1:]in f3["ADV"]):
            allpmi_ADV[k[0][0]]=math.log(f1[k]/(f2["ADV"][k[0]]*f3["ADV"][k[1:]]))

    return allpmi






#TESTS

m = "estrepublicain.extrait-aa.19998.outmalt"

l=(readLemmeEtCategorie(m))
#dictt=dict_tout_mot(readLemmeEtCategorie(m))
#get_list_delete(dictt,get_treshold_freq(dictt))
#print(frequency_w(l))
#print(frequency_context(l))
#print(frequency_w_et_context(l))
print(pmi(l))

