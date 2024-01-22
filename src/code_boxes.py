from code_editor import code_editor
import streamlit as st
from Cope.streamlit import ss
from Cope import debug
replacement_snippets = ''


def pattern_box(snippets):
    name = 'Enter EZRegex pattern:'
    default = ss.texts['tutorial']['defaultPattern']

    if ss.editor == 'Code Editor':
        st.markdown(name)

        prev_id = ss.code_pattern['id']

        resp = code_editor(default if ss.tutorial else (ss.code_pattern['text'] + ss.pattern_to_add),
            snippets=[snippets, ss.remove_snippets],
            focus=True,
            key='code_pattern',
            **ss.editor_kwargs
        )

        if prev_id != resp['id']:
            ss.pattern_to_add = ''
            st.rerun()

        pattern = resp['text']
        ss._pattern = pattern
    else:
        ss._pattern = default if ss.tutorial else (ss._pattern + ss.pattern_to_add)
        pattern = st.text_area(
            label=name,
            key='_pattern'
        )

    ss.pattern_to_add = ''

    return pattern


def replace_box(snippets):
    name = 'Enter replacement EZRegex:'
    default = ss.texts['tutorial']['defaultReplace']

    if ss.editor == 'Code Editor':
        st.markdown(name)

        prev_id = ss.code_replacement['id']
        resp = code_editor(default if ss.tutorial else (ss.code_replacement['text'] + ss.replacement_to_add),
            snippets=[replacement_snippets, ss.remove_snippets],
            key='code_replacement',
            **ss.editor_kwargs
        )

        if prev_id != resp['id']:
            ss.replacement_to_add = ''
            st.rerun()

        replacement = resp['text']
        ss._replacement = replacement
    else:
        ss._replacement = default if ss.tutorial else (ss._replacement + ss.replacement_to_add)
        replacement = st.text_area(
            label=name,
            key='_replacement'
        )

    ss.replacement_to_add = ''

    return replacement
