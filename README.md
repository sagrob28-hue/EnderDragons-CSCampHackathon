# diagnosis.py

A colourful terminal symptom checker, built entirely in Python 3 with no external
dependencies. Pick your symptoms from a category menu, get a diagnosis with a
confidence score, a plain-English description, advice on when to actually see a
doctor, and a link to the relevant NHS page.

**By: Team Ender Dragons**

> **This is not a medical tool.** It matches sets of symptoms against a small
> hand-written database for fun. It cannot diagnose anything. If you are unwell,
> speak to a real doctor.

---

## Running it

Requires **Python 3.11+** (the code uses `StrEnum` and `match` statements) and a
real terminal.

```bash
python3 main.py
```

### If you are running this from IntelliJ or PyCharm

You **must** enable terminal emulation, or the program will exit with an error:

**Run → Edit Configurations… → tick "Emulate terminal in output console"**

Without it, `stdin` is not a terminal, so single-keypress input is impossible.
The program detects this and tells you rather than crashing with a traceback.

---

## Controls

Everything is single-keypress — no need to press Enter after each choice.

| Key | Action |
|-----|--------|
| `a` / `d` | Move up and down the list |
| `ENTER` | Select a category, or toggle a symptom on/off |
| `v` | View your currently selected symptoms |
| `h` | Show the help screen |
| `q` | Get your diagnosis |
| `x` | Go back, or exit from the main menu |

---

## How it works

### Symptoms are a closed vocabulary

`Symptom` is a frozen dataclass that validates its name against
`Symptom.POSSIBLE_SYMPTOMS`, a dict of **11 categories** covering **90 unique
symptoms**. Names are normalised with `.strip().casefold()` before checking, and
an invalid name raises `ValueError` — so a `Symptom` object is always valid.

| Category | Symptoms |
|---|---|
| General | 13 |
| Head and Nervous System | 14 |
| Eyes | 5 |
| Ears, Nose and Throat | 11 |
| Chest and Breathing | 7 |
| Heart and Circulation | 11 |
| Stomach and Digestion | 13 |
| Urinary | 4 |
| Muscles, Bones and Joints | 7 |
| Skin, Hair and Nails | 8 |
| Sleep and Mood | 6 |

A few symptoms deliberately appear in more than one category — `jaundice` is
listed under both Skin and Digestion, because that is where people will look for
it. Since selections are stored in a set, picking the same symptom twice is
harmless.

### Matching is set similarity

`SymptomSet` wraps a `frozenset` of symptoms and overloads `@` (`__matmul__`) to
return the **Jaccard index** between two sets:

```
        |A ∩ B|
A @ B = ————————
        |A ∪ B|
```

That single number is the confidence score. `Diagnoser.diagnosis` scores your
selected symptoms against all **61 conditions** and returns the best match along
with its score.

Because Jaccard divides by the *union*, picking few symptoms caps your possible
confidence — select 3 symptoms against a 6-symptom condition and a perfect
partial match still scores 50%. Low percentages are normal and expected.

### Each condition carries real information

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Condition:
    name: str
    description: str
    when_to_seek_care: str
    link: str
```

All 61 NHS links were checked programmatically and return HTTP 200 with no
redirects.

---

## Project layout

| File | Contains |
|---|---|
| `main.py` | Menu screens, the main loop, and terminal setup/teardown |
| `diagnosis.py` | `Symptom`, `SymptomSet`, `Condition`, `Diagnoser` and the database |
| `ansi.py` | The `Ansi` escape-sequence enum and `IOUtils` |
| `keyboard.py` | Cross-platform single-keypress input |
| `loading_screen.py` | ASCII-art title screen and rainbow animation |

### `ansi.py`

`Ansi` is a `StrEnum`, so its members *are* strings and drop straight into
f-strings without `.value`:

```python
from ansi import Ansi

print(f"{Ansi.BOLD}{Ansi.RED}warning{Ansi.RESET}")
```

Alongside the constants there are helpers for things that take parameters —
`Ansi.fg(n)` and `Ansi.bg(n)` for 256-colour, `Ansi.to_hex(n)` to convert a
palette index to `#rrggbb`, and `Ansi.set_color(n)`, which sets the text colour
*and* the caret colour (OSC 12, a separate channel from normal text colour) and
flushes immediately.

Each category has its own colour, so the screen tells you where you are before
you read the header. The palette is tuned for a light terminal background.

### `keyboard.py`

Single keypresses without pressing Enter, on both macOS/Linux and Windows:

- **Unix** uses `termios` + `tty.setcbreak`, which disables echo and line
  buffering while leaving `Ctrl+C` working.
- **Windows** uses `msvcrt.getwch()`.
- Arrow keys are encoded completely differently on each platform (`\x1b[A` vs
  `\xe0` + `H`), so there are two lookup tables.
- `enable_ansi()` switches on VT processing, which Windows ships disabled.
- The terminal is always restored via `finally`, so a crash cannot leave your
  shell without echo.

---

## Known limitations

- Only the single best match is shown. Several conditions share symptoms, so the
  runner-up is often just as plausible.
- Symptom overlap is not weighted: `fatigue` appears in many conditions and
  counts exactly as much as a far more specific symptom like `facial droop`.
- The database is 61 conditions of simplified textbook presentations. Real
  illnesses vary enormously, overlap, and frequently occur together.
