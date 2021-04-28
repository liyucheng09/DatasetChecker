import streamlit as st
import json

st.title('标注中文常识问答数据集')
type=st.sidebar.selectbox('Train, Dev or Test?', ['dev', 'train', 'test'])

path=f"/Users/liyucheng/projects/KagNet-master/datasets/csqa_zh/{type}_rand_split_zh.jsonl"
edited_path=f"csqa_zh/{type}_edited_zh.jsonl"
counter_path='.counter'

@st.cache
def load_original_data():
    data=[]
    with open(path) as f:
        for line in f.readlines():
            data.append(json.loads(line))
    return data

def save_edited_data(data):
    with open(edited_path, 'a', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False)+'\n')

original_data=load_original_data()

with open(counter_path, 'r') as f:
    id = f.readline()
    id = 0 if id == "" else int(id)

stem=st.text_input('Stem', original_data[id]['question']['stem'])
choices=[]
for i in original_data[id]['question']['choice']:
    choices.append(st.text_input(i['label'], i['text']))
answer_concept=st.text_input("问题Concept", original_data[id]['question']['question_concept'])
st.write("正确答案： ", original_data[id]['answerKey'])

needed_saved={'answerKey': original_data[id]['answerKey'],
 'id': original_data[id]['id'],
 'question': {'choice': [{'label': 'A', 'text': choices[0]},
                         {'label': 'B', 'text': choices[1]},
                         {'label': 'C', 'text': choices[2]},
                         {'label': 'D', 'text': choices[3]},
                         {'label': 'E', 'text': choices[4]}],
              'question_concept': answer_concept,
              'stem': stem}}

if st.button('下一位！'):
    save_edited_data(needed_saved)
    id+=1
    with open(counter_path, "w") as f:
        f.truncate()
        f.write(f"{id}")


