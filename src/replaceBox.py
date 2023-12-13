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
replacement_snippets = ''

with open('snippetsRemove.txt', 'r') as f:
    snippetsRemove = f.read()

# Ensure there's *something* there so the code works
if "replacement" not in st.session_state:
    st.session_state.replacement = {'text':'', 'id':-1}


def replaceBox(snippets, defaultText):
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

    return replacement
