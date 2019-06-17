#!/usr/bin/env python3

#-*- coding: utf-8 -*-

#une fonction pour lire un corpus 

from collections import defaultdict, Counter

import pandas as pd

from itertools import dropwhile

def readLemmeEtCategorie(m):

	"""

	Cette fonction renvoie une liste des lemmes avec leurs catégorie morpho-syntaxique

	Args:

		m:une fichier

	Returns:

		une liste des tuples

	"""

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

	"""

	Cette fonction crée une dictionnaire des mots existant dans une fichier
	we can find out :
	1, the frequence of each w
	2, the frequence of each context (r,w') coresspondant with this w 

	Args:

		m:un liste des tuples

	returns:

		une dictionnaire de dictionnaires de type: 4 grand Catégorie(N,V,Adj,V):{(w,cat): {((-1/+1,(w',cat)):freq...]}}

	"""



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



	dict_all={} #on va créer une version de notre dictionnaire sans les contextes qui sont moins que le treshold





	for k,v in dict_mot.items():

		if k=='N':

			for i,j in v.items():

				for m,n in j.items():

					if n<=dict_treshold['N']:

						list_delete_N.append((m,n)) #enregistre les elts qui vont etre supprimé

					



		if k=='V':

			for i,j in v.items():

				for m,n in j.items():

					if n<=dict_treshold['V']:

						list_delete_V.append((m,n))







		if k=='A':

			for i,j in v.items():

				for m,n in j.items():

					if n<=dict_treshold['A']:

						list_delete_A.append((m,n))





		if k=='ADV':

			for i,j in v.items():

				for m,n in j.items():

					if n<=dict_treshold['ADV']:

						list_delete_ADV.append((m,n))



	print(dict_all)





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


"""
now we still have to do: 
1, a new dictionnary after deleting the very low frequency words
2, find out all the 3 parts of the frenquences
"""


	def newdict_tout_mot():
		'''
		here we have to delete all the words that we think are not useful
		so we can get the 3 types of the frenquences: f(w), f(r,w'), f(w,r,w')

		retuern:

		so in the end, it will still show like:
		une dictionnaire de dictionnaires de type: 4 grand Catégorie(N,V,Adj,V):{(w,cat): {((-1/+1,(w',cat)):freq...]}}

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
then we have to caqlculate the PMI and Cosine
'''








#TESTS

m = "estrepublicain.extrait-aa.19998.outmalt"

print(readLemmeEtCategorie(m))

#dictt=dict_tout_mot(readLemmeEtCategorie(m))

#get_list_delete(dictt,get_treshold_freq(dictt))