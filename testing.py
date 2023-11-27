import streamlit as st
import code_editor as _code_editor
from code_editor import code_editor
import random

# st.session_state['code'] = st.session_state['code']
# id = st.session_state.get('code')
print('-'*100)

if (beg := st.session_state.get('code')):
    print('session state at beginning:', beg['text'])
# if 'code' in st.session_state:
# print(st.session_state.get('code'))



def doThing():
    print('doing thing')
    # code += ' + thing!'
    if '_toAdd' in st.session_state:
        st.session_state['_toAdd'] += ' + thing!'
    else:
        st.session_state['_toAdd'] = ' + thing!'
    # st.rerun()
    # if st.session_state.get('code') is not None:
        # print('getting state')
        # st.session_state['code']['text'] += ' + thing!'
        # st.session_state['code']['id'] = str(random.randbytes(8))

st.button('add thing!', on_click=doThing)

cur = st.session_state['code']['text'] if st.session_state.get('code') is not None else ''
new = st.session_state.get('_toAdd')
if new is not None:
    print('adding')
    cur += new
    # st.session_state['_toAdd'] = ''
print('cur:', cur)
print('new:', new)
# with st.form('form'):


# if id is not None:
    # print(id['id'])
resp = code_editor(cur, key='code', snippets=['hello', 'hello world', 'oranges'], allow_reset=True, props={'wrapEnabled':True,})
print(resp['id'])
id = st.session_state.get('prevID')
if id is not None and id != resp['id']:
    print('resetting')
    st.session_state['_toAdd'] = ''
    st.session_state['prevID'] = resp['id']
    st.rerun()

st.session_state['prevID'] = resp['id']
# submitted = st.form_submit_button("Submit")
code = resp['text']
print('response:', resp)
print('code in editor:', code)

if (end := st.session_state.get('code')):
    print('session state at end:', end['text'])
    # print('session state at end:', end)

# print(_code_editor.components.)
# print(st.session_state)
# print(st._cache_data)
