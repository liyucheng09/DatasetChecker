import streamlit as st
import random
import json

st.title('CommonsenseQA Corpus')
path='/Users/liyucheng/projects/KagNet-master/datasets/csqa_new/'

@st.cache
def load_data(type):
    data_path=path+type+'_rand_split.jsonl'
    data=[]
    with open(data_path) as f:
        for i in f.read().split('\n'):
            if i:
                data.append(json.loads(i))
    return data

option1=st.sidebar.selectbox('Train, val or test ?', ['dev', 'test', 'train'])
dataset=load_data(option1)
id=random.randint(0, len(dataset)-1)
if st.button('Change one'): id=random.randint(0, len(dataset)-1)

# st.json(dataset[id])
st.header(dataset[id]['question']['stem'])
st.table(dataset[id]['question']['choices'])
st.text('Correct label:  '+dataset[id]['answerKey'])
st.text('Question Concept:  ' + dataset[id]['question']['question_concept'])