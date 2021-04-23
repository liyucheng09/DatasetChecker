import streamlit as st
import random
import json
from transformers import pipeline
from convert_csqa import get_fitb_from_question
import pandas as pd

st.title('CommonsenseQA Corpus')
path='/Users/liyucheng/projects/KagNet-master/datasets/csqa_new/'

@st.cache(
    hash_funcs={"transformers.pipelines.FillMaskPipeline" : lambda _ : None}
)
def load_pipeline():
    nlp=pipeline('fill-mask')
    return nlp

@st.cache
def load_data(type):
    data_path=path+type+'_rand_split.jsonl'
    data=[]
    with open(data_path) as f:
        for i in f.read().split('\n'):
            if i:
                data.append(json.loads(i))
    return data

def search_engine(ds, query):
    results=[]
    for i in ds:
        # print(i['question']['stem'].split())
        question_tokens=[w.lower() for w in i['question']['stem'].split()]
        if query in question_tokens:
            results.append(i)
    return results

option1=st.sidebar.selectbox('Train, val or test ?', ['dev', 'test', 'train'])
option2=st.sidebar.selectbox('Search Mode ?', ['False', 'True'])
dataset=load_data(option1)

if option2 == 'True':
    query=st.text_input('Search What? ', value='how')
    dataset=search_engine(dataset, query)

id=st.sidebar.slider('Choice a Instance: ', min_value=0, max_value=len(dataset)-1)

# st.json(dataset[id])
st.header(dataset[id]['question']['stem'])
st.table(dataset[id]['question']['choices'])
st.text('Correct label:  '+dataset[id]['answerKey'])
st.text('Question Concept:  ' + dataset[id]['question']['question_concept'])

st.title('Unsupervised Approach: Mask-Filling')
question_with_blank=get_fitb_from_question(dataset[id]['question']['stem'])
question_with_blank = st.text_input('Template: ', question_with_blank)
st.write(question_with_blank)

nlp=load_pipeline()
output=nlp(question_with_blank.replace("___", nlp.tokenizer.mask_token), top_k=nlp.tokenizer.vocab_size)

st.header('Top 5')
st.table(
    pd.DataFrame(output[:5])
)