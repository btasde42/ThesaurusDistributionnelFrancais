# ThesaurusDistributionnelFrançais
Le projet de L3 pour TAL, Thesaurus Distributionnel de la langue français de Haoming WANG et Beyza TASDELEN.

Le dossier contient deux fichiers .py et un fichiers .csv et quatre fichiers .pickle.

Pour pouvoir faire marcher l'interface les packeges #pickle et #tkinter doit etre installé sur votre ordinateur ou environnement conda.

#extract_sim_dict:
C'est le fichier qui produit une fichier .pickle qui contient le dictionnaire de similarité du fichier donnée dans le programme. Il produit également des fichier .csv qui contient les contextes suprimées au cours du proccessus de construction du data.

#main.py

C'est le fichier qui sert à faire marcher l'interface.
Pour l'activer:

-Tapez sur votre terminal : pytho3 main.py
-A gauche du fenetre ouverte choissisez File -->Ouvrir puis choissisez l'un de fichiers .pickle qu'on a crée avec le procédure extract_sim_dict
-Puis tapez un mot dans la partie de saisie
-Choissisez la catégorie morpho-syntaxique du mot
-Appuyez sur 'Save' puis 'Affiche'

Les 5 résultats le plus pertinants vont etre affiché!
