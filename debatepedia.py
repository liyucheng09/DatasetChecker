import streamlit as st
import random

st.title('XSum Corpus')
path='/Users/liyucheng/projects/Qsumm/data/debatepedia/'

@st.cache
def load_data(type):
    content, query, summary = type+'_content', type+'_query', type+'_summary'
    with open(path+content) as f:
        content=f.read().split('\n')
    with open(path+query) as f:
        query=f.read().split('\n')
    with open(path+summary) as f:
        summary=f.read().split('\n')
    results=[]
    for c,q,s in zip(content, query, summary):
        results.append({'content':c, 'query':q, 'summary':s})
    return results

option1=st.sidebar.selectbox('Train, val or test ?', ['train', 'valid', 'test'])
dataset=load_data(option1)
id=random.randint(0, len(dataset)-1)
if st.button('Change one'): id=random.randint(0, len(dataset)-1)

for k,v in dataset[id].items():
    st.header(k)
    st.write(v)