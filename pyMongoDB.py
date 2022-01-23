# -*- coding: utf-8 -*-
"""
Created on Fri Sep 17 14:52:16 2021

@author: zkw, lepercq, louesdon
"""

import os
os.chdir(os.getcwd())
import pandas as pd
import pymongo
#import seaborn
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.metrics import plot_confusion_matrix
from datetime import date

## 3 - Récupérer les informations stockées dans la bdd MongoDB
connex = pymongo.MongoClient("mongodb://localhost:27017/")   #serveur MongoDB
db = connex.p2_wec.wec                                             #se connecter à la bdd "wec" qui contient les différentes collections nécessaires au projet 

#créer l'index (déjà créé dans la base MongoDB)
#db.create_index([("matchId", pymongo.ASCENDING)], unique=True)          
print("nb de parties stockées : ", db.estimated_document_count(), "\n")

## importer les données de MongoDB dans Python

#ML
df = pd.DataFrame(db.find())
df['Victoire'] = [1 if e==200 else 0 for e in df['Win']]
y = df["Victoire"]
df = df.drop(columns=['_id',"Position_0","Position_1","Position_2","Position_3","Position_4","Position_5","Position_6","Position_7","Position_8","Position_9",
                      "Team_0","Team_1","Team_2","Team_3","Team_4","Team_5","Team_6","Team_7","Team_8","Team_9","Patch","matchId","EloDiff","Win",
                      "streak_0","streak_1","streak_2","streak_3","streak_4","streak_5","streak_6","streak_7","streak_8","streak_9", "Victoire"])

print(df.head())

#df.to_csv("WEC_sample.csv", sep=';', index=False)


#faire un random forest
print("apprentissage...10min (est.)")

#acc : 65.0374%
#X_train, X_test, y_train, y_test = train_test_split(df, y, test_size=0.33, random_state=42)
#clf = RandomForestClassifier(max_depth=3, random_state=0, min_samples_split = 4)

#acc : 67.17%
#X_train, X_test, y_train, y_test = train_test_split(df, y, test_size=0.33, random_state=42)
#clf = RandomForestClassifier(n_estimators = 10000, max_depth=30, bootstrap= False, random_state=0, min_samples_split = 30)

X_train, X_test, y_train, y_test = train_test_split(df, y, test_size=0.33, random_state=42)
clf = RandomForestClassifier(n_estimators = 10000, max_depth=60, bootstrap= False, random_state=0, min_samples_split = 30)

clf.fit(X_train, y_train)
y_predict = clf.predict(X_test)
predict_proba = clf.predict_proba(X_test)
print(y_predict)
print(predict_proba)

#for proba in predict_proba:
#    #récupérer les probas de gagner pour l'équipe bleue
#    print(proba[0])

conf = confusion_matrix(y_test, y_predict, labels = [0,1])
print(conf)
vrais = conf[0][0] + conf[1][1]
faux = conf[0][1] + conf[1][0]
print("Précision:",str(round(vrais/(vrais+faux)*100,2)),"%")
#plot_confusion_matrix(clf, X_test, y_test, normalize = "pred")  


joblib.dump(clf, "random_forest_1.joblib")
