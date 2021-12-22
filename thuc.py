import streamlit as st
import random
from glob import glob
from jieba.analyse import extract_tags as tfidf
import pandas as pd

st.set_page_config(
     layout="wide"
)

st.title('THUCNews 新闻语料库')

categories = glob('../bert_seq2seq-master/zh-wwm-roberta/THUCNews/*')
cat=st.sidebar.selectbox('选择一个新闻类别?', [cat[-2:] for cat in categories])

files = glob('../bert_seq2seq-master/zh-wwm-roberta/THUCNews/'+cat+'/**')
id=random.randint(0, len(files)-1)
st.button('Change one')

with open(files[id], encoding='utf-8') as f:
    st.header(files[id])
    text=f.read()
    kws=tfidf(text, withWeight=True)
    st.write(pd.DataFrame(kws))
    kws = [i[0] for i in kws]
    lines=text.split('\n')

    for line in lines:
        for kw in kws:
            if kw in line:
                line=line.replace(kw, f"-**{kw}**-")
        st.write(line)
        # st.text(line)