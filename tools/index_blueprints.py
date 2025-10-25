#!/usr/bin/env python3
import os
import re
import shutil
from pathlib import Path

ROOT = Path("/Users/invinciblelude/728 Cordant project/blueprints")
INCOMING = ROOT / "incoming"
CLASSIFIED = ROOT / "classified"
UNMATCHED = ROOT / "_unmatched"

# Map leading sheet prefix letters to folders
PREFIX_MAP = {
    "A": CLASSIFIED / "ARCH",
    "S": CLASSIFIED / "STRUCT",
    "E": CLASSIFIED / "MEP" / "ELEC",
    "P": CLASSIFIED / "MEP" / "PLUMB",
    "M": CLASSIFIED / "MEP" / "MECH",
    "C": CLASSIFIED / "CIVIL",
    "L": CLASSIFIED / "LANDSCAPE",
    "G": CLASSIFIED / "GENERAL",
    "T": CLASSIFIED / "GENERAL",  # sometimes title/typical
    "D": CLASSIFIED / "DETAILS",   # some sets use D for details
}

# Keywords fallback if prefix not clear
KEYWORDS = [
    (re.compile(r"elect(ric|rical|ricity)|lighting|switch|panel|recept|outlet", re.I), CLASSIFIED / "MEP" / "ELEC"),
    (re.compile(r"plumb|sanitary|waste|vent|water heater|WH|fixture schedule", re.I), CLASSIFIED / "MEP" / "PLUMB"),
    (re.compile(r"mech|HVAC|duct|supply|return|VAV|AHU|furnace|heat pump|condens", re.I), CLASSIFIED / "MEP" / "MECH"),
    (re.compile(r"struct|beam|joist|rebar|foundation|footing|shear|holdown|HDU|anchor", re.I), CLASSIFIED / "STRUCT"),
    (re.compile(r"civil|grading|drain|erosion|utility plan|site", re.I), CLASSIFIED / "CIVIL"),
    (re.compile(r"landscape|planting|irrigation", re.I), CLASSIFIED / "LANDSCAPE"),
    (re.compile(r"detail|section|enlarge|blow-?up", re.I), CLASSIFIED / "DETAILS"),
    (re.compile(r"general|legend|notes|symbols|index", re.I), CLASSIFIED / "GENERAL"),
    (re.compile(r"floor plan|elevation|window|door|finish|reflected ceiling|RCP|interior", re.I), CLASSIFIED / "ARCH"),
]

SHEET_REGEX = re.compile(r"^([A-Z])\s*-?\s*([0-9]+(?:\.[0-9]+)?)", re.I)


def ensure_dirs():
    for p in [ROOT, INCOMING, CLASSIFIED, UNMATCHED]:
        p.mkdir(parents=True, exist_ok=True)


def classify_path(path: Path):
    stem = path.stem
    m = SHEET_REGEX.match(stem)
    if m:
        prefix = m.group(1).upper()
        return PREFIX_MAP.get(prefix)
    # keyword fallback
    searchable_text = f"{stem} {path.parent.name} {str(path.parent)}"
    for regex, target in KEYWORDS:
        if regex.search(searchable_text):
            return target
    return None


def move_file(src: Path, dest_dir: Path):
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / src.name
    # avoid overwrite
    if dest.exists():
        base = dest.stem
        ext = dest.suffix
        i = 1
        while True:
            candidate = dest_dir / f"{base} ({i}){ext}"
            if not candidate.exists():
                dest = candidate
                break
            i += 1
    shutil.move(str(src), str(dest))


def main():
    ensure_dirs()
    if not INCOMING.exists():
        print(f"Incoming folder not found: {INCOMING}")
        return

    count = 0
    unmatched = 0
    for entry in sorted(INCOMING.rglob("*")):
        if not entry.is_file():
            continue
        if entry.suffix.lower() not in [".jpg", ".jpeg", ".png"]:
            continue
        target_dir = classify_path(entry)
        if target_dir is None:
            target_dir = UNMATCHED
            unmatched += 1
        move_file(entry, target_dir)
        count += 1
    print(f"Processed {count} files. Unmatched: {unmatched}. Classified output: {CLASSIFIED}")

if __name__ == "__main__":
    main()
