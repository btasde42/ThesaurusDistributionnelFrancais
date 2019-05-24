#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#une fonction pour lire un corpus 
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
				
def contextAdj(m):
	l=readLemmeEtCategorie(m)
	l = sorted(l, key = lambda categorie : categorie[1])#list de tuple
	listA=[]
	for i in range(len(l)):
		if l[i][1]=="A":
			listA.append(l[i][0]) #list de string
	#on doit creer les contexts entre les deut mots
	listcontxteA=[]
	for i in range(1,len(listA)):
		listcontxteA.append((listA[i-1],1,listA[i]))
		listcontxteA.append((listA[i],-1,listA[i-1]))
	#on cree une dictionnaire pour calculer les frequences
	adj={}
	for k in listcontxteA:
		adj[k]=adj.get(k,0)+1
	return adj
	
def contexteN(m):
	l=readLemmeEtCategorie(m)
	l = sorted(l, key = lambda categorie : categorie[1])#list de tuple
	listN=[]	
	for i in range(len(l)):
		if l[i][1]=="N":
			listN.append(l[i][0])
	listcontxteN=[]
	for i in range(1,len(listN)):
		listcontxteN.append((listN[i-1],1,listN[i]))
		listcontxteN.append((listN[i],-1,listN[i-1]))
	nom={}
	for k in listcontxteN:
		nom[k]=nom.get(k,0)+1
	return nom

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

def contexteADV(m):
	l=readLemmeEtCategorie(m)
	l = sorted(l, key = lambda categorie : categorie[1])#list de tuple
	listADV=[]
	for i in range(len(l)):
		if l[i][1]=="ADV":
			listADV.append(l[i][0])
	listcontxteADV=[]
	for i in range(1,len(listADV)):
		listcontxteADV.append((listADV[i-1],1,listADV[i]))
		listcontxteADV.append((listADV[i],-1,listADV[i-1]))
	adv={}
	for k in listcontxteADV:
		adv[k]=adv.get(k,0)+1
	return adv
	
m = "estrepublicain.extrait-aa.19998.outmalt"
#print(readLemmeEtCategorie(m))
print(contexteADV(m))
