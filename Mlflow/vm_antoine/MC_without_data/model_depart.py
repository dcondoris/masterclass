import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
import mlflow
import sys 

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

if len(sys.argv) == 1 : 
    criterion = "gini"
    depth = None
else: 
    criterion = sys.argv[1]
    try:
       depth = int(sys.argv[2]) 
    except:
        depth = None

df = pd.read_csv("hr_train_corrupted.csv")

y = df['left']
X = df.drop('left', axis=1)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

print("Train Set:", X_train.shape)
print("Test Set:", X_test.shape)

numerical_columns = ['satisfaction_level',
                     'last_evaluation', 'average_monthly_hours']

for col in numerical_columns:
    X_train[col].fillna(X_train[col].median(), inplace=True)
    X_test[col].fillna(X_train[col].median(), inplace=True)

categorical_columns = ['number_projects', 'time_spend_company',
                       'work_accident', 'promotion_last_5_years', 'position', 'salary']

for col in categorical_columns:
    X_train[col].fillna(X_train[col].mode()[0], inplace=True)
    X_test[col].fillna(X_train[col].mode()[0], inplace=True)

X_train = X_train.reset_index(drop=True)  # utile pour la concaténation
X_test = X_test.reset_index(drop=True)
y_train = y_train.reset_index(drop=True)
y_test = y_test.reset_index(drop=True)

X_train['salary'].replace(['low', 'medium', 'high'], [0, 1, 2], inplace=True)
ohe = OneHotEncoder().fit((X_train[['position']]))
positions = pd.DataFrame(ohe.transform(X_train[['position']]).toarray(), columns=ohe.categories_[0])

X_train_cl = pd.concat([X_train.drop('position', axis=1), positions], axis=1)

X_test['salary'].replace(['low', 'medium', 'high'], [0, 1, 2], inplace=True)

test_positions = pd.DataFrame(ohe.transform(X_test[['position']]).toarray(), columns=ohe.categories_[0])

X_test_cl = pd.concat([X_test.drop(['position'], axis=1), test_positions], axis=1)

scaler = StandardScaler()


X_train_scaled = scaler.fit_transform(X_train_cl)
X_test_scaled = scaler.transform(X_test_cl)

cl3 = RandomForestClassifier()
cl3.fit(X_train_scaled, y_train)

from sklearn.model_selection import GridSearchCV


param_grid = {'criterion': ['gini', 'entropy'], 'max_depth': np.arange(3, 15)}

clf_gs = GridSearchCV(cl3, param_grid, cv=5, verbose=1, scoring='recall')

clf_gs.fit(X_train_scaled, y_train)

print(clf_gs.best_params_)

clf_gs.score(X_test_scaled, y_test)



def compute_score(y, preds, alpha):
    return ((preds > y).sum() + alpha[preds < y].sum())/y.size



rf = RandomForestClassifier(criterion=criterion,max_depth=depth)
rf.fit(X_train,y_train)

pred_train = rf.predict(X_train)
pred_test = rf.predict(X_test)
alpha_train = X_train["last_evaluation"] * X_train["number_projects"]
alpha_test = X_test["last_evaluation"] * X_test["number_projects"]

custom_train = compute_score(y_train,pred_train,alpha_train)
custom_test = compute_score(y_test,pred_test,alpha_test)


print("criterion",criterion)
print("depth",depth)

print("custom_train",custom_train)
print("custom_test",custom_test)

print(model,f"model_{criterion}_{depth}")

