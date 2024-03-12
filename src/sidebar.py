import re
import ezregex as er
from ezregex import *
import streamlit as st
import json as _json
import inspect
from src.functions import snippify, camel2snake
from Cope.streamlit import ss

# from streamlit_javascript import st_javascript
from time import time as now
from streamlit_local_storage import LocalStorage
import streamlit.components.v1 as components


# Function for adding side bar elements to pattern when they're clicked
def add_part(input, add_to_replace_box=False):
    # If there's parameters, remove them. They can reference the side panel.
    input = re.sub(str('(' + matchMax(anything + optional(er.group(comma))) + ')'), '()', input)

    get = 'replacement' if add_to_replace_box else 'pattern'
    components.html("""
    <script>
    const doc = window.parent.document;
    const iframes = Array.from(doc.querySelectorAll("iframe"));
    const ace_layers = Array.from(iframes.find((e) => e.title === "code_editor.code_editor").contentDocument.getElementsByClassName("ace_layer"));
    const element = ace_layers.find((e) => e.classList.value === "ace_layer ace_text-layer");
    localStorage.setItem("_tmp", JSON.stringify(element.innerText));
    console.log('Loaded');
    </script>
    """,
        height=0,
        width=0,
    )
    ss.cur_pattern = LocalStorage().getItem('_tmp', .1)
    print(ss.cur_pattern)

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
    """ If we're switching between text box types, make sure the current text isn't lost """
    replacement = '' if (r := ss.get('replacement')) else r
    # We're switching from text editor to Code editor
    if ss.editor == 'Code Editor':
        ss.code_pattern = {'text':ss._pattern, 'id':-1}
        ss.code_replacement = {'text':ss._replacement, 'id':-1}
    else:
        # We're switching from Code ekditor to text editor
        ss._pattern = ss.code_pattern['text']
        ss._replacement = ss.code_replacement['text']
        # If we haven't changed anything since we forcefully made it a string, don't change it again
        # if 'replacement' in ss and type(replacement) is dict:
            # ss.replacement = replacement['text']
        # Causes niche errors if we don't do this
        # if 'replacement_toAdd' in ss:
            # del ss['replacement_toAdd']

    # params = st.experimental_get_query_params()
    # print(params)
    # # TODO: This is very inelegant. Fix this.
    # if 'editor' not in params:
    #     params['editor'] = [ss['_text_editor'].split(' ')[0].lower()]
    # else:
    #     try:
    #         params['editor'][0] = ss['_text_editor'].split(' ')[0].lower()
    #     except IndexError:
    #         params['editor'] = [ss['_text_editor'].split(' ')[0].lower()]

    # st.experimental_set_query_params(**params)

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
            editor = st.radio(
                'Text Boxes',
                ('Code Editor', 'Text Editor', 'Auto-Generate'),
                help=ss.texts['settings']['textBoxes'],
                key='editor',
                on_change=resolve_current_text
            )

            if editor == 'Auto-Generate':
                st.number_input('Calls', 1, None, 1000, 50, key='gen_calls', help=ss.texts['settings']['gen_calls'])
                st.number_input('Restarts', 1, 50, 3, 1, key='gen_restarts', help=ss.texts['settings']['gen_restarts'])
                st.number_input('Chunk Size', 2, 20, 5, 1, key='gen_chunk',  help=ss.texts['settings']['gen_chunk'])

        if ss.editor == 'Code Editor':
            # Apparently, these work in the sidebar. They're here, becuase they create some useless
            # vertical whitespace, and this way it just creates it at the bottom of the sidebar.

            # This exits out of the iframe document that streamlit-javascript puts around code,
            # then searches for iframes which hold documents (which is what the code box is in),
            # gets the one for the code box, and then searches for the div element inside that
            # that stores the code, and then gets the innerText from that and stores it in localStorage.
            # st_javascript("""localStorage.setItem("_tmp",
            #     JSON.stringify(Array.from( Array.from(window.frameElement.getRootNode().querySelectorAll("iframe")).find((e) => e.title === "code_editor.code_editor").contentDocument.getElementsByClassName("ace_layer")).find((e) => e.classList.value === "ace_layer ace_text-layer").innerText)
            # )""", key=now())



            # This uses a *seperate* library (cause streamlit-javascript bugged out on me repeatedly)
            # to get the value we just stored in localStorage
            # ss.cur_pattern = LocalStorage().getItem('_tmp', .1)

            # These are just because for some reason, it runs twice when the Submit button is pressed.
            # This just removes the first one and just uses the second one (because the first one
            # is outdated). Note that this occasionally doesn't run, but only if the input hasn't
            # changed, so it's okay, and occasionally runs twice, which is actually okay.
            # TODO refix this
            # ss._disable_run = not ss._disable_run

            print('----', ss.cur_pattern)

    return snippets
