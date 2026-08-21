"""Cross-platform single-keypress input (macOS/Linux + Windows)."""

import contextlib
import sys

try:                    # Windows
    import msvcrt
    WINDOWS = True
except ImportError:     # macOS / Linux
    import select
    import termios
    import tty
    WINDOWS = False


KEYS = {
    "\x1b[A": "UP",    "\x1b[B": "DOWN",   "\x1b[C": "RIGHT", "\x1b[D": "LEFT",
    "\x1b[H": "HOME",  "\x1b[F": "END",
    "\r": "ENTER",     "\n": "ENTER",      " ": "SPACE",      "\t": "TAB",
    "\x7f": "BACKSPACE",  "\x08": "BACKSPACE",
    "\x1b": "ESC",     "\x03": "CTRL_C",
}

# Windows sends two bytes for special keys: \x00 or \xe0, then one of these
WIN_KEYS = {
    "H": "UP", "P": "DOWN", "M": "RIGHT", "K": "LEFT",
    "G": "HOME", "O": "END", "S": "DELETE", "R": "INSERT",
}


def enable_ansi() -> None:
    """Windows needs VT processing switched on; no-op elsewhere."""
    if not WINDOWS:
        return
    import ctypes
    kernel32 = ctypes.windll.kernel32
    # ENABLE_PROCESSED_OUTPUT | ENABLE_WRAP_AT_EOL_OUTPUT
    # | ENABLE_VIRTUAL_TERMINAL_PROCESSING
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)


def supported() -> bool:
    """True if single-key input is actually available here."""
    if WINDOWS:
        return True
    try:
        return sys.stdin.isatty()
    except ValueError:
        return False


@contextlib.contextmanager
def cbreak_mode():
    """Single-key reads for the duration of the block."""
    if WINDOWS:
        yield                       # msvcrt already reads unbuffered
        return
    if not supported():
        raise RuntimeError(
            "stdin is not a terminal - single-key input unavailable.\n"
            "In IntelliJ: Run > Edit Configurations > "
            "tick 'Emulate terminal in output console'."
        )
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setcbreak(fd)
        yield
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)


def read_key() -> str:
    """Block for one keypress. Returns a KEYS name, or the raw character."""
    if WINDOWS:
        ch = msvcrt.getwch()
        if ch in ("\x00", "\xe0"):          # special-key prefix
            return WIN_KEYS.get(msvcrt.getwch(), "")
        return KEYS.get(ch, ch)

    ch = sys.stdin.read(1)
    if ch == "\x1b":                        # maybe an arrow key
        while select.select([sys.stdin], [], [], 0.001)[0]:
            ch += sys.stdin.read(1)
            if ch in KEYS or len(ch) > 5:
                break
    return KEYS.get(ch, ch)