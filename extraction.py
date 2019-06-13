#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#une fonction pour lire un corpus 

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
		une dictionnaire de dictionnaires de type: 4 grand Catégorie(N,V,Adj,V):{(w,cat): [((-1/+1,(w',cat)),freq)...]}}
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


	dict_verbe_f={}
	dict_nom_f={}
	dict_adj_f={}
	dict_adv_f={}

	for i in list_dict:
		if i[2][1] in ['N','A','V','ADV']:
			if i[0][1]=='N':	
				dict_nom_f[i]=dict_nom_f.get(i,0)+1
				if i[0] not in dict_nom:
					dict_nom[i[0]]=[(i[1:],1)]
					
				else:
					dict_nom[i[0]].append((i[1:],dict_nom_f[i]))



			if i[0][1]=='V':
				dict_verbe_f[i]=dict_verbe_f.get(i,0)+1
				if i[0] not in dict_verbe:
					dict_verbe[i[0]]=[(i[1:],1)]
				else:
					dict_verbe[i[0]].append((i[1:],dict_verbe_f[i]))
		


			if i[0][1]=='A':
				dict_adj_f[i]=dict_adj_f.get(i,0)+1
				if i[0] not in dict_adj:
					dict_adj[i[0]]=[(i[1:],1)]
				else:
					dict_adj[i[0]].append((i[1:],dict_adj_f[i]))

					
			if i[0][1]=='ADV':
				dict_adv_f[i]=dict_adv_f.get(i,0)+1
				if i[0] not in dict_adv:
					dict_adv[i[0]]=[(i[1:],1)]
				else:
					dict_adv[i[0]].append((i[1:],dict_adv_f[i]))

	dict_all['N']=dict_nom
	dict_all['V']=dict_verbe
	dict_all['A']=dict_adj
	dict_all['ADV']=dict_adv
	return dict_all




def get_treshold_freq(dictt):
	"""
	Args:
		dictt:Dict tout mot
	Returns:
		une dict des catégories morphosyntaxique et la fréquence limite des contexte comme leurs valeurs
	"""
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
				for l in j:
					nbr_contx+=1
					somme+=l[1]
			treshold_N=(((somme//nbr_contx)*10)//100) #on garde comme la fréquence d'élimination 10% de la fréquence moyenne
			somme=0 
			nbr_contx=0
		if k=='V':
			for i,j in v.items():
				for l in j:
					nbr_contx+=1
					somme+=l[1]
			treshold_V=(((somme//nbr_contx)*10)//100) 
			somme=0 
			nbr_contx=0
		if k=='A':
			for i,j in v.items():
				for l in j:
					nbr_contx+=1
					somme+=l[1]
			treshold_A=(((somme//nbr_contx)*10)//100) 
			somme=0 
			nbr_contx=0
		if k=='ADV':
			for i,j in v.items():
				for l in j:
					nbr_contx+=1
					somme+=l[1]
			treshold_ADV=(((somme//nbr_contx)*10)//100) 
	Dict_treshold['N']=treshold_N
	Dict_treshold['V']=treshold_V
	Dict_treshold['A']=treshold_A
	Dict_treshold['ADV']=treshold_ADV
	return Dict_treshold
	


"""def get_all_keys(dictt):
	
	#Renvoie une liste de tuples où il y a les clés uniques et leur frequence
	
	dict_key=OrderedDict()
	for k,v in dictt.items():
		dict_key[k[0]]=dict_key.get(k[0],0)+1

	
	list_key=[]
	for i,j in dict_key.items():			
		list_key.append((i,j))
	return list_key

"""
def get_list_delete(dict_mot,dict_treshold):
	"""
	Cette fonction crée une liste des contextes ou w qui vont etre enlévé de dict_tout_mot
	"""

	list_delete_N=[]
	list_delete_V=[]
	list_delete_A=[]
	list_delete_ADV=[]

	dict_all={} #on va créer une version de notre dictionnaire sans les contextes qui sont moins que le treshold
				#et sans les clés vidées après l'élimintion
	dict_nom={}
	dict_v={}
	dict_adj={}
	dict_adv={}

	dict_all={}
	for k,v in dict_mot.items():
		if k=='N':
			for i,j in v.items():
				for l in j:
					if l[1]<dict_treshold['N']:
						list_delete_N.append(l)
						j.remove(l)
			if len(j)>0:
				dict_nom[i]=j

		if k=='V':
			for i,j in v.items():
				for l in j:
					if l[1]<dict_treshold['V']:
						list_delete_V.append(l)
						j.remove(l)
			if len(j)>0:
				dict_v[i]=j

		if k=='A':
			for i,j in v.items():
				for l in j:
					if l[1]<dict_treshold['A']:
						list_delete_A.append(l)
						j.remove(l)
			if len(j)>0:
				dict_adj[i]=j

		if k=='ADV':
			for i,j in v.items():
				for l in j:
					if l[1]<dict_treshold['ADV']:
						list_delete_ADV.append(l)
						j.remove(l)
			if len(j)>0:
				dict_adv[i]=j

	dict_all['N']=dict_nom
	dict_all['V']=dict_v
	dict_all['A']=dict_adj
	dict_all['ADV']=dict_adv

	filename='deleted_contx.csv'
	with open(filename,'w') as f: #on enregistre les contextes qu'on va supprimer pour garder la trace
		for i in list(set(list_delete_N)):
				f.write("NOMS")
				f.write(str(i))
				f.write('\n')
		for i in list(set(list_delete_V)):
				f.write("VERBES")
				f.write(str(i))
				f.write('\n')
		for i in list(set(list_delete_A)):
				f.write("ADJECTIVES")
				f.write(str(i))
				f.write('\n')
		for i in list(set(list_delete_ADV)):
				f.write("ADVERBES")
				f.write(str(i))
				f.write('\n')

	f.close()

	return dict_all



#TESTS
m = "EP.tcs.melt.utf8.split-aa.outmalt"
#print(readLemmeEtCategorie(m))
#print(dict_tout_mot(m))
print(get_list_delete(dict_tout_mot(m),get_treshold_freq(dict_tout_mot(m))))
