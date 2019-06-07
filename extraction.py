#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#une fonction pour lire un corpus 
from spacy.vectors import Vectors
from collections import OrderedDict
import pandas as pd
def readLemmeEtCategorie(m):
	"""
	Cette fonction renvoie une liste des lemmes avec leurs catégorie morpho-syntaxique
	Args:
		m:une fichier
	Returns:
		une lite des tuples
	"""
	l=[]
	with open(m,"r") as f:
		lines = f.readlines() #chaque line est un list de string, donc lines est un list de list de string
		for line in lines:
			newline = line.split()
			if len(newline)!=0:
				l.append((newline[2],newline[3]))#une list de tuple
	return l #list de tuple
			
def dict_tout_mot(m):
	"""
	Cette fonction crée une dictionnaire des mots existant dans une fichier
	Args:
		m:un fichier
	returns:
		une dictionnaire
	"""
	l=readLemmeEtCategorie(m)
	list_dict=[]
	for i in range(len(l)):
		list_dict.append((l[i-1],1,l[i]))
		list_dict.append((l[i],-1,l[i-1]))
	#list_dict est une liste de [(('futur', 'A'), -1, ('de', 'P+D'))] (comme un model)

	dict_nom={}
	dict_verbe={}
	dict_adj={}
	dict_adv={}

	dict_all={}

	dict_all["N"]=dict_nom
	dict_all["V"]=dict_verbe
	dict_all["ADJ"]=dict_adj
	dict_all["ADV"]=dict_adv

	dict_nom_f={}
	for i in list_dict:
		if i[0][1]=="N":
			dict_nom_f[i]=dict_nom_f.get(i,0)+1

	for i in list_dict:
		if i[0][1]=="N":
			if i[0] in dict_nom:
				dict_nom[i[0]].append((i[1:],":",dict_nom_f[i]))
			else:
				dict_nom[i[0]]=[]
	#pour dict_nom, c'est un dictionnaire de dictionnaire

	dict_verbe_f={}
	for i in list_dict:
		if i[0][1]=="V":
			dict_verbe_f[i]=dict_verbe_f.get(i,0)+1

	for i in list_dict:
		if i[0][1]=="V":
			if i[0] in dict_verbe:
				dict_verbe[i[0]].append((i[1:],":",dict_verbe_f[i]))
			else:
				dict_verbe[i[0]]=[]


	dict_adj_f={}
	for i in list_dict:
		if i[0][1]=="ADJ":
			dict_adj_f[i]=dict_adj_f.get(i,0)+1

	for i in list_dict:
		if i[0][1]=="ADJ":
			if i[0] in dict_adj:
				dict_adj[i[0]].append((i[1:],":",dict_adj_f[i]))
			else:
				dict_adj[i[0]]=[]
	
	dict_adv_f={}
	for i in list_dict:
		if i[0][1]=="ADV":
			dict_adv_f[i]=dict_adv_f.get(i,0)+1

	for i in list_dict:
		if i[0][1]=="ADV":
			if i[0] in dict_adv:
				dict_adv[i[0]].append((i[1:],":",dict_adv_f[i]))
			else:
				dict_adv[i[0]]=[]
	
	print(dict_all)






def get_all_contexts(dictt):
	"""
	Renvoie une liste des contextes où il y a des contextes uniques et leur frequence 
	"""
	dict_contx=OrderedDict()
	for k,v in dictt.items():
		dict_contx[k[1:3]]=dict_contx.get(k[1:3],0)+1
	
	list_contx=[]
	for i,j in dict_contx.items():
		list_contx.append((i,j))
	return list_contx



def get_all_keys(dictt):
	"""
	Renvoie une liste de tuples où il y a les clés uniques et leur frequence
	"""
	dict_key=OrderedDict()
	for k,v in dictt.items():
		dict_key[k[0]]=dict_key.get(k[0],0)+1

	
	list_key=[]
	for i,j in dict_key.items():			
		list_key.append((i,j))
	return list_key

def get_treshold_freq(l):
	"""
	Renvoie la limite de fréquence pour éliminer les elts qui sont plus petits en prenant la moyenne
	"""
	summ=0
	nbr=0
	for t1,t2 in l:
		summ+=t2
		nbr+=1

	return summ//nbr

def get_list_delete(l):
	"""
	Cette fonction crée une liste des contextes ou w qui vont etre enlévé de dict_tout_mot
	"""
	treshold=get_treshold_freq(l)
	list_delete=[]
	for i,j in l:
		if j<treshold:
			list_delete.append((i,j))
	return list_delete

def get_cat_dict(cat, dictt):
	"""
	Cette fonction renvoie une dictionnaire quicontient comme clés des w d'une certain categorie
	morpho-syntx et comme valeur la liste de contexte qui apparaisse avec cette mot
	"""

	dict_cat=OrderedDict()

	for k,v in dictt.items():
		if k[0][1] == cat:
			if k[0] in dict_cat:
				dict_cat[k[0]].append((k[1:3],v))
			else:
				dict_cat[k[0]]=[]
	
	return dict_cat

def create_coocurency_vecs(dict_mot, keys, contextes):
	"""
	Cette fonction renvoie une espace vectorielle qui contient les w comme keys 
	Version tres lente !!! ça marche pas très bien pour le moment
	"""
	word_vectors=Vectors(shape=(len(keys),len(contextes)))
	#on cree un vecteur dans le dimentions des clés et contextes uniques
	list_freq=[]
	for key in keys:
		for k,v in dict_mot.items():
			if k[0]==key:
				list_freq.append(v)
			else:
				list_freq.append(0)
		print(key)
		print(list_freq)
		word_vectors.add(key,row=list_freq)
	



#TESTS
m = "estrepublicain.extrait-aa.19998.outmalt"
d=dict_tout_mot(m)
print(d)
#keys=get_all_keys(d)
#contx=get_all_contexts(d)
#create_coocurency_vecs(d,keys,contx)
#print(readLemmeEtCategorie(m))



