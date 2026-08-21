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

@dataclass(frozen=True)
class Condition:

    name: str
    description: str
    when_to_seek_care: str
    link: str

class Diagnoser:

    CONDITIONS = {
        SymptomSet('fever', 'sore throat', 'difficulty swallowing', 'swollen lymph nodes'): Condition(
            'Streptococcal pharyngitis',
            'A bacterial throat infection causing a sudden, severe sore throat with fever and swollen glands, usually without a cough.',
            'See a GP if the sore throat does not improve after a week, or sooner if you have a high fever or find it hard to swallow.',
            'https://www.nhs.uk/symptoms/sore-throat/'),

        SymptomSet('fever', 'coughing blood', 'cough', 'night sweats', 'weight loss'): Condition(
            'Tuberculosis',
            'A bacterial infection that usually attacks the lungs, producing a persistent cough, drenching night sweats and steady weight loss.',
            'See a GP urgently if you have had a cough for more than three weeks or have coughed up any blood.',
            'https://www.nhs.uk/conditions/tuberculosis-tb/'),

        SymptomSet('red eye', 'sneezing', 'nasal congestion', 'itching', 'runny nose'): Condition(
            'Allergic rhinitis',
            'An allergic reaction in the nose and eyes, most often to pollen, dust mites or animal dander. Commonly called hay fever.',
            'See a pharmacist first. Visit a GP if symptoms are not controlled by antihistamines or are disrupting your sleep.',
            'https://www.nhs.uk/conditions/allergic-rhinitis/'),

        SymptomSet('fever', 'night sweats', 'muscle pain', 'headache', 'chills', 'vomiting'): Condition(
            'Malaria',
            'A serious parasitic infection spread by mosquito bites, causing cycles of fever, violent shivering and sweating.',
            'Seek medical help immediately if you develop a fever during or within a year of travel to a malaria area.',
            'https://www.nhs.uk/conditions/malaria/'),

        SymptomSet('wheezing', 'low blood pressure', 'shortness of breath', 'itching', 'hives'): Condition(
            'Anaphylaxis',
            'A severe, rapid, whole-body allergic reaction that causes swelling, breathing difficulty and a sudden drop in blood pressure.',
            'Call 999 immediately. Use an adrenaline auto-injector at once if one is available.',
            'https://www.nhs.uk/conditions/anaphylaxis/'),

        SymptomSet('chest pain', 'shortness of breath', 'chest tightness', 'fatigue'): Condition(
            'Angina pectoris',
            'Chest pain caused by reduced blood flow to the heart muscle, typically brought on by exertion and eased by rest.',
            'See a GP for new chest pain on exertion. Call 999 if the pain is severe, lasts more than 15 minutes, or occurs at rest.',
            'https://www.nhs.uk/conditions/angina/'),

        SymptomSet('fever', 'hearing loss', 'ear pain', 'irritability'): Condition(
            'Otitis media',
            'An infection of the middle ear, very common in young children, causing earache, muffled hearing and fever.',
            'See a GP if symptoms last more than three days, or sooner if there is fluid coming from the ear.',
            'https://www.nhs.uk/conditions/ear-infections/'),

        SymptomSet('night sweats', 'one sided weakness', 'shortness of breath', 'nausea', 'chest pain'): Condition(
            'Myocardial infarction',
            'A heart attack: blood flow to part of the heart is blocked, causing crushing chest pain that may spread to the arm or jaw.',
            'Call 999 immediately. Do not wait to see whether the pain passes.',
            'https://www.nhs.uk/conditions/heart-attack/'),

        SymptomSet('insomnia', 'memory loss', 'muscle pain', 'fatigue', 'headache'): Condition(
            'Fibromyalgia',
            'A long-term condition causing widespread muscle pain, exhaustion and problems with memory and concentration.',
            'See a GP if widespread pain and fatigue have lasted more than three months and are affecting daily life.',
            'https://www.nhs.uk/conditions/fibromyalgia/'),

        SymptomSet('dizziness', 'hair loss', 'shortness of breath', 'fatigue', 'pale skin'): Condition(
            'Iron deficiency anaemia',
            'Too few healthy red blood cells because of low iron, leaving you tired, pale and breathless on mild exertion.',
            'See a GP for a blood test if you are persistently tired and breathless, especially with heavy periods or blood in your stool.',
            'https://www.nhs.uk/conditions/iron-deficiency-anaemia/'),

        SymptomSet('chest pain', 'coughing blood', 'shortness of breath', 'rapid heartbeat'): Condition(
            'Pulmonary embolism',
            'A blood clot blocking an artery in the lungs, causing sudden breathlessness and sharp chest pain that worsens on breathing in.',
            'Call 999. This is a medical emergency.',
            'https://www.nhs.uk/conditions/pulmonary-embolism/'),

        SymptomSet('fever', 'joint swelling', 'joint pain'): Condition(
            'Gout',
            'A form of arthritis where uric acid crystals collect in a joint, often the big toe, causing sudden intense pain and swelling.',
            'See a GP if you have sudden severe joint pain, or urgently if the joint is hot and you feel feverish.',
            'https://www.nhs.uk/conditions/gout/'),

        SymptomSet('dizziness', 'blurred vision', 'high blood pressure', 'headache'): Condition(
            'Hypertension',
            'Persistently raised blood pressure. It rarely causes symptoms but raises the long-term risk of heart attack and stroke.',
            'Get your blood pressure checked at a pharmacy or GP. Seek urgent help for severe headache with visual changes.',
            'https://www.nhs.uk/conditions/high-blood-pressure/'),

        SymptomSet('calf pain', 'leg swelling', 'muscle pain'): Condition(
            'Deep vein thrombosis',
            'A blood clot in a deep leg vein, causing a swollen, warm, painful calf. It can travel to the lungs if untreated.',
            'Contact 111 or a GP urgently. Call 999 if you also become breathless or develop chest pain.',
            'https://www.nhs.uk/conditions/deep-vein-thrombosis-dvt/'),

        SymptomSet('fever', 'malaise', 'fatigue', 'sore throat', 'swollen lymph nodes'): Condition(
            'Infectious mononucleosis',
            'Glandular fever, usually caused by the Epstein-Barr virus, producing a severe sore throat and fatigue that can last weeks.',
            'See a GP to confirm the diagnosis. Avoid contact sport for at least a month, as the spleen can be enlarged.',
            'https://www.nhs.uk/conditions/glandular-fever/'),

        SymptomSet('wheezing', 'productive cough', 'shortness of breath', 'fatigue'): Condition(
            'Chronic obstructive pulmonary disease',
            'Long-term lung damage, usually from smoking, that narrows the airways and causes a persistent phlegmy cough and breathlessness.',
            'See a GP about persistent breathlessness or a long-standing cough. Seek urgent help if breathing suddenly worsens.',
            'https://www.nhs.uk/conditions/chronic-obstructive-pulmonary-disease-copd/'),

        SymptomSet('low blood pressure', 'dizziness', 'fatigue', 'fainting', 'pale skin'): Condition(
            'Orthostatic hypotension',
            'A drop in blood pressure on standing up, causing brief dizziness or fainting as blood flow to the brain falls.',
            'See a GP if you faint, fall, or feel dizzy often, particularly if you take blood pressure medication.',
            'https://www.nhs.uk/conditions/low-blood-pressure-hypotension/'),

        SymptomSet('fever', 'cough', 'muscle pain', 'fatigue', 'headache', 'chills'): Condition(
            'Influenza',
            'A viral infection that comes on suddenly with fever, aching muscles and exhaustion. Usually more severe than a cold.',
            'Rest at home. Contact 111 if you are short of breath, symptoms worsen after a week, or you are in a high-risk group.',
            'https://www.nhs.uk/conditions/flu/'),

        SymptomSet('fever', 'cough', 'loss of smell', 'loss of taste', 'shortness of breath', 'fatigue'): Condition(
            'COVID-19',
            'An infection caused by the SARS-CoV-2 virus, notable for loss of smell and taste alongside fever and a dry cough.',
            'Stay home and avoid contact with others. Call 999 if you struggle to breathe or your lips turn blue.',
            'https://www.nhs.uk/conditions/covid-19/'),

        SymptomSet('fever', 'bruising easily', 'weight loss', 'fatigue', 'swollen lymph nodes'): Condition(
            'Acute myeloid leukaemia',
            'A fast-developing cancer of the blood-forming cells in bone marrow, causing fatigue, easy bruising and repeated infections.',
            'See a GP promptly about unexplained bruising, persistent fatigue or repeated infections.',
            'https://www.nhs.uk/conditions/acute-myeloid-leukaemia/'),

        SymptomSet('fever', 'night sweats', 'weight loss', 'itching', 'swollen lymph nodes'): Condition(
            'Lymphoma',
            'A cancer of the lymphatic system, typically causing painless swollen glands along with night sweats and weight loss.',
            'See a GP about a swollen gland that has not gone down within a few weeks, especially with night sweats.',
            'https://www.nhs.uk/conditions/non-hodgkin-lymphoma/'),

        SymptomSet('leg swelling', 'shortness of breath', 'fatigue', 'weight gain', 'swollen ankles'): Condition(
            'Congestive heart failure',
            'The heart cannot pump strongly enough, so fluid backs up into the lungs and legs causing breathlessness and swollen ankles.',
            'See a GP about persistent breathlessness or swollen ankles. Call 999 if you are severely breathless at rest.',
            'https://www.nhs.uk/conditions/heart-failure/'),

        SymptomSet('irregular heartbeat', 'dizziness', 'shortness of breath', 'fatigue', 'palpitations'): Condition(
            'Atrial fibrillation',
            'An irregular, often rapid heart rhythm that causes palpitations and tiredness, and raises the risk of stroke.',
            'See a GP if you notice a persistently irregular pulse. Call 999 for chest pain with palpitations.',
            'https://www.nhs.uk/conditions/atrial-fibrillation/'),

        SymptomSet('fever', 'nasal congestion', 'productive cough', 'eye pain', 'headache'): Condition(
            'Acute sinusitis',
            'Inflammation of the sinuses following a cold, causing facial pain, blocked nose and thick nasal discharge.',
            'See a GP if symptoms last more than 10 days without improving, or if you develop severe pain or swelling around the eye.',
            'https://www.nhs.uk/conditions/sinusitis-sinus-infection/'),

        SymptomSet('fever', 'productive cough', 'shortness of breath', 'chest pain', 'chills'): Condition(
            'Pneumonia',
            'Infection that inflames the air sacs of the lungs, causing a productive cough, fever and chest pain when breathing in.',
            'Contact a GP or 111 promptly. Call 999 if breathing is rapid and difficult or you become confused.',
            'https://www.nhs.uk/conditions/pneumonia/'),

        SymptomSet('wheezing', 'shortness of breath', 'chest tightness', 'cough'): Condition(
            'Asthma',
            'A long-term condition where the airways narrow and become inflamed, causing wheeze, chest tightness and coughing.',
            'See a GP about recurrent wheeze. Call 999 if your reliever inhaler is not helping and you cannot speak in full sentences.',
            'https://www.nhs.uk/conditions/asthma/'),

        SymptomSet('itching', 'dry skin', 'rash'): Condition(
            'Atopic dermatitis',
            'Eczema: dry, itchy, inflamed patches of skin that flare and settle, often starting in childhood.',
            'See a pharmacist for emollients. Visit a GP if the skin is weeping, crusted or not improving with treatment.',
            'https://www.nhs.uk/conditions/atopic-eczema/'),

        SymptomSet('sneezing', 'cough', 'nasal congestion', 'sore throat', 'runny nose'): Condition(
            'Common cold',
            'A mild viral infection of the nose and throat. It clears on its own, usually within a week to ten days.',
            'Rest and drink fluids. See a GP if symptoms last more than three weeks or you develop a high fever.',
            'https://www.nhs.uk/conditions/common-cold/'),

        SymptomSet('nausea', 'blurred vision', 'headache', 'sensitivity to light'): Condition(
            'Migraine',
            'A severe, often one-sided throbbing headache with nausea and sensitivity to light and sound, sometimes preceded by visual aura.',
            'See a GP if migraines are frequent or severe. Call 999 for a sudden agonising headache unlike any before.',
            'https://www.nhs.uk/conditions/migraine/'),

        SymptomSet('fever', 'sensitivity to light', 'neck stiffness', 'headache', 'confusion'): Condition(
            'Meningitis',
            'Inflammation of the membranes around the brain and spinal cord, causing severe headache, neck stiffness and fever.',
            'Call 999 immediately. Do not wait for a rash to appear.',
            'https://www.nhs.uk/conditions/meningitis/'),

        SymptomSet('facial droop', 'slurred speech', 'one sided weakness', 'blurred vision', 'confusion'): Condition(
            'Stroke',
            'Blood supply to part of the brain is cut off, causing sudden facial drooping, arm weakness and slurred speech.',
            'Call 999 immediately. Remember FAST: Face, Arms, Speech, Time. Every minute matters.',
            'https://www.nhs.uk/conditions/stroke/'),

        SymptomSet('seizure', 'confusion', 'memory loss', 'muscle weakness'): Condition(
            'Epilepsy',
            'A condition causing repeated seizures due to sudden bursts of electrical activity in the brain.',
            'See a GP after any first seizure. Call 999 if a seizure lasts over five minutes or another follows immediately.',
            'https://www.nhs.uk/conditions/epilepsy/'),

        SymptomSet('muscle weakness', 'insomnia', 'tremor', 'slurred speech'): Condition(
            'Parkinson disease',
            'A progressive brain condition causing tremor at rest, muscle stiffness and increasingly slow movement.',
            'See a GP if you notice a persistent tremor, stiffness or slowness of movement.',
            'https://www.nhs.uk/conditions/parkinsons-disease/'),

        SymptomSet('numbness', 'tingling', 'double vision', 'fatigue', 'muscle weakness'): Condition(
            'Multiple sclerosis',
            'The immune system attacks the protective coating around nerves, causing numbness, visual problems and fatigue in episodes.',
            'See a GP about unexplained numbness, weakness or vision changes lasting more than a day.',
            'https://www.nhs.uk/conditions/multiple-sclerosis/'),

        SymptomSet('insomnia', 'confusion', 'memory loss', 'irritability'): Condition(
            'Alzheimer disease',
            'The most common cause of dementia, causing gradually worsening memory loss, confusion and changes in mood.',
            'See a GP about persistent memory problems. Early assessment opens up support and treatment options.',
            'https://www.nhs.uk/conditions/alzheimers-disease/'),

        SymptomSet('back pain', 'tingling', 'muscle weakness', 'numbness'): Condition(
            'Peripheral neuropathy',
            'Damage to the nerves outside the brain and spinal cord, causing numbness, tingling and burning pain, usually in the feet and hands.',
            'See a GP about persistent numbness or tingling, particularly if you have diabetes.',
            'https://www.nhs.uk/conditions/peripheral-neuropathy/'),

        SymptomSet('hearing loss', 'dizziness', 'nausea', 'ringing in ears'): Condition(
            'Meniere disease',
            'An inner ear disorder causing attacks of vertigo, ringing in the ears and fluctuating hearing loss.',
            'See a GP about repeated episodes of vertigo with hearing loss or tinnitus.',
            'https://www.nhs.uk/conditions/menieres-disease/'),

        SymptomSet('fever', 'nausea', 'abdominal pain', 'diarrhea', 'vomiting'): Condition(
            'Gastroenteritis',
            'Infection of the stomach and bowel causing sudden diarrhoea and vomiting. It usually settles within a few days.',
            'Drink plenty of fluids. Contact 111 if you cannot keep fluids down, or see blood in your stool.',
            'https://www.nhs.uk/symptoms/diarrhoea-and-vomiting/'),

        SymptomSet('chest pain', 'hoarseness', 'heartburn', 'difficulty swallowing'): Condition(
            'Gastroesophageal reflux disease',
            'Stomach acid repeatedly flows back into the gullet, causing heartburn, an acid taste and hoarseness.',
            'See a pharmacist first. Visit a GP if symptoms persist for more than three weeks or swallowing becomes difficult.',
            'https://www.nhs.uk/conditions/heartburn-and-acid-reflux/'),

        SymptomSet('fever', 'loss of appetite', 'nausea', 'abdominal pain', 'vomiting'): Condition(
            'Appendicitis',
            'Inflammation of the appendix, causing pain that begins near the navel and settles in the lower right abdomen.',
            'Go to A&E or call 999. A burst appendix is life-threatening, so do not wait it out.',
            'https://www.nhs.uk/conditions/appendicitis/'),

        SymptomSet('constipation', 'abdominal pain', 'diarrhea', 'bloating'): Condition(
            'Irritable bowel syndrome',
            'A common long-term gut condition causing cramping, bloating and alternating diarrhoea and constipation.',
            'See a GP to rule out other causes, especially if you also have weight loss or bleeding.',
            'https://www.nhs.uk/conditions/irritable-bowel-syndrome-ibs/'),

        SymptomSet('fever', 'weight loss', 'blood in stool', 'abdominal pain', 'diarrhea'): Condition(
            'Inflammatory bowel disease',
            "Long-term inflammation of the digestive tract, covering Crohn's disease and ulcerative colitis.",
            'See a GP about persistent diarrhoea, blood in your stool or unexplained weight loss.',
            'https://www.nhs.uk/conditions/inflammatory-bowel-disease/'),

        SymptomSet('loss of appetite', 'vomiting blood', 'heartburn', 'nausea', 'abdominal pain'): Condition(
            'Peptic ulcer disease',
            'A sore in the lining of the stomach or small intestine, causing burning upper abdominal pain.',
            'See a GP about persistent stomach pain. Call 999 if you vomit blood or pass black, tarry stools.',
            'https://www.nhs.uk/conditions/stomach-ulcer/'),

        SymptomSet('dark urine', 'jaundice', 'pale stool', 'nausea', 'fatigue'): Condition(
            'Viral hepatitis',
            'Viral inflammation of the liver, causing yellowing of the skin and eyes, dark urine and profound tiredness.',
            'See a GP promptly if your skin or eyes turn yellow, or your urine darkens without explanation.',
            'https://www.nhs.uk/conditions/hepatitis/'),

        SymptomSet('jaundice', 'loss of appetite', 'nausea', 'abdominal pain', 'vomiting'): Condition(
            'Gallstone disease',
            'Hardened deposits in the gallbladder that can block the bile duct, causing sudden severe pain below the right ribs.',
            'See a GP about repeated episodes. Seek urgent care for pain lasting hours with fever or yellowing skin.',
            'https://www.nhs.uk/conditions/gallstones/'),

        SymptomSet('weight loss', 'bloating', 'rash', 'fatigue', 'diarrhea'): Condition(
            'Coeliac disease',
            'An immune reaction to gluten that damages the small intestine, causing bloating, diarrhoea and poor nutrient absorption.',
            'See a GP before cutting out gluten. Testing is only accurate while you are still eating it.',
            'https://www.nhs.uk/conditions/coeliac-disease/'),

        SymptomSet('weight loss', 'frequent urination', 'fatigue', 'excessive thirst', 'excessive hunger'): Condition(
            'Diabetes mellitus',
            'Blood sugar is too high because the body makes too little insulin or cannot use it properly, causing thirst and frequent urination.',
            'See a GP soon for a blood test. Seek urgent care for vomiting, drowsiness or breath smelling of pear drops.',
            'https://www.nhs.uk/conditions/diabetes/'),

        SymptomSet('constipation', 'hair loss', 'dry skin', 'cold intolerance', 'fatigue', 'weight gain'): Condition(
            'Hypothyroidism',
            'An underactive thyroid produces too little hormone, slowing the body down and causing tiredness, weight gain and cold intolerance.',
            'See a GP for a blood test if you are persistently tired, gaining weight and feeling the cold.',
            'https://www.nhs.uk/conditions/underactive-thyroid-hypothyroidism/'),

        SymptomSet('weight loss', 'tremor', 'palpitations', 'heat intolerance', 'anxiety'): Condition(
            'Hyperthyroidism',
            'An overactive thyroid floods the body with hormone, causing weight loss, tremor, palpitations and heat intolerance.',
            'See a GP for a blood test. Seek urgent care for a very rapid heartbeat with fever and confusion.',
            'https://www.nhs.uk/conditions/overactive-thyroid-hyperthyroidism/'),

        SymptomSet('weight loss', 'low blood pressure', 'nausea', 'fatigue', 'muscle weakness'): Condition(
            'Adrenal insufficiency',
            "Addison's disease: the adrenal glands make too little cortisol, causing exhaustion, weight loss and darkened skin.",
            'See a GP about persistent fatigue with weight loss. Call 999 for sudden severe weakness, vomiting and collapse.',
            'https://www.nhs.uk/conditions/addisons-disease/'),

        SymptomSet('abdominal pain', 'painful urination', 'frequent urination', 'blood in urine'): Condition(
            'Urinary tract infection',
            'A bacterial infection of the bladder or urethra, causing burning on passing urine and a constant urge to go.',
            'See a pharmacist or GP. Seek urgent care if you develop back pain, fever or shivering.',
            'https://www.nhs.uk/conditions/urinary-tract-infections-utis/'),

        SymptomSet('fever', 'painful urination', 'nausea', 'back pain', 'chills'): Condition(
            'Pyelonephritis',
            'A kidney infection, usually spreading up from the bladder, causing back or side pain with fever and shivering.',
            'Contact a GP or 111 the same day. Untreated kidney infections can cause lasting damage.',
            'https://www.nhs.uk/conditions/kidney-infection/'),

        SymptomSet('nausea', 'blood in urine', 'back pain', 'abdominal pain', 'vomiting'): Condition(
            'Kidney stones',
            'Hard deposits that form in the kidneys and cause severe waves of pain in the side or back as they pass.',
            'Contact 111 for severe pain. Go to A&E if you also have a fever, or are vomiting and unable to keep fluids down.',
            'https://www.nhs.uk/conditions/kidney-stones/'),

        SymptomSet('joint pain', 'joint swelling', 'fatigue', 'morning stiffness'): Condition(
            'Rheumatoid arthritis',
            'An autoimmune disease attacking the joint lining, causing symmetrical swelling and stiffness that is worst in the morning.',
            'See a GP early about joint swelling with morning stiffness lasting over 30 minutes. Early treatment prevents damage.',
            'https://www.nhs.uk/conditions/rheumatoid-arthritis/'),

        SymptomSet('back pain', 'joint swelling', 'joint pain', 'morning stiffness'): Condition(
            'Osteoarthritis',
            'Wear and tear of joint cartilage causing pain and stiffness that worsens with use and eases with rest.',
            'See a GP if joint pain limits daily activities or is not helped by over-the-counter painkillers.',
            'https://www.nhs.uk/conditions/osteoarthritis/'),

        SymptomSet('fever', 'joint swelling', 'joint pain', 'hair loss', 'rash', 'fatigue'): Condition(
            'Systemic lupus erythematosus',
            'An autoimmune disease that can affect skin, joints and organs, often with a butterfly-shaped rash across the face.',
            'See a GP about unexplained joint pain with rashes and fatigue, particularly if sunlight worsens the rash.',
            'https://www.nhs.uk/conditions/lupus/'),

        SymptomSet('itching', 'joint pain', 'dry skin', 'rash'): Condition(
            'Psoriasis',
            'An immune condition causing raised, scaly patches of skin, most often on elbows, knees and scalp.',
            'See a GP if patches are widespread, painful, or accompanied by joint pain and swelling.',
            'https://www.nhs.uk/conditions/psoriasis/'),

        SymptomSet('insomnia', 'memory loss', 'loss of appetite', 'fatigue', 'depressed mood'): Condition(
            'Major depressive disorder',
            'Persistent low mood and loss of interest lasting weeks or more, with changes to sleep, appetite and concentration.',
            'Talk to a GP. If you are having thoughts of harming yourself, call 111 or the Samaritans on 116 123 now.',
            'https://www.nhs.uk/mental-health/conditions/depression-in-adults/'),

        SymptomSet('insomnia', 'muscle pain', 'irritability', 'palpitations', 'anxiety'): Condition(
            'Generalised anxiety disorder',
            'Excessive worry about many things on most days, with restlessness, muscle tension and disturbed sleep.',
            'See a GP if anxiety is hard to control and interferes with work, sleep or relationships.',
            'https://www.nhs.uk/mental-health/conditions/generalised-anxiety-disorder-gad/'),

        SymptomSet('tingling', 'dizziness', 'shortness of breath', 'chest pain', 'palpitations', 'anxiety'): Condition(
            'Panic disorder',
            'Recurrent sudden attacks of intense fear with a pounding heart, breathlessness and tingling, peaking within minutes.',
            'See a GP. If this is your first episode of chest pain and breathlessness, get it checked urgently to rule out the heart.',
            'https://www.nhs.uk/mental-health/conditions/panic-disorder/'),

        SymptomSet('insomnia', 'excessive sleepiness', 'fatigue', 'headache', 'irritability'): Condition(
            'Obstructive sleep apnoea',
            'The airway repeatedly collapses during sleep, interrupting breathing and causing loud snoring and daytime sleepiness.',
            'See a GP if you snore heavily and feel sleepy in the day. Do not drive if you are struggling to stay awake.',
            'https://www.nhs.uk/conditions/sleep-apnoea/'),
    }

    @staticmethod
    def diagnosis(*symptoms: Symptom):

        if not all(isinstance(symptom, Symptom) for symptom in symptoms):
            raise TypeError("Expected Symptom arguments")

        symptoms = SymptomSet(*symptoms)

        key = max(Diagnoser.CONDITIONS, key=lambda symptom_set: symptom_set @ symptoms)

        return Diagnoser.CONDITIONS[key], key @ symptoms
