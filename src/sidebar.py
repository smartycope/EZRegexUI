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
    cur = st.session_state[get]['text']

    if cur is None or not len(cur):
        newPart = input
    elif re.search((optional(' ') + anyof('+', '<<', '>>', '*') + optional(' ') + stringEnd).str(), cur) is not None:
        newPart = input
    # This is really cool, but doesn't really work anymore
    # elif (m := re.search((er.group('()') + ow + stringEnd).str(), cur)) is not None:
        # newPart = cur[:(-len(m.group())) + 1] + input + ')'
    else:
        newPart = ' + ' + input

    if get+'_toAdd' in st.session_state:
        st.session_state[get+'_toAdd'] += newPart
    else:
        st.session_state[get+'_toAdd'] = newPart

def _tutorial(key):
    if st.session_state.tutorial:
        st.caption(texts['tutorial'][key])


def sidebar(operatorText):
    snippets = ''
    with st.sidebar:
        # st.image(logo)#, width=103)
        left, right = st.columns(2)
        style = left.radio('Style', ['camelCase', 'snake_case'], horizontal=True)
        right.markdown('')
        tutorial = right.checkbox('Walkthrough', key='tutorial')

        st.header('Elements')
        _tutorial('sidebar')

        s = ''
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

        with st.expander('Operators'):
            st.markdown(operatorText)

    return snippets
