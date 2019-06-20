
import pickle
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter import ttk

variable =""
mot=""
file=""
def set_cat(value):
    global variable
    variable = value

def save_word():
	global mot
	mot=entry.get()

def ouvrir():
	global file
	file=askopenfilename(title="Ouvrir un fichier",filetypes=[('Pickle files','.pickle')])

def get_words():
	global file
	global variable
	global mot
	XBASE, YBASE, DISTANCE = 10,20,20
	dictt=pickle.load(open(file, "rb"))
	if mot in dictt[variable].keys():
		sort=sorted(dictt[variable][mot],key=lambda x: x[1],reverse=True)
		if len(sort)<5: #on va prendre 5 mot le plus corréles
			for i,j in enumerate(sort):
				canvas.create_text((XBASE, YBASE+i * DISTANCE),text=j, anchor=W, fill='blue')
		else:
			for i,j in enumerate(sort[:5]):
				canvas.create_text((XBASE, YBASE+i * DISTANCE),text=j, anchor=W, fill='blue')
			

fen = Tk()
canvas = Canvas(fen)
canvas.pack(side=BOTTOM)

menubar=Menu(fen)
fen.config(menu=menubar)
filemenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="Ouvrir",command=ouvrir)

lab = Label(fen,text='Bienvenue choissisez une fichier à mettre comme base de données. Saissisez une mot pour chercher dans notre thésaurus et choissisez son catégorie morpho-syntaxique (N,V,Adj,Adv) svp!')
lab.pack()

entry_var=StringVar()
entry=Entry(fen,textvariable=entry_var)
entry.pack()


n= Checkbutton(fen,text='N',command=lambda *args: set_cat('N')).pack()
v=Checkbutton(fen,text='V',command=lambda *args: set_cat('V')).pack()
adj=Checkbutton(fen,text='A',command=lambda *args: set_cat('A')).pack()
adv=Checkbutton(fen,text='ADV',command=lambda *args: set_cat('ADV')).pack()

Button(fen,text='save',command=save_word).pack()
Button(fen,text='affiche',command=get_words).pack()

Button(fen, text='Quit', command=fen.quit).pack(side=RIGHT)

fen.mainloop()

