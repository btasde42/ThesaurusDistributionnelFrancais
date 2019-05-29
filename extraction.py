#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#une fonction pour lire un corpus 
from collections import OrderedDict
def readLemmeEtCategorie(m):
	l=[]
	with open(m,"r") as f:
		lines = f.readlines() #chaque line est un list de string, donc lines est un list de list de string
		for line in lines:
			newline = line.split()
			if len(newline)!=0:
				if (newline[3] == "ADV") or (newline[3]== "N") or (newline[3] == "V") or (newline[3]== "A"):
					l.append((newline[2],newline[3]))#une list de tuple
	return l #list de tuple
			
def dict_tout_mot(m):
	l=readLemmeEtCategorie(m)
	list_dict=[]
	for i in range(len(l)):
		list_dict.append((l[i-1],1,l[i]))
		list_dict.append((l[i],-1,l[i-1]))
	dict_tout=OrderedDict()
	for k in list_dict:
		dict_tout[k]=dict_tout.get(k,0)+1
	return dict_tout
'''
def contexreV(m):
	l=readLemmeEtCategorie(m)
	l = sorted(l, key = lambda categorie : categorie[1])#list de tuple
	listV=[]
	for i in range(len(l)):
		if l[i][1]=="V":
			listV.append(l[i][0])
	listcontxteV=[]
	for i in range(1,len(listV)):
		listcontxteV.append((listV[i-1],1,listV[i]))
		listcontxteV.append((listV[i],-1,listV[i-1]))
	verb={}
	for k in listcontxteV:
		verb[k]=verb.get(k,0)+1
	return verb
'''

#def vector(m):
#	list_de_vector=[]
#	length_dict=


def frenq_context(m):
	#donc ici nom est en fait une dictionnaire, chaque key est une tuple(w,r,w'), chaque key est une frequence
	#ici, on doit trouver une tuple, et sa frequence== kye, apres on doit trouver les autres tuples qui contien le meme w,
	frequenceDeMemeContext=OrderedDict()
	for n in dict_tout_mot(m):#n ici est une tuple((w,cat),r,(w',cat))	
		frequenceDeMemeContext[n[1:3]]=frequenceDeMemeContext.get(n[1:3],0)+1
	return frequenceDeMemeContext

		

#def weight(m):


	
m = "estrepublicain.extrait-aa.19998.outmalt"
#print(readLemmeEtCategorie(m))
print(dict_tout_mot(m))
#print(frenq_context(m))

