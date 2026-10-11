#!/usr/bin/env python3
"""Feedback loss must stop MiniGimbal closed-loop output."""

import re
from pathlib import Path


source = (Path(__file__).resolve().parents[1] / "MiniGimbal.hpp").read_text()
update = source.split("void Update() {", 1)[1].split("void Control() {", 1)[0]
control = source.split("void Control() {", 1)[1].split("void OnMonitor()", 1)[0]

for motor in ("motor_small_pitch_", "motor_scope_"):
    assert not re.search(rf"^\s*{motor}->Update\(\);", update, re.M), f"{motor} discards its online status"
    assert re.search(rf"{motor}->Update\(\)", update), f"{motor} must still be updated"
    assert re.search(rf"{motor}->Relax\(\)", control), f"{motor} must relax on feedback loss"
assert re.search(r"(?:online|fault|status)", control, re.I), "Control must gate PID output on feedback health"
print("PASS: MiniGimbal feedback loss guard")
