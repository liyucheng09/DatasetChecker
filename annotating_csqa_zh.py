import streamlit as st
import json

st.set_page_config(
     page_title='中文CSQA',
     layout="wide"
)

st.title('标注中文常识问答数据集')
st.subheader("每条确认无误后都要先点提交，再点下一个！")
type=st.sidebar.selectbox('Train, Dev or Test?', ['dev', 'train', 'test'])

zh_path=f"/Users/liyucheng/projects/KagNet-master/datasets/csqa_zh/{type}_rand_split_zh.jsonl"
en_path=f"/Users/liyucheng/projects/KagNet-master/datasets/csqa_new/{type}_rand_split.jsonl"
edited_path=f"csqa_zh/{type}_edited_zh.jsonl"
counter_path='.counter'

col1, col2 = st.beta_columns(2)

@st.cache
def load_original_data(path):
    data=[]
    with open(path) as f:
        for line in f.readlines():
            data.append(json.loads(line))
    return data

def save_edited_data(data):
    with open(edited_path, 'a', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False)+'\n')

original_data=load_original_data(zh_path)
en_data=load_original_data(en_path)

with open(counter_path, 'r') as f:
    id = f.readline()
    id = 0 if id == "" else int(id)

if st.button('下一个'):
    id+=1
    with open(counter_path, "w") as f:
        f.truncate()
        f.write(f"{id}")

with col1:
    stem=st.text_input('Stem', original_data[id]['question']['stem'])
    choices=[]
    for i in original_data[id]['question']['choice']:
        choices.append(st.text_input(i['label'], i['text']))
    answer_concept=st.text_input("问题Concept", original_data[id]['question']['question_concept'])
    st.write("正确答案： ", original_data[id]['answerKey'])

with col2:
    st.write("Stem: ", en_data[id]['question']['stem'])
    for i in en_data[id]['question']['choices']:
        st.write(i['label'], '.', i['text'])
    st.write(en_data[id]['question']['question_concept'])

if st.button('提交该条'):
    needed_saved={'answerKey': original_data[id]['answerKey'],
    'id': original_data[id]['id'],
    'question': {'choice': [{'label': 'A', 'text': choices[0]},
                            {'label': 'B', 'text': choices[1]},
                            {'label': 'C', 'text': choices[2]},
                            {'label': 'D', 'text': choices[3]},
                            {'label': 'E', 'text': choices[4]}],
                'question_concept': answer_concept,
                'stem': stem}}
    save_edited_data(needed_saved)
    st.write('已提交')

st.write(f'已完成: {id}/{len(original_data)}')
st.progress(id/len(original_data))