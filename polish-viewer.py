from pathlib import Path
p=Path(__file__).resolve().parent/'dist/app.js'
s=p.read_text(encoding='utf-8')
s=s.replace("focus.name||(focus.tag==='body'?'Document body':'No named element')", "focus.tag==='body'?'Document body':(focus.name||'No named element')")
s=s.replace("f.name||(f.tag==='body'?'Document body':f.tag||'—')", "f.tag==='body'?'Document body':(f.name||f.tag||'—')")
s=s.replace("const fixture=current.fixture?.publicPath;", "const candidate=current.fixture?.publicPath;const fixture=typeof candidate==='string'&&/^fixtures\\/campus\\.html\\?journey=(registration|dialog)&version=(broken|fixed)$/.test(candidate)?candidate:null;")
s=s.replace("const r=validateReport(JSON.parse(await file.text()));runs.push(r);", "const r=validateReport(JSON.parse(await file.text()));runs=runs.filter(existing=>existing.id!==r.id);runs.push(r);")
p.write_text(s, encoding='utf-8')
