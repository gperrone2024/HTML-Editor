import streamlit as st
import streamlit.components.v1 as components

# Config page for wide layout
st.set_page_config(
    page_title="WYSIWYG HTML Editor",
    layout="wide",
)

# HTML/CSS/JS for the editor
html_content = r"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WYSIWYG HTML Editor</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: white; color: #333; }
        .container { width: 100%; margin: 0 auto; padding: 20px; }
        .header { text-align: center; margin-bottom: 20px; padding-bottom: 15px; border-bottom: 2px solid #000; }
        .toolbar { background: #f5f5f5; padding: 10px; border: 1px solid #ddd; border-radius: 5px; margin-bottom: 10px; display: flex; flex-wrap: wrap; gap: 5px; align-items: center; }
        .toolbar button { background: white; border: 1px solid #ccc; padding: 6px 12px; cursor: pointer; border-radius: 3px; font-size: 12px; transition: background 0.2s; }
        .toolbar button:hover { background: #e0e0e0; }
        .toolbar select { padding: 5px; border: 1px solid #ccc; border-radius: 3px; margin: 0 5px; }
        .toolbar input[type="color"] { width: 30px; height: 30px; border: none; cursor: pointer; }
        .divider { width: 100%; height: 2px; background: #000; margin: 10px 0; }
        .editor-container { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; height: 600px; }
        .editor-panel { border: 1px solid #ddd; border-radius: 5px; overflow: hidden; }
        .panel-header { background: #f0f0f0; padding: 10px; font-weight: bold; border-bottom: 1px solid #ddd; }
        .editor, .html-editor { width: 100%; height: calc(100% - 45px); padding: 15px; border: none; outline: none; font-family: inherit; font-size: 14px; line-height: 1.5; overflow-y: auto; background: white; resize: none; }
        .html-editor { font-family: 'Courier New', monospace; background: #f8f8f8; white-space: pre-wrap; color: #333; }
        .table-controls { display: none; position: fixed; background: white; border: 2px solid #007acc; padding: 15px; border-radius: 5px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); z-index: 1000; min-width: 250px; }
        /* ...rest of styles unchanged...*/
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>WYSIWYG HTML Editor</h1>
        </div>
        <div class="toolbar">
            <button onclick="execCmd('bold')" title="Bold"><b>B</b></button>
            <button onclick="execCmd('italic')" title="Italic"><i>I</i></button>
            <button onclick="execCmd('underline')" title="Underline"><u>U</u></button>
            <button onclick="execCmd('strikeThrough')" title="Strikethrough"><s>S</s></button>
            <select onchange="execCmd('formatBlock', this.value)">
                <option value="">Format</option>
                <option value="h1">Heading 1</option>
                <option value="h2">Heading 2</option>
                <option value="h3">Heading 3</option>
                <option value="p">Paragraph</option>
                <option value="pre">Preformatted</option>
            </select>
            <button onclick="execCmd('insertUnorderedList')" title="Bullet List">• List</button>
            <button onclick="execCmd('insertOrderedList')" title="Numbered List">1. List</button>
            <input type="color" onchange="execCmd('foreColor', this.value)" title="Text Color">
            <input type="color" onchange="execCmd('backColor', this.value)" title="Background Color">
            <button onclick="insertTable()" title="Insert Table">Table</button>
            <button onclick="insertLink()" title="Insert Link">Link</button>
            <button onclick="insertImage()" title="Insert Image">Image</button>
            <button onclick="execCmd('removeFormat')" title="Clear Format">Clear</button>
            <button onclick="pasteAsPlainText()" title="Paste as Plain Text">Paste Plain</button>
            <button onclick="execCmd('undo')" title="Undo">↶</button>
            <button onclick="execCmd('redo')" title="Redo">↷</button>
        </div>
        <div class="divider"></div>
        <div class="editor-container">
            <div class="editor-panel">
                <div class="panel-header">Visual Editor</div>
                <div id="editor" class="editor" contenteditable="true"
                     oninput="updateHTML()"
                     onkeyup="updateHTML()"
                     onmouseup="updateHTML(); highlightSelectedHTML()"
                     onclick="handleTableSelection(event)"
                     onpaste="handlePaste(event)">
                    <h2>Welcome to the WYSIWYG Editor!</h2>
                    <p>Start typing here or paste your content.</p>
                </div>
            </div>
            <div class="editor-panel">
                <div class="panel-header">HTML Code</div>
                <textarea id="htmlEditor" class="html-editor"
                          oninput="updateVisual()"
                          onkeyup="updateVisual()"
                          placeholder="HTML code will appear here..."></textarea>
            </div>
        </div>
        <div class="table-controls" id="tableControls">
            <!-- Table controls markup unchanged -->
        </div>
    </div>
    <script>
        let selectedTable = null;
        function execCmd(command, value = null) {
            document.execCommand(command, false, value);
            updateHTML();
            document.getElementById('editor').focus();
        }
        function updateHTML() {
            document.getElementById('htmlEditor').value = document.getElementById('editor').innerHTML;
        }
        function updateVisual() {
            document.getElementById('editor').innerHTML = document.getElementById('htmlEditor').value;
        }
        /* Rest of JS logic (insertTable, insertLink, insertImage, table handling, pasteAsPlainText, shortcuts) unchanged */
    </script>
</body>
</html>
"""

# Embed the editor in Streamlit
components.html(html_content, height=700, scrolling=True)
