from enum import StrEnum
from sys import stdout
from platform import system
from subprocess import run

class IOUtils:

    """A class that has to do with input and output."""

    __slots__ = ()

    @staticmethod
    def sanitized(string: str, /):

        """Gets rid of leading and trailing whitespace,
        as well as making the string lowercase and
        normalizing non-ASCII characters."""

        return string.strip().casefold()

    @staticmethod
    def clear():

        """Clears the terminal using the subprocess module.
        This function works with both Mac and Windows."""

        command = "cls" if system() == "Windows" else "clear"
        run(command, shell=True)

    @staticmethod
    def write(prompt: str=""):

        """Writes to the terminal."""

        stdout.write(prompt)

_LEVELS = (0, 95, 135, 175, 215, 255)

class Ansi(StrEnum):
    """ANSI escape sequences. Members are real strings."""

    RESET = "\033[0m"

    # --- styles ---
    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    REVERSE = "\033[7m"
    HIDDEN = "\033[8m"
    STRIKE = "\033[9m"

    # --- styles off ---
    NO_BOLD = "\033[22m"
    NO_ITALIC = "\033[23m"
    NO_UNDERLINE = "\033[24m"
    NO_BLINK = "\033[25m"
    NO_REVERSE = "\033[27m"
    NO_STRIKE = "\033[29m"

    # --- foreground ---
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    DEFAULT = "\033[39m"

    # --- bright foreground ---
    BRIGHT_BLACK = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"

    # --- background ---
    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"
    BG_DEFAULT = "\033[49m"

    # --- bright background ---
    BG_BRIGHT_BLACK = "\033[100m"
    BG_BRIGHT_RED = "\033[101m"
    BG_BRIGHT_GREEN = "\033[102m"
    BG_BRIGHT_YELLOW = "\033[103m"
    BG_BRIGHT_BLUE = "\033[104m"
    BG_BRIGHT_MAGENTA = "\033[105m"
    BG_BRIGHT_CYAN = "\033[106m"
    BG_BRIGHT_WHITE = "\033[107m"

    CURSOR_RESET = "\033]112\033\\"
    BEGIN_SYNC = "\033[?2026h"
    END_SYNC = "\033[?2026l"

    @staticmethod
    def to_hex(n: int) -> str:
        """256-palette index -> #rrggbb, for OSC sequences."""
        if 16 <= n <= 231:
            n -= 16
            r, g, b = _LEVELS[n // 36], _LEVELS[(n // 6) % 6], _LEVELS[n % 6]
        elif 232 <= n <= 255:
            r = g = b = 8 + 10 * (n - 232)
        else:
            raise ValueError("use 16-255; 0-15 are terminal-theme defined")
        return f"#{r:02x}{g:02x}{b:02x}"

    @staticmethod
    def fg(n: int) -> str:
        return f"\033[38;5;{n}m"

    @staticmethod
    def bg(n: int) -> str:
        return f"\033[48;5;{n}m"

    @staticmethod
    def cursor(n: int) -> str:
        """OSC 12 - caret colour. Separate channel from SGR text colour."""
        return f"\033]12;{Ansi.to_hex(n)}\033\\"

    # --- imperative (write + flush immediately) ---

    @staticmethod
    def set_color(n: int) -> None:
        """Set text and caret color for everything that follows."""

        stdout.write(Ansi.fg(n) + Ansi.cursor(n))
        stdout.flush()

    @staticmethod
    def clear_color() -> None:
        stdout.write(Ansi.RESET + Ansi.CURSOR_RESET)
        stdout.flush()

    @staticmethod
    def key(keyboard_key: str):
        return f"{Ansi.ITALIC}[{keyboard_key}]{Ansi.NO_ITALIC}"
