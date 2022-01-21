import streamlit as st
import random
import pandas as pd
st.set_page_config(
     layout="wide"
)
st.title('ONEIE')

@st.cache
def read_file():
    df = pd.read_csv('data/oneie_test.tsv', sep='\t')
    return df

df = read_file()
id=random.randint(0, len(df.index)-1)
if st.button('Change one'): id=random.randint(0, len(df.index)-1)

line = df.iloc[id]
# print(line, type(line['entities']))
st.title('sentence')
st.markdown(line['tokens'])

st.title('entity')
st.markdown('🥕'.join([i[0] + ' --- ' + i[3] for i in eval(line['entities'])]))

st.title('event')
st.markdown('🥕'.join([i[0] + " --> " +i[3] for i in eval(line['triggers'])]))

st.title('roles')
st.markdown('🥕'.join([i[0] + " --> " +i[3] for i in eval(line['roles'])]))