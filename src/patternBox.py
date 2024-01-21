from code_editor import code_editor
import streamlit as st

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
        pattern = st.session_state['pattern']['text'] if 'pattern' in st.session_state else ''
        new = st.session_state.get('pattern_toAdd')
        if new is not None:
            pattern += new
        if st.session_state.tutorial:
            pattern = defaultText

        # snippetsRemove = [
        #     {'name':'None'},
        # ]

        resp = code_editor(pattern,
            key='pattern',
            snippets=[snippets, snippetsRemove],
            focus=True,
            **editorArgs
        )
        id = st.session_state.get('pattern_prevID')
        print(resp)
        print(new)
        print(pattern)
        if id is not None and id != resp['id']:
            st.session_state['pattern_toAdd'] = ''
            st.session_state['pattern_prevID'] = resp['id']
            st.rerun()

        st.session_state['pattern_prevID'] = resp['id']
    else:
        pattern = st.text_area(name, value=defaultText if st.session_state.tutorial else "", key='pattern')

    # TODO: remove this, this is a backup saftey measure
    if type(pattern) is dict:
        pattern = pattern['text']

    return pattern
