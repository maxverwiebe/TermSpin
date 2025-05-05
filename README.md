# TermSpin

*A tiny Python 3 helper for stylish terminal feedback.*

---

## Features

* Animated **spinners** & progress **bars** with ANSI colours
* Context‑manager API (`with Spinner(): …`)
* Configurable speed, colours, symbols
* ETA calculation for progress bars
* Zero dependencies – pure standard library

## Installation

1. Clone this repo
2. Move termspin dir into your project src code
3. Import termspin as seen in the examples
 
*PyPi coming soon :)*

## Quick Start

```python
# example1.py
from termspin import Spinner, SpinnerStyle

with Spinner(text="Thinking", theme=SpinnerStyle.WAVE, color="\033[96m"):
    heavy_calculation()
```

```python
# example2.py
from termspin import ProgressBar, BarStyle

bar = ProgressBar(total=100, style=BarStyle.STRIPED, show_eta=True)
for _ in range(100):
    do_work()
    bar.step()
bar.finish()
```

---

## Spinner Themes

| Enum    | Preview           |   |
| ------- | ----------------- | - |
| `DOTS`  | ⠋⠙⠹⠸⠼ …           |   |
| `LINE`  | - \\              | / |
| `ARROW` | → ↘ ↓ ↙ ← ↖ ↑ ↗   |   |
| `EARTH` | 🌍 🌎 🌏          |   |
| `CLOCK` | 🕛 🕐 🕑 … 🕚     |   |
| `WAVE`  | ▁ ▂ ▃ ▄ ▅ ▆ ▇ █ … |   |

## Progress‑Bar Styles

| Enum      | Fill | Empty | Borders |   |
| --------- | ---- | ----- | ------- | - |
| `CLASSIC` | =    | -     | \[ ]    |   |
| `BOLD`    | ■    | ␣     | ❮ ❯     |   |
| `MINIMAL` | \*   | ␣     |         |   |
| `HASH`    | #    | .     | \[ ]    |   |
| `EMOJI`   | 🚀   | ✨     | 🚩 🎯   |   |
| `ROUNDED` | ●    | ○     | ( )     |   |
| `STRIPED` | ▉    | ▏     | \[ ]    |   |
| `DOT`     | •    | ·     | { }     |   |
| `HEART`   | ❤    | ♡     | ❤ ❤     |   |
| `MUSIC`   | ♫    | ♩     | ♪ ♪     |   |
| `DNA`     | ▰    | ▱     | ⎡ ⎤     |   |
| `PIXEL`   | █    | ░     | ▐ ▌     |   |
