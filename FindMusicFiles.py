import os
import sys
import hashlib

class DocumentSearch:
 extension=('mp3','wma','m4a') #extension de fichiers de musique

 #ensemble de methode statiques generales qui pourraient etre utilisees en dehors de la classe
 @staticmethod
 def display_size(size):#renvoie la taille d'un fichier de maniere lisible
  new_size=size
  suffix="B"
  for puissance in ['','K','M','G','T']:
      if(new_size<1024):
          return "%3.f%s%s" %(new_size,puissance,suffix) 
      else:
          new_size/=1024
  return "Oh it's huge !"
 
 @staticmethod
 def display_title(title):
    print('\n'+title)
    print('-'*len(title))

 def  __init__(self):
    self.total_size=0
    self.files_list=[]#liste des fichiers audio
    self.hash_list=[]#permet de trouver les copies grace a une table de hashage
    if len(sys.argv)>1:
      self.pathname=os.chdir(sys.argv[1])#accede a l'endroit renseigné
      self.pathname=os.getcwd()
    else:
      self.pathname=os.getcwd()#definit l'endroit ou l'on se trouve
    self.get_audio_files_info()#actualise les differentes variables de la classe

 

 def get_audio_files_info(self):
    total_size=0
    for root, dirs, files in os.walk(self.pathname, topdown=False):
      for name in files:
        if '.' in name:#si le fichier possede une extension
          name_extension=name.split('.')
          if name_extension[len(name_extension)-1] in self.extension:#si le fichier a une extension correspondant à un fichier audio
            full_name=os.path.join(root,name)
            hash_code=hashlib.md5(name.encode('utf-8')).digest()
            if hash_code not in self.hash_list:
              self.hash_list+=[hash_code]#on store le nom du fichier et son encodage
              size=os.path.getsize(full_name)#donne la taille du fichier
              self.total_size+=size
              self.files_list+=[(name,size)]

 def get_song_files(self):
    song_files=[]
    for name, size in self.files_list:
      song_files+=[name]
    return(tuple(song_files))

 def get_size(self):
    return(len(self.files_list))
 
 #Fonctions d'affichage

 def display_files_and_size(self):#affichage des resultats
  self.display_title("Fichiers audio")
  for doc in self.files_list:
          display_string="%s utilise %s (soit %.2f %% du total)" %(doc[0], self.display_size(doc[1]), doc[1]/self.total_size*100)
          print(display_string)