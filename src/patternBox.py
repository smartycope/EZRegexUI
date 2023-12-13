import re
import ezregex as er
from ezregex import *
import streamlit as st
import json as _json
import builtins
from code_editor import code_editor
import inspect

editorArgs = dict(
    lang='python',
    theme='dark',
    height=(3, 10),
    allow_reset=True,
    props={'wrapEnabled':'true',},
    # focus=True,
)

# replacement_snippets = ''



with open('snippetsRemove.txt', 'r') as f:
    snippetsRemove = f.read()

def patternBox(snippets, defaultText):
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
    if id is not None and id != resp['id']:
        st.session_state['ezre_toAdd'] = ''
        st.session_state['ezre_prevID'] = resp['id']
        st.rerun()

    st.session_state['ezre_prevID'] = resp['id']

    return ezre
