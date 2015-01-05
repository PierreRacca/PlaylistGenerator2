## EXERCICE 1

etudiants = [
  ("Nom1", "Pre1", [ ("TDLOG", 12), ("1INFO", 13), ("Anglais", 12) ]),
  ("Nom2", "Pre2", [ ("IMG", 15), ("Anglais", 11) ])
]

prout
def affsimp(x):
    for k in x:
        for i in k:
         print(i)
         
def affsimpp(l):
    [print(i) for x in l for i in x]
             
affsimp(etudiants)
affsimpp(etudiants)



## EXERCICE 2

def dico2(l):
    res={}
    for x in l:
        res(x[0:2])=dict(x[2])
    return res 

    
## EXERCICE 3
    

moyennes={}
for x in etudiants:
    moyennes[x[0:2]]=sum([note[1] for note in x[2]])/len(x[2])
    
## EXERCICE 4

min_max={}

for x in etudiants:
    for note in x[2]:
        if not(note[0] in min_max):
             min_max[note[0]]= [note[1],note[1]]
        elif:
              min_max[note[0]][1]<note[1]:
                min_max[note[0]][1]=note[1]
            elif:
                min_max[note[0]][0]>note[1]:
                    min_max[note[0]][0]=note[1]