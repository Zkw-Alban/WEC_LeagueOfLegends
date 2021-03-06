# -*- coding: utf-8 -*-
"""
Created on Thu Sep 23 16:46:39 2021

@author: zkw, lepercq, louesdon
"""

import os
import pandas as pd
import pymongo
import seaborn
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.metrics import plot_confusion_matrix

os.chdir(r"D:\Antoine\CNAM\3A\WEC")

## 3 - Récupérer les informations stockées dans la bdd MongoDB
connex = pymongo.MongoClient("mongodb://127.0.0.1:27017/")   #serveur local
db = connex.wec.gamedata                                              #se connecter à la bdd "wec" qui contient les différentes collections nécessaires au projet 

#créer l'index (déjà créé dans la base MongoDB)
#db.create_index([("matchId", pymongo.ASCENDING)], unique=True)          
print("nb de parties stockées : ",db.estimated_document_count())
## importer les données de MongoDB dans Python

res = db.aggregate([ { "$group": { "_id": "$Win", 
                                  "nb": { "$sum": 1 } } },
                     { "$sort" : { "nb": -1}}
                     ])
df2 = pd.DataFrame(res)
df2.columns = ["Equipe2","Nombre de victoires"]
df2['Equipe'] = ["Rouge" if e==200 else "Bleu" for e in df2['Equipe2']]
graph = seaborn.catplot(x="Equipe", y="Nombre de victoires", data = df2, kind="bar", height=5)

#ML
df = pd.DataFrame(db.find())
#df['Victoire'] = [1 if e==200 else 0 for e in df['Win']]
y = df["Win"]
df = df.drop(columns=['_id', "Position_0", "Position_1", "Position_2",
                      "Position_3", "Position_4", "Position_5", "Position_6",
                      "Position_7", "Position_8", "Position_9", "Team_0", 
                      "Team_1", "Team_2", "Team_3", "Team_4", "Team_5",
                      "Team_6", "Team_7", "Team_8", "Team_9", "Patch", "matchId"])

#df.to_csv("WEC_sample.csv", sep=';', index=False)


#faire un random forest
X_train, X_test, y_train, y_test = train_test_split(df.drop('Win', axis=1), df["Win"], test_size=0.20, random_state=42)
clf = RandomForestClassifier(max_depth=10, random_state=0, min_samples_split = 4)
#clf = MLPClassifier(solver='sgd', alpha=1e-5, hidden_layer_sizes=(41, 32, 16, 2), random_state=1)
#clf = svm.SVC()
clf.fit(X_train, y_train)
y_predict = clf.predict(X_test)
#conf = confusion_matrix(y_test, y_predict, labels = [100,200])
plot_confusion_matrix(clf, X_test, y_test, normalize = "true")  