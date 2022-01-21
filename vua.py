from datasets import load_dataset
from lyc.data import get_hf_ds_scripts_path
import streamlit as st
import os
import numpy as np
from collections import OrderedDict

st.set_page_config(
     layout="wide"
)

st.title('VUA')

data_dir ='/Users/liyucheng/projects/acl2021-metaphor-generation-conceptual-main/EM/data/VUA20'

p = get_hf_ds_scripts_path('vua20')
data_files={'train': os.path.join(data_dir, 'train.tsv'), 'test': os.path.join(data_dir, 'test.tsv')}

@st.cache
def load_ds():
    print('reload ds!--')
    ds = load_dataset(p, data_files=data_files, name='combined')
    # ds1 = load_dataset(p, data_files=data_files, name='combined', split='train[:20%]')
    ds = load_dataset(p, data_files=data_files, name='combined', split='test')
    ds.set_format('numpy')
    token2sent = {}
    for index, i in enumerate(ds):
        target_words = i['tokens'][i['is_target']==1]
        target_index = np.where(i['is_target']==1)[0]
        for target, target_index in zip(target_words, target_index):
            if target not in token2sent:
                token2sent[target] = []
            token2sent[target].append([target_index, i['labels'][target_index], index]) # target_index, label, sentence_index
    ds.set_format(None)
    token2sent = OrderedDict(sorted(token2sent.items(), key=lambda t: -len(t[1])))
    return ds, token2sent

ds, token2sent = load_ds()

id = st.sidebar.slider('Select one example by id', min_value=0, max_value=len(ds)-1)
is_target, label = ds[id]['is_target'], ds[id]['labels']

st.table([ds[id]['tokens'], label])

target_key = st.sidebar.selectbox('Select a target word, it will show all examples with the target', [i[0]+':'+str(len(i[1])) for i in token2sent.items()])
target_id = target_key.split(':')[0]

st.header('🌙 means is metaphor, 🔥 means not metaphor')
for i in token2sent[target_id]:
    # print(i, ds[i[2]])
    words = ds['tokens'][i[2]]
    if i[1]:
        words[i[0]] = "🌙"+words[i[0]]
    else:
        words[i[0]] = "🔥"+words[i[0]]
    st.markdown(' '.join(words))