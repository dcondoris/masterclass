import streamlit as st

st.write('Hello World')

st.title('My Title')

age = st.slider('How old are you?', 0, 130, 25)
st.write("I'm ", age, 'years old')