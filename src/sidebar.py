import re
import ezregex as er
from ezregex import *
import streamlit as st
import json as _json
import builtins
from code_editor import code_editor
import inspect
from src.functions import snippify, camel2snake
# from src.functions import tutorial as _tutorial

logo = './favicon.png'

# All the text is stored in here to make the code look better
with open('text.json', 'r') as f:
    texts = _json.load(f)

# Function for adding side bar elements to ezre when they're clicked
def addPart(input, _replace=False):
    global replace, replacement
    # If there's parameters, remove them. They can reference the side panel.
    input = re.sub(str('(' + matchMax(anything + optional(er.group(comma))) + ')'), '()', input)
    get = 'ezre'
    if _replace:
        st.session_state['replace_mode'] = True
        replace = True
        get = 'replacement'

    # Actually get it from the session state
    if st.session_state['_text_editor'] == 'Code Editor':
        cur = st.session_state[get]['text']
    else:
        cur = st.session_state[get]

    # Figure out what needs to be added exactly
    if cur is None or not len(cur):
        newPart = input
    elif re.search((optional(' ') + anyof('+', '<<', '>>', '*') + optional(' ') + stringEnd).str(), cur) is not None:
        newPart = input
    # This doesn't really work with the Code editor
    elif st.session_state['_text_editor'] == 'Text Editor' and (m := re.search((er.group('()') + ow + stringEnd).str(), cur)) is not None:
        # We can do this here because this if block is only used if we're using the text editor
        st.session_state.ezre = st.session_state.ezre[:-1]
        newPart = cur[(-len(m.group()))+1:(-len(m.group()))+2] + input + ')'
    else:
        newPart = ' + ' + input

    # Set it to be added
    if st.session_state['_text_editor'] == 'Code Editor':
        if get+'_toAdd' in st.session_state:
            st.session_state[get+'_toAdd'] += newPart
        else:
            st.session_state[get+'_toAdd'] = newPart
    else:
        st.session_state.ezre += newPart

def _tutorial(key):
    if st.session_state.tutorial:
        st.caption(texts['tutorial'][key])

def resolve_current_text():
    """ If we're switching between text box types, make sure the current text isn't lost """
    if st.session_state['_text_editor'] == 'Code Editor':
        # We're switching from text editor to Code editor
        st.session_state.ezre = {'text':st.session_state.ezre, 'id':-1}
        st.session_state.replacement = {'text':st.session_state.replacement, 'id':-1}
    else:
        # We're switching from Code editor to text editor
        st.session_state.ezre = st.session_state.ezre['text']
        # If we haven't changed anything since we forcefully made it a string, don't change it again
        if 'replacement' in st.session_state and type(st.session_state.replacement) is dict:
            st.session_state.replacement = st.session_state.replacement['text']
        # Causes niche errors if we don't do this
        if 'replacement_toAdd' in st.session_state:
            del st.session_state['replacement_toAdd']

    params = st.experimental_get_query_params()
    params['editor'][0] = st.session_state['_text_editor'].split(' ')[0].lower()
    st.experimental_set_query_params(**params)


def sidebar(operatorText, settingsTexts):
    snippets = ''
    with st.sidebar:
        st.image(logo, )
        left, right = st.columns(2)
        style = left.radio('Style', ['camelCase', 'snake_case'], horizontal=True)
        right.markdown('')
        tutorial = right.checkbox('Walkthrough', key='tutorial')

        st.header('Elements')
        _tutorial('sidebar')

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

                    kwargs = {'_replace': True} if groupName == 'replacement' else {}
                    st.button(name, on_click=addPart, args=(name,), kwargs=kwargs, help=help)

                    if tutorial and help is not None:
                        st.caption(help)

        # Add the operators section
        with st.expander('Operators'):
            st.markdown(operatorText)

        # Add a settings section
        with st.expander('Settings'):
            st.radio('Text Boxes', ('Code Editor', 'Text Editor'), help=settingsTexts['textBoxes'], key='_text_editor', on_change=resolve_current_text)

    return snippets
