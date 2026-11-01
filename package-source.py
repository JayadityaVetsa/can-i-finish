"""Create the self-contained source download, excluding caches, credentials and Git metadata."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
root = Path(__file__).resolve().parent
files = [root / name for name in ['package.json','package-lock.json','start.mjs','server.mjs','cli.mjs','record-apple.mjs','record-viewer.mjs','record-hd-fixtures.mjs','README.md','LICENSE','package-source.py']]
files.append(root / 'docs/apple-contract.json')
for folder in ['lib','tests','dist']:
    files.extend(p for p in (root / folder).rglob('*') if p.is_file() and p.suffix not in {'.zip','.mp4'})
with ZipFile(root / 'dist' / 'runner-source.zip', 'w', ZIP_DEFLATED) as archive:
    for file in files:
        archive.write(file, file.relative_to(root))
print('Packaged', len(files), 'source and demonstration files')
