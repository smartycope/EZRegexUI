import re
import ezregex as er
from ezregex import *
import streamlit as st
import json as _json
import builtins
from code_editor import code_editor
import inspect
from src.functions import *
from src.patternBox import *
from src.replaceBox import *
from src.sidebar import *

# ─── SETUP ──────────────────────────────────────────────────────────────────────
# print('-'*100)
logo = './favicon.png'

# All the text is stored in here to make the code look better
with open('text.json', 'r') as f:
    texts = _json.load(f)

def _tutorial(key):
    if st.session_state.tutorial:
        st.caption(texts['tutorial'][key])

st.set_page_config(
    page_title='EZRegex',
    page_icon=logo,
    initial_sidebar_state='expanded',
    layout='wide',
    menu_items={
        'Get help': None,
        'Report a Bug': 'mailto:smartycope@gmail.com',
        'About': texts['about']
    }
)

# Apparently this has to be here?
# Ensure there's *something* there so the code works
if "ezre" not in st.session_state:
    st.session_state.ezre = {'text':'', 'id':-1}


# ─── Page ───────────────────────────────────────────────────────────────────────
# left, right = st.columns([.5, 1])
# right.image(logo, width=103)
st.title('EZRegex')
st.caption(f"Copeland Carter | version {er.__version__}")

# Yes, the sidebar returns the snippets. It's only because it's already looping
# through all the EZRegex elements to make all the sidebar buttons, so while we're
# looping, we might as well piggyback and collect all the snippets too.
snippets = sidebar(texts['operators'])

_tutorial('main')
left, right = st.columns([.85, .2])
right.button('Reload')
mode = left.radio('Mode',
    ['Search', 'Replace', 'Split'],
    captions=texts['modeCaptions'] if st.session_state.tutorial else None,
    horizontal=not st.session_state.tutorial,
    index=0 if not st.session_state.tutorial else 1,
    key='mode',
)

# ─── PATTERN BOX ────────────────────────────────────────────────────────────────
st.markdown('Enter EZRegex pattern:')
pattern = patternBox(snippets, texts['tutorial']['defaultPattern'])
_tutorial('ezre')

# ─── STRING INPUT BOX ───────────────────────────────────────────────────────────
string = st.text_area(
    'Enter string to match:',
    key='string',
    placeholder=texts['stringPlaceholder'],
    value=texts['tutorial']['defaultString'] if st.session_state.tutorial else ''
)
_tutorial('string')

# ─── REPLACEMENT PATTERN BOX ────────────────────────────────────────────────────
if mode == 'Replace':
    st.markdown('Enter replacement EZRegex:')
    replacement = replaceBox(snippets, texts['tutorial']['defaultReplace'])
    _tutorial('replaceBox')

# ─── MATCHES ────────────────────────────────────────────────────────────────────
# Generate all the match stuff, if we can
if len(pattern):
    if (var := runCode(pattern)) is not None:
        if not len(string):
            try:
                string = var.invert()
            except:
                st.error("Can't invert that expression. Try providing a string to match instead.")
        data = var._matchJSON(string)

        st.divider()
        st.markdown('### Looking for matches in:')

        # Display the match string html with groups all colored
        # double newline because markdown is weird like that
        st.markdown(data['stringHTML'].replace('\n', '\n\n'), True)
        _tutorial('matching')

        st.markdown('### Using regex:')
        st.code(data['regex'], language='regex')
        _tutorial('regex')

        st.markdown('### Matches:')
        _tutorial('matches')

        showMatches(data, texts['tutorial']['groups'])

        # The additional Replace and Split parts at the bottom
        if mode == 'Replace':
            st.divider()
            st.markdown('### Replaced String:')
            _tutorial('replaced')

            st.code(re.sub(
                data['regex'],
                str(runCode(replacement)) if len(replacement) else '',
                string
            ).replace('\n', '\n\n'), language=None)

        elif mode == 'Split':
            st.divider()
            st.markdown('### Split Parts:')
            _tutorial('split')
            parts = re.split(data['regex'], string)
            # for part in parts:
                # st.markdown(part)
            st.table(repr(i) for i in parts)
