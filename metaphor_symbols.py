import streamlit as st
import random
import pandas as pd
from nltk.corpus import wordnet as wn

st.set_page_config(
     layout="wide"
)
st.title('Symbols of Metaphorical and Literal Expressions')

@st.cache
def load_data():
    df = pd.read_csv('data/moh.conceptnet.bleu.tsv', sep='\t')
    return df

data = load_data()
data = data[data['metaphor_symbol']!='0']

id=random.randint(0, len(data.index)-1)
if st.button('Change one'): id=random.randint(0, len(data.index)-1)

# st.header('metaphorical and literal experssions')
st.markdown("**Metaphorical**:" + data.iloc[id]['metaphor'])
st.markdown("**Literal**...........:  " + data.iloc[id]['literal'])

target = data.iloc[id]['metaphor'].split()
for token in data.iloc[id]['literal'].split():
    if token in target:
        target.remove(token)

print(target, '--')

assert len(target) == 1
target = target[0]
print(target, '--')
glosses = {f'senses of {target}': [sense.definition() for sense in wn.synsets(target)], 'id': [str(sense) for sense in wn.synsets(target)]}
st.table(glosses)

st.header('symbols')
st.write(data.iloc[id]['metaphor_symbol'])
st.write(data.iloc[id]['literal_symbol'])

st.header('Bleu')
st.write(data.iloc[id]['bleu_score'])
