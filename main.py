import re
import ezregex as er
from ezregex import *
import streamlit as st
import json as _json
import builtins
from code_editor import code_editor

# TODO:
# groups are sequential within each match, (I think), they should be sequential globally
# Make group have a default named parameter instead of 2 seperate functions
# Figure out how to add the icon to GitHub Pages
# Make the buttons add at the cursor index, not at the end (or an option to)

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

# TODO:
# Breaking up the last line with \ or () will fail, cause we're adding the rtn = at the last line
#   - also if the last line is a comment, it will fail
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

def snippify(func:str):
    if '(' not in func:
        return func
    # else:
    return func


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

# The actual page
# left, right = st.columns([.09, 1])
# left.image(logo, width=103)
st.title('EZRegex')
st.caption(f"Copeland Carter | version {er.__version__}")

# Add all the side bar elements
with st.sidebar:
    left, right = st.columns([.65, .35])
    style = left.radio('Style', ['camelCase', 'snake_case'], horizontal=True)
    right.markdown('')
    tutorial = right.checkbox('Walkthrough')

    st.header('Elements')
    _tutorial('sidebar')
    with open('elements.json', 'r') as f:
        erElements = _json.load(f)
    for groupName, i in erElements.items():
        with st.expander(groupName):
            if i['description'] is not None:
                st.caption(i['description'])
            for camel, snake, help in i['elements']:
                kwargs = {'_replace': True} if groupName == 'Replacement' else {}
                if style == 'camelCase':
                    name = camel
                else:
                    name = camel if snake is None else snake
                st.button(name, on_click=addPart, args=(name,), kwargs=kwargs, help=help)

                if tutorial and help is not None:
                    st.caption(help)

                # Now that we made the buttons, while we're here, also make the snippets
                snippets += f'snippet {name}\n\t{snippify(name)}\n'

    with st.expander('Operators'):
        st.markdown(texts['operators'])


# The initial widgets
_tutorial('main')
st.markdown('Enter EZRegex pattern:')

# ezre pattern box
ezre = st.session_state['ezre']['text'] if 'ezre' in st.session_state else ''
new = st.session_state.get('ezre_toAdd')
if new is not None:
    ezre += new
if tutorial:
    ezre = texts['tutorial']['defaultPattern']

snippetsRemove= ''
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

# String input box
placeholder = st.empty()
string = placeholder.text_area(
    'Enter string to match:',
    key='string',
    placeholder=texts['stringPlaceholder'],
    value=texts['tutorial']['defaultString'] if tutorial else ''
)
_tutorial('string')

# Replacement pattern box
st.markdown('Enter replacement EZRegex:')
replacementPlaceholder = st.empty()
tutorialReplacementPlaceholder = st.empty()
left, right = st.columns([.85, .15])
right.button('Reload')
# replace = left.checkbox('Replacement Mode', key='replace_mode', value=tutorial)
mode = left.radio('Mode',
    ['Search', 'Replace', 'Split'],
    captions=texts['modeCaptions'] if tutorial else None,
    horizontal=not tutorial,
    index=0 if not tutorial else 1,
)

with replacementPlaceholder:
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

# If it's in the wrong mode, erase the box we just made.
if mode != 'Replace':
    replacementPlaceholder.empty()
elif tutorial:
    tutorialReplacementPlaceholder.caption(texts['tutorial']['replaceBox'])

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
                latex = f'$\\text{{\color{{{match["match"]["color"]}}}{escape(match["match"]["string"])}}} \\textit{{({match["match"]["start"]}:{match["match"]["end"]})}}$'
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
