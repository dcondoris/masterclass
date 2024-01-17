# -*- coding: utf-8 -*-
"""
Created on Thu Jun  2 18:30:27 2022
"""

import pandas as pd 
import seaborn as sns 
import numpy as np 
import streamlit as st 
import matplotlib.pyplot as plt 
import plotly.express as px 
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression 
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from model import prediction, scores


df = pd.read_csv('titanic.csv', index_col = 0)

st.sidebar.title("Sommaire")

pages = ['Introduction', 'Dataviz', 'Modélisation']

page = st.sidebar.radio("Aller vers",pages)


if page == pages[0] : 
    st.title("Mon premier streamlit")
    
    
    st.markdown("Prédiction de la survie d'un passager du [titanic](https://www.kaggle.com/c/titanic)")
    
    
    st.dataframe(df.head())
    
    if st.checkbox("Afficher les valeurs manquantes"):
        st.dataframe(df.isna().sum())
        

elif page == pages[1]:
    st.write("## Dataviz")
    
    fig = plt.figure()
    sns.countplot(x ="Survived", data = df)
    st.pyplot(fig)
    
    fig_class = plt.figure()
    sns.countplot(x ="Pclass", data = df)
    st.pyplot(fig_class)
    
    hist_surv = px.histogram(df, x = 'Survived', color = 'Sex', barmode = "group")
    st.plotly_chart(hist_surv)
    
    hist_sun = px.sunburst(df, path = ["Sex", 'Pclass', 'Survived'])
    st.plotly_chart(hist_sun)
    
    
elif page == pages[2]:  
    st.write("## Modélisation")
    
    choices = ['Random Forest', 'SVC', 'Logistic Regression']

    prediction = st.cache_data(prediction)

    option = st.selectbox(
        'Which model do you want to try ?',
        choices)

    st.write('You selected :', option)

    clf = prediction(option)

    display = st.radio(
        "What do you want to display ?",
        ('Accuracy', 'Confusion matrix'))

    if display == 'Accuracy':
        st.write(scores(clf, display))
    elif display == 'Confusion matrix':
        st.dataframe(scores(clf, display))
            
    
    
    
    
    
    
    
    
    