import re
import ezregex as er
from ezregex import *
import streamlit as st
import json as _json
import inspect
from src.functions import snippify, camel2snake
from Cope.streamlit import ss


# Function for adding side bar elements to pattern when they're clicked
def add_part(input, add_to_replace_box=False):
    # If there's parameters, remove them. They can reference the side panel.
    input = re.sub(str('(' + matchMax(anything + optional(er.group(comma))) + ')'), '()', input)

    get = 'replacement' if add_to_replace_box else 'pattern'

    # Actually get it from the session state
    cur = ss[f'_{get}']

    # Figure out what needs to be added exactly
    if cur is None or not len(cur):
        to_add = input
    elif re.search((optional(' ') + anyof('+', '<<', '>>', '*') + optional(' ') + stringEnd).str(), cur) is not None:
        to_add = input
    # This doesn't really work with the Code editor
    elif ss.editor == 'Text Editor' and (m := re.search((er.group('()') + ow + stringEnd).str(), cur)) is not None:
        # We can do this here because this if block is only used if we're using the text editor
        # ss._pattern = ss._pattern[:-1]
        ss[f'_{get}'] = ss[f'_{get}'][:-1]
        to_add = cur[(-len(m.group()))+1:(-len(m.group()))+2] + input + ')'
    else:
        to_add = ' + ' + input

    # Set it to be added
    # if ss['_text_editor'] == 'Code Editor':
    #     if get+'_toAdd' in ss:
    #         ss[get+'_toAdd'] += to_add
    #     else:
    #         ss[get+'_toAdd'] = to_add

    # else:
    # ss.pattern += to_add
    ss[f'{get}_to_add'] += to_add


def resolve_current_text():
    raise NotImplementedError('TODO')
    """ If we're switching between text box types, make sure the current text isn't lost """
    replacement = '' if (r := ss.get('replacement')) else r
    if ss['_text_editor'] == 'Code Editor':
        # We're switching from text editor to Code editor
        ss.pattern = {'text':ss.pattern, 'id':-1}
        ss.replacement = {'text':replacement, 'id':-1}
    else:
        # We're switching from Code ekditor to text editor
        ss.pattern = ss.pattern['text']
        # If we haven't changed anything since we forcefully made it a string, don't change it again
        if 'replacement' in ss and type(replacement) is dict:
            ss.replacement = replacement['text']
        # Causes niche errors if we don't do this
        if 'replacement_toAdd' in ss:
            del ss['replacement_toAdd']

    params = st.experimental_get_query_params()
    # print(params)
    # TODO: This is very inelegant. Fix this.
    if 'editor' not in params:
        params['editor'] = [ss['_text_editor'].split(' ')[0].lower()]
    else:
        try:
            params['editor'][0] = ss['_text_editor'].split(' ')[0].lower()
        except IndexError:
            params['editor'] = [ss['_text_editor'].split(' ')[0].lower()]

    st.experimental_set_query_params(**params)

# Because strings are preserved, we have to reset these on going out of tutorial mode
def erase_current_strings():
    if not ss.tutorial:
        ss.reset()

def sidebar():
    snippets = ''
    with st.sidebar:
        st.image('./favicon.png')
        left, right = st.columns(2)
        style = left.radio('Style', ['camelCase', 'snake_case'], horizontal=True, index=1)
        right.markdown('')
        right.checkbox('Walkthrough', key='tutorial', on_change=erase_current_strings)

        st.header('Elements')
        ss._tutorial('sidebar')

        s = ''
        # Add all the buttons
        for groupName, elements in er.__groups__.items():
            with st.expander(groupName.title()):
                # Add the optional group description
                if groupName in er.__docs__['groups_docs']:
                    st.caption(er.__docs__['groups_docs'][groupName])

                for element in elements:
                    if element in er.__docs__:
                        help = er.__docs__[element]
                    else:
                        help = None

                    name = element
                    if style == 'snake_case' and groupName != 'flags':
                        name = camel2snake(element)

                    # Now that we made the buttons, while we're here, also make the snippets
                    snip = f'snippet {name}\n\t{snippify(name)}\n'
                    snippets += snip

                    actual = globals()[element]
                    if type(actual) is not EZRegex:
                        sig = inspect.signature(actual)
                        name += '(' + ', '.join(p.name for p in sig.parameters.values()) + ')'

                    st.button(name, on_click=add_part, args=(name, groupName == 'replacement'), help=help)

                    if ss.tutorial and help is not None:
                        st.caption(help)

        # Add the operators section
        with st.expander('Operators'):
            st.markdown(ss.texts['operators'])

        # Add a settings section
        with st.expander('Settings'):
            st.radio('Text Boxes', ('Code Editor', 'Text Editor'), help=ss.texts['settings']['textBoxes'], key='editor', on_change=resolve_current_text)

    return snippets
