import streamlit as st
import random
import pandas as pd
st.set_page_config(
     layout="wide"
)
st.title('MELD Dataset')

@st.cache
def load_xsum(type):
    df = pd.read_csv(f'/Users/liyucheng/projects/ERC/data/DialogueRNN_features/MELD-master/data/MELD/{type}_sent_emo.csv', index_col='Sr No.')
    return [i for i in df.groupby('Dialogue_ID')]

option1=st.sidebar.selectbox('Train, val or test ?', ['train', 'dev', 'test'])
dialogues=load_xsum(option1)
id=random.randint(0, len(dialogues)-1)
if st.button('Change one'): id=random.randint(0, len(dialogues)-1)

st.table(dialogues[id][1])