"""Illustrative symptom/condition data. Not a diagnostic tool — the symptom
sets are simplified textbook presentations, not clinical criteria."""

SYMPTOMS = [
    "fever",
    "chills",
    "fatigue",
    "malaise",
    "night sweats",
    "weight loss",
    "weight gain",
    "loss of appetite",
    "headache",
    "dizziness",
    "fainting",
    "confusion",
    "memory loss",
    "blurred vision",
    "double vision",
    "eye pain",
    "red eye",
    "hearing loss",
    "ear pain",
    "ringing in ears",
    "runny nose",
    "nasal congestion",
    "sneezing",
    "sore throat",
    "hoarseness",
    "cough",
    "productive cough",
    "coughing blood",
    "shortness of breath",
    "wheezing",
    "chest pain",
    "chest tightness",
    "palpitations",
    "rapid heartbeat",
    "irregular heartbeat",
    "high blood pressure",
    "low blood pressure",
    "swollen ankles",
    "leg swelling",
    "calf pain",
    "nausea",
    "vomiting",
    "vomiting blood",
    "diarrhea",
    "constipation",
    "abdominal pain",
    "bloating",
    "heartburn",
    "difficulty swallowing",
    "jaundice",
    "dark urine",
    "pale stool",
    "blood in stool",
    "frequent urination",
    "painful urination",
    "blood in urine",
    "excessive thirst",
    "excessive hunger",
    "joint pain",
    "joint swelling",
    "morning stiffness",
    "muscle pain",
    "muscle weakness",
    "back pain",
    "neck stiffness",
    "rash",
    "itching",
    "hives",
    "dry skin",
    "bruising easily",
    "hair loss",
    "pale skin",
    "numbness",
    "tingling",
    "tremor",
    "seizure",
    "slurred speech",
    "facial droop",
    "one sided weakness",
    "sensitivity to light",
    "loss of smell",
    "loss of taste",
    "insomnia",
    "excessive sleepiness",
    "anxiety",
    "depressed mood",
    "irritability",
    "heat intolerance",
    "cold intolerance",
    "swollen lymph nodes",
]

CONDITIONS = {
    # --- Respiratory / ENT ---
    frozenset({"runny nose", "sneezing", "sore throat", "nasal congestion", "cough"}):
        "Common cold",
    frozenset({"fever", "chills", "muscle pain", "fatigue", "cough", "headache"}):
        "Influenza",
    frozenset({"fever", "cough", "loss of smell", "loss of taste", "fatigue",
               "shortness of breath"}):
        "COVID-19",
    frozenset({"fever", "productive cough", "shortness of breath", "chest pain",
               "chills"}):
        "Pneumonia",
    frozenset({"wheezing", "shortness of breath", "chest tightness", "cough"}):
        "Asthma",
    frozenset({"productive cough", "shortness of breath", "wheezing", "fatigue"}):
        "Chronic obstructive pulmonary disease",
    frozenset({"cough", "night sweats", "weight loss", "fever", "coughing blood"}):
        "Tuberculosis",
    frozenset({"sneezing", "itching", "runny nose", "red eye", "nasal congestion"}):
        "Allergic rhinitis",
    frozenset({"sore throat", "fever", "swollen lymph nodes",
               "difficulty swallowing"}):
        "Streptococcal pharyngitis",
    frozenset({"nasal congestion", "headache", "eye pain", "fever",
               "productive cough"}):
        "Acute sinusitis",
    frozenset({"ear pain", "hearing loss", "fever", "irritability"}):
        "Otitis media",

    # --- Cardiovascular ---
    frozenset({"chest pain", "shortness of breath", "nausea", "night sweats",
               "one sided weakness"}):
        "Myocardial infarction",
    frozenset({"chest pain", "chest tightness", "shortness of breath",
               "fatigue"}):
        "Angina pectoris",
    frozenset({"shortness of breath", "leg swelling", "swollen ankles", "fatigue",
               "weight gain"}):
        "Congestive heart failure",
    frozenset({"palpitations", "irregular heartbeat", "fatigue", "dizziness",
               "shortness of breath"}):
        "Atrial fibrillation",
    frozenset({"high blood pressure", "headache", "blurred vision", "dizziness"}):
        "Hypertension",
    frozenset({"calf pain", "leg swelling", "muscle pain"}):
        "Deep vein thrombosis",
    frozenset({"shortness of breath", "chest pain", "rapid heartbeat",
               "coughing blood"}):
        "Pulmonary embolism",
    frozenset({"dizziness", "fainting", "low blood pressure", "pale skin",
               "fatigue"}):
        "Orthostatic hypotension",

    # --- Neurological ---
    frozenset({"headache", "sensitivity to light", "nausea", "blurred vision"}):
        "Migraine",
    frozenset({"headache", "neck stiffness", "fever", "sensitivity to light",
               "confusion"}):
        "Meningitis",
    frozenset({"facial droop", "one sided weakness", "slurred speech", "confusion",
               "blurred vision"}):
        "Stroke",
    frozenset({"seizure", "confusion", "memory loss", "muscle weakness"}):
        "Epilepsy",
    frozenset({"tremor", "muscle weakness", "slurred speech", "insomnia"}):
        "Parkinson disease",
    frozenset({"numbness", "tingling", "double vision", "muscle weakness",
               "fatigue"}):
        "Multiple sclerosis",
    frozenset({"memory loss", "confusion", "irritability", "insomnia"}):
        "Alzheimer disease",
    frozenset({"numbness", "tingling", "muscle weakness", "back pain"}):
        "Peripheral neuropathy",
    frozenset({"dizziness", "ringing in ears", "hearing loss", "nausea"}):
        "Meniere disease",

    # --- Gastrointestinal / hepatic ---
    frozenset({"nausea", "vomiting", "diarrhea", "abdominal pain", "fever"}):
        "Gastroenteritis",
    frozenset({"heartburn", "chest pain", "difficulty swallowing", "hoarseness"}):
        "Gastroesophageal reflux disease",
    frozenset({"abdominal pain", "nausea", "vomiting", "loss of appetite",
               "fever"}):
        "Appendicitis",
    frozenset({"abdominal pain", "bloating", "diarrhea", "constipation"}):
        "Irritable bowel syndrome",
    frozenset({"abdominal pain", "diarrhea", "blood in stool", "weight loss",
               "fever"}):
        "Inflammatory bowel disease",
    frozenset({"abdominal pain", "heartburn", "nausea", "vomiting blood",
               "loss of appetite"}):
        "Peptic ulcer disease",
    frozenset({"jaundice", "dark urine", "pale stool", "fatigue", "nausea"}):
        "Viral hepatitis",
    frozenset({"abdominal pain", "nausea", "vomiting", "jaundice",
               "loss of appetite"}):
        "Gallstone disease",
    frozenset({"diarrhea", "bloating", "weight loss", "fatigue", "rash"}):
        "Celiac disease",

    # --- Endocrine / metabolic ---
    frozenset({"excessive thirst", "frequent urination", "excessive hunger",
               "weight loss", "fatigue"}):
        "Diabetes mellitus",
    frozenset({"fatigue", "weight gain", "cold intolerance", "dry skin",
               "constipation", "hair loss"}):
        "Hypothyroidism",
    frozenset({"weight loss", "heat intolerance", "palpitations", "anxiety",
               "tremor"}):
        "Hyperthyroidism",
    frozenset({"fatigue", "muscle weakness", "weight loss", "low blood pressure",
               "nausea"}):
        "Adrenal insufficiency",

    # --- Renal / urinary ---
    frozenset({"painful urination", "frequent urination", "abdominal pain",
               "blood in urine"}):
        "Urinary tract infection",
    frozenset({"back pain", "fever", "chills", "nausea", "painful urination"}):
        "Pyelonephritis",
    frozenset({"back pain", "abdominal pain", "blood in urine", "nausea",
               "vomiting"}):
        "Kidney stones",

    # --- Musculoskeletal / rheumatologic ---
    frozenset({"joint pain", "joint swelling", "morning stiffness", "fatigue"}):
        "Rheumatoid arthritis",
    frozenset({"joint pain", "morning stiffness", "joint swelling", "back pain"}):
        "Osteoarthritis",
    frozenset({"joint pain", "joint swelling", "rash", "fever", "fatigue",
               "hair loss"}):
        "Systemic lupus erythematosus",
    frozenset({"joint pain", "joint swelling", "fever"}):
        "Gout",
    frozenset({"muscle pain", "fatigue", "insomnia", "headache", "memory loss"}):
        "Fibromyalgia",

    # --- Hematologic / infectious ---
    frozenset({"fatigue", "pale skin", "shortness of breath", "dizziness",
               "hair loss"}):
        "Iron deficiency anemia",
    frozenset({"fatigue", "bruising easily", "fever", "weight loss",
               "swollen lymph nodes"}):
        "Leukemia",
    frozenset({"fever", "night sweats", "weight loss", "swollen lymph nodes",
               "itching"}):
        "Lymphoma",
    frozenset({"fever", "sore throat", "swollen lymph nodes", "fatigue",
               "malaise"}):
        "Infectious mononucleosis",
    frozenset({"fever", "chills", "night sweats", "headache", "muscle pain",
               "vomiting"}):
        "Malaria",

    # --- Dermatologic / allergic ---
    frozenset({"hives", "itching", "shortness of breath", "wheezing",
               "low blood pressure"}):
        "Anaphylaxis",
    frozenset({"rash", "itching", "dry skin"}):
        "Atopic dermatitis",
    frozenset({"rash", "dry skin", "itching", "joint pain"}):
        "Psoriasis",

    # --- Psychiatric / sleep ---
    frozenset({"depressed mood", "fatigue", "insomnia", "loss of appetite",
               "memory loss"}):
        "Major depressive disorder",
    frozenset({"anxiety", "palpitations", "insomnia", "irritability",
               "muscle pain"}):
        "Generalized anxiety disorder",
    frozenset({"anxiety", "palpitations", "chest pain", "shortness of breath",
               "dizziness", "tingling"}):
        "Panic disorder",
    frozenset({"excessive sleepiness", "insomnia", "headache", "fatigue",
               "irritability"}):
        "Obstructive sleep apnea",
}