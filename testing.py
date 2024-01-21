import streamlit as st
import code_editor as _code_editor
from code_editor import code_editor
import random

print('-'*100)

# if (beg := st.session_state.get('code')):
#     print('session state at beginning:', beg['text'])

# def get_pattern():
#     return '' if (ezre := st.experimental_get_query_params().get('pattern')) is None else ezre[0]

# def set_pattern(to):
#     params = st.experimental_get_query_params()
#     params['pattern'] = to
#     st.experimental_set_query_params(**params)


# def doThing():
#     print('doing thing')
#     set_pattern(get_pattern() + '+ thing!')
#     # if '_toAdd' in st.session_state:
#     #     st.session_state['_toAdd'] += ' + thing!'
#     # else:
#     #     st.session_state['_toAdd'] = ' + thing!'

# st.button('add thing!', on_click=doThing)

# # cur = st.session_state['code']['text'] if st.session_state.get('code') is not None else ''
# cur = get_pattern()
# # new = st.session_state.get('_toAdd')
# # if new is not None:
# #     print('adding')
# #     cur += new
# print('cur:', cur)
# # print('new:', new)


# resp = code_editor(cur, key='code', snippets=['hello', 'hello world', 'oranges'], allow_reset=True, props={'wrapEnabled':True,}, )
# # print(resp['id'])
# # id = st.session_state.get('prevID')
# # if id is not None and id != resp['id']:
# #     print('resetting')
# #     st.session_state['_toAdd'] = ''
# #     st.session_state['prevID'] = resp['id']
# #     st.rerun()

# # st.session_state['prevID'] = resp['id']
# # code = resp['text']
# # print('response:', resp)
# # print('code in editor:', code)

# # if (end := st.session_state.get('code')):
# #     print('session state at end:', end['text'])

# print('resp:', resp['text'])
# print('query:', get_pattern())

if 'pattern' not in st.session_state:
    st.session_state.pattern = []

print(st.session_state)

elements = ['space', 'matchMax(args)', 'newline']

if st.session_state.get('_delete_manual'):
    st.session_state['manual'] = ''
    del st.session_state['_delete_manual']
#     default = ''
# else:
#     default = '' if (d := st.session_state.get('manual')) is None else d
# empty = st.empty()
string = st.text_input('manual text', key='manual')
pattern = st.session_state.pattern
if len(string):
    st.session_state.pattern = st.session_state.pattern + [string]
    # Empty the box
    st.session_state['_delete_manual'] = True
    st.rerun()
    # empty.empty()
# string = empty.text_input('manual text', key='manual2')

# def format(a):
    # print(a)
    # return a

from collections import Counter

def limit_duplicates(l):
    result = []
    for item in l:
        count = Counter(l)[item]
        if count <= 2:
            result.extend([item] * count)
        else:
            result.append(item)
    return result

pattern = st.multiselect('test', limit_duplicates(elements + st.session_state.pattern), key='pattern', default=pattern)

'Pattern'
pattern
'Options'
limit_duplicates(elements + st.session_state.pattern)
