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
    depth = 5
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


categorical_columns = ['number_projects', 'time_spend_company',
                       'work_accident', 'promotion_last_5_years', 'position', 'salary']



##UNCOMMENT
mlflow.set_tracking_uri("http://34.248.235.26:5000")



def compute_score(y, preds, alpha):
    return ((preds > y).sum() + alpha[preds < y].sum())/y.size


with mlflow.start_run():
    num_impute = SimpleImputer(strategy="median")

    cat_impute = SimpleImputer(strategy="most_frequent")

    cat_trans = Pipeline(steps=[("cat_imputer",cat_impute), ("encod", OneHotEncoder())])
    num_trans = Pipeline(
        steps=[
            ("num_impute",num_impute),
            ("scaling",StandardScaler())
        ]
    )

    preprocessor = ColumnTransformer(
        transformers = [
            ("num",num_trans,numerical_columns),
            ("cat",cat_trans,categorical_columns)
        ]
    )

    model = Pipeline(
        steps = [
            ("prep",preprocessor),
            ("clf",RandomForestClassifier(criterion=criterion,max_depth=depth))
        ]
    )

    model.fit(X_train,y_train)

    model.predict(X_test)

    pred_train = model.predict(X_train)
    pred_test = model.predict(X_test)
    alpha_train = X_train["last_evaluation"] * X_train["number_projects"]
    alpha_test = X_test["last_evaluation"] * X_test["number_projects"]

    custom_train = compute_score(y_train,pred_train,alpha_train)
    custom_test = compute_score(y_test,pred_test,alpha_test)


    mlflow.log_param("criterion",criterion)
    mlflow.log_param("depth",depth)

    mlflow.log_metric("custom_train",custom_train)
    mlflow.log_metric("custom_test",custom_test)

    mlflow.sklearn.log_model(model,f"model_{criterion}_{depth}")

