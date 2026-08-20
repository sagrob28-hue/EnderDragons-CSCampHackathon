from data import SYMPTOMS, CONDITIONS
from difflib import get_close_matches

if __name__ == "__main__":

    symptoms = set()

    while True:

        print(symptoms)

        new_symptom = input("Input Symptoms -> ").lower().strip()

        if new_symptom in {"quit", "exit", "end"}:
            break

        if new_symptom in SYMPTOMS:
            symptoms.add(new_symptom)

        else:
            symptom_corrected = get_close_matches(new_symptom, SYMPTOMS)
            if not symptom_corrected:
                continue
            else:
                symptoms.add(symptom_corrected[0])

