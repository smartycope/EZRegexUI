import streamlit as st
from code_editor import code_editor
from streamlit_javascript import st_javascript
import streamlit as st
import code_editor as _code_editor
from code_editor import code_editor
import streamlit.components.v1 as components
from bs4 import BeautifulSoup as BS


# st.session_state['code'] = st.session_state['code']
# id = st.session_state.get('code')
print('-'*100)

if (beg := st.session_state.get('code')):
    print('session state at beginning:', beg['text'])
# if 'code' in st.session_state:
# print(st.session_state.get('code'))

# st.text('CODE HERE')

# print('CODE HERE:', st_javascript('window.parent.document.querySelector("#root > div:nth-child(1) > div.withScreencast > div > div > div > section > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi4 > div > div > div:nth-child(1) > div > div").textContent'))


print('COOKIE:', st_javascript('window.parent.document.cookie'))

# place = st.empty()
# components.html('''<script>
#         window.parent.window.addEventListener('beforeunload', function (event) {
#             // Your code here
#             // This will be executed before the page is unloaded.
#             // You can show a confirmation message or perform cleanup operations.
#             console.log('unloading...');
#         });
#     </script>''')


def doThing():
    print('doing thing')
    # try:
        # current = BS(st_javascript('''function(){
        #     const parentDoc = window.parent.document;
        #     const iframe = parentDoc.querySelector("#root > div:nth-child(1) > div.withScreencast > div > div > div > section > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi4 > div > div > div:nth-child(2) > iframe");
        #     const line = iframe.contentDocument.querySelector('#REACT_ACE_EDITOR > div.ace_scroller > div > div.ace_layer.ace_text-layer > div');
        #     // console.log(typeof line.outerHTML);
        #     return line.outerHTML;
        # }()'''), features='html.parser').get_text()
    # except:
    #     print('~~~~~~~~~ failed ~~~~~~~~~')
    # else:
    #     print('current:', current)


    # html = st_javascript('''function(){
    #     const parentDoc = window.parent.document;
    #     const iframe = parentDoc.querySelector("#root > div:nth-child(1) > div.withScreencast > div > div > div > section > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi4 > div > div > div:nth-child(3) > iframe");
    #     const line = iframe.contentDocument.querySelector('#REACT_ACE_EDITOR > div.ace_scroller > div > div.ace_layer.ace_text-layer > div');
    #     console.log(line.outerHTML);
    #     return line.outerHTML;
    # }()''', key=11)

    # try:
    #     soup = BS(html, features='html.parser')
    #     current = soup.get_text()
    # except:
    #     print('Failed:', html)
    # else:
    #     print('current:', current)



    # components.html('<script>window.parent.document.querySelector("#root > div:nth-child(1) > div.withScreencast > div > div > div > section > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi4 > div > div > div:nth-child(1) > div > div").textContent = "CODE WHERE?";</script>')

    components.html('''<div><script>
        const parentDoc = window.parent.document;
        const iframe = parentDoc.querySelector("#root > div:nth-child(1) > div.withScreencast > div > div > div > section > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi4 > div > div > div:nth-child(4) > iframe");
        console.log(iframe);
        const line = iframe.contentDocument.querySelector('#REACT_ACE_EDITOR > div.ace_scroller > div > div.ace_layer.ace_text-layer > div');
        console.log(line.textContent);
        line.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', ctrlKey: true }));
        //parentDoc.cookie = "username=John Doe;";
        //document.cookie = "context=" + line.textContent + "; expires=Thu, 18 Dec 2023 12:00:00 UTC; path=/;
        //return line.outerHTML;
    </script></div>''')


    # code += ' + thing!'
    if '_toAdd' in st.session_state:
        st.session_state['_toAdd'] += ' + thing!'
    else:
        st.session_state['_toAdd'] = ' + thing!'
    # st.rerun()
    # if st.session_state.get('code') is not None:
        # print('getting state')
        # st.session_state['code']['text'] += ' + thing!'
        # st.session_state['code']['id'] = str(random.randbytes(8))

cur = st.session_state['code']['text'] if st.session_state.get('code') is not None else ''
new = st.session_state.get('_toAdd')
if new is not None:
    print('adding')
    cur += new
    # st.session_state['_toAdd'] = ''
print('cur:', cur)
print('new:', new)
# with st.form('form'):


buttonVar = st.button('add thing!', on_click=doThing)


# code = code_editor('thing', allow_reset=True, buttons=buttons)


# if id is not None:
    # print(id['id'])
resp = code_editor(cur, key='code', snippets=['hello', 'hello world', 'oranges'], allow_reset=True, props={'wrapEnabled':True,})
print(resp['id'])
id = st.session_state.get('prevID')
if id is not None and id != resp['id']:
    print('resetting')
    st.session_state['_toAdd'] = ''
    st.session_state['prevID'] = resp['id']
    st.rerun()

st.session_state['prevID'] = resp['id']
# submitted = st.form_submit_button("Submit")
code = resp['text']
print('response:', resp)
print('code in editor:', code)

if (end := st.session_state.get('code')):
    print('session state at end:', end['text'])
    # print('session state at end:', end)


# print(st_javascript('''document.addEventListener('DOMContentLoaded', function(){
#             const parentDoc = window.parent.document;
#             const iframe = parentDoc.querySelector("#root > div:nth-child(1) > div.withScreencast > div > div > div > section > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi4 > div > div > div:nth-child(2) > iframe");
#             const line = iframe.contentDocument.querySelector('#REACT_ACE_EDITOR > div.ace_scroller > div > div.ace_layer.ace_text-layer > div');
#             // console.log(typeof line.outerHTML);
#             return line.outerHTML;
#         })'''))

# if buttonVar:
#     try:
#         current = BS(st_javascript('''function(){
#             const parentDoc = window.parent.document;
#             const iframe = parentDoc.querySelector("#root > div:nth-child(1) > div.withScreencast > div > div > div > section > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi4 > div > div > div:nth-child(2) > iframe");
#             const line = iframe.contentDocument.querySelector('#REACT_ACE_EDITOR > div.ace_scroller > div > div.ace_layer.ace_text-layer > div');
#             // console.log(typeof line.outerHTML);
#             return line.outerHTML;
#         }()'''), features='html.parser').get_text()
#     except:
#         pass
#     else:
#         print('current:', current)

# st.write(code)


# if 'add' not in st.session_state:
#     st.session_state.add = ''

# st.button('update', on_click=addThing):













# print(_code_editor.components.)
# print(st.session_state)
# print(st._cache_data)
    # print(st_javascript('''function(){
    #     return 'hello world';
    # }()''',key=8))


# if doit:
#     print(st_javascript('''function(){
#         const parentDoc = window.parent.document;
#         const iframe = parentDoc.querySelector("#root > div:nth-child(1) > div.withScreencast > div > div > div > section > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi4 > div > div > div:nth-child(1) > iframe");
#         const line = iframe.contentDocument.querySelector('#REACT_ACE_EDITOR > div.ace_scroller > div > div.ace_layer.ace_text-layer > div');
#         console.log(typeof line.outerHTML);
#         return line.outerHTML;
#     }()'''))
# return window.parent.document.querySelector("#root > div:nth-child(1) > div.withScreencast > div > div > div > section > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi4 > div > div > div:nth-child(2) > iframe").contentDocument.querySelector('#REACT_ACE_EDITOR > div.ace_scroller > div > div.ace_layer.ace_text-layer > div').outerHTML;}()'''))
    # print(st_javascript('''function(){
            # return 'hello world!';
        # }()''',key=7))
    # print(st_javascript('''console.log(window.parent.document.querySelector("#root > div:nth-child(1) > div.withScreencast > div > div > div > section > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi4 > div > div > div:nth-child(2) > iframe").contentDocument.querySelector('#REACT_ACE_EDITOR > div.ace_scroller > div > div.ace_layer.ace_text-layer > div'))'''))
    # <div>
    # <div class="shown"></div>
    # <script>
# get()
    # </script>
    # </div>

# print(st_javascript('''function(){
#         return 7;
#     }()'''))
# return_value = st_javascript("""await fetch("https://reqres.in/api/products/3").then(function(response) {
#     return 6;
# }) """)
# print(return_value)
# return_value = st_javascript("""function() {
#         // const parentDoc = window.parent.document;
#         // const iframe = parentDoc.querySelector("#root > div:nth-child(1) > div.withScreencast > div > div > div > section > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi4 > div > div > div:nth-child(2) > iframe");
#         // const line = iframe.contentDocument.querySelector('#REACT_ACE_EDITOR > div.ace_scroller > div > div.ace_layer.ace_text-layer > div');
#         // console.log(typeof line.outerHTML);
#         // return line.outerHTML;
#     return 6;
# }() """)
# print('----', return_value)

# import time


# document.addEventListener('DOMContentLoaded', function () {
#             // Access the first iframe in the document
#             // const iframe = document.querySelector("#root > div:nth-child(1) > div.withScreencast > div > div > div > section > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi4 > div > div > div:nth-child(1) > iframe");
#             const parentDocument = window.parent.document;
#             const iframe = parentDocument.querySelector("#root > div:nth-child(1) > div.withScreencast > div > div > div > section > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi4 > div > div > div:nth-child(1) > iframe").contentDocument.querySelector('#REACT_ACE_EDITOR > div.ace_scroller > div > div.ace_layer.ace_text-layer > div')
#             //console.log(parentDocument)
#             //console.log(document.querySelector("html"));
#             //console.log(document.querySelector("#root"));
#             //console.log(iframe);

#             if (iframe) {
#                 // Access the iframe document
#                 const iframeDocument = iframe.contentDocument;
#                 // console.log(iframeDocument);

#                 // Check if the element exists in the iframe
#                 const element = iframeDocument.querySelector('#REACT_ACE_EDITOR > div.ace_scroller > div > div.ace_layer.ace_text-layer > div');

#                 console.log(element);


#             return element
#         });

# while True:
#     token = st_javascript('parent.window.token')
#     if token:
#         break
#     time.sleep(1)
    # <div>
    # <div class="shown"></div>
    # <iframe src="http://localhost:8501/component/code_editor.code_editor/index.html?streamlitUrl=http%3A%2F%2Flocalhost%3A8501%2F" id="yourIframe"></iframe>
    # <script>
    #     document.addEventListener('DOMContentLoaded', function () {
    #         // Access the iframe document
    #         const iframeDocument = document.querySelector('#root > div:nth-child(1) > div.withScreencast > div > div > div > section > div.block-container.st-emotion-cache-1y4p8pa.ea3mdgi4 > div > div > div:nth-child(1)').contentDocument;

    #         console.log(element);

    #         // Check if the element exists in the iframe
    #         const element = iframeDocument.;

    #         console.log(element);

    #         if (element) {
    #             element.dispatchEvent(new KeyboardEvent('keydown', { key: 'k' }));
    #             document.querySelector('.shown').textContent = 'Found it!';
    #         } else {
    #             document.querySelector('.shown').textContent = 'Element not found.';
    #         }
    #     });
    # </script>
    # </div>
    # ''')


    # '''
    # <div class="shown"></div>
    # <script>
    # document.addEventListener('DOMContentLoaded', function () {
    #     const element = document.querySelector('#REACT_ACE_EDITOR .div.ace_scroller');
    #     console.log(element);

    #     if (element) {
    #         element.dispatchEvent(new KeyboardEvent('keydown', { key: 'k' }));
    #         document.querySelector('.shown').textContent = 'Found it!';
    #     } else {
    #         document.querySelector('.shown').textContent = 'Element not found.';
    #     }
    # });
    # </script>
    # ''')


    # const button = document.getElementById('my-button');

# button.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', ctrlKey: true }));

#     <div>
#     <div class="copyElement"></div>
#     <script src="http://localhost:8501/component/code_editor.code_editor/static/js/CodeEditor.tsx"></script>

#     <script>
#         // const button = document.querySelector('button');
#         // const aceEditor = useRef<AceEditor>(null);
#         // const editor = aceEditor.current?.editor;
#         // editor.execCommand("submit");

#         document.querySelector('.copyElement').innerHTML = "Hello World";
#     </script>
#     </div>
#     ''')


# (editor: any) => {
    # const outgoingMode = editor.getSession().$modeId.split("/").pop();
    # Streamlit.setComponentValue({id: v1().slice(0,8), type: "submit", text: editor.getValue(), lang: outgoingMode, cursor: editor.getCursorPosition()});
    # }
# const onChangeHandler = (newCode: string) => {
#     setCode(newCode);
#   }


# const editor = aceEditor.current?.editor;

# print(components.)

# /html/body/div[1]/div/div/div[2]/div/div[3]/div
