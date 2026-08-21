from diagnosis import Diagnoser, Symptom
from sys import stdout
from keyboard import enable_ansi, cbreak_mode, read_key
from ansi import Ansi, IOUtils
from loading_screen import LoadingScreen

# TO DO:
# Add loading screen
# Add KeyboardInterrupt banner

# Make diagnosis screen more interesting
# Add information of diagnosis / cures / description with diagnosis
# Add links to NHS.uk with each disease.

# Add README.md, fix .gitignore issues

# Experiment with other set-matching algorithms

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

            choice = read_key()

            match choice:
                case "x":
                    return self.symptoms
                case "ENTER":
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

        IOUtils.write(f"Press {Ansi.key('ENTER')} to continue.")
        read_key()

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

        IOUtils.write(f"Press {Ansi.key('ENTER')} to continue.")
        read_key()

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

            IOUtils.write(f"Press a key.")

            stdout.flush()
            key = read_key()

            match key:

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
                case "ENTER":
                    category = list(Symptom.POSSIBLE_SYMPTOMS)[self.index]
                    self.symptoms = SymptomModifier(category, self.symptoms).modify().copy()

            self.index %= len(Symptom.POSSIBLE_SYMPTOMS)

        if self.symptoms:
            condition = Diagnoser.diagnosis(*self.symptoms)
            IOUtils.write(f"\n[Diagnosis] You have: {condition.upper()}!")

if __name__ == "__main__":

    try:

        enable_ansi()
        IOUtils.write("\033[?25l")
        stdout.flush()
        LoadingScreen.load()

        with cbreak_mode():
            Main().main()

    except KeyboardInterrupt:
        IOUtils.write(f"{Ansi.RED}\n\n[KeyboardInterrupt] Exiting...{Ansi.DEFAULT}")
    finally:
        stdout.write("\033[?25h\033[0m\033]112\033\\")
        stdout.flush()