from .multiple_choice_quiz import MultipleChoiceQuiz
from .function_test import FunctionTest
from .free_text_test import FreeTextTest
from .select_multiple_quiz import SelectMultipleQuiz
from .value_test import ValueTest
from .quiz_hint import QuizHint
from datetime import datetime
import ipywidgets as widgets

disch_summ = """
Service: MEDICINE

Chief Complaint:
5 days worsening SOB, DOE

History of Present Illness:
Pt is a 63M w/ h/o metastatic carcinoid tumor, HTN, 
hyperlipidemia who reports increasing SOB and DOE starting about 
a month ago but worsening significantly within the last 5 days. 
It has recently gotten so bad he can barely get up out of a 
chair without getting short of breath. He reports orthopnea but no PND. 

He reports no fever or chills, no URI symptoms, no recent travel, no changes 
in his medications.

Pt also reports ~5 episodes of chest pain in the last few weeks 
which he describes as pressure on his mid-sternum and usually 
occurs during exertion.

Past Medical History:
1. metastatic carcinoid tumor, Dx'ed 2002
2. hypertension
3. hyperlipidemia
4. carotid endarterectomy 1999
5. depression/anxiety

Social History:
Previously homeless, now lives with two daughters. Currently employed full-time.

Family History:
early CAD

Brief Hospital Course:
1. SOB: likely from CHF
The patient was initially diuresed for mild pulmonary edema: he 
received 20 IV Lasix on night of admission and 40mg [**9-10**], with 
good UOP. On [**9-10**], pt was reporting improvement of symptoms and 
able to walk around his room with 4L O2 NC. The following day he 
reported feeling worse, with increasing SOB, and was found to 
now be in oliguric renal failure. CXR [**9-11**] 8am showed showed 
atelectasis with possible superimposed pneumonia. Emergent TTE 
showed decreased EF (30%), anteroapical infarct with 
moderate-to-severe overall left ventricular contractile 
dysfunction; bicusapid aortic valve with at least mild aortic 
stenosis. He was sent to the MICU.

Medications on Admission:
ASA 81mg po qd
Lipitor 20mg po qpm

Discharge Disposition:
Extended Care
Discharge Diagnosis:
Primary: congestive heart failure
Secondary: metastatic carcinoid tumor, hypertension, 
hyperlipidemia, diabetes mellitus type 2, basal cell carcinoma

Discharge Condition:
good, stable
"""

quiz_disch_summ1 = MultipleChoiceQuiz("What is the main reason the patient came to the hospital?",
                  answer="He was experiencing shortness of breath.",
                  options=[
                      "He was referred by his oncologist.",
                      "He had a fever."
                  ])

quiz_disch_summ2 = SelectMultipleQuiz("Which of the following conditions does the patient have?.",
                  answer=["Congestive Heart Failure", "Diabetes", "Cancer"],
                  options=["Pneumonia", "Coronary Artery Disease"]
                  )

quiz_disch_summ3 = MultipleChoiceQuiz("The patient doesn't have any living relatives.", answer="False", shuffle_answer=False)

quiz_disch_summ4 = FreeTextTest("How many episodes of chest pain has the patient had in the last few weeks?", answer=["5", "five"])

quiz_precision = MultipleChoiceQuiz("What is the precision/PPV of the system?", answer=0.727, options=[0.4, 0.727, 0.8, 0.9, ],
                                   shuffle_answer=False)

quiz_recall = MultipleChoiceQuiz("What is the recall/sensitivity of the system?", answer=0.8, options=[0.4, 0.727, 0.8, 0.9, ],
                                shuffle_answer=False)

hint_covid_performance = QuizHint("This hint is for the following quiz.", hints=[
    widgets.HTML("""Of the 100 patients who have Covid, how many were classified as positive? """),
    widgets.HTML("""Are there any negative patients who were classified as positive? """),
])

quiz_covid_performance = MultipleChoiceQuiz("""What is the estimated prevalence of Covid?""",
                  answer="0.075",
                  options=["0.075", "0.15", "0.2", "0.05"])

quiz_rule_based_v_statistical1 = MultipleChoiceQuiz("""To identify patients with cancer, you review notes and annotate cases of cancer in text. 
You then feed your annnotations into a deep neural network which makes predictions on new documents.""",
                  answer="Statistical",
                  options=["Rule-Based", "Statistical"])

quiz_rule_based_v_statistical2 = MultipleChoiceQuiz("""You build a Covid-19 surveillance system with NLP which identifies patients who are positive for Covid.  
You first identify terms which refer to Covid such as 'COVID-19', 'SARS-COV-2', 'novel coronavirus'.
Then you implement logic to exclude mentions which refer to past medical history or to being exposed to someone else with Covid.""",
                  answer="Rule-Based",
                  options=["Rule-Based", "Statistical"])

quiz_text_3 = MultipleChoiceQuiz("""<h4>TODO</h4>Using the variable `text` that we defined above, what would be the value of
<p style="font-family:courier";>text[3]</p>""", answer="e",
                  options=["i", "Chi", "e", "E"])

quiz_len_empty = FreeTextTest('What value would be generated by the following code:</br><p style="font-family:courier";>len("")</p> ',
            answer=0)

quiz_split_pna_empty = MultipleChoiceQuiz("""What would happen if you split the string `"pna"` on an empty string?""",
                  answer="['p', 'n', 'a']",
                  options=["An error would be raised.", "You'd get an empty list.", "['pna']"])

hint_tokenize_disch_summ = QuizHint(hints=[
    widgets.HTML("""If 'He' and 'he' both appear in the document, how would you make sure they count as the same token?"""),
    widgets.HTML("""If you wanted to also get counts of tokens, you could use Python's `Counter` class:</br>
    <p style="font-family:courier";>from collections import Counter</br>help(Counter)</p>"""),
])


def test_get_section_name_validation_func(func):
    texts = [
        "Chief Complaint:\n5 days worsening SOB, DOE",
        "History of Present Illness:\nPt is a 63M w/ h/o metastatic carcinoid tumor.",
        "Social History:\nLives alone with two daughters."
    ]
    expected = ["Chief Complaint", "History of Present Illness", "Social History"]
    for text, expected in zip(texts, expected):
        if (actual := func(text)) != expected:
            print(f"Incorrect. Expected {expected}, got {actual} for {text}")
            return
    print("That is correct!")
test_get_section_name = ValueTest(validation_func=test_get_section_name_validation_func)


def test_pneumonia_in_text_validation_func(func):
    pna_strings = [
        "The patient has pneumonia.",
        "INDICATION: EVALUATE FOR PNEUMONIA",
        "Patient shows symptoms concerning for pna.",
        "The chest image found no evidence of pna",
    ]
    for string in pna_strings:
        if (actual := func(string)) is not True:
            print(f"Incorrect. Expected True, got {actual} with string {string}")
            return
    if func("") is True:
        print(f"Incorrect. Expected False, got True with \"\"")
        return
    print("That is correct!")
test_pneumonia_in_text = ValueTest(validation_func=test_pneumonia_in_text_validation_func)

quiz_mc_pneumonia_in_text = MultipleChoiceQuiz("If the function above returns True, that means the note indicates the patient has pneumonia.", answer="False")

hint_generate_chief_complaint = QuizHint(hints=[
    widgets.HTML("""Your output should like like:</br><img src="./media/hint_generate_chief_complaint.png" width="75%"></img>""")
])

quiz_medical_concepts_1 = MultipleChoiceQuiz("""
Pt is a 63M w/ h/o <strong>metastatic carcinoid tumor</strong>, <strong>HTN</strong> and <strong>hyperlipidemia</strong>
""",
                  options=["Diagnoses", "Medications", "Signs and Symptoms", "Social Determinants"],
                   answer="Diagnoses"
                  )

quiz_medical_concepts_2 = MultipleChoiceQuiz("""
Medications on Admission:
<ol>
<li> <strong>ASA 81mg po qd</strong></li>
<li><strong>Lipitor 20mg po qpm</strong> </li>
</ul>
""",
        options=["Diagnoses", "Medications", "Signs and Symptoms", "Social Determinants"],
        answer="Medications"
                  )

quiz_medical_concepts_3 = MultipleChoiceQuiz("""
Previously <strong>homeless</strong> 2012-2013. Currently <strong>lives with his two daughters</strong>. 
He is <strong>employed full-time</strong>.
""",
                  options=["Diagnoses", "Medications", "Signs and Symptoms", "Social Determinants"],
                   answer="Social Determinants"
                  )

def test_dx_text_validation_func(doc):
    if len(doc.ents) != 3:
        print(f"Incorrect. doc should have 3 ents, not {len(doc.ents)}")
        return
    if (ent_labels := {ent.label_ for ent in doc.ents}) != {"DIAGNOSIS"}:
        print(f"Incorrect. doc should only have 'DIAGNOSIS' entities, your doc has {ent_labels}")
        return
    expected_texts = {"metastatic carcinoid tumor", "HTN", "hyperlipidemia"}
    if (ent_texts := {ent.text for ent in doc.ents}) != expected_texts:
        print(f"Incorrect. Your doc has entities {ent_texts}, should have {expected_texts}")
        return
    print("That is correct!")
test_dx_text = ValueTest(validation_func=test_dx_text_validation_func)

def test_ckd_stage_x_validation_func(nlp):
    for text in ["CKD Stage 3", "ckd stage 4", "ckd stage 5", "ckd"]:
        doc = nlp(text)
        if len(doc.ents) != 1:
            print(f"Doc should have 1 ent, not {len(doc.ents)} for '{doc}'")
            return
        ent = doc.ents[0]
        if "stage" in text:
            if (ent[:2].text.lower() != "ckd stage") or (ent[-1].text.lower() not in ("3", "4", "5")):
                print(f"Incorrect entity '{ent}' in '{doc}'")
                return
        if ent.label_ != "DIAGNOSIS":
            print(f"ent should have a label of 'DIAGNOSIS', not '{ent.label_}'")
            return
    print("That is correct!")


test_ckd_stage_x = ValueTest(validation_func=test_ckd_stage_x_validation_func)

hint_discharge_summ_target_rules = QuizHint(hints=[
    widgets.HTML("""Here is an example of some rules:</br>
    <img src="./media/hint_disch_summ_target_rules.png" width="60%"></img>"""),
    widgets.HTML("""Here is processed text using these rules:</br>
    <img src="./media/hint_disch_summ_extracted.png" width="70%"></img>""")
])


def build_nlp_context(rules=True):
    import medspacy
    from medspacy.target_matcher import TargetRule
    if rules:
        nlp = medspacy.load()
    else:
        nlp = medspacy.load(disable=["medspacy_context"])
        nlp.add_pipe("medspacy_context", config={"rules": False})

    target_rules = [
        TargetRule("pneumonia", "DIAGNOSIS"),
        TargetRule("bronchitis", "DIAGNOSIS"),
        TargetRule("nephrectomy", "PROCEDURE"),
        TargetRule("pneumothorax", "DIAGNOSIS"),
        TargetRule("breast cancer", "DIAGNOSIS"),
        TargetRule("warfarin", "MEDICATION"),
        TargetRule("rash", "SIGN/SYMPTOM"),
        TargetRule("diabetes", "DIAGNOSIS"),

        TargetRule("COVID-19", "DIAGNOSIS", pattern=r"covid-?(19)?"),
        TargetRule("SARS-COV-2", "DIAGNOSIS")
    ]

    nlp.get_pipe("medspacy_target_matcher").add(target_rules)

    return nlp

quiz_pneumonia_negated_select_multiple = SelectMultipleQuiz(
    "Select all sentences where pneumonia is negated.",
    answer=[1, 3], options=list(range(1,6)), shuffle_answer=False)

quiz_context_attributes1 = SelectMultipleQuiz(
    "He was previously <strong>homeless</strong>.",
    answer=["is_historical"],
    options=["is_negated", "is_historical", "is_uncertain", "is_family", "is_hypothetical"],
    shuffle_answer=False
)

quiz_context_attributes2 = SelectMultipleQuiz(
    "If you develop any <strong>bleeding</strong>, go to the ER right away.",
    answer=["is_hypothetical"],
    options=["is_negated", "is_historical", "is_uncertain", "is_family", "is_hypothetical"],
    shuffle_answer=False
)

quiz_context_attributes3 = SelectMultipleQuiz(
    "Her father had a <strong>heart attack</strong> in 1996.",
    answer=["is_historical", "is_family"],
    options=["is_negated", "is_historical", "is_uncertain", "is_family", "is_hypothetical"],
    shuffle_answer=False
)

quiz_context_attributes4 = SelectMultipleQuiz(
    "The patient presents with symptoms concerning for <strong>Covid-19</strong>.",
    answer=["is_uncertain"],
    options=["is_negated", "is_historical", "is_uncertain", "is_family", "is_hypothetical"],
    shuffle_answer=False
)

quiz_context_attributes5 = SelectMultipleQuiz(
    "He lives with his <strong>two daughters.</strong>",
    answer=[],
    options=["is_negated", "is_historical", "is_uncertain", "is_family", "is_hypothetical"],
    shuffle_answer=False
)

def test_classify_covid_validation_func(func):
    nlp = build_nlp_context()
    texts = [
        "The patient has Covid-19.",
        "Her husband recently came down with Covid. He is isolated and doing okay. She tested positive for SARS-COV-2 one week later.",
        "If you test positive for SARS-COV-2, isolate according to CDC guidelines.",
        "She recently had a positive PCR for Covid-19.",
        "She had symptoms which were concerning for Covid-19 but her Covid test was negative."
    ]
    labels = ["POS", "POS", "NEG", "POS", "NEG"]
    for (text, label) in zip(texts, labels):
        doc = nlp(text)
        pred = func(doc)
        if pred != label:
            print(f"Incorrect. Expected {label}, got {pred} for doc: '{text}'")
            return
    print("That is correct!")
test_classify_covid = ValueTest(validation_func=test_classify_covid_validation_func)

hint_custom_context = QuizHint(hints=[
    widgets.HTML("""Here is output of the processed texts with added target rules and context rules:</br></br>
    <img src="./media/hint_custom_context.png" width="75%"></img>""")
])

quiz_note_categories = SelectMultipleQuiz("Which of the following note types are stored in MIMIC?.",
                                         answer=['DISCHARGE_SUMMARY', 'MD Notes', 'Nursing/Other', 'RADIOLOGY_REPORT'],
                                         options=['DISCHARGE_SUMMARY', "EMERGENCY_NOTE", 'MD Notes', 'Nursing/Other', "PROGRESS_NOTE", 'RADIOLOGY_REPORT']
                                         )


quiz_pna_in_disch_summ = MultipleChoiceQuiz("""<h4>TODO</h4>
The doc above should have an entity of pneumonia highlighted. What section of the note did that occur in?""",
                    answer="MRI (Imaging)",
                    options=[
                        "Chief Complaint",
                        "Hospital Course",
                        "Pertinent Results (Labs and Studies)"
                    ])

quiz_n_rad_reports = FreeTextTest("How many radiology reports did this hospitalization have?", answer=[5, "five"])
quiz_rad_interpretation = SelectMultipleQuiz("""<h4>TODO</h4>
According to radiology report #3, what does the radiologist think caused the rounded opacity overlying the left ilium?
Select all that apply.""",
                  answer=["Aspiration Pneumonia", "Left Hilar Mass", "Scoliosis", "Complications from Ventilation"])

def test_load_nlp_validation_func(nlp):
    from spacy.lang.en import English
    if not isinstance(nlp, English):
        print(f"Incorrect. nlp should have type spacy.lang.en.English, not {type(nlp)}")
        return

    expected_pipe_names = ['medspacy_pyrush', 'medspacy_target_matcher', 'medspacy_context']
    if (actual_pipe_names := nlp.pipe_names) != expected_pipe_names:
        print(f"Incorrect. nlp.pipe_names should be {expected_pipe_names}, not {actual_pipe_names}")

    print("That is correct!")

test_load_nlp = ValueTest(validation_func=test_load_nlp_validation_func)

def test_load_nlp_add_sectionizer_validation_func(nlp):
    from spacy.lang.en import English
    if not isinstance(nlp, English):
        print(f"Incorrect. nlp should have type spacy.lang.en.English, not {type(nlp)}")
        return

    expected_pipe_names = ['medspacy_pyrush', 'medspacy_target_matcher', 'medspacy_context', "medspacy_sectionizer"]
    if (actual_pipe_names := nlp.pipe_names) != expected_pipe_names:
        print(f"Incorrect. nlp.pipe_names should be {expected_pipe_names}, not {actual_pipe_names}")

    print("That is correct!")

test_load_nlp_add_sectionizer = ValueTest(validation_func=test_load_nlp_add_sectionizer_validation_func)

quiz_pna_annotation1 = MultipleChoiceQuiz(
    """<p style="font-family:courier";>
    REASON FOR THIS EXAMINATION:</br>
      Please evaluate for infiltrates. </br>
      </br>
     IMPRESSION: </br>No radiographic evidence of pneumonia.</p></br>""",
    answer=0,
    options=[0, 1], shuffle_answer=False
)

quiz_pna_annotation2 = MultipleChoiceQuiz(
    """<p style="font-family:courier";>IMPRESSION:  Findings consistent with CHF, although underlying bilateral lower</br>
     lobe pneumonias cannot be excluded. Follow up.</p></br>""",
    answer=1,
    options=[0, 1], shuffle_answer=False
)

quiz_pna_annotation3 = MultipleChoiceQuiz(
    """<p style="font-family:courier";>IMPRESSION:</br>
     1. Mild CHF.</br>
     2. Left lower lobe consolidation with effusion, probably representing pneumonia.</p></br>""",
    answer=1,
    options=[0, 1], shuffle_answer=False
)

quiz_pna_annotation4 = MultipleChoiceQuiz(
    """<p style="font-family:courier";>IMPRESSION:</br>

     1) Tubes and lines as described above.</br>

     2) No acute infiltrate or consolidation.</p></br>""",
    answer=0,
    options=[0, 1], shuffle_answer=False
)

quiz_num_pna_notes = FreeTextTest("How many notes are annotated in this dataset?", answer=140)

quiz_num_pos_pna_notes = MultipleChoiceQuiz("How proportion of notes are annotated as positive?",
                                           answer="49%",
                                           options=["68", "68%", "34%"])

test_classify_pna_1 = ValueTest(expected=0)
test_classify_pna_2 = ValueTest(expected=1)


def evaluate_system(df):
    import pandas as pd
    """Evaluate the predictions made by the NLP system and compare against the reference standard
    and baseline NLP system. Returns a DataFrame with nlp and baseline scores."""
    from sklearn.metrics import classification_report
    rslts_baseline = classification_report(df["document_classification"], df["baseline_document_classification"],
                                           output_dict=True)
    rslts_nlp = classification_report(df["document_classification"], df["nlp_document_classification"],
                                      output_dict=True)
    cols = ("system", "accuracy", "precision", "recall", "f1-score", "n_positive", "n_total")
    rows = []
    for name, rslts in zip(("baseline", "nlp"), (rslts_baseline, rslts_nlp)):
        rows.append(
            (name, rslts["accuracy"], rslts["1"]["precision"], rslts["1"]["recall"],
             rslts["1"]["f1-score"], rslts["1"]["support"], len(df)))
    return pd.DataFrame(rows, columns=cols)

def read_pneumonia_data(train_test="train", n_random=None):
    directory = f"../data"
    import os
    import pandas as pd
    filepath = os.path.join(directory, f"pneumonia_data_{train_test}.json")
    print("Reading data from:", filepath)

    df = pd.read_json(filepath)
    if n_random is not None:
        df = df.sample(n=n_random).reset_index(drop=True)
    return df

def read_doc_annotations(train_test="train", n=None):
    import os
    directory = f"../data/pneumonia_data/{train_test}/"
    import pandas as pd
    print('Reading annotations from directory : ' + directory)
    data = []

    filenames = os.listdir(directory)
    if n is not None:
        filenames = filenames[:n]
    for name in filenames:
        if name.endswith('.txt') or name.endswith('.ann'):
            basename = name.split('.')[0]
            text_fp = os.path.join(directory, basename + ".txt")
            anno_fp = os.path.join(directory, basename + ".ann")
            with open(text_fp) as f:
                text = f.read()
            document_classification = read_document_annotation(anno_fp)
            data.append((basename, text, document_classification))
    df = pd.DataFrame(data, columns=["filename", "text", "document_classification", ])

    return df

def read_document_annotation(fp):
    with open(fp) as f:
        for line in f:
            if "PNEUMONIA_DOC_NO" in line:
                return 0
            if "PNEUMONIA_DOC_YES" in line:
                return 1
    return

def add_document_classifications(df, docs, classify_pna):
    df["nlp_document_classification"] = [classify_pna(doc) for doc in docs]
    df["doc"] = docs
    return df

quiz_type_text0 = MultipleChoiceQuiz("""What would be the value of <p style="font-family:courier";>text[0]</p>""",
                  options=["'Chief'", "'C'"], answer="'C'")
