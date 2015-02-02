import numpy as np
import os
import random as rd

class ErrorFile(Exception):
	def __init__(self, file_name):
		self.file_name=file_name
	def __str__(self):
		return repr(self.file_name)

class ScoreMatrix:
	def __init__(self):
		rd.seed()#on initialise le generateur de nombre aleatoire a la creation de la matrice
		self.load_file()#charge la matrice des scores self.score_matrix
		self.decimal_choice=5#choix du nombre de decimal de l'arrondi
		self.is_normalized=False

	def load_file(self):
		self.file_name="Test_ScoreMatrix.txt" #Nom du fichier ou est sauvegardee la matrice des scores
		curr_dir=os.getcwd() #donne le dossier courant
		try:
			found_file=False #on verifie que le fichier est bien present dans le dossier courrant
			for path in os.walk(curr_dir,topdown=False):
				if self.file_name in path[2]:
					self.file_name=os.path.join(path[0],self.file_name)
					found_file=True
					break
			if(found_file==False):
				raise ErrorFile(self.file_name)
			else:
				self.score_matrix=np.genfromtxt(self.file_name,delimiter=',')
		except ErrorFile as e:
			print("File not found : ",e)

	def normalize_matrix(self):#normalise la matrice en arrondissant les valeurs
		self.score_matrix=np.around(self.score_matrix/np.sum(self.score_matrix,axis=0),decimals=self.decimal_choice)
		self.is_normalized=True

	def select_score(self,column): #renvoie la ligne i tq ligne correspond au score
		if (self.is_normalized==False):
			self.normalize_matrix()
		N=rd.randint(1,pow(10,self.decimal_choice))/pow(10,self.decimal_choice) #tire un nombre decimal au hasard entre 0,000001 et 1
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

    def attribute_score(self, taux, column): #taux d'ecoute a recuperer d'un autre fichier
        ligne = select_score(self, column)
        score_chanson_ecoutee = self.score_matrix[ligne, column]
        if taux > 0.1 and taux < 0.5 :
            score_chanson_ecoutee+ = (1/0.4)*taux - 0.25
        elif taux > 0.5:
            score_chanson_ecoutee+= 1








#numpy.savetxt("nom_fichier.txt",M)





