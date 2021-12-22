import gensim
from datasets import load_dataset
import streamlit as st

lda_path = '/Users/liyucheng/projects/XSum-master/XSum-Dataset/lda-train-document-lemma-topic-512-iter-1000/lda.model'

@st.cache()
def load_ds():
    return load_dataset('xsum')

@st.cache(allow_output_mutation=True)
def load_lda():
    return gensim.models.ldamulticore.LdaMulticore.load(lda_path, mmap='r')

ds = load_ds()
lda = load_lda()

ds_part = st.sidebar.radio('ds', ('train', 'validation', 'test'))
ds = ds[ds_part]
id = st.sidebar.slider('article id', min_value=0, max_value=len(ds)-1)

article = ds[id]

st.header('Summary')
st.write(article['summary'])

st.header('Doc')
st.write(article['document'])

bow = lda.id2word.doc2bow(article['document'].split())
topics = lda.get_document_topics(bow, per_word_topics=1e-8, minimum_probability=1e-8, minimum_phi_value=1e-8)

dt, wt, phi = topics
totoken = lambda x: [[lda.id2word.id2token[i[0]], i[1:]] for i in x]


selected_t = sorted(dt, key=lambda x:x[1], reverse=True)[:5]
st.table(selected_t)

phi = totoken(sorted(phi, key=lambda x: max([i[1] for i in x[1]]) if len(x[1])!=0 else 1e-8 , reverse=True))
st.table(phi)