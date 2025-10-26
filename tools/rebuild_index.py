#!/usr/bin/env python3
"""
Rebuild docs/assets/index.json from classified blueprints.
"""
import json
from pathlib import Path

root = Path('/Users/invinciblelude/728 Cordant project/docs/blueprints')
out = Path('/Users/invinciblelude/728 Cordant project/docs/assets/index.json')

sections = [
    ('ARCH', root / 'classified' / 'ARCH'),
    ('STRUCT', root / 'classified' / 'STRUCT'),
    ('MEP/ELEC', root / 'classified' / 'MEP' / 'ELEC'),
    ('MEP/MECH', root / 'classified' / 'MEP' / 'MECH'),
    ('MEP/PLUMB', root / 'classified' / 'MEP' / 'PLUMB'),
    ('CIVIL', root / 'classified' / 'CIVIL'),
    ('SITE', root / 'classified' / 'SITE'),
    ('LANDSCAPE', root / 'classified' / 'LANDSCAPE'),
    ('DETAILS', root / 'classified' / 'DETAILS'),
    ('SCHEDULES', root / 'classified' / 'SCHEDULES'),
    ('GENERAL', root / 'classified' / 'GENERAL'),
    ('_unmatched', root / '_unmatched'),
]

idx = {}
for name, folder in sections:
    files = []
    if folder.exists():
        for p in sorted(list(folder.glob('*.jp*g')) + list(folder.glob('*.png'))):
            files.append({
                'name': p.name,
                'href': '/blueprints/' + str(p.relative_to(root)).replace('\\', '/')
            })
    idx[name] = files

out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(idx, indent=2))

print(f"✅ Updated {out}")
print(f"Categories: {dict((k, len(v)) for k, v in idx.items())}")

