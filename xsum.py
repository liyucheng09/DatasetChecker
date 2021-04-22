import streamlit as st
from datasets import load_dataset
import random

st.title('XSum Corpus')

@st.cache
def load_xsum():
    return load_dataset('xsum', cache_dir='/Users/liyucheng/projects/model_cache')

option1=st.sidebar.selectbox('Train, val or test ?', ['train', 'validation', 'test'])
ds=load_xsum()
id=random.randint(0, len(ds[option1])-1)
if st.button('Change one'): id=random.randint(0, len(ds[option1])-1)

for k,v in ds[option1][id].items():
    st.header(k)
    st.write(v)