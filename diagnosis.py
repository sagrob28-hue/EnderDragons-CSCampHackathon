from dataclasses import dataclass
from typing import ClassVar

@dataclass(frozen=True)
class Symptom:

    POSSIBLE_SYMPTOMS: ClassVar[dict[str, list[str]]] = {

    "General": [
        "fever",
        "chills",
        "fatigue",
        "malaise",
        "night sweats",
        "weight loss",
        "weight gain",
        "loss of appetite",
        "excessive thirst",
        "excessive hunger",
        "heat intolerance",
        "cold intolerance",
        "swollen lymph nodes",
    ],
    "Head and Nervous System": [
        "headache",
        "dizziness",
        "fainting",
        "confusion",
        "memory loss",
        "seizure",
        "tremor",
        "slurred speech",
        "facial droop",
        "one sided weakness",
        "numbness",
        "tingling",
        "sensitivity to light",
        "neck stiffness",
    ],
    "Eyes": [
        "blurred vision",
        "double vision",
        "eye pain",
        "red eye",
        "sensitivity to light",
    ],
    "Ears, Nose and Throat": [
        "hearing loss",
        "ear pain",
        "ringing in ears",
        "runny nose",
        "nasal congestion",
        "sneezing",
        "sore throat",
        "hoarseness",
        "loss of smell",
        "loss of taste",
        "difficulty swallowing",
    ],
    "Chest and Breathing": [
        "cough",
        "productive cough",
        "coughing blood",
        "shortness of breath",
        "wheezing",
        "chest pain",
        "chest tightness",
    ],
    "Heart and Circulation": [
        "palpitations",
        "rapid heartbeat",
        "irregular heartbeat",
        "high blood pressure",
        "low blood pressure",
        "swollen ankles",
        "leg swelling",
        "calf pain",
        "pale skin",
        "fainting",
        "dizziness",
    ],
    "Stomach and Digestion": [
        "nausea",
        "vomiting",
        "vomiting blood",
        "diarrhea",
        "constipation",
        "abdominal pain",
        "bloating",
        "heartburn",
        "difficulty swallowing",
        "blood in stool",
        "pale stool",
        "jaundice",
        "loss of appetite",
    ],
    "Urinary": [
        "frequent urination",
        "painful urination",
        "blood in urine",
        "dark urine",
    ],
    "Muscles, Bones and Joints": [
        "joint pain",
        "joint swelling",
        "morning stiffness",
        "muscle pain",
        "muscle weakness",
        "back pain",
        "neck stiffness",
    ],
    "Skin, Hair and Nails": [
        "rash",
        "itching",
        "hives",
        "dry skin",
        "bruising easily",
        "hair loss",
        "pale skin",
        "jaundice",
    ],
    "Sleep and Mood": [
        "insomnia",
        "excessive sleepiness",
        "anxiety",
        "depressed mood",
        "irritability",
        "fatigue",
    ],
}

    name: str

    @staticmethod
    def is_valid_symptom(name: str) -> bool:
        return any(name in symptoms for symptoms in Symptom.POSSIBLE_SYMPTOMS.values())

    def __post_init__(self):

        object.__setattr__(self, "name", self.name.strip().casefold())

        if not Symptom.is_valid_symptom(self.name):
            raise ValueError(f"Invalid symptom name: {self.name}")

    def __repr__(self):
        return f"Symptom('{self.name}')"

    def __str__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)

class SymptomSet:

    def __init__(self, *symptoms: str | Symptom):

        if all(isinstance(symptom, str) for symptom in symptoms):

            self.symptoms = frozenset(map(lambda x: Symptom(x), symptoms))

        elif all(isinstance(symptom, Symptom) for symptom in symptoms):

            self.symptoms = frozenset(symptoms)

        else:

            raise TypeError("Expected str or Symptom arguments")

    def __eq__(self, other):

        return self.symptoms == other.symptoms

    def __hash__(self):

        return hash(self.symptoms)

    def __repr__(self):

        return f"{type(self).__name__}({', '.join(repr(symptom.name) for symptom in self.symptoms)})"

    def __len__(self):

        return len(self.symptoms)

    def __contains__(self, symptom):

        return symptom in self.symptoms

    def __iter__(self):

        return iter(self.symptoms)

    def __or__(self, other):

        return type(self)(*(self.symptoms | other.symptoms))

    def __and__(self, other):

        return type(self)(*(self.symptoms & other.symptoms))

    def __matmul__(self, other):

        return len(self & other) / len(self | other)

class Diagnoser:

    CONDITIONS = {SymptomSet('fever', 'sore throat', 'difficulty swallowing', 'swollen lymph nodes'): 'Streptococcal '
                                                                                                      'pharyngitis',
                  SymptomSet('fever', 'coughing blood', 'cough', 'night sweats', 'weight loss'): 'Tuberculosis',
                  SymptomSet('red eye', 'sneezing', 'nasal congestion', 'itching', 'runny nose'): 'Allergic '
                                                                                                  'rhinitis',
                  SymptomSet('fever', 'night sweats', 'muscle pain', 'headache', 'chills', 'vomiting'): 'Malaria',
                  SymptomSet('wheezing', 'low blood pressure', 'shortness of breath', 'itching', 'hives'): 'Anaphylaxis',
                  SymptomSet('chest pain', 'shortness of breath', 'chest tightness', 'fatigue'): 'Angina '
                                                                                                 'pectoris',
                  SymptomSet('fever', 'hearing loss', 'ear pain', 'irritability'): 'Otitis '
                                                                                   'media',
                  SymptomSet('night sweats', 'one sided weakness', 'shortness of breath', 'nausea', 'chest pain'): 'Myocardial '
                                                                                                                   'infarction',
                  SymptomSet('insomnia', 'memory loss', 'muscle pain', 'fatigue', 'headache'): 'Fibromyalgia',
                  SymptomSet('dizziness', 'hair loss', 'shortness of breath', 'fatigue', 'pale skin'): 'Iron '
                                                                                                       'deficiency '
                                                                                                       'anemia',
                  SymptomSet('chest pain', 'coughing blood', 'shortness of breath', 'rapid heartbeat'): 'Pulmonary '
                                                                                                        'embolism',
                  SymptomSet('fever', 'joint swelling', 'joint pain'): 'Gout',
                  SymptomSet('dizziness', 'blurred vision', 'high blood pressure', 'headache'): 'Hypertension',
                  SymptomSet('calf pain', 'leg swelling', 'muscle pain'): 'Deep vein thrombosis',
                  SymptomSet('fever', 'malaise', 'fatigue', 'sore throat', 'swollen lymph nodes'): 'Infectious '
                                                                                                   'mononucleosis',
                  SymptomSet('wheezing', 'productive cough', 'shortness of breath', 'fatigue'): 'Chronic '
                                                                                                'obstructive '
                                                                                                'pulmonary '
                                                                                                'disease',
                  SymptomSet('low blood pressure', 'dizziness', 'fatigue', 'fainting', 'pale skin'): 'Orthostatic '
                                                                                                     'hypotension',
                  SymptomSet('fever', 'cough', 'muscle pain', 'fatigue', 'headache', 'chills'): 'Influenza',
                  SymptomSet('fever', 'cough', 'loss of smell', 'loss of taste', 'shortness of breath', 'fatigue'): 'COVID-19',
                  SymptomSet('fever', 'bruising easily', 'weight loss', 'fatigue', 'swollen lymph nodes'): 'Leukemia',
                  SymptomSet('fever', 'night sweats', 'weight loss', 'itching', 'swollen lymph nodes'): 'Lymphoma',
                  SymptomSet('leg swelling', 'shortness of breath', 'fatigue', 'weight gain', 'swollen ankles'): 'Congestive '
                                                                                                                 'heart '
                                                                                                                 'failure',
                  SymptomSet('irregular heartbeat', 'dizziness', 'shortness of breath', 'fatigue', 'palpitations'): 'Atrial '
                                                                                                                    'fibrillation',
                  SymptomSet('fever', 'nasal congestion', 'productive cough', 'eye pain', 'headache'): 'Acute '
                                                                                                       'sinusitis',
                  SymptomSet('fever', 'productive cough', 'shortness of breath', 'chest pain', 'chills'): 'Pneumonia',
                  SymptomSet('wheezing', 'shortness of breath', 'chest tightness', 'cough'): 'Asthma',
                  SymptomSet('itching', 'dry skin', 'rash'): 'Atopic dermatitis',
                  SymptomSet('sneezing', 'cough', 'nasal congestion', 'sore throat', 'runny nose'): 'Common '
                                                                                                    'cold',
                  SymptomSet('nausea', 'blurred vision', 'headache', 'sensitivity to light'): 'Migraine',
                  SymptomSet('fever', 'sensitivity to light', 'neck stiffness', 'headache', 'confusion'): 'Meningitis',
                  SymptomSet('facial droop', 'slurred speech', 'one sided weakness', 'blurred vision', 'confusion'): 'Stroke',
                  SymptomSet('seizure', 'confusion', 'memory loss', 'muscle weakness'): 'Epilepsy',
                  SymptomSet('muscle weakness', 'insomnia', 'tremor', 'slurred speech'): 'Parkinson '
                                                                                         'disease',
                  SymptomSet('numbness', 'tingling', 'double vision', 'fatigue', 'muscle weakness'): 'Multiple '
                                                                                                     'sclerosis',
                  SymptomSet('insomnia', 'confusion', 'memory loss', 'irritability'): 'Alzheimer '
                                                                                      'disease',
                  SymptomSet('back pain', 'tingling', 'muscle weakness', 'numbness'): 'Peripheral '
                                                                                      'neuropathy',
                  SymptomSet('hearing loss', 'dizziness', 'nausea', 'ringing in ears'): 'Meniere '
                                                                                        'disease',
                  SymptomSet('fever', 'nausea', 'abdominal pain', 'diarrhea', 'vomiting'): 'Gastroenteritis',
                  SymptomSet('chest pain', 'hoarseness', 'heartburn', 'difficulty swallowing'): 'Gastroesophageal '
                                                                                                'reflux '
                                                                                                'disease',
                  SymptomSet('fever', 'loss of appetite', 'nausea', 'abdominal pain', 'vomiting'): 'Appendicitis',
                  SymptomSet('constipation', 'abdominal pain', 'diarrhea', 'bloating'): 'Irritable '
                                                                                        'bowel '
                                                                                        'syndrome',
                  SymptomSet('fever', 'weight loss', 'blood in stool', 'abdominal pain', 'diarrhea'): 'Inflammatory '
                                                                                                      'bowel '
                                                                                                      'disease',
                  SymptomSet('loss of appetite', 'vomiting blood', 'heartburn', 'nausea', 'abdominal pain'): 'Peptic '
                                                                                                             'ulcer '
                                                                                                             'disease',
                  SymptomSet('dark urine', 'jaundice', 'pale stool', 'nausea', 'fatigue'): 'Viral '
                                                                                           'hepatitis',
                  SymptomSet('jaundice', 'loss of appetite', 'nausea', 'abdominal pain', 'vomiting'): 'Gallstone '
                                                                                                      'disease',
                  SymptomSet('weight loss', 'bloating', 'rash', 'fatigue', 'diarrhea'): 'Celiac '
                                                                                        'disease',
                  SymptomSet('weight loss', 'frequent urination', 'fatigue', 'excessive thirst', 'excessive hunger'): 'Diabetes '
                                                                                                                      'mellitus',
                  SymptomSet('constipation', 'hair loss', 'dry skin', 'cold intolerance', 'fatigue', 'weight gain'): 'Hypothyroidism',
                  SymptomSet('weight loss', 'tremor', 'palpitations', 'heat intolerance', 'anxiety'): 'Hyperthyroidism',
                  SymptomSet('weight loss', 'low blood pressure', 'nausea', 'fatigue', 'muscle weakness'): 'Adrenal '
                                                                                                           'insufficiency',
                  SymptomSet('abdominal pain', 'painful urination', 'frequent urination', 'blood in urine'): 'Urinary '
                                                                                                             'tract '
                                                                                                             'infection',
                  SymptomSet('fever', 'painful urination', 'nausea', 'back pain', 'chills'): 'Pyelonephritis',
                  SymptomSet('nausea', 'blood in urine', 'back pain', 'abdominal pain', 'vomiting'): 'Kidney '
                                                                                                     'stones',
                  SymptomSet('joint pain', 'joint swelling', 'fatigue', 'morning stiffness'): 'Rheumatoid '
                                                                                              'arthritis',
                  SymptomSet('back pain', 'joint swelling', 'joint pain', 'morning stiffness'): 'Osteoarthritis',
                  SymptomSet('fever', 'joint swelling', 'joint pain', 'hair loss', 'rash', 'fatigue'): 'Systemic '
                                                                                                       'lupus '
                                                                                                       'erythematosus',
                  SymptomSet('itching', 'joint pain', 'dry skin', 'rash'): 'Psoriasis',
                  SymptomSet('insomnia', 'memory loss', 'loss of appetite', 'fatigue', 'depressed mood'): 'Major '
                                                                                                          'depressive '
                                                                                                          'disorder',
                  SymptomSet('insomnia', 'muscle pain', 'irritability', 'palpitations', 'anxiety'): 'Generalized '
                                                                                                    'anxiety '
                                                                                                    'disorder',
                  SymptomSet('tingling', 'dizziness', 'shortness of breath', 'chest pain', 'palpitations', 'anxiety'): 'Panic '
                                                                                                                       'disorder',
                  SymptomSet('insomnia', 'excessive sleepiness', 'fatigue', 'headache', 'irritability'): 'Obstructive '
                                                                                                         'sleep '
                                                                                                         'apnea'
                  }

    @staticmethod
    def diagnosis(*symptoms: Symptom):

        if not all(isinstance(symptom, Symptom) for symptom in symptoms):
            raise TypeError("Expected Symptom arguments")

        symptoms = SymptomSet(*symptoms)

        key = max(Diagnoser.CONDITIONS, key=lambda symptom_set: symptom_set @ symptoms)

        return Diagnoser.CONDITIONS[key]
