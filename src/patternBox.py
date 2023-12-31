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

with open('snippetsRemove.txt', 'r') as f:
    snippetsRemove = f.read()

def patternBox(snippets, defaultText):
    name = 'Enter EZRegex pattern:'
    if st.session_state['_text_editor'] == 'Code Editor':
        st.markdown(name)
        ezre = st.session_state['ezre']['text'] if 'ezre' in st.session_state else ''
        new = st.session_state.get('ezre_toAdd')
        if new is not None:
            ezre += new
        if st.session_state.tutorial:
            ezre = defaultText

        # snippetsRemove = [
        #     {'name':'None'},
        # ]

        resp = code_editor(ezre,
            key='ezre',
            snippets=[snippets, snippetsRemove],
            focus=True,
            **editorArgs
        )
        id = st.session_state.get('ezre_prevID')
        print(resp)
        print(new)
        print(ezre)
        if id is not None and id != resp['id']:
            st.session_state['ezre_toAdd'] = ''
            st.session_state['ezre_prevID'] = resp['id']
            st.rerun()

        st.session_state['ezre_prevID'] = resp['id']
    else:
        ezre = st.text_area(name, value=defaultText if st.session_state.tutorial else "", key='ezre')

    # TODO: remove this, this is a backup saftey measure
    if type(ezre) is dict:
        ezre = ezre['text']

    return ezre
