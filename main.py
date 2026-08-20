from diagnosis import Diagnoser, Symptom
from sys import stdout
from platform import system
from subprocess import run

# TO DO:
# Implement the new user interface
# Make real time input
# Add colors
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

class Main:

    def __init__(self):

        self.symptoms = set()

    def write_symptoms(self):

        if not self.symptoms:
            return

        n = len(self.symptoms)

        max_len = max(map(lambda s: len(s.name), self.symptoms))

        IOUtils.write(f"You have {n} symptom{'' if n == 1 else 's'} selected:\n")
        IOUtils.write("~" * (max_len + 6) + "\n")

        for symptom in self.symptoms:
            IOUtils.write(f"| - {symptom.name.upper():<{max_len}} |\n")

        IOUtils.write("~" * (max_len + 6) + "\n")

    def main(self):

        while True:

            IOUtils.clear()

            self.write_symptoms()

            symptom_name = IOUtils.input("Input Symptoms -> ", sanitize=True)

            if symptom_name in {"quit", "exit"}:
                break

            try:
                symptom = Symptom(symptom_name)
            except ValueError:
                continue

            self.symptoms.add(symptom)

        if self.symptoms:
            condition = Diagnoser.diagnosis(*self.symptoms)
            IOUtils.write(f"[Diagnosis] You have: {condition.upper()}!")

if __name__ == "__main__":

    Main().main()