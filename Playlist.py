## TESTS
#a=mutagen.mp4.MP4('06 Trouble.m4a')

#b=a.tags

#for x in b.keys():
 #   if x!='covr':
  #      print(b[x])

#print(a["\xa9nam"])

#c=[[i*j for i in range(0,10)] for j in range(0,10)]

#rep=dict()
#parcours('/Users/pierreraccaglia/Music/iTunes/iTunes Media/Music/',rep)
#print(rep['Trouble'][2])

#c=[[0 for i in range(0,len(rep))] for j in range(0,len(rep))]

#attrib(c,rep)
#print(c)

##CHOIX DES LIBRAIRIES
import mutagen.mp4,os, sys, os.path


##DEFINITION DES FONCTIONS

type2fichier=['.m4a']
def parcours(chemin,reponse):
    os.chdir(chemin)
    for chanson in os.listdir():
        if os.path.isfile(chanson):
            ext=os.path.splitext(chanson)[1]
            if ext in type2fichier:
                a=mutagen.mp4.MP4(chanson).tags
                if ("\xa9gen" in a.keys() and "\xa9nam" in a.keys() and "\xa9ART" in a.keys()):
                    reponse[a["\xa9nam"][0]]=[len(reponse),a["\xa9nam"][0],a["\xa9ART"][0],a["\xa9gen"][0]]
                elif "\xa9nam" in a.keys():
                    reponse[a["\xa9nam"][0]]=[len(reponse),'NULL','NULL','NULL']
                #print(a["\xa9nam"],a["\xa9ART"])
        elif os.path.isdir(chanson):
                parcours(chanson,reponse)
    os.chdir('..')

 
def attrib(matrice,reponse):
    for nom1 in reponse.keys():
        for nom2 in reponse.keys():
            if reponse[nom1][2]==reponse[nom2][2] and nom1!=nom2:
                matrice[reponse[nom1][0]][reponse[nom2][0]]+=10
            elif reponse[nom1][3]==reponse[nom2][3] and nom1!=nom2:
                matrice[reponse[nom1][0]][reponse[nom2][0]]+=5
                
            

##FONCTION GLOBALE
def meta(chemin):
    rep=dict()
    parcours(chemin,rep)
    c=[[1 for i in range(0,len(rep))] for j in range(0,len(rep))]
    attrib(c,rep)
    s=[]
    for i in range(len(c)):
        #k=sum(c[i])
        for p in range(len(c)):
            c[i][p]=c[i][p]/16
    print(c)

meta('/Users/pierreraccaglia/Music/iTunes/iTunes Media/Music/')
    
    

