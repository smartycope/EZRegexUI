import re
import ezregex as er
from ezregex import *
import streamlit as st
import json as _json
from Cope.streamlit import ss

# ─── SETUP ──────────────────────────────────────────────────────────────────────
# Ensures that all the defaults are properly loaded
ss.setup(
    editor='Text Editor',
    # The raw text in the pattern box, code editor or no -- is the key of the text box
    _pattern='',
    pattern_to_add='',
    # The raw text in the replacement box, code editor or no -- is the key of the text box
    _replacement='',
    replacement_to_add='',
    # The raw response from the code box -- is the key of the code box
    code_replacement={'text':'', 'id':-1},
    # The raw response from the pattern code box -- is the key of the code box
    code_pattern={'text':'', 'id':-1},
    # The string in the string to match box -- is the key of the string box
    string='',
    editor_kwargs = dict(
        lang='python',
        theme='dark',
        height=(3, 10),
        allow_reset=True,
        props={'wrapEnabled':'true',},
        # focus=True,
    )
)


def _tutorial(key):
    if ss.tutorial:
        st.caption(ss.texts['tutorial'][key])
ss._tutorial = _tutorial

# Load ss with all the default values *before* we load all the functions and things
from src.functions import *
from src.code_boxes import *
from src.sidebar import *


# All the text is stored in here to make the code look better
# Only load once, for optimization
if ss.texts is None:
    with open('text.json', 'r') as f:
        ss.texts = _json.load(f)

if ss.remove_snippets is None:
    with open('snippetsRemove.txt', 'r') as f:
        ss.remove_snippets = f.read()


st.set_page_config(
    page_title='EZRegex',
    page_icon='./favicon.png',
    initial_sidebar_state='expanded',
    layout='wide',
    menu_items={
        'Get help': None,
        'Report a Bug': 'mailto:smartycope@gmail.com',
        'About': ss.texts['about']
    }
)


# ─── Sidebar ────────────────────────────────────────────────────────────────────
# Yes, the sidebar returns the snippets. It's only because it's already looping
# through all the EZRegex elements to make all the sidebar buttons, so while we're
# looping, we might as well piggyback and collect all the snippets too.
snippets = sidebar()


# ─── Page ───────────────────────────────────────────────────────────────────────
st.title('EZRegex')
st.caption(f"Copeland Carter | v{er.__version__}")

_tutorial('main')

left, right = st.columns([.85, .2])
right.button('Reload')
mode = left.radio('Mode',
    ['Search', 'Replace', 'Split'],
    captions=ss.texts['modeCaptions'] if ss.tutorial else None,
    horizontal=not ss.tutorial,
    index=0 if not ss.tutorial else 1,
    key='mode',
)


# ─── PATTERN BOX ────────────────────────────────────────────────────────────────
pattern = pattern_box(snippets)
_tutorial('pattern')


# ─── STRING INPUT BOX ───────────────────────────────────────────────────────────
string = st.text_area(
    'Enter string to match:',
    placeholder=ss.texts['stringPlaceholder'],
    value=ss.texts['tutorial']['defaultString'] if ss.tutorial else ss.string,
    key='string',
)
_tutorial('string')


# ─── REPLACEMENT PATTERN BOX ────────────────────────────────────────────────────
if mode == 'Replace':
    replacement = replace_box(snippets)
    _tutorial('replaceBox')

# ─── MATCHES ────────────────────────────────────────────────────────────────────
# Generate all the match stuff, if we can
if len(pattern):
    if (var := run_code(pattern)) is not None:
        # If it's just a string, make it an EZRegex type
        if type(var) is str:
            var = er.raw(var)

        # If there's nothing in the box of stuff to match, invert to genenerate something that would match
        if not len(string):
            try:
                string = var.invert()
            except:
                st.error("Can't invert that expression. Try providing a string to match instead.")

        # Get all the details
        data = var._matchJSON(string)

        st.divider()
        '### Looking for matches in:'

        # Display the match string html with groups all colored
        # double newline because markdown is weird like that
        st.markdown(data['stringHTML'].replace('\n', '\n\n'), True)
        _tutorial('matching')

        '### Using regex:'
        st.code(data['regex'], language='regex')
        _tutorial('regex')

        '### Matches:'
        _tutorial('matches')

        show_matches(data, mode)

        # The additional Replace and Split parts at the bottom
        if mode == 'Replace':
            st.divider()
            '### Replaced String:'
            _tutorial('replaced')

            st.code(re.sub(
                data['regex'],
                str(run_code(replacement)) if len(replacement) else '',
                string
            ).replace('\n', '\n\n'), language=None)

        elif mode == 'Split':
            st.divider()
            '### Split Parts:'
            _tutorial('split')
            parts = re.split(data['regex'], string)
            st.table(repr(i) for i in parts)
