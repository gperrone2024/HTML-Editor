import streamlit as st
from streamlit.components.v1 import html

# Configure the Streamlit app
st.set_page_config(page_title="WYSIWYG HTML Editor", layout="wide")
st.title("WYSIWYG HTML Editor")

# Define the HTML, CSS, and JavaScript for the editor
editor_html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WYSIWYG HTML Editor</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: white; color: #333; }
        .container { max-width: 1400px; margin: 0 auto; padding: 20px; }
        .header { text-align: center; margin-bottom: 20px; padding-bottom: 15px; border-bottom: 2px solid #000; }
        .toolbar { background: #f5f5f5; padding: 10px; border: 1px solid #ddd; border-radius: 5px; margin-bottom: 10px; display: flex; flex-wrap: wrap; gap: 5px; align-items: center; }
        .toolbar button { background: white; border: 1px solid #ccc; padding: 6px 12px; cursor: pointer; border-radius: 3px; font-size: 12px; transition: background 0.2s; }
        .toolbar button:hover { background: #e0e0e0; }
        .toolbar button.active { background: #007acc; color: white; }
        .toolbar select, .toolbar input[type="color"] { margin: 0 5px; }
        .divider { width: 100%; height: 2px; background: #000; margin: 10px 0; }
        .editor-container { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; height: 600px; }
        .editor-panel { border: 1px solid #ddd; border-radius: 5px; overflow: hidden; }
        .panel-header { background: #f0f0f0; padding: 10px; font-weight: bold; border-bottom: 1px solid #ddd; }
        .editor { height: calc(100% - 45px); padding: 15px; border: none; outline: none; font-family: inherit; font-size: 14px; line-height: 1.5; overflow-y: auto; background: white; }
        .html-editor { font-family: 'Courier New', monospace; background: #f8f8f8; white-space: pre-wrap; color: #333; resize: none; }
        .table-controls { display: none; position: fixed; background: white; border: 2px solid #007acc; padding: 15px; border-radius: 5px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); z-index: 1000; min-width: 250px; }
        .table-controls h3 { margin-bottom: 10px; color: #007acc; }
        .table-controls label { display: block; margin: 8px 0 3px 0; font-weight: 500; }
        .table-controls input { width: 100%; padding: 5px; border: 1px solid #ddd; border-radius: 3px; margin-bottom: 8px; }
        .table-controls button { background: #007acc; color: white; border: none; padding: 8px 15px; border-radius: 3px; cursor: pointer; margin: 5px 5px 0 0; }
        .table-controls .close-btn { background: #dc3545; }
        .editor table { border-collapse: collapse; margin: 10px 0; }
        .editor table td, .editor table th { border: 1px solid #ddd; padding: 8px; min-width: 50px; min-height: 25px; }
        .editor table.selected { outline: 2px solid #007acc; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header"><h1>WYSIWYG HTML Editor</h1></div>
        <div class="toolbar">
            <button onclick="execCmd('bold')" title="Bold"><b>B</b></button>
            <button onclick="execCmd('italic')" title="Italic"><i>I</i></button>
            <button onclick="execCmd('underline')" title="Underline"><u>U</u></button>
            <button onclick="execCmd('strikeThrough')" title="Strikethrough"><s>S</s></button>
            <select onchange="execCmd('formatBlock', this.value)"> <option value="">Format</option> <option value="h1">Heading 1</option> <option value="h2">Heading 2</option> <option value="h3">Heading 3</option> <option value="p">Paragraph</option> </select>
            <button onclick="execCmd('insertUnorderedList')">• List</button>
            <button onclick="execCmd('insertOrderedList')">1. List</button>
            <input type="color" onchange="execCmd('foreColor', this.value)" title="Text Color">
            <input type="color" onchange="execCmd('backColor', this.value)" title="Background Color">
            <button onclick="insertTable()">Table</button>
            <button onclick="insertLink()">Link</button>
            <button onclick="insertImage()">Image</button>
            <button onclick="execCmd('removeFormat')">Clear</button>
            <button onclick="execCmd('undo')">↶</button>
            <button onclick="execCmd('redo')">↷</button>
        </div>
        <div class="divider"></div>
        <div class="editor-container">
            <div class="editor-panel">
                <div class="panel-header">Visual Editor</div>
                <div id="editor" class="editor" contenteditable onkeyup="updateHTML()" onclick="handleTableSelection(event)">Welcome to the WYSIWYG Editor! Start typing or paste content here.</div>
            </div>
            <div class="editor-panel">
                <div class="panel-header">HTML Code</div>
                <textarea id="htmlEditor" class="editor html-editor" onkeyup="updateVisual()" placeholder="HTML code will appear here..."></textarea>
            </</div>
        </div>
    </div>
    <script>
        function execCmd(cmd, val=null) { document.execCommand(cmd, false, val); updateHTML(); }
        function updateHTML() { document.getElementById('htmlEditor').value = document.getElementById('editor').innerHTML; }
        function updateVisual() { document.getElementById('editor').innerHTML = document.getElementById('htmlEditor').value; }
        function insertTable() { let r=prompt('Number of rows','3'), c=prompt('Number of cols','3'); if(r&&c){let t='<table border="1" cellpadding="8" cellspacing="0">'; for(let i=0;i<r;i++){t+='<tr>'; for(let j=0;j<c;j++) t+='<td>Cell</td>'; t+='</tr>';} t+='</table>'; execCmd('insertHTML', t);} }
        function insertLink() { let u=prompt('Enter URL','https://'), t=prompt('Enter link text','Link'); if(u&&t) execCmd('insertHTML', `<a href="${u}" target="_blank">${t}</a>`); }
        function insertImage() { let u=prompt('Image URL',''), a=prompt('Alt text','Img'); if(u) execCmd('insertHTML', `<img src="${u}" alt="${a}" style="max-width:100%;">`); }
        document.addEventListener('DOMContentLoaded', updateHTML);
    </script>
</body>
</html>
'''

# Embed the editor in the Streamlit app
html(editor_html, height=800, scrolling=True)
