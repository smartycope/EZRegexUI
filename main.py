import sys
import re
import io
import contextlib
import ezregex as er
from ezregex import *
from streamlit import components
import streamlit as st
import json as _json
import builtins

# For exec globals
input = ''

# One less dependancy
def rgbToHex(rgb):
    """ Translates an rgb tuple of int to a tkinter friendly color code """
    return f'#{int(rgb[0]):02x}{int(rgb[1]):02x}{int(rgb[2]):02x}'

def invertColor(rgba):
    """ Inverts a color """
    return tuple(255 - c for c in rgba)

# Function for adding side bar elements to ezre when they're clicked
def addPart(input, _replace=False):
    global replace, replacement
    # If there's parameters, remove them. They can reference the side panel.
    input = re.sub(str('(' + matchMax(anything + optional(er.group(comma))) + ')'), '()', input)
    cur = ezre
    get = 'ezre'
    if _replace:
        st.session_state['replace_mode'] = True
        replace = True
        get = 'replaceBox'
        cur = replacement

    if not len(cur):
        st.session_state[get] = input
    elif re.search((optional(' ') + anyof('+', '<<', '>>', '*') + optional(' ') + stringEnd).str(), cur) is not None:
        st.session_state[get] = cur + input
    elif (m := re.search((er.group('()') + ow + stringEnd).str(), cur)) is not None:
        st.session_state[get] = cur[:(-len(m.group())) + 1] + input + ')'
    else:
        st.session_state[get] = cur + ' + ' + input

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
    keywords = set(dir(builtins) + dir(er) + re.findall((lineStart + group(word) + ifFollowedBy(ow + '=')).str(), s))
    # print(anyExcept(anyof(*keywords), type='.*'))
    # s = re.sub((anyExcept('literal', type='.*')).str(), '"' + replace_entire.str() + '"', s)
    return '\n'.join(s.splitlines()[:-1]) + '\n_rtn = '  + s.splitlines()[-1]


about = """
    # EZRegex
    An readable and intuitive way to generate Regular Expressions

    EZRegex is also a fully fledged Python package on PyPi and github! Check it out at
    - https://github.com/smartycope/ezregex
    - https://pypi.org/project/ezregex/
        - pip install ezregex

    This website, and associated package is liscensed under the MIT License. No rights reserved.

    If you'd like to make a donation, my venmo is @Copeland-Carter

    All credit goes to Copeland Carter, the Computer Goblin.
"""
st.set_page_config(page_title='EZRegex', initial_sidebar_state='expanded', menu_items={
    'Get help': None,
    'Report a Bug': 'mailto:smartycope@gmail.com',
    'About': about
})
st.title('EZRegex')
st.caption(f"Copeland Carter | version {er.__version__}")


# Add all the side bar elements
with st.sidebar:
    left, right = st.columns(2)
    style = left.radio('Style', ['camelCase', 'snake_case'])
    tutorial = right.checkbox('Tutorial')

    st.header('Elements')
    if tutorial:
        st.caption('These are all a bunch of elements that represent various levels of abstraction of Regular Expression elements. Use them to specify parts of a string. Hover over to see more info')
    with open('elements.json', 'r') as f:
        elements = _json.load(f)
    for groupName, i in elements.items():
        with st.expander(groupName):
            if i['description'] is not None:
                st.caption(i['description'])
            for camel, snake, help in i['elements']:
                kwargs = {'_replace': True} if groupName == 'Replacement' else {}
                if style == 'camelCase':
                    st.button(camel, on_click=addPart, args=(camel,), kwargs=kwargs, help=help)
                else:
                    st.button(camel if snake is None else snake, on_click=addPart, args=(camel if snake is None else snake,), kwargs=kwargs, help=help)
                if tutorial and help is not None:
                    st.caption(help)
    with st.expander('Operators'):
        st.markdown("""
            - `+`, `<<`, `>>`
                - These all do the same thing: combine expressions
            - `*`
                - This does what you think it does. Multiplies an expression a number of times
            - `+`
                - A unary + operator acts exactly as a match_max() does, or, if you're familiar with regex syntax, the + operator
            - `[]`
                - Coming soon! Not implemented yet, but they will do things similar to match_amt() and match_range()
        """)

# The initial widgets
ezrePlaceholder = st.empty()
ezre = ezrePlaceholder.text_area('Enter EZRegex code:', key='ezre', help='This accepts valid Python syntax. The last line must be an EZRegex expression', value="var = lineStart + group(word)\nvar + ow + '=' + ow + namedGroup('value', +anything)" if tutorial else '')
if tutorial:
    st.caption('This accepts valid Python syntax. The last line must be an EZRegex expression')

placeholder = st.empty()
string = placeholder.text_area('Enter string to match:', key='string', placeholder='Leave empty to automatically generate an example of what it would match', value="foo = 8 - 9\nbar='hello world!'" if tutorial else '')
if tutorial:
    st.caption('Put text here you want to try to match the pattern against. Or you can leave it empty to auto-generate some text which would match the pattern')

replacementPlaceholder = st.empty()
tutorialReplacementPlaceholder = st.empty()
left, right = st.columns([.85, .15])
right.button('Reload')
replace = left.checkbox('Replacement Mode', key='replace_mode', value=tutorial)
replacement = replacementPlaceholder.text_area('Enter replacement EZRegex:', key='replaceBox', help='This accepts valid Python syntax. The last line must be an EZRegex expression', value="replaceGroup(1) + ': ' + replaceGroup('value') + ','" if tutorial else '')

if not replace:
    replacementPlaceholder.empty()
elif tutorial:
    tutorialReplacementPlaceholder.caption('Here, put text you want to replace (uses re.sub()). Use the replacement section to add groups')

# Generate all the match stuff, if we can
if len(ezre):
    successful = False
    # Run the code, get the var, and get the JSON search info
    # Set the variable before the end of the last line so we can do variables in the text_area
    code = formatInput2code(ezre)
    print(code)
    local = {}
    print(0)
    try:
        print(1)
        exec(code, globals(), local)
        print(5)
        var = local['_rtn']
        if not len(string):
            try:
                print(4)
                string = var.invert()
                print(3)
            except:# NotImplementedError:
                st.error("Can't invert that expression. Try providing a string to match instead.")
        json = var._matchJSON(string)
        print(2)
    except TypeError:
        st.error('Invalid parameters')
    except SyntaxError:
        st.error('Invalid syntax in EZRegex code')
    except Exception as err:
        st.exception(err)
    else:
        successful = True
    print(successful)
    if successful:
        st.divider()

        # left, right = st.columns([.85, .15])
        st.markdown('### Looking for matches in:')
        # I don't know WHY this works, but it does, so nobody touch it
        # right.button('Reload')
        # Display the match string html with groups all colored
        st.markdown(json['stringHTML'], True)
        if tutorial:
            st.caption('Here you can see your string (provided, or generated). Text color denotes induvidual matches, and background color indicates seperate matched named and unnamed groups.')

        st.markdown('### Using regex:')
        st.code(json['regex'], language='regex')
        if tutorial:
            st.caption('This is the regex which gets generated when you compile the EZRegex string. You can copy this into your program if you don\'t want to use the ezregex python package directly.')

        st.markdown('### Matches:')
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
            fold = st.expander(latex, (len(json['matches']) == 1) and not replace)

            if not len(match['unnamedGroups']) and not len(match['namedGroups']):
                fold.markdown('No groups captured')
                break

            if tutorial:
                fold.caption('These are the named and unnamed groups found in the match, also color coded and indexed. Remember that group #0 is always the entire match')

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

        if tutorial:
            st.caption('Here there are all the matches found in the string. They\'re all color coded for easy locating. The numbers in parenthesis are the indecies which the match is in the string')
        if replace:
            st.markdown('### Replaced String:')
            try:
                if len(replacement):
                    code = '\n'.join(replacement.splitlines()[:-1]) + '\n_rtn = '  + replacement.splitlines()[-1]
                    local = {}
                    exec(code, globals(), local)
                    repl = local['_rtn']
                else:
                    repl = ''
                st.markdown(re.sub(json['regex'], str(repl), string))
            except TypeError:
                st.error('Invalid parameters in replacement')
            except SyntaxError:
                st.error('Invalid syntax in replacement')
            except Exception as err:
                st.exception(err)
            else:
                successful = True

            if tutorial:
                st.caption('This is the string you would get if you replaced the `pattern` with the `replacement` in the `string`.')
