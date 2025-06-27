import streamlit as st
import streamlit.components.v1 as components

# Configura la pagina in modalità wide per sfruttare tutta la larghezza disponibile
st.set_page_config(
    page_title="WYSIWYG HTML Editor",
    layout="wide",
)

# HTML/CSS/JS del WYSIWYG editor
html_content = r"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WYSIWYG HTML Editor</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: white;
            color: #333;
        }
        .container {
            width: 100%;             /* Rimuove il max-width per usare tutta la larghezza */
            margin: 0 auto;
            padding: 20px;
        }
        .header {
            text-align: center;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 2px solid #000;
        }
        .toolbar {
            background: #f5f5f5;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            margin-bottom: 10px;
            display: flex;
            flex-wrap: wrap;
            gap: 5px;
            align-items: center;
        }
        .toolbar button { background: white; border: 1px solid #ccc; padding: 6px 12px; cursor: pointer; border-radius: 3px; font-size: 12px; transition: background 0.2s; }
        .toolbar button:hover { background: #e0e0e0; }
        .toolbar button.active { background: #007acc; color: white; }
        .toolbar select { padding: 5px; border: 1px solid #ccc; border-radius: 3px; margin: 0 5px; }
        .toolbar input[type="color"] { width: 30px; height: 30px; border: none; cursor: pointer; }
        .divider { width: 100%; height: 2px; background: #000; margin: 10px 0; }
        .editor-container { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; height: 600px; }
        .editor-panel { border: 1px solid #ddd; border-radius: 5px; overflow: hidden; }
        .panel-header { background: #f0f0f0; padding: 10px; font-weight: bold; border-bottom: 1px solid #ddd; }
        .editor { height: calc(100% - 45px); padding: 15px; border: none; outline: none; font-family: inherit; font-size: 14px; line-height: 1.5; overflow-y: auto; background: white; }
        .html-editor { font-family: 'Courier New', monospace; background: #f8f8f8; white-space: pre-wrap; color: #333; resize: none; }
        .table-controls { display: none; position: fixed; background: white; border: 2px solid #007acc; padding: 15px; border-radius: 5px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); z-index: 1000; min-width: 250px; }
        /* ... resto dello stile invariato ... */
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>WYSIWYG HTML Editor</h1>
        </div>
        <div class="toolbar">
            <!-- Bottoni di formattazione -->
            <button onclick="execCmd('bold')" title="Bold"><b>B</b></button>
            <button onclick="execCmd('italic')" title="Italic"><i>I</i></button>
            <button onclick="execCmd('underline')" title="Underline"><u>U</u></button>
            <button onclick="execCmd('strikeThrough')" title="Strikethrough"><s>S</s></button>
            <select onchange="execCmd('formatBlock', this.value)">
                <option value="">Format</option>
                <option value="h1">Heading 1</option>
                <!-- ... altre opzioni ... -->
            </select>
            <!-- Altri controlli ... -->
        </div>
        <div class="divider"></div>
        <div class="editor-container">
            <div class="editor-panel">
                <div class="panel-header">Visual Editor</div>
                <div id="editor" class="editor" contenteditable="true" onkeyup="updateHTML()" onmouseup="updateHTML(); highlightSelectedHTML()" onclick="handleTableSelection(event)" onpaste="handlePaste(event)">
                    <h2>Welcome to the WYSIWYG Editor!</h2>
                    <p>Start typing here...</p>
                </div>
            </div>
            <div class="editor-panel">
                <div class="panel-header">HTML Code</div>
                <textarea id="htmlEditor" class="editor html-editor" onkeyup="updateVisual()" placeholder="HTML code..."></textarea>
            </div>
        </div>
        <!-- Controlli per le tabelle... -->
    </div>
    <script>
        // Qui va lo script JavaScript originale per execCmd, updateHTML, insertTable, ecc.
    </script>
</body>
</html>
"""

# Renderizza il componente HTML/JS all'interno di Streamlit
components.html(html_content, height=700, scrolling=True)
