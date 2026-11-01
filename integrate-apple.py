from pathlib import Path
root = Path(__file__).resolve().parent
html = root / 'dist/index.html'
s = html.read_text(encoding='utf-8')
s = s.replace('<span>Northstar Campus<small>Controlled demonstration</small></span>', '<span id="workspace-site">Northstar Campus<small>Controlled demonstration</small></span>')
s = s.replace('<nav aria-label="Journeys">', '<nav aria-label="Journeys"><button class="journey" data-journey="apple-voiceover"><span>↗</span><span>Apple · VoiceOver guide<small>Real public-site task</small></span><b>LIVE</b></button>')
s = s.replace('<strong>Registration details</strong>', '<strong id="finish-goal">Registration details</strong>')
s = s.replace('<button class="side-action" id="method">', '<a class="side-action" href="demo.html">▶ Watch the demo</a><button class="side-action" id="method">')
s = s.replace('<span>Northstar Campus <span>', '<span>Northstar Campus <span>')
s = s.replace('Northstar Campus <span>/</span>', '<span id="breadcrumb-site">Northstar Campus</span> <span>/</span>')
s = s.replace('<h3>Registration details</h3>', '<h3>Registration details</h3>')
html.write_text(s, encoding='utf-8')
app = root / 'dist/app.js'
s = app.read_text(encoding='utf-8')
s = s.replace('renderFindings();renderTrace();showFrame(', 'decorateRun();renderFindings();renderTrace();showFrame(')
s = s.replace("function renderComparison(){const before", "function renderComparison(){document.querySelector('.fix-panel').hidden=false;const before")
s = s.replace("if(!before||!after){$('contract-match')", "if(!before||!after){document.querySelector('.fix-panel').hidden=true;$('contract-match')")
s = s.replace("$('compare-button').onclick=()=>setView('compare');", "$('compare-button').onclick=()=>{if(current?.external){journey='registration';variant='broken';selectRun();}setView('compare');};")
s = s.replace("runs=data.runs.map(validateReport);$('generated')", "runs=data.runs.map(validateReport);try{const external=await fetch('evidence/apple-voiceover.json');if(external.ok){const apple=validateReport(await external.json());runs.push(apple);journey=apple.id;}}catch{}$('generated')")
s += '''
function decorateRun(){
 const external=!!current.external;
 $('finish-goal').textContent=current.contract.goal||'Defined task assertion';
 $('workspace-site').replaceChildren(document.createTextNode(external?'Apple.com':'Northstar Campus'),element('small',{text:external?'Independent live-site observation':'Controlled demonstration'}));
 $('breadcrumb-site').textContent=external?'Apple.com':'Northstar Campus';
 if(external)$('crumb').textContent='iPhone VoiceOver setup';
 document.querySelector('.variant-control').hidden=external||!current.fixture;
 $('compare-button').textContent=external?'See a controlled fix comparison ↗':'Compare before & after ↗';
 $('frame').style.aspectRatio=`${current.engine?.viewport?.width||1280} / ${current.engine?.viewport?.height||900}`;
 if(external){$('fixture-link').hidden=false;$('fixture-link').textContent='Open Apple task page ↗';$('fixture-link').href='https://www.apple.com/accessibility/';$('run-summary').textContent=current.outcome==='passed'?'Reached Apple’s iPhone VoiceOver setup article using only the recorded keyboard sequence. This is one task observation, not an audit of Apple.':current.findings[0]?.summary||'The recorded sequence did not complete.';}
 else $('fixture-link').textContent='Try fixture ↗';
}
'''
app.write_text(s, encoding='utf-8')
