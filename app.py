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
        html, body, #editorWrapper { height: 100%; margin: 0; padding: 0; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: white; color: #333; }
        .container { display: flex; flex-direction: column; height: 100%; padding: 10px; box-sizing: border-box; }
        .toolbar { background: #f5f5f5; padding: 10px; border: 1px solid #ddd; border-radius: 5px; display: flex; flex-wrap: wrap; gap: 5px; }
        .toolbar button, .toolbar select, .toolbar input[type="color"] { margin: 0 2px; }
        .editor-row { flex: 1; display: grid; grid-template-columns: 1fr 1fr; gap: 10px; overflow: hidden; margin-top: 10px; }
        .editor-panel { display: flex; flex-direction: column; border: 1px solid #ddd; border-radius: 5px; overflow: hidden; }
        .panel-header { background: #f0f0f0; padding: 8px; font-weight: bold; border-bottom: 1px solid #ddd; }
        .editor, .html-editor { flex: 1; padding: 10px; border: none; outline: none; font-family: inherit; font-size: 14px; line-height: 1.5; overflow: auto; white-space: pre-wrap; }
        .html-editor { font-family: 'Courier New', monospace; background: #f8f8f8; color: #333; position: relative; }
        .table-controls { display: none; position: absolute; background: white; border: 2px solid #007acc; padding: 10px; border-radius: 5px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); z-index: 1000; }
        .table-controls input { width: 100%; margin-bottom: 5px; padding: 4px; }
        .table-controls button { margin-right: 5px; padding: 5px 10px; }
        .editor table.selected { outline: 2px solid #007acc; }
        @media (max-width: 768px) { .editor-row { grid-template-columns: 1fr; } }
    </style>
</head>
<body>
    <div class="container" id="editorWrapper">
        <div class="toolbar">
            <button onclick="execCmd('bold')"><b>B</b></button>
            <button onclick="execCmd('italic')"><i>I</i></button>
            <button onclick="execCmd('underline')"><u>U</u></button>
            <button onclick="execCmd('strikeThrough')"><s>S</s></button>
            <select onchange="execCmd('formatBlock', this.value)"><option value="">Format</option><option value="h1">H1</option><option value="h2">H2</option><option value="h3">H3</option><option value="p">P</option></select>
            <button onclick="execCmd('insertUnorderedList')">• List</button>
            <button onclick="execCmd('insertOrderedList')">1. List</button>
            <input type="color" onchange="execCmd('foreColor', this.value)">
            <input type="color" onchange="execCmd('backColor', this.value)">
            <button onclick="insertTable()">Table</button>
            <button onclick="insertLink()">Link</button>
            <button onclick="insertImage()">Image</button>
            <button onclick="execCmd('removeFormat')">Clear</button>
            <button onclick="execCmd('undo')">↶</button>
            <button onclick="execCmd('redo')">↷</button>
        </div>
        <div class="editor-row">
            <div class="editor-panel">
                <div class="panel-header">Visual Editor</div>
                <div id="editor" class="editor" contenteditable="true" onkeyup="updateHTML()" onmouseup="updateHTML(); highlightSelectedHTML()" onclick="handleTableSelection(event)">Start typing here...</div>
            </div>
            <div class="editor-panel" style="position: relative;">
                <div class="panel-header">HTML Code</div>
                <textarea id="htmlEditor" class="editor html-editor" onkeyup="updateVisual()" placeholder="HTML appears here..."></textarea>
                <div class="table-controls" id="tableControls">
                    <input id="tblWidth" placeholder="Width (e.g. 100% or 400px)">
                    <input id="tblBorder" type="number" placeholder="Border px">
                    <input id="tblCellPadding" type="number" placeholder="Cell Padding px">
                    <input id="tblCellSpacing" type="number" placeholder="Cell Spacing px">
                    <button onclick="applyTableSettings()">Apply</button>
                    <button onclick="closeTableControls()">Close</button>
                </div>
            </div>
        </div>
    </div>
    <script>
        let selectedTable = null;
        function execCmd(cmd, val=null) { document.execCommand(cmd, false, val); updateHTML(); }
        function updateHTML() { htmlEditor.value = editor.innerHTML; }
        function updateVisual() { editor.innerHTML = htmlEditor.value; }
        function insertTable() {
            const r = prompt('Rows','3'), c = prompt('Cols','3');
            if(r && c) {
                let tbl = `<table border="1" cellpadding="8" cellspacing="0">`;
                for(let i=0;i<r;i++){ tbl += '<tr>'+Array(c).fill('<td>Cell</td>').join('')+'</tr>'; }
                tbl += '</table>';
                execCmd('insertHTML', tbl);
            }
        }
        function insertLink() { const u=prompt('URL','https://'), t=prompt('Text','Link'); if(u&&t) execCmd('insertHTML', `<a href="${u}" target="_blank">${t}</a>`); }
        function insertImage() { const u=prompt('URL',''), a=prompt('Alt',''); if(u) execCmd('insertHTML', `<img src="${u}" alt="${a}" style="max-width:100%;">`); }
        function handleTableSelection(e) {
            document.querySelectorAll('table.selected').forEach(t=>t.classList.remove('selected'));
            const tbl = e.target.closest('table'); selectedTable = tbl;
            if(tbl) { tbl.classList.add('selected'); showTableControls(e.pageX, e.pageY); } else closeTableControls();
        }
        function showTableControls(x, y) {
            const ctrl = document.getElementById('tableControls');
            const s = selectedTable;
            document.getElementById('tblWidth').value = s.style.width || s.getAttribute('width') || '';
            document.getElementById('tblBorder').value = s.getAttribute('border')||1;
            document.getElementById('tblCellPadding').value = s.getAttribute('cellpadding')||8;
            document.getElementById('tblCellSpacing').value = s.getAttribute('cellspacing')||0;
            ctrl.style.display='block'; ctrl.style.left=x+'px'; ctrl.style.top=y+'px';
        }
        function applyTableSettings() {
            if(!selectedTable) return;
            const w=document.getElementById('tblWidth').value;
            const b=document.getElementById('tblBorder').value;
            const p=document.getElementById('tblCellPadding').value;
            const s=document.getElementById('tblCellSpacing').value;
            selectedTable.style.width=w;
            selectedTable.setAttribute('border',b);
            selectedTable.setAttribute('cellpadding',p);
            selectedTable.setAttribute('cellspacing',s);
            updateHTML(); closeTableControls();
        }
        function closeTableControls() { document.getElementById('tableControls').style.display='none'; if(selectedTable) selectedTable.classList.remove('selected'); selectedTable=null; }
        function highlightSelectedHTML() {
            const sel = window.getSelection(); if(sel.rangeCount===0||sel.isCollapsed) return;
            const range = sel.getRangeAt(0);
            const dv = document.createElement('div'); dv.appendChild(range.cloneContents());
            const snippet = dv.innerHTML.trim().replace(/\s+/g,' ');
            const code = htmlEditor.value;
            const idx = code.indexOf(snippet);
            if(idx>-1) {
                htmlEditor.focus(); htmlEditor.setSelectionRange(idx, idx+snippet.length);
            }
        }
        const editor = document.getElementById('editor');
        const htmlEditor = document.getElementById('htmlEditor');
        document.addEventListener('DOMContentLoaded', ()=>{ updateHTML(); });
    </script>
</body>
</html>
'''

# Embed into Streamlit
html(editor_html, height=900, scrolling=True)
