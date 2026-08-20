from data import SYMPTOMS, CONDITIONS
from difflib import get_close_matches
from functools import partial

def jaccard_similarity(symptoms1, symptoms2):

    return len(symptoms1 & symptoms2) / len(symptoms1 | symptoms2)

def print_symptoms(symptoms):

    if not symptoms:
        return

    n = len(symptoms)

    max_len = max(map(len, symptoms))

    print("~" * (max_len + 6))

    for symptom in symptoms:
        print(f"| - {symptom.upper():<{max_len}} |")

    print("~" * (max_len + 6))

if __name__ == "__main__":

    symptoms = set()

    while True:

        print_symptoms(symptoms)

        symptom = input("Input Symptoms -> ").lower().strip()

        if symptom in {"quit", "exit"}:
            break

        if symptom in SYMPTOMS:
            symptoms.add(symptom)

        else:
            symptom = get_close_matches(symptom, SYMPTOMS)
            if not symptom:
                continue
            else:
                symptoms.add(symptom[0])

    condition = CONDITIONS[max(CONDITIONS, key=partial(jaccard_similarity, symptoms))]
    print(f"[Diagnosis] You have: {condition.upper()}!")
