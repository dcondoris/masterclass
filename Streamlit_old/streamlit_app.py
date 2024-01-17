import streamlit as st
import pandas as pd
from model import prediction, scores

st.title('Masterclass Streamlit')

st.header('Prediction of the Titanic Survivors')

choices = ['Random Forest', 'SVC', 'Logistic Regression']

#prediction = st.cache(prediction, suppress_st_warning=True, persist=False)

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