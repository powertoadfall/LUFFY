import hashlib
import re

path = 'README.md'
text = open(path, encoding='utf-8').read()
start_marker = '### 📝 Complete TODO List\n\n'
end_marker = '\n## 🤝 Contributing'
start = text.index(start_marker) + len(start_marker)
end = text.index(end_marker, start)
block = text[start:end]

pattern = re.compile(r'^- \[ \] \*\*(.+?):(\d+)\*\* - (.*)$')
entries = []
for line in block.split('\n'):
    if not line.strip():
        continue
    match = pattern.match(line)
    if not match:
        raise SystemExit('Unexpected TODO line: ' + line)
    entries.append((match.group(1), int(match.group(2)), match.group(3)))

remove = {
    'luffy/deepscaler/utils.py': {45, 46, 47, 48, 49},
    'luffy/verl/verl/protocol.py': {114, 115, 116, 131, 132, 134},
}
update = {
    'luffy/deepscaler/utils.py': {
        50: 45, 51: 46, 52: 47,
        88: 107, 89: 108, 90: 109, 91: 110,
        92: 111, 93: 112, 94: 113, 95: 114,
    },
    'luffy/verl/verl/protocol.py': {
        117: 114, 118: 115,
        133: 136, 135: 137,
        156: 169, 252: 265, 338: 351,
    },
}

new_entries = []
for file_path, line_number, description in entries:
    if line_number in remove.get(file_path, set()):
        continue
    line_number = update.get(file_path, {}).get(line_number, line_number)
    new_entries.append((file_path, line_number, description))

new_entries.sort(key=lambda item: (item[0], item[1]))
new_block = ''.join(f'- [ ] **{file_path}:{line_number}** - {description}\n'
                    for file_path, line_number, description in new_entries)
new_text = text[:start] + new_block + text[end:]
new_text = new_text.rstrip('\n') + '\n\n'
with open(path, 'w', encoding='utf-8') as handle:
    handle.write(new_text)

data = new_text.encode('utf-8')
sha = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
print('entries:', len(new_entries))
print('bytes:', len(data))
print('blob sha:', sha)
if sha != '2d0e63fbb656bd00df4a9528b41bc09c1a925ddf':
    raise SystemExit('Unexpected README result: ' + sha)
