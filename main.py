from diagnosis import Diagnoser, Symptom
from sys import stdout
from platform import system
from subprocess import run

# TO DO:
# Make real time input
# Add colors
# Add ASCII Art
# Add loading screen
# Add KeyboardInterrupt banner
# Add README.md, fix .gitignore issues
# Make diagnosis screen more interesting
# Add information of diagnosis / cures / description with diagnosis
# Add links to NHS.uk with each disease.
# Experiment with other set-matching algorithms

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

        IOUtils.write(f"[{self.category.upper()}]\n")
        IOUtils.write("~" * (max_len + 8) + "\n")

        for symptom in available_symptoms:
            IOUtils.write(f"| {symptom.title():<{max_len}} |\n")

        IOUtils.write("~" * (max_len + 8) + "\n")
        IOUtils.write("Press [a]/[d] to navigate, [ENTER] to select, [x] to exit.\n")

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

        max_len = max(map(lambda s: len(s.name), self.symptoms))

        IOUtils.write(f"You have {n} symptom{'' if n == 1 else 's'} selected:\n")
        IOUtils.write("~" * (max_len + 6) + "\n")

        for symptom in self.symptoms:
            IOUtils.write(f"| - {symptom.name.upper():<{max_len}} |\n")

        IOUtils.write("~" * (max_len + 6) + "\n")

        IOUtils.input("Press [ENTER] to continue: ")

class Help:

    STRINGS = [
        "This program is designed to help you diagnose your symptoms.",
        "Note: DO NOT use this for actual medical advice :)",
        "You select symptoms by selecting a category that your symptom falls under.",
        "Use the keys [a] and [d] to navigate through categories.",
        "Press [ENTER] to select a category.",
        "From there, you will be presented with a list of symptoms to select.",
        "Again, use [a] and [d] to navigate through the list, and press [ENTER] to select or deselect a symptom.",
        "Use [x] to exit.",
        "Use [v] to view your selected symptoms.",
        "Use [h] to view this help menu.",
        "When you have exited the selection process, your diagnosis will be presented!",
        "Good luck!"
    ]

    @staticmethod
    def write_help():

        IOUtils.clear()

        for string in Help.STRINGS:
            IOUtils.write(f"- {string}\n")

        IOUtils.input("Press [ENTER] to continue: ")

class Main:

    def __init__(self):

        self.symptoms = set()

        self.index = 0

    def write_gui(self):

        categories = list(Symptom.POSSIBLE_SYMPTOMS)

        max_len = max(map(len, categories)) + 2
        categories[self.index] = f"> {categories[self.index]}"

        IOUtils.write("Symptom Categories:\n")
        IOUtils.write("~" * (max_len + 4) + "\n")

        for category in categories:
            IOUtils.write(f"| {category:<{max_len}} |\n")

        IOUtils.write("~" * (max_len + 4) + "\n")

        IOUtils.write(f"<{len(self.symptoms)} symptom{'' if len(self.symptoms) == 1 else 's'} selected>\n")

        IOUtils.write("Press [a]/[d] to navigate, [ENTER] to select, [h] for help.\n")

    def main(self):

        while True:

            IOUtils.clear()

            self.write_gui()

            x = IOUtils.input("-> ", sanitize=True)

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