from code_editor import code_editor
import streamlit as st
from Cope.streamlit import ss
from Cope import debug
from ezregex import generate_regex
replacement_snippets = ''


def pattern_box(snippets):
    name = 'Enter EZRegex pattern:'
    default = ss.texts['tutorial']['defaultPattern']

    if ss.editor == 'Code Editor':
        st.markdown(name)

        prev_id = ss.code_pattern['id']

        # new = ss.code_pattern['text'] + ss.pattern_to_add
        new = (ss.cur_pattern or "") + ss.pattern_to_add
        print("current pattern is", ss.cur_pattern)
        resp = code_editor(default if ss.tutorial else new,
            snippets=[snippets, ss.remove_snippets],
            focus=True,
            key='code_pattern',
            **ss.editor_kwargs
        )

        if prev_id != resp['id']:
            print('rerunning')
            ss.pattern_to_add = ''
            st.rerun()

        # pattern = resp['text']
        # Don't bother getting the text from the box, get the text it's supposed to be
        pattern = new
        ss._pattern = pattern
        # print('pattern is', ss._pattern)

    elif ss.editor == 'Text Editor':
        ss._pattern = default if ss.tutorial else (ss._pattern + ss.pattern_to_add)
        pattern = st.text_area(
            label=name,
            key='_pattern'
        )
    # Make the data editor to put in things that are supposed to match and not match
    else:
        pattern = ''
        with st.form('_generation_form'):
            names = ('Strings That Should Match', 'Strings That Shouldn\'t Match')

            data = st.data_editor(
                # ss.data,
                [['', '']]*3,
                hide_index=True,
                use_container_width=True,
                column_config={str(cnt): st.column_config.TextColumn(default='', label=names[cnt]) for cnt in range(2)},
                num_rows='dynamic',
                key='_data'
            )

            if st.form_submit_button('Generate'):
                winners = []
                losers = []
                for w, l in data:
                    winners.append(w)
                    losers.append(l)

                # Add the raw, so it works nicely with the rest of our existing code
                pattern = 'raw("' + generate_regex(winners, losers, ss.gen_calls, ss.gen_restarts, ss.gen_chunk) + '")'


    ss.pattern_to_add = ''

    if ss.tutorial:
        return default

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
    # elif ss.editor == 'Text Editor'
    else:
        ss._replacement = default if ss.tutorial else (ss._replacement + ss.replacement_to_add)
        replacement = st.text_area(
            label=name,
            key='_replacement'
        )

    ss.replacement_to_add = ''

    if ss.tutorial:
        return default

    return replacement
