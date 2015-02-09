import numpy as np
import os
import random as rd
import FindMusicFiles as FMF

class ErrorFile(Exception):
	def __init__(self, file_name):
		self.file_name=file_name
	def __str__(self):
		return repr(self.file_name)

class ErrorMatrix(Exception):
	def __init__(self,value):
		self.value=value
	def __str__(self):
		return repr(self.value)

class ScoreMatrix:
	def __init__(self):
		rd.seed()#on initialise le generateur de nombre aleatoire a la creation de la matrice
		try:
			self.init_matrix()#initialise la matrice des scores
		except ErrorMatrix as e:
			print("Unable to initiate the score matrix. Current value is : ",e)
		self.decimal_choice=5#choix du nombre de decimal de l'arrondi
		self.is_normalized=False

	def init_matrix(self):
		self.score_matrix=None
		#initialise la matrice avec un fichier existant
		try:
			self.score_matrix=self.load_file()
		#initialise directement la matrice
		except ErrorFile as e:
			print("File not found  creating a new one")
			D=FMF.DocumentSearch()
			matrix_size=D.get_size()
			self.score_matrix=np.array([matrix_size,matrix_size])
			self.score_matrix.fill(1)
			np.savetxt(self.file_name,self.score_matrix)
		if self.score_matrix==None:
			raise ErrorMatrix(self.score_matrix)


	def load_file(self):
		self.file_name="Test_ScoreMatrix.txt" #Nom du fichier ou est sauvegardee la matrice des scores
		curr_dir=os.getcwd() #donne le dossier courant
		found_file=False #on verifie que le fichier est bien present dans le dossier courrant
		for path in os.walk(curr_dir,topdown=False):
			if self.file_name in path[2]:
				self.file_name=os.path.join(path[0],self.file_name)
				found_file=True
				break
		if(found_file==False):
			raise ErrorFile(self.file_name)
		else:
			score_matrix=np.genfromtxt(self.file_name,delimiter=',')
			return(score_matrix)

	def normalize_matrix(self):#normalise la matrice en arrondissant les valeurs
		self.score_matrix=np.around(self.score_matrix/np.sum(self.score_matrix,axis=0),decimals=self.decimal_choice)
		self.is_normalized=True

	def select_score(self,column): #renvoie la ligne i tq ligne correspond au score
		if (self.is_normalized==False):
			self.normalize_matrix()
		N=rd.randint(1,pow(10,self.decimal_choice))/pow(10,self.decimal_choice) #tire un nombre decimal au hasard
		candidates=np.sort(self.score_matrix[:,column])
		print(N)
		candidates[:]=candidates[::-1]
		sum_prob=0
		select_score=0
		for score in candidates:
			if N<=sum_prob+score:
				select_score=score
				break
			else:
				sum_prob+=score
		print(select_score)
		item=np.where(self.score_matrix[:,column]==select_score)#renvoie une sequence avec les lignes ou l'on trouve la valeur select_score
		item=rd.choice(item[0])#prend une ligne au hasard parmi celles ci-dessus
		return(item)

	def update_score(self, taux, listened_music, previous_music): 
		## Modification du score de la chanson ecoutee par rapport a la chanson ecoutee avant
	    if taux > 0.1 and taux < 0.5 :
	        self.score_matrix[listened_music, previous_music] += (1/0.4)*taux - 0.25
	    elif taux > 0.5:
	        self.score_matrix[listened_music, previous_music] += 1
	    self.is_normalized=False
		## Sauvegarde de la matrice actualisee
	    self.save_score_matrix()

	def save_score_matrix(self):
	    np.savetxt(self.file_name,self.score_matrix)

	def test (self) :
		self.initialize_matrix()
		##Theorie : music_analysis(music_library)
		##Theorie : music= rand(music_library)
		new_music=self.select_score(music)
		taux=0
		while not getkey():
			ecoute_chanson(new_music)
			taux = recupere_taux (new_music)
			self.attribute_score(taux,new_music, music)
			music = new_music
			new_music=self.select_score(music)