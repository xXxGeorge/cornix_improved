#!/usr/bin/env python3
"""Cheap structural checks; native ZMK tests remain the behavioral authority."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
keymap = (ROOT / "config/cornix.keymap").read_text()
positions = (ROOT / "config/includes/cornix54.h").read_text()
layout = (ROOT / "boards/jzf/cornix/cornix-layouts.dtsi").read_text()
mapping = re.search(r"map\s*=\s*<(.*?)>;", layout, re.S).group(1)
count = len(re.findall(r"\bRC\(", mapping))
assert count == 50, f"Review migration: physical layout now has {count} positions"

layers = re.findall(r"layer(\d+)\s*\{(.*?)\n\s*\};", keymap, re.S)
assert [int(n) for n, _ in layers] == list(range(9))
for number, body in layers:
    bindings = re.search(r"\bbindings\s*=\s*<(.*?)>;", body, re.S).group(1)
    assert bindings.count("&") == count, f"Layer {number} has wrong binding count"

labels = dict((name, int(value)) for name, value in re.findall(
    r"^#define\s+([LR][TMBHP]\d)\s+(\d+)", positions, re.M))
assert set(labels.values()) == set(range(count)), "Position labels must cover the matrix"
assert len(labels.values()) == len(set(labels.values())), "Aliased position labels"
assert all(0 <= value < count for value in labels.values()), "Position outside the matrix"
assert [labels[k] for k in ['LM3','LM2','RM1','RM2','RM3']] == [14,15,19,20,21]

combos = (ROOT / "config/includes/kanata-combos.dtsi").read_text()
assert 'slow-release;' not in combos, "Review release tests before enabling slow-release"
assert 'RM1 RM3' not in combos, "J+L must retain normal HRM/letter ordering"
assert not re.search(r'layers\s*=\s*<[^>]*\b(?:FN|NAV|BT)\b', combos)
assert 'zmk-helpers' not in keymap, "Native keymap should not require helper macros"
print(f"Checked {len(layers)} layers, {count} positions, and combo scope invariants")
