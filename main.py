import re
import ezregex as er
from ezregex import *
import streamlit as st
import json as _json
import builtins
from code_editor import code_editor
import inspect

# ─── TODO ───────────────────────────────────────────────────────────────────────
# groups are sequential within each match, (I think), they should be sequential globally
# Make group have a default named parameter instead of 2 seperate functions
# Figure out how to add the icon to GitHub Pages
# Make the buttons add at the cursor index, not at the end (or an option to)
# Option for which method of inverting we use
# Add a run button in the pattern box for mobile
# Penultimate lines ending in \ will break
# Add a code box holding the replacement regex as well
# Replacement box just disappears after you submit the ezre pattern
# add settings for inverting
# I think latex breaks on underscores
# Remove snippets
# add icon somewhere on page
# Somehow add a button which generates n number of example matches
# Add some sort of not found box if seach fails

# ─── SETUP ──────────────────────────────────────────────────────────────────────
# print('-'*100)
logo = './favicon.png'
snippets = ''
replacement_snippets = ''
# For exec globals
input = ''
editorArgs = dict(
    lang='python',
    theme='dark',
    height=(3, 10),
    allow_reset=True,
    props={'wrapEnabled':'true',},
    # focus=True,
)

# Ensure there's *something* there so the code works
if "ezre" not in st.session_state:
    st.session_state.ezre = {'text':'', 'id':-1}
if "replacement" not in st.session_state:
    st.session_state.replacement = {'text':'', 'id':-1}

# All the text is stored in here to make the code look better
with open('text.json', 'r') as f:
    texts = _json.load(f)

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

# ─── FUNCTIONS ──────────────────────────────────────────────────────────────────
# One less dependancy
def rgbToHex(rgb):
    return f'#{int(rgb[0]):02x}{int(rgb[1]):02x}{int(rgb[2]):02x}'

def invertColor(rgba):
    return tuple(255 - c for c in rgba)

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

# Make LaTeX happy
def escape(s):
    s = re.escape(s)
    s = re.sub(r'\\-', '-', s)
    s = re.sub(r'\\\(', '(', s)
    s = re.sub(r'\\\)', ')', s)
    s = re.sub(r'\\\?', '?', s)
    # s = re.sub(r'$', r'\$', s)
    # s = re.sub(r'$', '\$', s)
    return s.strip()

def formatInput2code(s):
    # keywords = set(dir(builtins) + dir(er) + re.findall((lineStart + group(word) + ifFollowedBy(ow + '=')).str(), s))
    # print(anyExcept(anyof(*keywords), type='.*'))
    # s = re.sub((anyExcept('literal', type='.*')).str(), '"' + replace_entire.str() + '"', s)
    lines = s.splitlines()
    # Remove the last lines which are actually comments
    while s.splitlines()[-1].strip().startswith('#'):
        lines.pop(-1)
    # Insert the variable assignment to the last line
    lines.append('\n_rtn = '  + lines.pop(-1))
    return '\n'.join(lines)

def _tutorial(key):
    if tutorial:
        st.caption(texts['tutorial'][key])

def camel2snake(camel):
    mach = re.sub((group(lowercase) + group(uppercase)).str(), (rgroup(1) + '_' + rgroup(2)).str(), camel)
    if mach is None:
        return camel
    else:
        return mach.lower()

def snippify(func:str):
    element = globals()[func]
    # If this is true, it's a basic singleton without parameters
    if type(element) is EZRegex:
        return func
    else:
        sig = inspect.signature(element)
        rtn = func + '(' + ', '.join('${' + str(cnt+1) + ':' + p.name + '}' for cnt, p in enumerate(sig.parameters.values()) if p.default == inspect._empty) + ')' + '$0'
        return rtn

# ─── Page ───────────────────────────────────────────────────────────────────────
# The actual page
# left, right = st.columns([.09, 1])
# left.image(logo, width=103)
st.title('EZRegex')
st.caption(f"Copeland Carter | version {er.__version__}")

# ─── SIDEBAR ────────────────────────────────────────────────────────────────────
# Add all the side bar elements
with st.sidebar:
    left, right = st.columns(2)
    style = left.radio('Style', ['camelCase', 'snake_case'], horizontal=True)
    right.markdown('')
    tutorial = right.checkbox('Walkthrough')

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
        st.markdown(texts['operators'])

# ─── MAIN PAGE ──────────────────────────────────────────────────────────────────
_tutorial('main')
left, right = st.columns([.85, .2])
right.button('Reload')
# replace = left.checkbox('Replacement Mode', key='replace_mode', value=tutorial)
mode = left.radio('Mode',
    ['Search', 'Replace', 'Split'],
    captions=texts['modeCaptions'] if tutorial else None,
    horizontal=not tutorial,
    index=0 if not tutorial else 1,
    key='mode',
)

# ─── PATTERN BOX ────────────────────────────────────────────────────────────────
st.markdown('Enter EZRegex pattern:')
ezre = st.session_state['ezre']['text'] if 'ezre' in st.session_state else ''
new = st.session_state.get('ezre_toAdd')
if new is not None:
    ezre += new
if tutorial:
    ezre = texts['tutorial']['defaultPattern']

snippetsRemove = ''
resp = code_editor(ezre,
    key='ezre',
    snippets=[snippets, snippetsRemove],
    **editorArgs
)
id = st.session_state.get('ezre_prevID')
if id is not None and id != resp['id']:
    st.session_state['ezre_toAdd'] = ''
    st.session_state['ezre_prevID'] = resp['id']
    st.rerun()

st.session_state['ezre_prevID'] = resp['id']
_tutorial('ezre')

# ─── STRING INPUT BOX ───────────────────────────────────────────────────────────
placeholder = st.empty()
string = placeholder.text_area(
    'Enter string to match:',
    key='string',
    placeholder=texts['stringPlaceholder'],
    value=texts['tutorial']['defaultString'] if tutorial else ''
)
_tutorial('string')

# replacementPlaceholder = st.empty()
# tutorialReplacementPlaceholder = st.empty()

# ─── REPLACEMENT PATTERN BOX ────────────────────────────────────────────────────
# with replacementPlaceholder:
if mode == 'Replace':
    st.markdown('Enter replacement EZRegex:')
    replacement = st.session_state['replacement']['text'] if 'replacement' in st.session_state else ''
    new = st.session_state.get('replacement_toAdd')
    if new is not None:
        replacement += new
    if tutorial:
        replacement = texts['tutorial']['defaultReplace']

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

    _tutorial('replaceBox')

# print(f'mode: {mode}')
# If it's in the wrong mode, erase the box we just made.
# if mode != 'Replace':
    # print('erasing')
    # replacementPlaceholder.empty()
# elif tutorial:
    # tutorialReplacementPlaceholder.caption(texts['tutorial']['replaceBox'])

# ezre = st.session_state.ezre['text']
# replacement = st.session_state.replacement['text']
# Generate all the match stuff, if we can
if len(ezre):
    successful = False
    # Run the code, get the var, and get the JSON search info
    # Set the variable before the end of the last line so we can do variables in the text_area
    try:
        local = {}
        exec(formatInput2code(ezre), globals(), local)
        var = local['_rtn']
        if not len(string):
            try:
                string = var.invert()
            except:
                st.error("Can't invert that expression. Try providing a string to match instead.")
        json = var._matchJSON(string)
    except TypeError as err:
        st.error('Invalid parameters in EZRegex pattern:')
        st.exception(err.with_traceback(None))
    except SyntaxError as err:
        st.error('Invalid syntax in EZRegex pattern:')
        st.exception(err.with_traceback(None))
    except Exception as err:
        st.exception(err.with_traceback(None))
    else:
        successful = True

    if successful:
        st.divider()

        # left, right = st.columns([.85, .15])
        st.markdown('### Looking for matches in:')

        # Display the match string html with groups all colored
        # double newline because markdown is weird like that
        st.markdown(json['stringHTML'].replace('\n', '\n\n'), True)
        _tutorial('matching')

        st.markdown('### Using regex:')
        st.code(json['regex'], language='regex')
        _tutorial('regex')

        st.markdown('### Matches:')
        _tutorial('matches')
        for match in json['matches']:
            # st.markdown(f"""
                # <style>
                # div[data-testid="stExpander"] div[role="button"] p {{
                #     color: {match['match']['color']};
                # }}
                # </style>
            # """, unsafe_allow_html=True)

            # We're using latex here because for SOME reason expanders support named colors, but NOT arbitrary colors
            if '$' in match['match']['string']:
                # Apparently, there's no way to escape a $ that I can find
                latex = f'{escape(match["match"]["string"])} ({match["match"]["start"]}:{match["match"]["end"]})'
            else:
                latex = f'$\\text{{\\color{{{match["match"]["color"]}}}{escape(match["match"]["string"])}}} \\textit{{({match["match"]["start"]}:{match["match"]["end"]})}}$'
            fold = st.expander(latex, (len(json['matches']) == 1) and mode != 'Replace')

            if not len(match['unnamedGroups']) and not len(match['namedGroups']):
                fold.markdown('No groups captured')
                break

            if tutorial:
                fold.caption(texts['tutorial']['groups'])

            if len(match['unnamedGroups']):
                fold.markdown('#### Unnamed Groups')

            for cnt, group in enumerate(match['unnamedGroups']):
                inverse = rgbToHex(invertColor([int(c, base=16) for c in match['match']['color'][1::2]]))
                fold.markdown(f'''
                    {cnt+1}: <span style="background-color: {group["color"]}; color: {inverse};">{group["string"]}</span>
                    <span style="color: white; font-style: italic;"> ({group["start"]}:{group["end"]})</span>
                ''', True)

            if len(match['namedGroups']):
                fold.markdown('#### Named Groups')
            for name, group in match['namedGroups'].items():
                inverse = rgbToHex(invertColor([int(c, base=16) for c in match['match']['color'][1::2]]))
                fold.markdown(f'''
                    {name}: <span style="background-color: {group["color"]}; color: {inverse};">{group["string"]}</span>
                    <span style="color: white; font-style: italic;"> ({group["start"]}:{group["end"]})</span>
                ''', True)
        # The additional Replace and Split parts at the bottom
        if mode == 'Replace':
            st.divider()
            st.markdown('### Replaced String:')
            _tutorial('replaced')
            try:
                if len(replacement):
                    local = {}
                    exec(formatInput2code(replacement), globals(), local)
                    repl = local['_rtn']
                else:
                    repl = ''
                st.code(re.sub(json['regex'], str(repl), string).replace('\n', '\n\n'), language=None)
            except TypeError as err:
                st.error('Invalid parameters in replacement pattern:')
                st.exception(err.with_traceback(None))
            except SyntaxError as err:
                st.error('Invalid syntax in replacement pattern:')
                st.exception(err.with_traceback(None))
            except Exception as err:
                st.exception(err.with_traceback(None))
            else:
                successful = True
        elif mode == 'Split':
            st.divider()
            st.markdown('### Split Parts:')
            _tutorial('split')
            parts = re.split(json['regex'], string)
            # for part in parts:
                # st.markdown(part)
            st.table(repr(i) for i in parts)
