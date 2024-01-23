import streamlit as st
import re
import ezregex as er
from ezregex import *
import builtins
import inspect
from rich import print
from Cope.colors import parse_color
from typing import Literal
from Cope.streamlit import ss
import colorsys

def rgbToHex(rgb):
    return f'#{int(rgb[0]):02x}{int(rgb[1]):02x}{int(rgb[2]):02x}'

# Remove this when Cope>=2.3.2
def complimentary_color(*color, rtn:Literal['html', 'rgb', 'rgba', 'opengl', 'hsv', 'hls', 'yiq']='rgb'):
    """ Returns the color opposite it on the color wheel, with the same saturation and value. """
    h, s, v = parse_color(*color, rtn='hsv')
    return parse_color(*map(lambda i: i*255, colorsys.hsv_to_rgb((h + .5) % 1.0001, s, v)), rtn=rtn)

# Make LaTeX happy
# TODO $ are uncolored
# [`~!@#$%^&*()-_=+[{]}\|;:'",<.>/?¢]]
def escape_latex(s):
    # Escape backslashes before we add any
    s = re.sub(r'\\', '\\\\textbackslash', s)

    to_escape = '&%#_{}'
    for esc in to_escape:
        s = re.sub(esc, f'\\{esc}', s)

    # In LaTeX, these are handled differently
    s = re.sub('~',  '\\\\textasciitilde ', s)
    s = re.sub(r'\^',  '\\\\textasciicircum ', s)

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
        return func + '(' + ', '.join(
            '${' + str(cnt+1) + ':' + p.name + '}'
            for cnt, p in enumerate(sig.parameters.values())
            if p.default == inspect._empty
        ) + ')' + '$0'

def run_code(pattern):
    successful = False
    # Run the code, get the var, and get the JSON search info
    # Set the variable before the end of the last line so we can do variables in the text_area
    try:
        local = {}
        exec(formatInput2code(pattern), globals(), local)
        var = local['_rtn']
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

    return var if successful else None

def show_matches(data, mode):
    if not len(data['matches']):
        st.info('No Matches Found')
        return

    for match in data['matches']:
        # This is the html hack way of doing it. It doesn't work as well as the latex version.
        # st.markdown(f"""
            # <style>
            # div[data-testid="stExpander"] div[role="button"] p {{
            #     color: {match['match']['color']};
            # }}
            # </style>
        # """, unsafe_allow_html=True)

        # We're using latex here because for SOME reason expanders support named colors, but NOT arbitrary colors
        # Cause that makes sense.
        if '$' in match['match']['string']:
            # Apparently, there's no way to escape a $ that I can find
            latex = f'{escape_latex(match["match"]["string"])} ({match["match"]["start"]}:{match["match"]["end"]})'
        else:
            latex = f'$\\text{{\\color{{{match["match"]["color"]}}}{escape_latex(match["match"]["string"])}}} \\textit{{({match["match"]["start"]}:{match["match"]["end"]})}}$'
        fold = st.expander(latex, (len(data['matches']) == 1) and mode != 'Replace')

        if not len(match['unnamedGroups']) and not len(match['namedGroups']):
            fold.markdown('No groups captured')
            continue

        if ss.tutorial:
            fold.caption(ss.texts['tutorial']['groups'])

        if len(match['unnamedGroups']):
            fold.markdown('#### Unnamed Groups')

        for cnt, group in enumerate(match['unnamedGroups']):
            inverse = rgbToHex(complimentary_color([int(c, base=16) for c in match['match']['color'][1::2]]))
            fold.markdown(f'''
                {cnt+1}: <span style="background-color: {group["color"]}; color: {inverse};">{group["string"]}</span>
                <span style="color: white; font-style: italic;"> ({group["start"]}:{group["end"]})</span>
            ''', True)

        if len(match['namedGroups']):
            fold.markdown('#### Named Groups')
        for name, group in match['namedGroups'].items():
            inverse = rgbToHex(complimentary_color([int(c, base=16) for c in match['match']['color'][1::2]]))
            fold.markdown(f'''
                {name}: <span style="background-color: {group["color"]}; color: {inverse};">{group["string"]}</span>
                <span style="color: white; font-style: italic;"> ({group["start"]}:{group["end"]})</span>
            ''', True)
