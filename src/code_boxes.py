from code_editor import code_editor
import streamlit as st
from Cope.streamlit import ss

replacement_snippets = ''


def pattern_box(snippets):
    name = 'Enter EZRegex pattern:'
    default = ss.texts['tutorial']['defaultPattern']

    if ss.editor == 'Code Editor':
        st.markdown(name)

        prev_id = ss.code_pattern['id']

        resp = code_editor(default if ss.tutorial else (ss.code_pattern + ss.pattern_to_add),
            key='code_pattern',
            snippets=[snippets, ss.remove_snippets],
            focus=True,
            **ss.editor_kwargs
        )

        if prev_id != resp['id']:
            ss.pattern_to_add = ''
            st.rerun()

        pattern = resp['text']
        ss._pattern = pattern
    else:
        pattern = st.text_area(
            name,
            default if ss.tutorial else (ss._pattern + ss.pattern_to_add),
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
        resp = code_editor(default if ss.tutorial else (ss.code_replacement + ss.replacement_to_add),
            snippets=[replacement_snippets, snippetsRemove],
            key='replacement',
            **ss.editor_kwargs
        )

        if prev_id != resp['id']:
            ss.replacement_to_add = ''
            st.rerun()

        replacement = resp['text']
        ss._replacement = replacement
    else:
        replacement = st.text_area(
            name,
            default if ss.tutorial else (ss.get('replacement') or ""),
            key='replacement'
        )

    ss.pattern_to_add = ''

    return replacement
