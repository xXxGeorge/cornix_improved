"""Generate independent input/output specifications for ZMK's native runner.

Delays are AFTER each event (the mock driver also delays the first event by
its own delay). Expected HID events are written by hand, never accepted from
the implementation. Run with Python 3, then from zmk/app execute
`./run-test.sh <absolute-path-to-tests/kanata/generated>`.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent / "generated"


def down(pos, delay=8):
    return ("PRESS", pos, delay)


def up(pos, delay=8):
    return ("RELEASE", pos, delay)


def hid(state, code, implicit=0, explicit=0):
    return (f"{state}: usage_page 0x07 keycode 0x{code:02X} "
            f"implicit_mods 0x{implicit:02X} explicit_mods 0x{explicit:02X}")


def press(code, implicit=0, explicit=0):
    return hid("pressed", code, implicit, explicit)


def release(code, implicit=0, explicit=0):
    return hid("released", code, implicit, explicit)


def tap(code, implicit=0):
    return [press(code, implicit), release(code, implicit)]


def select_layer(position):
    # Use the actual Bluetooth-layer selectors; no test-only layer shortcut.
    return [down(40, 30), down(position, 30), up(position), up(40, 40)]


CASES = {
    # Physical S/D = 14/15; J/K/L = 19/20/21. Letters use USB HID usages.
    "sd-symbol": ([down(14), down(15, 40), up(14), up(15)], tap(0x2D, 2)),
    "ds-symbol": ([down(15), down(14, 40), up(15), up(14)], tap(0x2D, 2)),
    "jk-symbol": ([down(19), down(20, 40), up(19), up(20)], tap(0x34)),
    "kl-symbol": ([down(20), down(21, 40), up(20), up(21)], tap(0x34, 2)),
    "typing-idle-protection": (
        [down(1), up(1), down(14), down(15), up(14), up(15)],
        tap(0x14) + [press(0x16), press(0x07), release(0x16), release(0x07)]),
    "same-hand-nested-no-mod": (
        [down(14, 40), down(16, 30), up(16), up(14)],
        [press(0x16), press(0x09), release(0x09), release(0x16)]),
    "jl-keeps-order": (
        [down(19), down(21, 40), up(21), up(19)],
        [press(0x0D), press(0x0F), release(0x0F), release(0x0D)]),
    "lj-keeps-order": (
        [down(21), down(19, 40), up(19), up(21)],
        [press(0x0F), press(0x0D), release(0x0D), release(0x0F)]),
    "single-hrm-cross-hand": (
        [down(14, 40), down(18, 30), up(18), up(14)],
        [press(0xE0), press(0x0B), release(0x0B), release(0xE0)]),
    "sd-held-modifiers": (
        [down(14), down(15, 320), down(18, 30), up(18), up(14), up(15)],
        [press(0xE1, explicit=1), press(0x0B), release(0x0B),
         release(0xE1, explicit=1)]),
    "sd-cross-hand-early-hold": (
        [down(14), down(15, 40), down(18, 30), up(18), up(14), up(15)],
        [press(0xE1, explicit=1), press(0x0B), release(0x0B),
         release(0xE1, explicit=1)]),
    "jk-held-add-alt": (
        [down(19), down(20, 320), down(13, 320), down(1, 30),
         up(1), up(13), up(19), up(20)],
        [press(0xE5, explicit=128), press(0xE2), press(0x14), release(0x14),
         release(0xE2), release(0xE5, explicit=128)]),
    "consecutive-symbol-combos": (
        [down(14), down(15, 40), up(14), up(15, 30),
         down(19), down(20, 40), up(19), up(20, 30),
         down(20), down(21, 40), up(20), up(21)],
        tap(0x2D, 2) + tap(0x34) + tap(0x34, 2)),
    "symbol-layer-numbers": (
        [down(42, 240), down(14), down(15, 40), up(14), up(15), up(42)],
        tap(0x2E)),
    "thumb-escape-tap": ([down(42, 40), up(42)], tap(0x29)),
    "caps-escape-tap": ([down(12, 40), up(12)], tap(0x29)),
    "thumb-backspace": ([down(44, 40), up(44)], tap(0x2A)),
    "base-return": ([down(23, 40), up(23)], tap(0x28)),
    "thumb-f13-tap": ([down(43, 40), up(43)], tap(0x68)),
    "thumb-shifts": (
        [down(41), down(46), up(41), up(46)],
        [press(0xE1), press(0xE5), release(0xE1), release(0xE5)]),
    "thumb-function-hold": (
        [down(43), down(19, 30), up(19), up(43)], tap(0x40)),
    "space-roll-remains-text": (
        [down(45, 30), down(1, 30), up(45), up(1)],
        [press(0x2C), press(0x14), release(0x2C), release(0x14)]),
    "navigation-disables-hrm-combos": (
        [down(12, 240), down(19), down(20, 40), up(19), up(20), up(12)],
        [press(0x51), press(0x52), release(0x51), release(0x52)]),
    "function-disables-symbol-combos": (
        [down(40, 30), down(35, 30), up(35), up(40, 30), down(2), down(3, 40), up(2), up(3)],
        [press(0x1A), press(0x08), release(0x1A), release(0x08)]),
    "function-homerow-fkeys": (
        [down(43, 240), down(14), down(15, 40), up(14), up(15), up(43)],
        [press(0x3B), press(0x3C), release(0x3B), release(0x3C)]),
    "number-thumb-taps": (
        select_layer(19) +
        [down(41, 40), up(41), down(42, 40), up(42), down(43, 40), up(43),
         down(44, 40), up(44), down(45, 40), up(45), down(46, 40), up(46)],
        tap(0xE1) + tap(0x29) + tap(0x68) + tap(0x2A) + tap(0x2C) + tap(0xE5)),
    "symbols-transparent-thumb-taps": (
        select_layer(34) +
        [down(41, 40), up(41), down(42, 40), up(42), down(43, 40), up(43),
         down(44, 40), up(44), down(45, 40), up(45), down(46, 40), up(46)],
        tap(0xE1) + tap(0x29) + tap(0x68) + tap(0x2A) + tap(0x2C) + tap(0xE5)),
    "number-function-release-restores-number": (
        select_layer(19) +
        [down(43, 240), down(13, 30), up(13), up(43, 40), down(19, 30), up(19)],
        tap(0x3A) + tap(0x5C)),  # F1, keypad 4
    "number-symbols-release-restores-number": (
        select_layer(19) +
        [down(42, 240), down(13, 30), up(13), up(42, 40), down(19, 30), up(19)],
        tap(0x1E) + tap(0x5C)),  # 1, keypad 4
    "symbols-function-release-restores-symbols": (
        select_layer(34) +
        [down(43, 240), down(13, 30), up(13), up(43, 40), down(13, 30), up(13)],
        tap(0x3A) + tap(0x1E)),
    "symbols-released-before-function": (
        [down(42, 240), down(43, 240), down(13, 30), up(13), up(42, 40),
         down(13, 30), up(13), up(43, 40), down(1, 30), up(1)],
        tap(0x3A) + tap(0x3A) + tap(0x14)),  # FN survives, then back to Base Q
    "function-released-before-symbols": (
        [down(42, 240), down(43, 240), down(13, 30), up(13), up(43, 40),
         down(13, 30), up(13), up(42, 40), down(1, 30), up(1)],
        tap(0x3A) + tap(0x1E) + tap(0x14)),  # FN -> Symbols -> Base
    "symbols-backspace-double-tap-no-caps-word": (
        select_layer(34) +
        [down(44, 30), up(44, 30), down(44, 30), up(44, 40)] +
        select_layer(18) + [down(1, 30), up(1)],
        tap(0x2A) + tap(0x2A) + tap(0x14)),
}


def main():
    # Remove obsolete generated fixtures after a case is renamed. Preserve
    # downloaded build logs and any other files in the same directories.
    if ROOT.exists():
        for folder in ROOT.iterdir():
            if folder.is_dir() and folder.name not in CASES:
                for filename in ("native_sim.keymap", "native_sim.conf",
                                 "events.patterns", "keycode_events.snapshot"):
                    (folder / filename).unlink(missing_ok=True)
    for name, (events, expected) in CASES.items():
        held = set()
        for kind, pos, delay in events:
            assert 0 <= pos < 50 and delay > 0, name
            if kind == "PRESS":
                assert pos not in held, (name, "duplicate press", pos)
                held.add(pos)
            else:
                assert pos in held, (name, "unmatched release", pos)
                held.remove(pos)
        assert not held, (name, "keys left held", held)
        folder = ROOT / name
        folder.mkdir(parents=True, exist_ok=True)
        # The final delay lets queued releases/log messages drain before exit.
        events = events[:-1] + [(events[-1][0], events[-1][1], 500)]
        sequence = "\n".join(
            f"    ZMK_MOCK_{kind}({pos // 10},{pos % 10},{delay})"
            for kind, pos, delay in events)
        (folder / "native_sim.keymap").write_text(
            '#include "../../fixture.dtsi"\n&kscan { events = <\n' + sequence + '\n>; };\n')
        (folder / "native_sim.conf").write_text(
            'CONFIG_ZMK_POINTING=y\nCONFIG_ZMK_BLE=n\nCONFIG_GPIO=n\n')
        (folder / "events.patterns").write_text('s/.*hid_listener_keycode_//p\n')
        (folder / "keycode_events.snapshot").write_text("\n".join(expected) + "\n")
    print(f"Generated {len(CASES)} ZMK event regression cases")


if __name__ == "__main__":
    main()
