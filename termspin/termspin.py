from __future__ import annotations

import sys
import threading
import time
from enum import Enum, auto
from typing import Callable, Sequence

_ESC = "\033["
_RESET = f"{_ESC}0m"
_HIDE = f"{_ESC}?25l"
_SHOW = f"{_ESC}?25h"
_CLEAR_LINE = f"{_ESC}2K"
_CARRIAGE = "\r"

class SpinnerStyle(Enum):
    """Different styles for the Spinner."""
    DOTS = auto()
    LINE = auto()
    ARROW = auto()
    EARTH = auto()
    CLOCK = auto()
    WAVE = auto()

    def frames(self) -> Sequence[str]:
        return {
            SpinnerStyle.DOTS:  ("⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"),
            SpinnerStyle.LINE:  ("-", "\\", "|", "/"),
            SpinnerStyle.ARROW: ("→", "↘", "↓", "↙", "←", "↖", "↑", "↗"),
            SpinnerStyle.EARTH: ("🌍", "🌎", "🌏"),
            SpinnerStyle.CLOCK: ("🕛", "🕐", "🕑", "🕒", "🕓", "🕔", "🕕", "🕖", "🕗", "🕘", "🕙", "🕚"),
            SpinnerStyle.WAVE:  ("▁", "▂", "▃", "▄", "▅", "▆", "▇", "█", "▇", "▆", "▅", "▄", "▃", "▂", "▁"),
        }[self]


class Spinner:
    """Shows a spinner."""
    def __init__(
        self,
        text: str = "",
        *,
        theme: SpinnerStyle = SpinnerStyle.DOTS,
        color: str = "\033[32m",
        interval: float = 0.1,
        final_symbol: str | None = None,
        final_text: str | None = None,
        callback: Callable[[], None] | None = None,
    ):
        self._text = text
        self._theme = theme
        self._color = color
        self._interval = interval
        self._final_symbol = final_symbol or "✔"
        self._final_text = final_text or " Done"
        self._callback = callback

        self._stop_evt = threading.Event()
        self._thread: threading.Thread | None = None

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc, tb):
        self.stop()

    def start(self):
        if self._thread and self._thread.is_alive():
            return  # already running
        self._stop_evt.clear()
        self._thread = threading.Thread(target=self._animate, daemon=True)
        sys.stdout.write(_HIDE)
        self._thread.start()

    def stop(self) -> None:
        self._stop_evt.set()
        if self._thread:
            self._thread.join()
            
        # clear spinner and show final symbol/text
        sys.stdout.write(f"{_CLEAR_LINE}{_CARRIAGE}{self._color}{self._final_symbol}{_RESET} {self._final_text}\n")
        sys.stdout.write(_SHOW)
        sys.stdout.flush()
        if self._callback:
            self._callback()

    def _animate(self) -> None:
        frames = self._theme.frames()
        idx = 0
        while not self._stop_evt.is_set():
            frame = frames[idx % len(frames)]
            sys.stdout.write(
                f"{_CARRIAGE}{_CLEAR_LINE}{self._color}{frame}{_RESET} {self._text}"
            )
            sys.stdout.flush()
            idx += 1
            time.sleep(self._interval)

# From here ProgressBar --

class BarStyle(Enum):
    """Different styles for the ProgressBar."""
    
    CLASSIC = auto()
    BOLD = auto()
    MINIMAL = auto()
    HASH = auto()
    EMOJI = auto()
    ROUNDED = auto()
    STRIPED = auto()
    DOT = auto()
    HEART = auto()
    MUSIC = auto()
    DNA = auto()
    PIXEL = auto()

    def spec(self):
        return {
            BarStyle.CLASSIC: dict(width=30, fill="=", empty="-", left="[", right="]", color="\033[34m"),
            BarStyle.BOLD: dict(width=50, fill="■", empty=" ", left="❮", right="❯", color="\033[35m"),
            BarStyle.MINIMAL: dict(width=20, fill="*", empty=" ", left="", right="", color="\033[36m"),
            BarStyle.HASH: dict(width=40, fill="#", empty=".", left="[", right="]", color="\033[32m"),
            BarStyle.EMOJI: dict(width=25, fill="🚀", empty="✨", left="🚩", right="🎯", color="\033[33m"),
            BarStyle.ROUNDED: dict(width=30, fill="●", empty="○", left="(",  right=")", color="\033[96m"),
            BarStyle.STRIPED: dict(width=40, fill="▉", empty="▏", left="[",  right="]", color="\033[91m"),
            BarStyle.DOT:     dict(width=35, fill="•", empty="·", left="{",  right="}", color="\033[94m"),
            BarStyle.HEART:   dict(width=25, fill="❤", empty="♡", left="❤", right="❤", color="\033[31m"),
            BarStyle.MUSIC:   dict(width=35, fill="♫", empty="♩", left="♪",  right="♪", color="\033[95m"),
            BarStyle.DNA:     dict(width=30, fill="▰", empty="▱", left="⎡",  right="⎤", color="\033[92m"),
            BarStyle.PIXEL:   dict(width=40, fill="█", empty=" ░", left="▐",  right="▌", color="\033[90m"),
        }[self]


class ProgressBar:
    """Simple textual progress bar with optional 'live' ETA."""

    def __init__(
        self,
        total: int,
        *,
        style: BarStyle = BarStyle.CLASSIC,
        show_percent: bool = True,
        show_eta: bool = False,
        update_interval: float = 0.1,
        callback: Callable[[], None] | None = None,
    ) -> None:
        self._total = max(1, total)
        self._style = style
        self._show_percent = show_percent
        self._show_eta = show_eta
        self._interval = update_interval
        self._callback = callback

        cfg = style.spec()
        self._width = cfg["width"]
        self._fill = cfg["fill"]
        self._empty = cfg["empty"]
        self._left = cfg["left"]
        self._right = cfg["right"]
        self._color = cfg["color"]

        self._value = 0
        self._start_time: float | None = None
        self._lock = threading.Lock()
        self._done_evt = threading.Event()
        self._thread = threading.Thread(target=self._render_loop, daemon=True)
        self._thread.start()

    def step(self, n: int = 1) -> None:
        with self._lock:
            if self._start_time is None:
                self._start_time = time.time()
            self._value = min(self._total, self._value + n)
            if self._value >= self._total:
                self._done_evt.set()

    def finish(self):
        self._value = self._total
        self._done_evt.set()
        self._thread.join()
        sys.stdout.write("\n" + _SHOW)
        sys.stdout.flush()
        if self._callback:
            self._callback()

    def _render_loop(self):
        sys.stdout.write(_HIDE)
        while not self._done_evt.is_set():
            self._render()
            time.sleep(self._interval)
        self._render()  # final render
        sys.stdout.write(_RESET)

    def _render(self):
        with self._lock:
            ratio = self._value / self._total
            filled = int(ratio * self._width)
            empty = self._width - filled
            bar = f"{self._left}{self._fill * filled}{self._empty * empty}{self._right}"
            pieces: list[str] = [self._color + bar + _RESET]
            if self._show_percent:
                pieces.append(f" {ratio * 100:6.2f}%")
            if self._show_eta and self._start_time is not None and self._value:
                elapsed = time.time() - self._start_time
                remaining = elapsed * (self._total / self._value - 1)
                pieces.append(f" ETA {remaining:6.1f}s")
            sys.stdout.write(f"{_CARRIAGE}{_CLEAR_LINE}{''.join(pieces)}")
            sys.stdout.flush()