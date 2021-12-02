from django.shortcuts import render
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

model = joblib.load("influmodel.sav")

def home(request):
    return render(request, "index.html")

def res(lis):
    print(model.predict([lis]))

def result(request):
    lis =[2000,80,50,60]
    # lis.append(request.Get['Followers'])
    # lis.append(request.Get['hired rate'])
    # lis.append(request.Get['hours worked'])
    # lis.append(request.Get['accuracy'])

    print(model.predict([lis]))
    return render(request, "result.html")

