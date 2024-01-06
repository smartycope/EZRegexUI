import streamlit as st
from code_editor import code_editor

editorArgs = dict(
    lang='python',
    theme='dark',
    height=(3, 10),
    allow_reset=True,
    props={'wrapEnabled':'true',},
    # focus=True,
)
replacement_snippets = ''

with open('snippetsRemove.txt', 'r') as f:
    snippetsRemove = f.read()

# Ensure there's *something* there so the code works
# TODO: This section is copied from main.py. It should be in either one or the other
default_editor = 'Code Editor'
if 'replacement' not in st.session_state:
    if st.experimental_get_query_params().get('editor') is None:
        st.session_state.ezre = {'text':'', 'id':-1}  if default_editor == 'Code Editor' else ''
    elif st.experimental_get_query_params().get('editor') == 'text' or st.experimental_get_query_params().get('editor')[0] == 'text':
        st.session_state.ezre = ''
    else:
        st.session_state.ezre = {'text':'', 'id':-1}



def replaceBox(snippets, defaultText):
    name = 'Enter replacement EZRegex:'
    if st.session_state['_text_editor'] == 'Code Editor':
        st.markdown(name)

        replacement = st.session_state['replacement']['text'] if 'replacement' in st.session_state else ''
        new = st.session_state.get('replacement_toAdd')
        if new is not None:
            replacement += new
        if st.session_state.tutorial:
            replacement = defaultText

        resp = code_editor(replacement,
            key='replacement',
            snippets=[replacement_snippets, snippetsRemove],
            **editorArgs
        )
        id = st.session_state.get('replacement_prevID')
        if id is not None and id != resp['id']:
            st.session_state['replacement_toAdd'] = ''
            st.session_state['replacement_prevID'] = resp['id']
            st.rerun()

        st.session_state['replacement_prevID'] = resp['id']

    else:
        replacement = st.text_area(name, defaultText if st.session_state.tutorial else "", key='replacement')

    # TODO: remove this, this is a backup saftey measure
    if type(replacement) is dict:
        replacement = replacement['text']

    return replacement
