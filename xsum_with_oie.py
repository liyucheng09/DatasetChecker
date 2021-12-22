import streamlit as st
import pickle
import re
import json

# with open('58111.json') as f:
#     st.json(json.load(f))

data_path = 'xsum_with_oie.pkl'

st.set_page_config(
     page_title='Xsum-OIE',
     layout="wide"
)

@st.cache()
def load_data():
    with open(data_path, 'rb') as f:
        data = pickle.load(f)
    return data

data = load_data()
chosen = st.sidebar.slider('Choose one article', min_value=0, max_value=len(data)-1, value=0)

document, summary, doc_verbs, summary_verbs = \
     data[chosen]['document'], data[chosen]['summary'], data[chosen]['doc_verbs'], data[chosen]['summary_verbs']

st.header('Summary')

st.write(summary)

st.header('Summary verbs')

for i in summary_verbs:
    st.text(re.findall(r'\[(.*?)\]', i['description']))

st.header('Doc')

st.write(document)

st.header('Doc verbs')

for i in doc_verbs:
    st.write(re.findall(r'\[(.*?)\]', i['description']))
