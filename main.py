from diagnosis import Diagnoser, Symptom
from sys import stdout
from platform import system
from subprocess import run
from enum import StrEnum

# TO DO:
# Make real time input
# Add ASCII Art
# Add loading screen
# Add KeyboardInterrupt banner

# Add README.md, fix .gitignore issues

# Make diagnosis screen more interesting
# Add information of diagnosis / cures / description with diagnosis
# Add links to NHS.uk with each disease.

# Experiment with other set-matching algorithms

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

class IOUtils:

    """A class that has to do with input and output
    (mostly input)."""

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
    def input(prompt: str="", /, *, sanitize: bool=False):

        """An issue with some terminals is that
        sometimes, after an input call, the text jitters.
        This can be (mostly) fixed using this function,
        which first writes the prompt to the terminal separately
        and then gets the input. An optional parameter,
        sanitize, can also be used to automatically sanitize
        the input."""

        stdout.write(prompt)

        x = input()
        return IOUtils.sanitized(x) if sanitize else x

    @staticmethod
    def write(prompt: str=""):

        """Writes to the terminal."""

        stdout.write(prompt)

class SymptomModifier:

    CATEGORY_COLORS = {
        "General":                    64,  # olive
        "Head and Nervous System":    91,  # dark violet
        "Eyes":                       37,  # dark cyan
        "Ears, Nose and Throat":      30,  # dark teal
        "Chest and Breathing":        26,  # dark blue
        "Heart and Circulation":     124,  # dark red
        "Stomach and Digestion":     166,  # burnt orange
        "Urinary":                   136,  # mustard
        "Muscles, Bones and Joints":  28,  # forest green
        "Skin, Hair and Nails":      132,  # dusty rose
        "Sleep and Mood":             61,  # slate indigo
    }

    def __init__(self, category: str, symptoms: set[Symptom]):

        if category not in Symptom.POSSIBLE_SYMPTOMS:
            raise ValueError(f"Invalid category: {category}")

        self.symptoms = symptoms
        self.category = category

        self.index = 0

    def toggle(self):

        symptom = Symptom.POSSIBLE_SYMPTOMS[self.category][self.index]

        if Symptom(symptom) in self.symptoms:
            self.symptoms.remove(Symptom(symptom))
        else:
            self.symptoms.add(Symptom(symptom))

    def write_gui(self):

        available_symptoms = Symptom.POSSIBLE_SYMPTOMS[self.category].copy()

        max_len = max(map(len, available_symptoms)) + 2

        for i, symptom in enumerate(available_symptoms):

            box = "(X)" if Symptom(symptom) in self.symptoms else "( )"

            if i == self.index:
                symptom = f"> {symptom}"

            available_symptoms[i] = f"{symptom:<{max_len}} {box}"

        Ansi.set_color(self.CATEGORY_COLORS[self.category])
        IOUtils.write(f"{Ansi.ITALIC}[{self.category.upper()}]{Ansi.NO_ITALIC}\n")
        IOUtils.write("~" * (max_len + 8) + "\n")

        for i, symptom in enumerate(available_symptoms):
            x = Ansi.REVERSE if i == self.index else ""
            IOUtils.write(f"| {x}{symptom.title():<{max_len}}{Ansi.NO_REVERSE} |\n")

        IOUtils.write("~" * (max_len + 8) + "\n")
        IOUtils.write(f"{Ansi.UNDERLINE}Press {Ansi.key('a')}/{Ansi.key('d')} to navigate, {Ansi.key('ENTER')} to select, {Ansi.key('x')} to exit.\n{Ansi.NO_UNDERLINE}")

    def modify(self):

        while True:

            IOUtils.clear()
            self.write_gui()

            choice = IOUtils.input("-> ", sanitize=True)

            match choice:
                case "x":
                    return self.symptoms
                case "":
                    self.toggle()
                case "a":
                    self.index -= 1
                case "d":
                    self.index += 1

            self.index %= len(Symptom.POSSIBLE_SYMPTOMS[self.category])

class SymptomViewer:

    def __init__(self, symptoms: set[Symptom]):

        self.symptoms = symptoms

    def view(self):

        if not self.symptoms:
            return

        n = len(self.symptoms)

        IOUtils.clear()

        Ansi.set_color(35) # spring green

        max_len = max(map(lambda s: len(s.name), self.symptoms))

        IOUtils.write(f"{Ansi.ITALIC}You have {Ansi.BOLD}{n}{Ansi.NO_BOLD} symptom{'' if n == 1 else 's'} selected:\n{Ansi.NO_ITALIC}")
        IOUtils.write("~" * (max_len + 6) + "\n")

        for symptom in self.symptoms:
            IOUtils.write(f"| - {symptom.name.upper():<{max_len}} |\n")

        IOUtils.write("~" * (max_len + 6) + "\n")

        IOUtils.input(f"Press {Ansi.key('ENTER')} to continue: ")

class Help:

    STRINGS = [
        f"{Ansi.BOLD}{Ansi.UNDERLINE}Help:{Ansi.NO_UNDERLINE}{Ansi.NO_BOLD}",
        f"This program is designed to help you {Ansi.UNDERLINE}diagnose your symptoms.{Ansi.NO_UNDERLINE}",
        f"Note: {Ansi.BOLD}DO NOT{Ansi.NO_BOLD} use this for actual medical advice :)",
        "You select symptoms by selecting a category that your symptom falls under.",
        f"Use the keys {Ansi.key('a')} and {Ansi.key('d')} to navigate through categories.",
        f"Press {Ansi.key('ENTER')} to select a category.",
        "From there, you will be presented with a list of symptoms to select.",
        f"Again, use {Ansi.key('a')} and {Ansi.key('d')} to navigate through the list, and press [ENTER] to select or deselect a symptom.",
        f"Use {Ansi.key('x')} to exit.",
        f"Use {Ansi.key('v')} to view your selected symptoms.",
        f"Use {Ansi.key('h')} to view this help menu.",
        "When you have exited the selection process, your diagnosis will be presented!",
        f"{Ansi.REVERSE}Good luck!{Ansi.NO_REVERSE}"
    ]

    @staticmethod
    def write_help():

        IOUtils.clear()

        Ansi.set_color(131) # brick

        for string in Help.STRINGS:
            IOUtils.write(f"- {string}\n")

        IOUtils.input(f"Press {Ansi.key('ENTER')} to continue: ")

class Main:

    def __init__(self):

        self.symptoms = set()

        self.index = 0

    def write_gui(self):

        categories = list(Symptom.POSSIBLE_SYMPTOMS)

        max_len = max(map(len, categories)) + 2
        categories[self.index] = f"> {categories[self.index]}"

        Ansi.set_color(127) # dark magenta

        IOUtils.write(f"{Ansi.ITALIC}Symptom Categories:{Ansi.NO_ITALIC}\n")

        IOUtils.write("~" * (max_len + 4) + "\n")

        for i, category in enumerate(categories):

            x = Ansi.REVERSE if i == self.index else ""

            IOUtils.write(f"| {x}{category:<{max_len}}{Ansi.NO_REVERSE} |\n")

        IOUtils.write("~" * (max_len + 4) + "\n")

        IOUtils.write(Ansi.BOLD)

        IOUtils.write(f"<{len(self.symptoms)} symptom{'' if len(self.symptoms) == 1 else 's'} selected>\n")

        IOUtils.write(Ansi.NO_BOLD)

        IOUtils.write(
        f"{Ansi.UNDERLINE}Press {Ansi.key('a')}/{Ansi.key('d')} to navigate, {Ansi.key('ENTER')} to select, {Ansi.key('h')} for help.\n{Ansi.NO_UNDERLINE}"
        )

    def main(self):

        while True:

            IOUtils.clear()

            self.write_gui()

            x = IOUtils.input(f"-> ", sanitize=True)

            match x:

                case "x":
                    break
                case "a":
                    self.index -= 1
                case "d":
                    self.index += 1
                case "v":
                    SymptomViewer(self.symptoms).view()
                case "h":
                    Help.write_help()
                case "":
                    category = list(Symptom.POSSIBLE_SYMPTOMS)[self.index]
                    self.symptoms = SymptomModifier(category, self.symptoms).modify().copy()

            self.index %= len(Symptom.POSSIBLE_SYMPTOMS)

        if self.symptoms:
            condition = Diagnoser.diagnosis(*self.symptoms)
            IOUtils.write(f"[Diagnosis] You have: {condition.upper()}!")

if __name__ == "__main__":

    Main().main()