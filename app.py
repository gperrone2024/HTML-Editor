import streamlit as st
from streamlit.components.v1 import html

# Configure the Streamlit app
st.set_page_config(page_title="WYSIWYG HTML Editor", layout="wide")
st.title("WYSIWYG HTML Editor")

# HTML, CSS, JS snippet for the editor
editor_html = '''
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  #toolbar { background: #f5f5f5; padding: 8px; border-bottom: 1px solid #ddd; display: flex; gap: 4px; }
  #toolbar button, #toolbar select, #toolbar input[type=color] { padding: 4px; font-size: 14px; }
  #container { display: flex; height: 80vh; }
  #editor, #code { flex: 1; padding: 8px; border: 1px solid #ddd; font-family: monospace; font-size: 14px; overflow: auto; }
  #editor { outline: none; }
  #tableControls { display: none; position: absolute; background: white; border: 1px solid #007acc; padding: 6px; z-index: 10; }
  #tableControls input { width: 100%; margin: 4px 0; }
  table.selected { outline: 2px solid #007acc; }
</style>

<div id="toolbar">
  <button onclick="exec('bold')">B</button>
  <button onclick="exec('italic')">I</button>
  <button onclick="exec('underline')">U</button>
  <select onchange="exec('formatBlock', this.value)">
    <option value="">Format</option>
    <option value="h1">H1</option>
    <option value="h2">H2</option>
    <option value="p">P</option>
  </select>
  <button onclick="exec('insertUnorderedList')">•</button>
  <button onclick="exec('insertOrderedList')">1.</button>
  <input type="color" onchange="exec('foreColor', this.value)">
  <button onclick="insertTable()">Table</button>
</div>

<div id="container">
  <div id="editor" contenteditable="true" onkeyup="update()" onclick="selectTable(event)">Type here...</div>
  <div style="position: relative; flex: 1;">
    <textarea id="code" onkeyup="sync()"></textarea>
    <div id="tableControls">
      <input id="w" placeholder="width (e.g.100%)">
      <input id="b" placeholder="border px">
      <input id="p" placeholder="padding px">
      <input id="s" placeholder="spacing px">
      <button onclick="apply()">OK</button>
      <button onclick="hide()">X</button>
    </div>
  </div>
</div>

<script>
  let selTable;
  function exec(cmd, val) { document.execCommand(cmd, false, val); update(); }
  function update() { document.getElementById('code').value = document.getElementById('editor').innerHTML; }
  function sync() { document.getElementById('editor').innerHTML = document.getElementById('code').value; }
  function insertTable() {
    const r = +prompt('rows',3), c = +prompt('cols',3);
    let t = '<table border="1" cellpadding="8" cellspacing="0">';
    for(let i=0;i<r;i++){ t += '<tr>' + '<td>Cell</td>'.repeat(c) + '</tr>'; }
    t += '</table>';
    exec('insertHTML', t);
  }
  function selectTable(e) {
    document.querySelectorAll('table').forEach(t=>t.classList.remove('selected'));
    selTable = e.target.closest('table');
    if (!selTable) return hide();
    selTable.classList.add('selected');
    const rect = selTable.getBoundingClientRect();
    const c = document.getElementById('tableControls');
    c.style.top = rect.bottom + 'px';
    c.style.left = rect.left + 'px';
    c.style.display = 'block';
    ['w','b','p','s'].forEach(id => {
      let attr = {w:'style.width', b:'border', p:'cellpadding', s:'cellspacing'}[id];
      document.getElementById(id).value = selTable[attr] || selTable.getAttribute(attr) || '';
    });
  }
  function apply() {
    selTable.style.width = document.getElementById('w').value;
    selTable.setAttribute('border', document.getElementById('b').value);
    selTable.setAttribute('cellpadding', document.getElementById('p').value);
    selTable.setAttribute('cellspacing', document.getElementById('s').value);
    update(); hide();
  }
  function hide() { document.getElementById('tableControls').style.display = 'none'; if(selTable) selTable.classList.remove('selected'); }
  document.addEventListener('selectionchange', ()=>{
    const sel = window.getSelection(); if (!sel.rangeCount) return;
    const html = sel.toString() && sel.getRangeAt(0).cloneContents().textContent.trim();
    if (!html) return;
    const code = document.getElementById('code');
    const idx = code.value.indexOf(html);
    if (idx>=0) { code.focus(); code.setSelectionRange(idx, idx+html.length); }
  });
  update();
</script>
'''

# render
html(editor_html, height=850)
