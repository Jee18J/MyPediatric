# import streamlit as st
# import pandas as pd
# import numpy as np
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.preprocessing import LabelEncoder

# # Medical knowledge base
# SYMPTOM_DEFINITIONS = {
#     "FEVER": {
#         "follow_up": [
#             {"question": "Severity", "type": "radio", 
#              "options": ["<100°F (mild)", "100-102°F (moderate)", ">102°F (severe)"],
#              "weights": {"<100°F (mild)": 0.7, "100-102°F (moderate)": 1.0, ">102°F (severe)": 1.5}}
#         ],
#         "red_flags": [">102°F for >3 days", "Fever with stiff neck"]
#     },
#     "COUGH": {
#         "follow_up": [
#             {"question": "Type", "type": "selectbox",
#              "options": ["Dry", "Wet/Phlegmy", "Barking", "Whooping"],
#              "weights": {"Dry": 1.0, "Wet/Phlegmy": 1.2, "Barking": 1.8, "Whooping": 2.0}}
#         ]
#     }
# }

# @st.cache_data
# def load_data():
#     df = pd.read_csv("dataset/trial_updated.csv")
#     return df

# def main():
#     st.set_page_config(page_title="Pediatric Symptom Checker", page_icon="👶")
#     st.title("👶 Pediatric Symptom Checker")
    
#     # Step 1: Primary symptom selection
#     st.header("Step 1: Select your child's main symptoms")
#     primary_symptoms = st.multiselect(
#         "What symptoms is your child experiencing?",
#         options=list(SYMPTOM_DEFINITIONS.keys()),
#         placeholder="Select symptoms..."
#     )
    
#     # Step 2: Detailed symptom questions
#     symptom_details = {}
#     for symptom in primary_symptoms:
#         st.subheader(f"Details about {symptom.lower()}")
        
#         for question in SYMPTOM_DEFINITIONS[symptom]["follow_up"]:
#             response = None
#             if question["type"] == "radio":
#                 response = st.radio(
#                     question["question"],
#                     options=question["options"],
#                     key=f"{symptom}_{question['question']}"
#                 )
#             elif question["type"] == "selectbox":
#                 response = st.selectbox(
#                     question["question"],
#                     options=question["options"],
#                     key=f"{symptom}_{question['question']}"
#                 )
            
#             if response:
#                 symptom_details[f"{symptom}"] = question["weights"][response]
    
#     # Step 3: Predict
#     if st.button("Analyze Symptoms", type="primary"):
#         if not primary_symptoms:
#             st.warning("Please select at least one symptom")
#             return
        
#         # Load data
#         df = load_data()
        
#         # Prepare features (only numerical columns)
#         numerical_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
#         if "CONDITION" in numerical_cols:
#             numerical_cols.remove("CONDITION")
        
#         X = df[numerical_cols]
#         y = df["CONDITION"]
        
#         # Train model
#         model = RandomForestClassifier()
#         model.fit(X, y)
        
#         # Prepare input features
#         input_features = {col: 0.0 for col in numerical_cols}
        
#         # Apply symptom weights
#         for symptom, weight in symptom_details.items():
#             if symptom in input_features:
#                 input_features[symptom] = weight
        
#         # Convert to DataFrame
#         input_df = pd.DataFrame([input_features])[numerical_cols]
        
#         # Make prediction
#         prediction = model.predict(input_df)[0]
#         probabilities = model.predict_proba(input_df)[0]
        
#         st.success(f"Most likely condition: **{prediction}**")
        
#         # Show probabilities
#         st.subheader("Condition Probabilities")
#         prob_df = pd.DataFrame({
#             "Condition": model.classes_,
#             "Probability": probabilities
#         }).sort_values("Probability", ascending=False)
#         st.dataframe(prob_df.head(5))
        
#         # Show red flags
#         st.subheader("Red Flags to Watch For")
#         for symptom in primary_symptoms:
#             if "red_flags" in SYMPTOM_DEFINITIONS[symptom]:
#                 for flag in SYMPTOM_DEFINITIONS[symptom]["red_flags"]:
#                     st.warning(f"⚠️ {flag}")

# if __name__ == "__main__":
#     main()import streamlit as st


# WORKING

# import streamlit as st
# import pandas as pd
# import numpy as np
# from sklearn.ensemble import RandomForestClassifier

# # Medical knowledge base with all symptoms
# SYMPTOM_DEFINITIONS = {
#     "FEVER": {
#         "follow_up": [
#             {"question": "Severity", "type": "radio", 
#              "options": ["<100°F (mild)", "100-102°F (moderate)", ">102°F (severe)"],
#              "weights": {"<100°F (mild)": 0.7, "100-102°F (moderate)": 1.0, ">102°F (severe)": 1.5}}
#         ],
#         "red_flags": [">102°F for >3 days", "Fever with stiff neck"]
#     },
#     "COUGH": {
#         "follow_up": [
#             {"question": "Type", "type": "selectbox",
#              "options": ["Dry", "Wet/Phlegmy", "Barking", "Whooping"],
#              "weights": {"Dry": 1.0, "Wet/Phlegmy": 1.2, "Barking": 1.8, "Whooping": 2.0}}
#         ],
#         "red_flags": ["Whooping sound when breathing in", "Lasting more than 3 weeks"]
#     },
#     "RUNNY_NOSE": {
#         "follow_up": [
#             {"question": "Discharge Color", "type": "selectbox",
#              "options": ["Clear", "White", "Yellow", "Green"],
#              "weights": {"Clear": 1.0, "White": 1.1, "Yellow": 1.3, "Green": 1.5}}
#         ]
#     },
#     "SNEEZING": {
#         "follow_up": [
#             {"question": "Frequency", "type": "radio",
#              "options": ["Occasional", "Frequent", "Constant"],
#              "weights": {"Occasional": 1.0, "Frequent": 1.3, "Constant": 1.5}}
#         ]
#     },
#     "MUSCLE_ACHES": {
#         "follow_up": [
#             {"question": "Severity", "type": "radio",
#              "options": ["Mild", "Moderate", "Severe"],
#              "weights": {"Mild": 1.0, "Moderate": 1.3, "Severe": 1.7}}
#         ]
#     },
#     "HEADACHE": {
#         "follow_up": [
#             {"question": "Location", "type": "selectbox",
#              "options": ["Forehead", "Temples", "Back of head", "Whole head"],
#              "weights": {"Forehead": 1.0, "Temples": 1.2, "Back of head": 1.5, "Whole head": 1.8}}
#         ],
#         "red_flags": ["Worst headache of life", "With neck stiffness"]
#     },
#     "WHEEZING": {
#         "follow_up": [
#             {"question": "When it occurs", "type": "selectbox",
#              "options": ["At night", "After exercise", "With allergies", "All the time"],
#              "weights": {"At night": 1.2, "After exercise": 1.5, "With allergies": 1.3, "All the time": 1.8}}
#         ],
#         "red_flags": ["Difficulty speaking due to breathing problems"]
#     },
#     "SHORTNESS_OF_BREATH": {
#         "follow_up": [
#             {"question": "Severity", "type": "radio",
#              "options": ["Mild (only with activity)", "Moderate (some limitation)", "Severe (at rest)"],
#              "weights": {"Mild (only with activity)": 1.2, "Moderate (some limitation)": 1.6, "Severe (at rest)": 2.0}}
#         ],
#         "red_flags": ["Lips or face turning blue"]
#     }
# }

# @st.cache_data
# def load_data():
#     df = pd.read_csv("dataset/trial_updated.csv")
#     # Fill NaN values with 0 for all symptoms
#     symptom_cols = [col for col in df.columns if col != "CONDITION"]
#     df[symptom_cols] = df[symptom_cols].fillna(0)
#     return df

# def main():
#     st.set_page_config(page_title="Pediatric Symptom Checker", page_icon="👶", layout="wide")
#     st.title("👶 Pediatric Symptom Checker")
    
#     # Load data
#     df = load_data()
    
#     # Get all available symptoms from dataset
#     all_symptoms = [col for col in df.columns if col not in ["CONDITION", "FEVER_SEVERITY", "COUGH_TYPE"]]
    
#     # Step 1: Primary symptom selection
#     with st.expander("Step 1: Select main symptoms", expanded=True):
#         primary_symptoms = st.multiselect(
#             "What symptoms is your child experiencing?",
#             options=all_symptoms,
#             placeholder="Select symptoms..."
#         )
    
#     # Step 2: Detailed symptom questions
#     symptom_details = {}
#     if primary_symptoms:
#         with st.expander("Step 2: Provide symptom details", expanded=True):
#             for symptom in primary_symptoms:
#                 if symptom in SYMPTOM_DEFINITIONS:
#                     st.subheader(f"Details about {symptom.lower().replace('_', ' ')}")
                    
#                     for question in SYMPTOM_DEFINITIONS[symptom]["follow_up"]:
#                         response = None
#                         if question["type"] == "radio":
#                             response = st.radio(
#                                 question["question"],
#                                 options=question["options"],
#                                 key=f"{symptom}_{question['question']}"
#                             )
#                         elif question["type"] == "selectbox":
#                             response = st.selectbox(
#                                 question["question"],
#                                 options=question["options"],
#                                 key=f"{symptom}_{question['question']}"
#                             )
                        
#                         if response:
#                             symptom_details[symptom] = {
#                                 "value": 1.0,  # Base value
#                                 "weight": question["weights"][response]
#                             }
#                 else:
#                     # For symptoms without follow-up questions
#                     severity = st.slider(
#                         f"Severity of {symptom.lower().replace('_', ' ')}",
#                         min_value=0.1,
#                         max_value=2.0,
#                         value=1.0,
#                         step=0.1,
#                         key=symptom
#                     )
#                     symptom_details[symptom] = {
#                         "value": severity,
#                         "weight": 1.0
#                     }
    
#     # Step 3: Predict
#     if st.button("Analyze Symptoms", type="primary", use_container_width=True):
#         if not primary_symptoms:
#             st.warning("Please select at least one symptom")
#             return
        
#         # Prepare features (only numerical columns)
#         numerical_cols = [col for col in df.columns if col != "CONDITION"]
#         X = df[numerical_cols]
#         y = df["CONDITION"]
        
#         # Train model
#         model = RandomForestClassifier()
#         model.fit(X, y)
        
#         # Prepare input features
#         input_features = {col: 0.0 for col in numerical_cols}
        
#         # Apply symptom weights
#         for symptom, details in symptom_details.items():
#             if symptom in input_features:
#                 input_features[symptom] = details["value"] * details["weight"]
        
#         # Special handling for severity subtypes
#         if "FEVER" in symptom_details and "FEVER_SEVERITY" in numerical_cols:
#             input_features["FEVER_SEVERITY"] = symptom_details["FEVER"]["weight"]
        
#         if "COUGH" in symptom_details and "COUGH_TYPE" in numerical_cols:
#             input_features["COUGH_TYPE"] = symptom_details["COUGH"]["weight"]
        
#         # Convert to DataFrame
#         input_df = pd.DataFrame([input_features])[numerical_cols]
        
#         # Make prediction
#         prediction = model.predict(input_df)[0]
#         probabilities = model.predict_proba(input_df)[0]
        
#         # Display results
#         col1, col2 = st.columns([1, 2])
        
#         with col1:
#             st.success(f"### Most likely condition: **{prediction}**")
            
#             # Show probabilities
#             st.subheader("Top Possible Conditions")
#             prob_df = pd.DataFrame({
#                 "Condition": model.classes_,
#                 "Probability": probabilities
#             }).sort_values("Probability", ascending=False).head(5)
#             st.dataframe(prob_df.style.format({"Probability": "{:.2%}"}), hide_index=True)
        
#         with col2:
#             # Show red flags
#             st.subheader("⚠️ Red Flags to Watch For")
#             red_flags_found = False
#             for symptom in primary_symptoms:
#                 if symptom in SYMPTOM_DEFINITIONS and "red_flags" in SYMPTOM_DEFINITIONS[symptom]:
#                     for flag in SYMPTOM_DEFINITIONS[symptom]["red_flags"]:
#                         st.error(f"• {flag}")
#                         red_flags_found = True
            
#             if not red_flags_found:
#                 st.info("No urgent red flags identified based on current symptoms")
            
#             # General advice
#             st.subheader("ℹ️ Recommended Actions")
#             if prediction in ["Meningitis", "Severe Pneumonia"]:
#                 st.error("**Seek emergency medical care immediately**")
#             elif prediction in ["Influenza (Flu)", "Bronchiolitis"]:
#                 st.warning("**Contact your pediatrician within 24 hours**")
#             else:
#                 st.info("**Monitor symptoms and contact doctor if they worsen**")

# if __name__ == "__main__":
#     main()

#WORKING


# import streamlit as st
# import pandas as pd
# import numpy as np
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.preprocessing import LabelEncoder

# # Enhanced medical knowledge base with more pediatric symptoms and refined weights
# SYMPTOM_DEFINITIONS = {
#     "FEVER": {
#         "follow_up": [
#             {"question": "Temperature", "type": "radio", 
#              "options": ["<100.4°F (normal)", "100.4-102.2°F (low-grade)", "102.2-104°F (moderate)", ">104°F (high)"],
#              "weights": {"<100.4°F (normal)": 0.5, "100.4-102.2°F (low-grade)": 1.0, "102.2-104°F (moderate)": 1.8, ">104°F (high)": 2.5},
#              "note": "In infants <3 months, any fever >100.4°F requires immediate evaluation"},
#             {"question": "Duration", "type": "selectbox",
#              "options": ["<24 hours", "1-3 days", "3-7 days", ">7 days"],
#              "weights": {"<24 hours": 0.8, "1-3 days": 1.0, "3-7 days": 1.5, ">7 days": 2.0}}
#         ],
#         "red_flags": [
#             "Fever >100.4°F in infant <3 months",
#             "Fever >104°F",
#             "Fever with stiff neck or photophobia",
#             "Fever with petechial rash",
#             "Fever lasting >5 days"
#         ],
#         "who_notes": "Fever patterns can help differentiate diseases - sustained in typhoid, quotidian in malaria"
#     },
#     "COUGH": {
#         "follow_up": [
#             {"question": "Type", "type": "selectbox",
#              "options": ["Dry", "Productive", "Barking", "Whooping", "Staccato"],
#              "weights": {"Dry": 1.0, "Productive": 1.2, "Barking": 1.8, "Whooping": 2.2, "Staccato": 2.0},
#              "note": "Barking cough suggests croup, whooping suggests pertussis"},
#             {"question": "Timing", "type": "radio",
#              "options": ["Daytime", "Nighttime", "With feeding", "After exercise", "All day"],
#              "weights": {"Daytime": 1.0, "Nighttime": 1.3, "With feeding": 1.5, "After exercise": 1.7, "All day": 1.5}}
#         ],
#         "red_flags": [
#             "Whooping sound on inspiration",
#             "Cough causing vomiting",
#             "Cough with cyanosis",
#             "Cough lasting >3 weeks",
#             "Sudden onset cough (possible aspiration)"
#         ]
#     },
#     "RESPIRATORY_DISTRESS": {
#         "follow_up": [
#             {"question": "Severity", "type": "radio",
#              "options": ["None", "Mild (intercostal retractions)", "Moderate (nasal flaring)", "Severe (grunting, head bobbing)"],
#              "weights": {"None": 0, "Mild (intercostal retractions)": 1.5, "Moderate (nasal flaring)": 2.0, "Severe (grunting, head bobbing)": 3.0},
#              "note": "WHO defines tachypnea as RR >60 in <2mo, >50 in 2-12mo, >40 in 1-5y"}
#         ],
#         "red_flags": [
#             "Respiratory rate >60/min",
#             "Cyanosis",
#             "Grunting",
#             "Severe retractions",
#             "Inability to speak/cry"
#         ]
#     },
#     "RASH": {
#         "follow_up": [
#             {"question": "Type", "type": "selectbox",
#              "options": ["Maculopapular", "Vesicular", "Petechial/Purpuric", "Urticarial", "Erythematous"],
#              "weights": {"Maculopapular": 1.0, "Vesicular": 1.5, "Petechial/Purpuric": 2.5, "Urticarial": 1.3, "Erythematous": 1.2},
#              "note": "Petechial rash requires immediate evaluation for meningococcemia"},
#             {"question": "Distribution", "type": "radio",
#              "options": ["Face", "Trunk", "Extremities", "Palms/soles", "Generalized"],
#              "weights": {"Face": 1.0, "Trunk": 1.2, "Extremities": 1.1, "Palms/soles": 1.8, "Generalized": 1.5}}
#         ],
#         "red_flags": [
#             "Petechial/purpuric rash",
#             "Rash with fever",
#             "Rash with mucosal involvement",
#             "Rapidly spreading rash",
#             "Rash with blistering"
#         ]
#     },
#     "VOMITING": {
#         "follow_up": [
#             {"question": "Frequency", "type": "radio",
#              "options": ["1-2 times", "3-5 times", ">5 times", "Projectile"],
#              "weights": {"1-2 times": 1.0, "3-5 times": 1.5, ">5 times": 2.0, "Projectile": 2.2},
#              "note": "Projectile vomiting in infants suggests pyloric stenosis"},
#             {"question": "Content", "type": "selectbox",
#              "options": ["Food", "Bile (green)", "Blood", "Coffee-ground"],
#              "weights": {"Food": 1.0, "Bile (green)": 1.8, "Blood": 2.5, "Coffee-ground": 2.3}}
#         ],
#         "red_flags": [
#             "Bilious vomiting",
#             "Hematemesis",
#             "Projectile vomiting in infants",
#             "Vomiting with severe abdominal pain",
#             "Vomiting with altered mental status"
#         ]
#     },
#     "DIARRHEA": {
#         "follow_up": [
#             {"question": "Frequency", "type": "radio",
#              "options": ["2-4 loose stools/day", "5-8 loose stools/day", ">8 loose stools/day", "Watery"],
#              "weights": {"2-4 loose stools/day": 1.0, "5-8 loose stools/day": 1.5, ">8 loose stools/day": 2.0, "Watery": 2.2},
#              "note": "WHO defines diarrhea as ≥3 loose stools/day"},
#             {"question": "Appearance", "type": "selectbox",
#              "options": ["Loose", "Mucoid", "Bloody", "Rice-water"],
#              "weights": {"Loose": 1.0, "Mucoid": 1.3, "Bloody": 2.0, "Rice-water": 2.2}}
#         ],
#         "red_flags": [
#             "Bloody diarrhea",
#             "Signs of dehydration (no tears, sunken eyes)",
#             "Diarrhea >2 weeks",
#             "Diarrhea with high fever",
#             ">8 watery stools/day"
#         ]
#     },
#     "EAR_PAIN": {
#         "follow_up": [
#             {"question": "Severity", "type": "radio",
#              "options": ["Mild", "Moderate", "Severe", "Disrupting sleep"],
#              "weights": {"Mild": 1.0, "Moderate": 1.3, "Severe": 1.7, "Disrupting sleep": 1.9},
#              "note": "Pulling ears in infants may indicate otitis media"},
#             {"question": "Duration", "type": "selectbox",
#              "options": ["<24 hours", "1-3 days", ">3 days"],
#              "weights": {"<24 hours": 1.0, "1-3 days": 1.2, ">3 days": 1.5}}
#         ],
#         "red_flags": [
#             "Ear pain with fever >102°F",
#             "Swelling behind ear",
#             "Facial weakness",
#             "Severe pain with sudden relief (possible rupture)"
#         ]
#     },
#     "SORE_THROAT": {
#         "follow_up": [
#             {"question": "Severity", "type": "radio",
#              "options": ["Mild", "Moderate", "Severe", "Unable to swallow"],
#              "weights": {"Mild": 1.0, "Moderate": 1.3, "Severe": 1.8, "Unable to swallow": 2.5},
#              "note": "Consider strep if >3 years with fever and no cough"},
#             {"question": "Appearance", "type": "selectbox",
#              "options": ["Red", "Exudate", "Ulcers", "Swollen tonsils"],
#              "weights": {"Red": 1.0, "Exudate": 1.5, "Ulcers": 1.8, "Swollen tonsils": 1.7}}
#         ],
#         "red_flags": [
#             "Drooling/inability to swallow",
#             "Neck stiffness with sore throat",
#             "Trismus (difficulty opening mouth)",
#             "Voice changes (hot potato voice)"
#         ]
#     },
#     "ABDOMINAL_PAIN": {
#         "follow_up": [
#             {"question": "Location", "type": "selectbox",
#              "options": ["Diffuse", "Periumbilical", "Right lower quadrant", "Epigastric", "Left lower quadrant"],
#              "weights": {"Diffuse": 1.0, "Periumbilical": 1.2, "Right lower quadrant": 2.0, "Epigastric": 1.5, "Left lower quadrant": 1.8},
#              "note": "RLQ pain suggests appendicitis, rebound tenderness is concerning"},
#             {"question": "Severity", "type": "radio",
#              "options": ["Mild", "Moderate", "Severe", "Doubled over"],
#              "weights": {"Mild": 1.0, "Moderate": 1.5, "Severe": 2.0, "Doubled over": 2.5}}
#         ],
#         "red_flags": [
#             "Right lower quadrant pain",
#             "Pain with vomiting",
#             "Rebound tenderness",
#             "Pain waking child from sleep",
#             "Abdominal rigidity"
#         ]
#     },
#     "DEHYDRATION": {
#         "follow_up": [
#             {"question": "Signs", "type": "checkbox",
#              "options": ["Dry mouth", "No tears", "Sunken eyes", "Decreased urine output", "Lethargy"],
#              "weights": {"Dry mouth": 1.0, "No tears": 1.3, "Sunken eyes": 1.5, "Decreased urine output": 1.7, "Lethargy": 2.0},
#              "note": "WHO dehydration classification: none/some/severe"}
#         ],
#         "red_flags": [
#             "No urine >12 hours",
#             "Sunken fontanelle in infants",
#             "Lethargy/unresponsiveness",
#             "Unable to keep down fluids",
#             "Capillary refill >3 seconds"
#         ]
#     }
# }

# # Enhanced dataset with more conditions and refined weights based on medical literature
# MEDICAL_DATA = """
# CONDITION,FEVER,COUGH,RUNNY_NOSE,SNEEZING,FEVER_SEVERITY,COUGH_TYPE,MUSCLE_ACHES,HEADACHE,WHEEZING,RESPIRATORY_DISTRESS,RASH,VOMITING,DIARRHEA,EAR_PAIN,SORE_THROAT,ABDOMINAL_PAIN,DEHYDRATION
# Common Cold,0.3,1.0,1.8,1.5,0.5,1.0,0.2,0.3,0.0,0.0,0.0,0.0,0.0,0.0,0.2,0.0,0.0
# Influenza (Flu),1.8,1.5,0.5,0.3,1.5,1.2,1.8,1.7,0.0,0.3,0.0,0.8,0.3,0.0,0.3,0.5,0.3
# Bronchiolitis,0.8,2.0,0.8,0.5,0.8,1.8,0.3,0.2,2.5,2.2,0.0,0.5,0.3,0.0,0.0,0.0,0.5
# Pneumonia,2.0,2.2,0.3,0.1,1.8,2.0,1.0,1.2,1.5,2.5,0.0,0.3,0.0,0.0,0.0,0.0,0.8
# Meningitis,2.2,0.3,0.1,0.0,2.2,0.3,1.8,2.8,0.0,0.5,1.5,1.8,0.3,0.0,0.0,0.0,1.5
# Asthma,0.3,1.8,0.5,0.7,0.3,1.5,0.0,0.3,3.0,2.5,0.0,0.0,0.0,0.0,0.0,0.0,0.3
# Allergic Rhinitis,0.0,0.5,2.0,2.2,0.0,0.5,0.0,0.0,1.5,0.0,0.8,0.0,0.0,0.0,0.0,0.0,0.0
# COVID-19,1.7,1.8,0.7,0.5,1.5,1.7,1.5,1.7,0.8,1.5,0.5,0.8,0.5,0.0,0.3,0.5,0.7
# Strep Throat,1.5,0.5,0.3,0.1,1.2,0.3,0.8,1.5,0.0,0.0,0.0,0.5,0.0,0.0,0.0,2.2,0.5
# Croup,0.8,2.5,0.5,0.3,0.8,2.2,0.3,0.5,2.2,2.0,0.0,0.3,0.0,0.0,0.0,0.0,0.3
# Gastroenteritis,0.5,0.0,0.0,0.0,0.3,0.0,0.5,0.3,0.0,0.0,0.0,2.2,2.5,0.0,0.0,0.5,1.8
# Urinary Tract Infection,1.5,0.0,0.0,0.0,1.2,0.0,0.3,0.5,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.8,1.2
# Appendicitis,0.8,0.0,0.0,0.0,0.5,0.0,0.0,0.5,0.0,0.0,0.0,1.8,0.5,0.0,0.0,2.5,1.0
# Hand-Foot-Mouth Disease,1.0,0.3,0.5,0.3,0.8,0.3,0.5,0.8,0.0,0.0,2.2,0.8,0.3,0.0,0.5,1.2,0.5
# Roseola,2.0,0.0,0.3,0.0,1.8,0.0,0.3,0.5,0.0,0.0,1.8,0.3,0.0,0.0,0.0,0.0,0.3
# Pertussis,0.5,3.0,0.5,0.3,0.3,3.0,0.0,0.0,0.0,1.8,0.0,1.5,0.0,0.0,0.0,0.0,1.0
# Measles,2.2,1.5,1.0,0.5,2.0,1.2,1.0,1.5,0.0,0.5,2.5,0.8,0.3,0.0,0.5,1.0,1.2
# Chickenpox,1.5,0.3,0.3,0.0,1.2,0.3,0.8,1.0,0.0,0.0,2.8,0.5,0.0,0.0,0.0,0.5,0.8
# """

# @st.cache_data
# def load_data():
#     from io import StringIO
#     df = pd.read_csv(StringIO(MEDICAL_DATA))
#     # Fill NaN values with 0 for all symptoms
#     symptom_cols = [col for col in df.columns if col != "CONDITION"]
#     df[symptom_cols] = df[symptom_cols].fillna(0)
#     return df

# def calculate_age_risk_factor(age):
#     """Calculate risk factor based on age (higher risk for infants and immunocompromised)"""
#     if age < 3: return 1.5  # Higher weight for infants
#     elif age < 12: return 1.2  # Moderate weight for young children
#     else: return 1.0  # Standard weight for older children

# def main():
#     st.set_page_config(page_title="Pediatric Symptom Checker", page_icon="👶", layout="wide")
#     st.title("👶 Pediatric Symptom Checker")
    
#     # Load data
#     df = load_data()
    
#     # Get all available symptoms from dataset
#     all_symptoms = [col for col in df.columns if col != "CONDITION"]
    
#     # Age input
#     with st.expander("Patient Information", expanded=True):
#         col1, col2 = st.columns(2)
#         with col1:
#             age = st.number_input("Age (months)", min_value=0, max_value=216, value=24, step=1)
#         with col2:
#             medical_history = st.multiselect(
#                 "Medical History (select all that apply)",
#                 options=["Asthma", "Diabetes", "Heart Condition", "Immunocompromised", "Prematurity"],
#                 default=[]
#             )
    
#     # Step 1: Primary symptom selection
#     with st.expander("Step 1: Select main symptoms", expanded=True):
#         primary_symptoms = st.multiselect(
#             "What symptoms is your child experiencing?",
#             options=all_symptoms,
#             placeholder="Select symptoms..."
#         )
    
#     # Step 2: Detailed symptom questions
#     symptom_details = {}
#     if primary_symptoms:
#         with st.expander("Step 2: Provide symptom details", expanded=True):
#             for symptom in primary_symptoms:
#                 if symptom in SYMPTOM_DEFINITIONS:
#                     st.subheader(f"Details about {symptom.lower().replace('_', ' ')}")
                    
#                     symptom_weight = 1.0  # Base weight
                    
#                     for question in SYMPTOM_DEFINITIONS[symptom]["follow_up"]:
#                         response = None
#                         if question["type"] == "radio":
#                             response = st.radio(
#                                 question["question"],
#                                 options=question["options"],
#                                 key=f"{symptom}_{question['question']}"
#                             )
#                         elif question["type"] == "selectbox":
#                             response = st.selectbox(
#                                 question["question"],
#                                 options=question["options"],
#                                 key=f"{symptom}_{question['question']}"
#                             )
#                         elif question["type"] == "checkbox":
#                             response = st.multiselect(
#                                 question["question"],
#                                 options=question["options"],
#                                 key=f"{symptom}_{question['question']}"
#                             )
                        
#                         if response:
#                             if isinstance(response, list):  # For checkbox questions
#                                 for item in response:
#                                     symptom_weight *= question["weights"][item]
#                             else:  # For radio/selectbox
#                                 symptom_weight *= question["weights"][response]
                    
#                     symptom_details[symptom] = {
#                         "value": 1.0,  # Base value
#                         "weight": symptom_weight
#                     }
                    
#                     # Show clinical notes if available
#                     if "note" in SYMPTOM_DEFINITIONS[symptom]:
#                         st.info(SYMPTOM_DEFINITIONS[symptom]["note"])
#                 else:
#                     # For symptoms without follow-up questions
#                     severity = st.slider(
#                         f"Severity of {symptom.lower().replace('_', ' ')}",
#                         min_value=0.1,
#                         max_value=3.0,
#                         value=1.0,
#                         step=0.1,
#                         key=symptom
#                     )
#                     symptom_details[symptom] = {
#                         "value": severity,
#                         "weight": 1.0
#                     }
    
#     # Step 3: Predict
#     if st.button("Analyze Symptoms", type="primary", use_container_width=True):
#         if not primary_symptoms:
#             st.warning("Please select at least one symptom")
#             return
        
#         # Prepare features (only numerical columns)
#         numerical_cols = [col for col in df.columns if col != "CONDITION"]
#         X = df[numerical_cols]
#         y = df["CONDITION"]
        
#         # Train model
#         model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
#         model.fit(X, y)
        
#         # Prepare input features
#         input_features = {col: 0.0 for col in numerical_cols}
        
#         # Apply symptom weights and age factor
#         age_factor = calculate_age_risk_factor(age)
#         for symptom, details in symptom_details.items():
#             if symptom in input_features:
#                 input_features[symptom] = details["value"] * details["weight"] * age_factor
        
#         # Additional weight for concerning medical history
#         if "Immunocompromised" in medical_history:
#             for symptom in input_features:
#                 if input_features[symptom] > 0:
#                     input_features[symptom] *= 1.5
        
#         # Convert to DataFrame
#         input_df = pd.DataFrame([input_features])[numerical_cols]
        
#         # Make prediction
#         prediction = model.predict(input_df)[0]
#         probabilities = model.predict_proba(input_df)[0]
        
#         # Display results
#         col1, col2 = st.columns([1, 2])
        
#         with col1:
#             st.success(f"### Most likely condition: **{prediction}**")
            
#             # Show probabilities
#             st.subheader("Top Possible Conditions")
#             prob_df = pd.DataFrame({
#                 "Condition": model.classes_,
#                 "Probability": probabilities
#             }).sort_values("Probability", ascending=False).head(5)
            
#             # Format probabilities with colors
#             def color_probs(val):
#                 color = 'red' if val > 0.7 else 'orange' if val > 0.3 else 'green'
#                 return f'color: {color}; font-weight: bold'
            
#             st.dataframe(
#                 prob_df.style.format({"Probability": "{:.2%}"})
#                       .applymap(color_probs, subset=['Probability']),
#                 hide_index=True
#             )
        
#         with col2:
#             # Show red flags
#             st.subheader("⚠️ Red Flags to Watch For")
#             red_flags_found = False
#             for symptom in primary_symptoms:
#                 if symptom in SYMPTOM_DEFINITIONS and "red_flags" in SYMPTOM_DEFINITIONS[symptom]:
#                     for flag in SYMPTOM_DEFINITIONS[symptom]["red_flags"]:
#                         st.error(f"• {flag}")
#                         red_flags_found = True
            
#             # Additional red flags based on age
#             if age < 3 and "FEVER" in primary_symptoms:
#                 st.error("• Fever in infants <3 months requires immediate evaluation")
#                 red_flags_found = True
            
#             if not red_flags_found:
#                 st.info("No urgent red flags identified based on current symptoms")
            
#             # General advice
#             st.subheader("ℹ️ Recommended Actions")
#             if prediction in ["Meningitis", "Severe Pneumonia", "Sepsis"]:
#                 st.error("""
#                 **EMERGENCY: Seek immediate medical attention**
#                 - Call emergency services or go to nearest ER
#                 - Do not delay treatment for these conditions
#                 """)
#             elif prediction in ["Bronchiolitis", "Moderate Pneumonia", "Dehydration"]:
#                 st.warning("""
#                 **Urgent: Contact your pediatrician within 4-6 hours**
#                 - Monitor closely for worsening symptoms
#                 - Keep child hydrated
#                 - Watch for signs of respiratory distress
#                 """)
#             elif prediction in ["Influenza (Flu)", "Asthma Exacerbation", "Strep Throat"]:
#                 st.warning("""
#                 **Contact your pediatrician within 24 hours**
#                 - Rest and fluids
#                 - Monitor fever pattern
#                 - Watch for complications
#                 """)
#             else:
#                 st.info("""
#                 **Monitor at home**
#                 - Symptomatic treatment as needed
#                 - Contact doctor if symptoms worsen or persist >3 days
#                 - Ensure adequate hydration
#                 """)
            
#             # Special considerations based on age and history
#             if age < 6:
#                 st.info("ℹ️ For infants under 6 months, always consult a doctor for any significant symptoms")
            
#             if "Immunocompromised" in medical_history:
#                 st.warning("⚠️ Immunocompromised children may need earlier evaluation for fever or infection")

# if __name__ == "__main__":
#     main()


#WORKING

# import streamlit as st
# import pandas as pd
# import numpy as np
# from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
# from sklearn.preprocessing import LabelEncoder

# # Enhanced medical knowledge base with more pediatric symptoms and refined weights
# SYMPTOM_DEFINITIONS = {
#     "FEVER": {
#         "follow_up": [
#             {"question": "Temperature", "type": "radio", 
#              "options": ["<100.4°F (normal)", "100.4-102.2°F (low-grade)", "102.2-104°F (moderate)", ">104°F (high)"],
#              "weights": {"<100.4°F (normal)": 0.5, "100.4-102.2°F (low-grade)": 1.0, "102.2-104°F (moderate)": 1.8, ">104°F (high)": 2.5},
#              "note": "In infants <3 months, any fever >100.4°F requires immediate evaluation"},
#             {"question": "Duration", "type": "selectbox",
#              "options": ["<24 hours", "1-3 days", "3-7 days", ">7 days"],
#              "weights": {"<24 hours": 0.8, "1-3 days": 1.0, "3-7 days": 1.5, ">7 days": 2.0}}
#         ],
#         "red_flags": [
#             "Fever >100.4°F in infant <3 months",
#             "Fever >104°F",
#             "Fever with stiff neck or photophobia",
#             "Fever with petechial rash",
#             "Fever lasting >5 days"
#         ],
#         "who_notes": "Fever patterns can help differentiate diseases - sustained in typhoid, quotidian in malaria"
#     },
#     "COUGH": {
#         "follow_up": [
#             {"question": "Type", "type": "selectbox",
#              "options": ["Dry", "Productive", "Barking", "Whooping", "Staccato"],
#              "weights": {"Dry": 1.0, "Productive": 1.2, "Barking": 1.8, "Whooping": 2.2, "Staccato": 2.0},
#              "note": "Barking cough suggests croup, whooping suggests pertussis"},
#             {"question": "Timing", "type": "radio",
#              "options": ["Daytime", "Nighttime", "With feeding", "After exercise", "All day"],
#              "weights": {"Daytime": 1.0, "Nighttime": 1.3, "With feeding": 1.5, "After exercise": 1.7, "All day": 1.5}}
#         ],
#         "red_flags": [
#             "Whooping sound on inspiration",
#             "Cough causing vomiting",
#             "Cough with cyanosis",
#             "Cough lasting >3 weeks",
#             "Sudden onset cough (possible aspiration)"
#         ]
#     },
#     "RESPIRATORY_DISTRESS": {
#         "follow_up": [
#             {"question": "Severity", "type": "radio",
#              "options": ["None", "Mild (intercostal retractions)", "Moderate (nasal flaring)", "Severe (grunting, head bobbing)"],
#              "weights": {"None": 0, "Mild (intercostal retractions)": 1.5, "Moderate (nasal flaring)": 2.0, "Severe (grunting, head bobbing)": 3.0},
#              "note": "WHO defines tachypnea as RR >60 in <2mo, >50 in 2-12mo, >40 in 1-5y"}
#         ],
#         "red_flags": [
#             "Respiratory rate >60/min",
#             "Cyanosis",
#             "Grunting",
#             "Severe retractions",
#             "Inability to speak/cry"
#         ]
#     },
#     "RASH": {
#         "follow_up": [
#             {"question": "Type", "type": "selectbox",
#              "options": ["Maculopapular", "Vesicular", "Petechial/Purpuric", "Urticarial", "Erythematous"],
#              "weights": {"Maculopapular": 1.0, "Vesicular": 1.5, "Petechial/Purpuric": 2.5, "Urticarial": 1.3, "Erythematous": 1.2},
#              "note": "Petechial rash requires immediate evaluation for meningococcemia"},
#             {"question": "Distribution", "type": "radio",
#              "options": ["Face", "Trunk", "Extremities", "Palms/soles", "Generalized"],
#              "weights": {"Face": 1.0, "Trunk": 1.2, "Extremities": 1.1, "Palms/soles": 1.8, "Generalized": 1.5}}
#         ],
#         "red_flags": [
#             "Petechial/purpuric rash",
#             "Rash with fever",
#             "Rash with mucosal involvement",
#             "Rapidly spreading rash",
#             "Rash with blistering"
#         ]
#     },
#     "VOMITING": {
#         "follow_up": [
#             {"question": "Frequency", "type": "radio",
#              "options": ["1-2 times", "3-5 times", ">5 times", "Projectile"],
#              "weights": {"1-2 times": 1.0, "3-5 times": 1.5, ">5 times": 2.0, "Projectile": 2.2},
#              "note": "Projectile vomiting in infants suggests pyloric stenosis"},
#             {"question": "Content", "type": "selectbox",
#              "options": ["Food", "Bile (green)", "Blood", "Coffee-ground"],
#              "weights": {"Food": 1.0, "Bile (green)": 1.8, "Blood": 2.5, "Coffee-ground": 2.3}}
#         ],
#         "red_flags": [
#             "Bilious vomiting",
#             "Hematemesis",
#             "Projectile vomiting in infants",
#             "Vomiting with severe abdominal pain",
#             "Vomiting with altered mental status"
#         ]
#     },
#     "DIARRHEA": {
#         "follow_up": [
#             {"question": "Frequency", "type": "radio",
#              "options": ["2-4 loose stools/day", "5-8 loose stools/day", ">8 loose stools/day", "Watery"],
#              "weights": {"2-4 loose stools/day": 1.0, "5-8 loose stools/day": 1.5, ">8 loose stools/day": 2.0, "Watery": 2.2},
#              "note": "WHO defines diarrhea as ≥3 loose stools/day"},
#             {"question": "Appearance", "type": "selectbox",
#              "options": ["Loose", "Mucoid", "Bloody", "Rice-water"],
#              "weights": {"Loose": 1.0, "Mucoid": 1.3, "Bloody": 2.0, "Rice-water": 2.2}}
#         ],
#         "red_flags": [
#             "Bloody diarrhea",
#             "Signs of dehydration (no tears, sunken eyes)",
#             "Diarrhea >2 weeks",
#             "Diarrhea with high fever",
#             ">8 watery stools/day"
#         ]
#     },
#     "EAR_PAIN": {
#         "follow_up": [
#             {"question": "Severity", "type": "radio",
#              "options": ["Mild", "Moderate", "Severe", "Disrupting sleep"],
#              "weights": {"Mild": 1.0, "Moderate": 1.3, "Severe": 1.7, "Disrupting sleep": 1.9},
#              "note": "Pulling ears in infants may indicate otitis media"},
#             {"question": "Duration", "type": "selectbox",
#              "options": ["<24 hours", "1-3 days", ">3 days"],
#              "weights": {"<24 hours": 1.0, "1-3 days": 1.2, ">3 days": 1.5}}
#         ],
#         "red_flags": [
#             "Ear pain with fever >102°F",
#             "Swelling behind ear",
#             "Facial weakness",
#             "Severe pain with sudden relief (possible rupture)"
#         ]
#     },
#     "SORE_THROAT": {
#         "follow_up": [
#             {"question": "Severity", "type": "radio",
#              "options": ["Mild", "Moderate", "Severe", "Unable to swallow"],
#              "weights": {"Mild": 1.0, "Moderate": 1.3, "Severe": 1.8, "Unable to swallow": 2.5},
#              "note": "Consider strep if >3 years with fever and no cough"},
#             {"question": "Appearance", "type": "selectbox",
#              "options": ["Red", "Exudate", "Ulcers", "Swollen tonsils"],
#              "weights": {"Red": 1.0, "Exudate": 1.5, "Ulcers": 1.8, "Swollen tonsils": 1.7}}
#         ],
#         "red_flags": [
#             "Drooling/inability to swallow",
#             "Neck stiffness with sore throat",
#             "Trismus (difficulty opening mouth)",
#             "Voice changes (hot potato voice)"
#         ]
#     },
#     "ABDOMINAL_PAIN": {
#         "follow_up": [
#             {"question": "Location", "type": "selectbox",
#              "options": ["Diffuse", "Periumbilical", "Right lower quadrant", "Epigastric", "Left lower quadrant"],
#              "weights": {"Diffuse": 1.0, "Periumbilical": 1.2, "Right lower quadrant": 2.0, "Epigastric": 1.5, "Left lower quadrant": 1.8},
#              "note": "RLQ pain suggests appendicitis, rebound tenderness is concerning"},
#             {"question": "Severity", "type": "radio",
#              "options": ["Mild", "Moderate", "Severe", "Doubled over"],
#              "weights": {"Mild": 1.0, "Moderate": 1.5, "Severe": 2.0, "Doubled over": 2.5}}
#         ],
#         "red_flags": [
#             "Right lower quadrant pain",
#             "Pain with vomiting",
#             "Rebound tenderness",
#             "Pain waking child from sleep",
#             "Abdominal rigidity"
#         ]
#     },
#     "DEHYDRATION": {
#         "follow_up": [
#             {"question": "Signs", "type": "checkbox",
#              "options": ["Dry mouth", "No tears", "Sunken eyes", "Decreased urine output", "Lethargy"],
#              "weights": {"Dry mouth": 1.0, "No tears": 1.3, "Sunken eyes": 1.5, "Decreased urine output": 1.7, "Lethargy": 2.0},
#              "note": "WHO dehydration classification: none/some/severe"}
#         ],
#         "red_flags": [
#             "No urine >12 hours",
#             "Sunken fontanelle in infants",
#             "Lethargy/unresponsiveness",
#             "Unable to keep down fluids",
#             "Capillary refill >3 seconds"
#         ]
#     },
#     "NECK_STIFFNESS": {
#         "follow_up": [
#             {"question": "Severity", "type": "radio",
#              "options": ["Mild discomfort", "Moderate stiffness", "Severe (chin can't touch chest)"],
#              "weights": {"Mild discomfort": 1.5, "Moderate stiffness": 2.0, "Severe (chin can't touch chest)": 3.0},
#              "note": "Severe neck stiffness with fever suggests meningitis"}
#         ],
#         "red_flags": [
#             "Inability to flex neck",
#             "Neck stiffness with fever",
#             "Opisthotonus (arching backward)"
#         ]
#     },
#     "PHOTOPHOBIA": {
#         "follow_up": [
#             {"question": "Severity", "type": "radio",
#              "options": ["Mild light sensitivity", "Moderate (avoids light)", "Severe (eyes tightly closed)"],
#              "weights": {"Mild light sensitivity": 1.5, "Moderate (avoids light)": 2.0, "Severe (eyes tightly closed)": 2.5},
#              "note": "Photophobia with headache may indicate meningitis"}
#         ],
#         "red_flags": [
#             "Photophobia with headache",
#             "Photophobia with neck stiffness"
#         ]
#     },
#     "COUGH_POST_TUSSIVE": {
#         "follow_up": [
#             {"question": "Occurs after coughing", "type": "radio",
#              "options": ["Never", "Sometimes", "Always"],
#              "weights": {"Never": 0.0, "Sometimes": 1.5, "Always": 2.0},
#              "note": "Post-tussive vomiting is classic for pertussis"}
#         ],
#         "red_flags": [
#             "Recurrent post-tussive vomiting"
#         ]
#     },
#     "COUGH_PAROXYSMAL": {
#         "follow_up": [
#             {"question": "Coughing fits", "type": "radio",
#              "options": ["None", "Occasional fits", "Frequent prolonged fits"],
#              "weights": {"None": 0.0, "Occasional fits": 1.8, "Frequent prolonged fits": 2.5},
#              "note": "Paroxysmal coughing is characteristic of pertussis"}
#         ],
#         "red_flags": [
#             "Paroxysms followed by whoop",
#             "Cyanosis during coughing fits"
#         ]
#     },
#     "STRAWBERRY_TONGUE": {
#         "follow_up": [
#             {"question": "Tongue appearance", "type": "radio",
#              "options": ["Normal", "White coating", "Red bumps", "Bright red with bumps"],
#              "weights": {"Normal": 0.0, "White coating": 0.5, "Red bumps": 1.5, "Bright red with bumps": 2.5},
#              "note": "Strawberry tongue is seen in scarlet fever and Kawasaki disease"}
#         ],
#         "red_flags": [
#             "Bright red tongue with prominent papillae"
#         ]
#     },
#     "KOPLIK_SPOTS": {
#         "follow_up": [
#             {"question": "Oral lesions", "type": "radio",
#              "options": ["None", "Small white spots on buccal mucosa"],
#              "weights": {"None": 0.0, "Small white spots on buccal mucosa": 2.5},
#              "note": "Koplik spots are pathognomonic for measles"}
#         ],
#         "red_flags": [
#             "White spots on buccal mucosa with fever"
#         ]
#     },
#     "STOMATITIS": {
#         "follow_up": [
#             {"question": "Mouth ulcers", "type": "radio",
#              "options": ["None", "1-3 ulcers", ">3 ulcers"],
#              "weights": {"None": 0.0, "1-3 ulcers": 1.5, ">3 ulcers": 2.0},
#              "note": "Painful oral ulcers are characteristic of hand-foot-mouth disease"}
#         ],
#         "red_flags": [
#             "Painful mouth ulcers preventing eating/drinking"
#         ]
#     }
# }

# # Enhanced dataset with more conditions and refined weights based on medical literature
# MEDICAL_DATA = """
# CONDITION,FEVER,COUGH,RUNNY_NOSE,SNEEZING,FEVER_SEVERITY,COUGH_TYPE,MUSCLE_ACHES,HEADACHE,WHEEZING,RESPIRATORY_DISTRESS,RASH,VOMITING,DIARRHEA,EAR_PAIN,SORE_THROAT,ABDOMINAL_PAIN,DEHYDRATION,NECK_STIFFNESS,PHOTOPHOBIA,CONJUNCTIVITIS,LYMPH_NODES,URINARY_FREQUENCY,DYSURIA,COUGH_POST_TUSSIVE,APNEA,COUGH_PAROXYSMAL,COUGH_NIGHTTIME,STRAWBERRY_TONGUE,KOPLIK_SPOTS,STOMATITIS
# Common Cold,0.3,1.0,1.8,1.5,0.5,1.0,0.2,0.3,0.0,0.0,0.0,0.0,0.0,0.0,0.2,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
# Influenza (Flu),1.8,1.5,0.5,0.3,1.5,1.2,1.8,1.7,0.0,0.3,0.0,0.8,0.3,0.0,0.3,0.5,0.3,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
# Bronchiolitis,0.8,2.0,0.8,0.5,0.8,1.8,0.3,0.2,2.5,2.2,0.0,0.5,0.3,0.0,0.0,0.0,0.5,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.8,0.0,1.5,0.0,0.0,0.0
# Pneumonia,2.0,2.2,0.3,0.1,1.8,2.0,1.0,1.2,1.5,2.5,0.0,0.3,0.0,0.0,0.0,0.0,0.8,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
# Meningitis,2.2,0.3,0.1,0.0,2.2,0.3,1.8,2.8,0.0,0.5,1.5,1.8,0.3,0.0,0.0,0.0,1.5,3.0,2.5,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
# Asthma,0.3,1.8,0.5,0.7,0.3,1.5,0.0,0.3,3.0,2.5,0.0,0.0,0.0,0.0,0.0,0.0,0.3,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,2.0,0.0,0.0,0.0
# Allergic Rhinitis,0.0,0.5,2.0,2.2,0.0,0.5,0.0,0.0,1.5,0.0,0.8,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.5,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
# COVID-19,1.7,1.8,0.7,0.5,1.5,1.7,1.5,1.7,0.8,1.5,0.5,0.8,0.5,0.0,0.3,0.5,0.7,0.0,0.0,0.3,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
# Strep Throat,1.5,0.5,0.3,0.1,1.2,0.3,0.8,1.5,0.0,0.0,0.0,0.5,0.0,0.0,2.2,0.5,0.0,0.0,0.0,0.0,1.5,0.0,0.0,0.0,0.0,0.0,0.0,1.8,0.0,0.0
# Croup,0.8,2.5,0.5,0.3,0.8,2.2,0.3,0.5,2.2,2.0,0.0,0.3,0.0,0.0,0.0,0.0,0.3,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.5,0.0,0.0,0.0,0.0
# Gastroenteritis,0.5,0.0,0.0,0.0,0.3,0.0,0.5,0.3,0.0,0.0,0.0,2.2,2.5,0.0,0.0,0.5,1.8,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
# UTI,1.5,0.0,0.0,0.0,1.2,0.0,0.3,0.5,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.8,1.2,0.0,0.0,0.0,0.0,2.0,2.2,0.0,0.0,0.0,0.0,0.0,0.0,0.0
# Appendicitis,0.8,0.0,0.0,0.0,0.5,0.0,0.0,0.5,0.0,0.0,0.0,1.8,0.5,0.0,0.0,2.5,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
# Hand-Foot-Mouth,1.0,0.3,0.5,0.3,0.8,0.3,0.5,0.8,0.0,0.0,2.2,0.8,0.3,0.0,0.5,1.2,0.5,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,2.0
# Roseola,2.0,0.0,0.3,0.0,1.8,0.0,0.3,0.5,0.0,0.0,1.8,0.3,0.0,0.0,0.0,0.0,0.3,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
# Pertussis,0.5,3.0,0.5,0.3,0.3,3.0,0.0,0.0,0.0,1.8,0.0,1.5,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,1.5,0.0,2.5,0.0,0.0,0.0,0.0
# Measles,2.2,1.5,1.0,0.5,2.0,1.2,1.0,1.5,0.0,0.5,2.5,0.8,0.3,0.0,0.5,1.0,1.2,0.0,1.5,1.0,0.5,0.0,0.0,0.0,0.0,0.0,0.0,0.0,2.0,0.0
# Chickenpox,1.5,0.3,0.3,0.0,1.2,0.3,0.8,1.0,0.0,0.0,2.8,0.5,0.0,0.0,0.0,0.5,0.8,0.0,0.0,0.3,0.3,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
# Otitis Media,1.0,0.0,0.5,0.0,0.8,0.0,0.0,0.5,0.0,0.0,0.0,0.3,0.0,1.8,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
# Sinusitis,1.2,0.8,1.5,0.8,1.0,0.8,0.5,1.5,0.0,0.0,0.0,0.3,0.0,0.0,1.5,0.0,0.0,0.0,0.5,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
# RSV,1.5,2.2,1.0,0.5,1.2,2.0,0.3,0.5,2.5,2.2,0.0,0.5,0.3,0.0,0.0,0.0,0.5,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.8,0.0,0.0,0.0,0.0
# Scarlet Fever,2.0,0.3,0.3,0.0,1.8,0.3,1.0,1.5,0.0,0.0,2.5,0.8,0.0,0.0,1.8,0.5,0.0,0.0,0.0,0.0,1.5,0.0,0.0,0.0,0.0,0.0,0.0,2.0,0.0,0.0
# Fifth Disease,1.0,0.3,0.5,0.3,0.8,0.3,0.5,0.8,0.0,0.0,2.0,0.3,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.3,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
# Impetigo,0.3,0.0,0.0,0.0,0.3,0.0,0.0,0.0,0.0,0.0,2.5,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.5,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
# Conjunctivitis,0.3,0.0,0.5,0.3,0.3,0.0,0.0,0.0,0.0,0.0,0.5,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.5,2.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
# Pharyngitis,1.2,0.5,0.5,0.3,1.0,0.5,0.5,1.0,0.0,0.0,0.0,0.3,0.0,0.0,1.5,0.0,0.0,0.0,0.0,0.3,0.8,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
# Pyloric Stenosis,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,2.5,0.0,0.0,0.0,0.0,1.5,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
# Intussusception,0.8,0.0,0.0,0.0,0.5,0.0,0.0,0.0,0.0,0.0,0.0,2.2,1.5,0.0,0.0,0.0,2.5,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
# Kawasaki Disease,2.5,0.5,0.8,0.0,2.2,0.5,0.5,1.5,0.0,0.5,2.0,0.5,0.3,0.0,0.0,1.5,0.8,0.5,0.0,1.5,1.8,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.5
# Rheumatic Fever,1.5,0.5,0.3,0.0,1.2,0.5,1.5,1.8,0.0,0.5,1.5,0.3,0.0,0.0,0.0,1.8,0.5,0.3,0.0,0.5,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
# Epiglottitis,2.0,0.8,0.0,0.0,1.8,0.8,1.0,1.2,0.0,2.5,0.0,0.5,0.0,0.0,0.0,2.5,0.0,1.5,0.0,0.0,1.5,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
# Cellulitis,1.5,0.0,0.0,0.0,1.2,0.0,0.5,0.8,0.0,0.0,1.8,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
# Mononucleosis,1.8,0.5,0.3,0.0,1.5,0.5,1.5,2.0,0.0,0.0,0.8,0.5,0.0,0.0,0.0,1.8,0.8,0.0,0.5,0.5,2.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
# Rotavirus,0.5,0.0,0.0,0.0,0.3,0.0,0.3,0.5,0.0,0.0,0.0,1.5,2.5,0.0,0.0,0.0,1.8,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
# Pinworms,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.3,0.0,0.0,0.0,0.0,0.0,1.5,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
# """

# @st.cache_data
# def load_data():
#     from io import StringIO
#     df = pd.read_csv(StringIO(MEDICAL_DATA))
#     # Fill NaN values with 0 for all symptoms
#     symptom_cols = [col for col in df.columns if col != "CONDITION"]
#     df[symptom_cols] = df[symptom_cols].fillna(0)
#     return df

# def calculate_age_risk_factor(age):
#     """Calculate risk factor based on age (higher risk for infants and immunocompromised)"""
#     if age < 3: return 1.5  # Higher weight for infants
#     elif age < 12: return 1.2  # Moderate weight for young children
#     else: return 1.0  # Standard weight for older children

# def apply_clinical_overrides(prediction, symptoms, age):
#     """Apply clinical rules to override model predictions when specific patterns are detected"""
#     # Meningitis override
#     if "NECK_STIFFNESS" in symptoms and "FEVER" in symptoms and "PHOTOPHOBIA" in symptoms and age < 5:
#         return "Meningitis (clinical override)", 0.95
    
#     # Pertussis pattern
#     if "COUGH_PAROXYSMAL" in symptoms and "COUGH_POST_TUSSIVE" in symptoms:
#         return "Pertussis (clinical override)", 0.9
        
#     # Kawasaki criteria
#     if "FEVER" in symptoms and "STRAWBERRY_TONGUE" in symptoms and "RASH" in symptoms and age < 5:
#         return "Kawasaki Disease (clinical override)", 0.85
    
#     # Scarlet fever
#     if "STRAWBERRY_TONGUE" in symptoms and "SORE_THROAT" in symptoms and "RASH" in symptoms:
#         return "Scarlet Fever (clinical override)", 0.85
    
#     # Measles
#     if "KOPLIK_SPOTS" in symptoms and "FEVER" in symptoms and "RASH" in symptoms:
#         return "Measles (clinical override)", 0.9
    
#     return prediction, None

# def main():
#     st.set_page_config(page_title="Pediatric Symptom Checker", page_icon="👶", layout="wide")
#     st.title("👶 Pediatric Symptom Checker")
    
#     # Load data
#     df = load_data()
    
#     # Get all available symptoms from dataset
#     all_symptoms = [col for col in df.columns if col != "CONDITION"]
    
#     # Age input
#     with st.expander("Patient Information", expanded=True):
#         col1, col2 = st.columns(2)
#         with col1:
#             age = st.number_input("Age (months)", min_value=0, max_value=216, value=24, step=1)
#         with col2:
#             medical_history = st.multiselect(
#                 "Medical History (select all that apply)",
#                 options=["Asthma", "Diabetes", "Heart Condition", "Immunocompromised", "Prematurity"],
#                 default=[]
#             )
    
#     # Step 1: Primary symptom selection
#     with st.expander("Step 1: Select main symptoms", expanded=True):
#         primary_symptoms = st.multiselect(
#             "What symptoms is your child experiencing?",
#             options=all_symptoms,
#             placeholder="Select symptoms..."
#         )
    
#     # Step 2: Detailed symptom questions
#     symptom_details = {}
#     if primary_symptoms:
#         with st.expander("Step 2: Provide symptom details", expanded=True):
#             for symptom in primary_symptoms:
#                 if symptom in SYMPTOM_DEFINITIONS:
#                     st.subheader(f"Details about {symptom.lower().replace('_', ' ')}")
                    
#                     symptom_weight = 1.0  # Base weight
                    
#                     for question in SYMPTOM_DEFINITIONS[symptom]["follow_up"]:
#                         response = None
#                         if question["type"] == "radio":
#                             response = st.radio(
#                                 question["question"],
#                                 options=question["options"],
#                                 key=f"{symptom}_{question['question']}"
#                             )
#                         elif question["type"] == "selectbox":
#                             response = st.selectbox(
#                                 question["question"],
#                                 options=question["options"],
#                                 key=f"{symptom}_{question['question']}"
#                             )
#                         elif question["type"] == "checkbox":
#                             response = st.multiselect(
#                                 question["question"],
#                                 options=question["options"],
#                                 key=f"{symptom}_{question['question']}"
#                             )
                        
#                         if response:
#                             if isinstance(response, list):  # For checkbox questions
#                                 for item in response:
#                                     symptom_weight *= question["weights"][item]
#                             else:  # For radio/selectbox
#                                 symptom_weight *= question["weights"][response]
                    
#                     symptom_details[symptom] = {
#                         "value": 1.0,  # Base value
#                         "weight": symptom_weight
#                     }
                    
#                     # Show clinical notes if available
#                     if "note" in SYMPTOM_DEFINITIONS[symptom]:
#                         st.info(SYMPTOM_DEFINITIONS[symptom]["note"])
#                 else:
#                     # For symptoms without follow-up questions
#                     severity = st.slider(
#                         f"Severity of {symptom.lower().replace('_', ' ')}",
#                         min_value=0.1,
#                         max_value=3.0,
#                         value=1.0,
#                         step=0.1,
#                         key=symptom
#                     )
#                     symptom_details[symptom] = {
#                         "value": severity,
#                         "weight": 1.0
#                     }
    
#     # Step 3: Predict
#     if st.button("Analyze Symptoms", type="primary", use_container_width=True):
#         if not primary_symptoms:
#             st.warning("Please select at least one symptom")
#             return
        
#         # Prepare features (only numerical columns)
#         numerical_cols = [col for col in df.columns if col != "CONDITION"]
#         X = df[numerical_cols]
#         y = df["CONDITION"]
        
#         # Train model - using GradientBoosting for better performance
#         model = GradientBoostingClassifier(
#             n_estimators=200,
#             learning_rate=0.1,
#             max_depth=4,
#             min_samples_leaf=3,
#             random_state=42
#         )
#         model.fit(X, y)
        
#         # Prepare input features
#         input_features = {col: 0.0 for col in numerical_cols}
        
#         # Apply symptom weights and age factor
#         age_factor = calculate_age_risk_factor(age)
#         for symptom, details in symptom_details.items():
#             if symptom in input_features:
#                 input_features[symptom] = details["value"] * details["weight"] * age_factor
        
#         # Additional weight for concerning medical history
#         if "Immunocompromised" in medical_history:
#             for symptom in input_features:
#                 if input_features[symptom] > 0:
#                     input_features[symptom] *= 1.5
        
#         # Convert to DataFrame
#         input_df = pd.DataFrame([input_features])[numerical_cols]
        
#         # Make prediction
#         prediction = model.predict(input_df)[0]
#         probabilities = model.predict_proba(input_df)[0]
        
#         # Apply clinical overrides
#         override_prediction, override_prob = apply_clinical_overrides(prediction, primary_symptoms, age)
#         if override_prediction:
#             prediction = override_prediction
        
#         # Display results
#         col1, col2 = st.columns([1, 2])
        
#         with col1:
#             st.success(f"### Most likely condition: **{prediction}**")
            
#             # Show probabilities
#             st.subheader("Top Possible Conditions")
#             prob_df = pd.DataFrame({
#                 "Condition": model.classes_,
#                 "Probability": probabilities
#             }).sort_values("Probability", ascending=False).head(5)
            
#             # Highlight overridden condition if applicable
#             if override_prediction:
#                 prob_df.loc[prob_df['Condition'] == override_prediction.split(' (')[0], 'Probability'] = override_prob
            
#             # Format probabilities with colors
#             def color_probs(val):
#                 color = 'red' if val > 0.7 else 'orange' if val > 0.3 else 'green'
#                 return f'color: {color}; font-weight: bold'
            
#             st.dataframe(
#                 prob_df.style.format({"Probability": "{:.2%}"})
#                       .applymap(color_probs, subset=['Probability']),
#                 hide_index=True
#             )
        
#         with col2:
#             # Show red flags
#             st.subheader("⚠️ Red Flags to Watch For")
#             red_flags_found = False
            
#             # Check symptom-specific red flags
#             for symptom in primary_symptoms:
#                 if symptom in SYMPTOM_DEFINITIONS and "red_flags" in SYMPTOM_DEFINITIONS[symptom]:
#                     for flag in SYMPTOM_DEFINITIONS[symptom]["red_flags"]:
#                         st.error(f"• {flag}")
#                         red_flags_found = True
            
#             # Age-specific red flags
#             if age < 3 and "FEVER" in primary_symptoms:
#                 st.error("• Fever in infants <3 months requires immediate evaluation")
#                 red_flags_found = True
                
#             if age < 6 and "COUGH" in primary_symptoms and "WHEEZING" in primary_symptoms:
#                 st.error("• Wheezing in infants <6 months may indicate serious illness")
#                 red_flags_found = True
                
#             if "PETECHIAL/PURPURIC" in primary_symptoms and "FEVER" in primary_symptoms:
#                 st.error("• Petechial rash with fever may indicate meningococcemia - seek IMMEDIATE care")
#                 red_flags_found = True
            
#             if not red_flags_found:
#                 st.info("No urgent red flags identified based on current symptoms")
            
#             # General advice
#             st.subheader("ℹ️ Recommended Actions")
#             if "Meningitis" in prediction:
#                 st.error("""
#                 **EMERGENCY: Seek immediate medical attention**
#                 - This is a medical emergency requiring IV antibiotics
#                 - Go to nearest ER immediately
#                 - Do not wait for symptoms to worsen
#                 """)
#             elif "Epiglottitis" in prediction:
#                 st.error("""
#                 **EMERGENCY: Do not examine throat**
#                 - Risk of complete airway obstruction
#                 - Keep child calm and upright
#                 - Call emergency services immediately
#                 """)
#             elif prediction in ["Bronchiolitis", "Pneumonia", "Dehydration"]:
#                 st.warning("""
#                 **Urgent: Contact your pediatrician within 4-6 hours**
#                 - Monitor respiratory rate closely
#                 - Keep child hydrated
#                 - Watch for signs of worsening distress
#                 """)
#             elif prediction in ["Influenza (Flu)", "Strep Throat", "Pertussis"]:
#                 st.warning("""
#                 **Contact your pediatrician within 24 hours**
#                 - Rest and fluids
#                 - Monitor fever pattern
#                 - Watch for complications
#                 - May need specific testing/treatment
#                 """)
#             else:
#                 st.info("""
#                 **Monitor at home**
#                 - Symptomatic treatment as needed
#                 - Contact doctor if symptoms worsen or persist >3 days
#                 - Ensure adequate hydration
#                 - Watch for new symptoms
#                 """)
            
#             # Special considerations based on age and history
#             if age < 6:
#                 st.info("ℹ️ For infants under 6 months, always consult a doctor for any significant symptoms")
            
#             if "Immunocompromised" in medical_history:
#                 st.warning("⚠️ Immunocompromised children may need earlier evaluation for fever or infection")

# if __name__ == "__main__":
#     main()

#MODEL ERROR 

# import streamlit as st
# import pandas as pd
# import numpy as np
# from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, StackingClassifier
# from sklearn.linear_model import LogisticRegression
# from sklearn.svm import SVC
# from sklearn.preprocessing import LabelEncoder

# # Enhanced medical knowledge base with more pediatric symptoms and refined weights
# SYMPTOM_DEFINITIONS = {
#     "FEVER": {
#         "follow_up": [
#             {"question": "Temperature", "type": "radio", 
#              "options": ["<100.4°F (normal)", "100.4-102.2°F (low-grade)", "102.2-104°F (moderate)", ">104°F (high)"],
#              "weights": {"<100.4°F (normal)": 0.5, "100.4-102.2°F (low-grade)": 1.0, "102.2-104°F (moderate)": 1.8, ">104°F (high)": 2.5},
#              "note": "In infants <3 months, any fever >100.4°F requires immediate evaluation"},
#             {"question": "Duration", "type": "selectbox",
#              "options": ["<24 hours", "1-3 days", "3-7 days", ">7 days"],
#              "weights": {"<24 hours": 0.8, "1-3 days": 1.0, "3-7 days": 1.5, ">7 days": 2.0}}
#         ],
#         "red_flags": [
#             "Fever >100.4°F in infant <3 months",
#             "Fever >104°F",
#             "Fever with stiff neck or photophobia",
#             "Fever with petechial rash",
#             "Fever lasting >5 days"
#         ],
#         "who_notes": "Fever patterns can help differentiate diseases - sustained in typhoid, quotidian in malaria"
#     },
#     "COUGH": {
#         "follow_up": [
#             {"question": "Type", "type": "selectbox",
#              "options": ["Dry", "Productive", "Barking", "Whooping", "Staccato"],
#              "weights": {"Dry": 1.0, "Productive": 1.2, "Barking": 1.8, "Whooping": 2.2, "Staccato": 2.0},
#              "note": "Barking cough suggests croup, whooping suggests pertussis"},
#             {"question": "Timing", "type": "radio",
#              "options": ["Daytime", "Nighttime", "With feeding", "After exercise", "All day"],
#              "weights": {"Daytime": 1.0, "Nighttime": 1.3, "With feeding": 1.5, "After exercise": 1.7, "All day": 1.5}}
#         ],
#         "red_flags": [
#             "Whooping sound on inspiration",
#             "Cough causing vomiting",
#             "Cough with cyanosis",
#             "Cough lasting >3 weeks",
#             "Sudden onset cough (possible aspiration)"
#         ]
#     },
#     "RESPIRATORY_DISTRESS": {
#         "follow_up": [
#             {"question": "Severity", "type": "radio",
#              "options": ["None", "Mild (intercostal retractions)", "Moderate (nasal flaring)", "Severe (grunting, head bobbing)"],
#              "weights": {"None": 0, "Mild (intercostal retractions)": 1.5, "Moderate (nasal flaring)": 2.0, "Severe (grunting, head bobbing)": 3.0},
#              "note": "WHO defines tachypnea as RR >60 in <2mo, >50 in 2-12mo, >40 in 1-5y"}
#         ],
#         "red_flags": [
#             "Respiratory rate >60/min",
#             "Cyanosis",
#             "Grunting",
#             "Severe retractions",
#             "Inability to speak/cry"
#         ]
#     },
#     "RASH": {
#         "follow_up": [
#             {"question": "Type", "type": "selectbox",
#              "options": ["Maculopapular", "Vesicular", "Petechial/Purpuric", "Urticarial", "Erythematous"],
#              "weights": {"Maculopapular": 1.0, "Vesicular": 1.5, "Petechial/Purpuric": 2.5, "Urticarial": 1.3, "Erythematous": 1.2},
#              "note": "Petechial rash requires immediate evaluation for meningococcemia"},
#             {"question": "Distribution", "type": "radio",
#              "options": ["Face", "Trunk", "Extremities", "Palms/soles", "Generalized"],
#              "weights": {"Face": 1.0, "Trunk": 1.2, "Extremities": 1.1, "Palms/soles": 1.8, "Generalized": 1.5}}
#         ],
#         "red_flags": [
#             "Petechial/purpuric rash",
#             "Rash with fever",
#             "Rash with mucosal involvement",
#             "Rapidly spreading rash",
#             "Rash with blistering"
#         ]
#     },
#     "VOMITING": {
#         "follow_up": [
#             {"question": "Frequency", "type": "radio",
#              "options": ["1-2 times", "3-5 times", ">5 times", "Projectile"],
#              "weights": {"1-2 times": 1.0, "3-5 times": 1.5, ">5 times": 2.0, "Projectile": 2.2},
#              "note": "Projectile vomiting in infants suggests pyloric stenosis"},
#             {"question": "Content", "type": "selectbox",
#              "options": ["Food", "Bile (green)", "Blood", "Coffee-ground"],
#              "weights": {"Food": 1.0, "Bile (green)": 1.8, "Blood": 2.5, "Coffee-ground": 2.3}}
#         ],
#         "red_flags": [
#             "Bilious vomiting",
#             "Hematemesis",
#             "Projectile vomiting in infants",
#             "Vomiting with severe abdominal pain",
#             "Vomiting with altered mental status"
#         ]
#     },
#     "DIARRHEA": {
#         "follow_up": [
#             {"question": "Frequency", "type": "radio",
#              "options": ["2-4 loose stools/day", "5-8 loose stools/day", ">8 loose stools/day", "Watery"],
#              "weights": {"2-4 loose stools/day": 1.0, "5-8 loose stools/day": 1.5, ">8 loose stools/day": 2.0, "Watery": 2.2},
#              "note": "WHO defines diarrhea as ≥3 loose stools/day"},
#             {"question": "Appearance", "type": "selectbox",
#              "options": ["Loose", "Mucoid", "Bloody", "Rice-water"],
#              "weights": {"Loose": 1.0, "Mucoid": 1.3, "Bloody": 2.0, "Rice-water": 2.2}}
#         ],
#         "red_flags": [
#             "Bloody diarrhea",
#             "Signs of dehydration (no tears, sunken eyes)",
#             "Diarrhea >2 weeks",
#             "Diarrhea with high fever",
#             ">8 watery stools/day"
#         ]
#     },
#     "EAR_PAIN": {
#         "follow_up": [
#             {"question": "Severity", "type": "radio",
#              "options": ["Mild", "Moderate", "Severe", "Disrupting sleep"],
#              "weights": {"Mild": 1.0, "Moderate": 1.3, "Severe": 1.7, "Disrupting sleep": 1.9},
#              "note": "Pulling ears in infants may indicate otitis media"},
#             {"question": "Duration", "type": "selectbox",
#              "options": ["<24 hours", "1-3 days", ">3 days"],
#              "weights": {"<24 hours": 1.0, "1-3 days": 1.2, ">3 days": 1.5}}
#         ],
#         "red_flags": [
#             "Ear pain with fever >102°F",
#             "Swelling behind ear",
#             "Facial weakness",
#             "Severe pain with sudden relief (possible rupture)"
#         ]
#     },
#     "SORE_THROAT": {
#         "follow_up": [
#             {"question": "Severity", "type": "radio",
#              "options": ["Mild", "Moderate", "Severe", "Unable to swallow"],
#              "weights": {"Mild": 1.0, "Moderate": 1.3, "Severe": 1.8, "Unable to swallow": 2.5},
#              "note": "Consider strep if >3 years with fever and no cough"},
#             {"question": "Appearance", "type": "selectbox",
#              "options": ["Red", "Exudate", "Ulcers", "Swollen tonsils"],
#              "weights": {"Red": 1.0, "Exudate": 1.5, "Ulcers": 1.8, "Swollen tonsils": 1.7}}
#         ],
#         "red_flags": [
#             "Drooling/inability to swallow",
#             "Neck stiffness with sore throat",
#             "Trismus (difficulty opening mouth)",
#             "Voice changes (hot potato voice)"
#         ]
#     },
#     "ABDOMINAL_PAIN": {
#         "follow_up": [
#             {"question": "Location", "type": "selectbox",
#              "options": ["Diffuse", "Periumbilical", "Right lower quadrant", "Epigastric", "Left lower quadrant"],
#              "weights": {"Diffuse": 1.0, "Periumbilical": 1.2, "Right lower quadrant": 2.0, "Epigastric": 1.5, "Left lower quadrant": 1.8},
#              "note": "RLQ pain suggests appendicitis, rebound tenderness is concerning"},
#             {"question": "Severity", "type": "radio",
#              "options": ["Mild", "Moderate", "Severe", "Doubled over"],
#              "weights": {"Mild": 1.0, "Moderate": 1.5, "Severe": 2.0, "Doubled over": 2.5}}
#         ],
#         "red_flags": [
#             "Right lower quadrant pain",
#             "Pain with vomiting",
#             "Rebound tenderness",
#             "Pain waking child from sleep",
#             "Abdominal rigidity"
#         ]
#     },
#     "DEHYDRATION": {
#         "follow_up": [
#             {"question": "Signs", "type": "checkbox",
#              "options": ["Dry mouth", "No tears", "Sunken eyes", "Decreased urine output", "Lethargy"],
#              "weights": {"Dry mouth": 1.0, "No tears": 1.3, "Sunken eyes": 1.5, "Decreased urine output": 1.7, "Lethargy": 2.0},
#              "note": "WHO dehydration classification: none/some/severe"}
#         ],
#         "red_flags": [
#             "No urine >12 hours",
#             "Sunken fontanelle in infants",
#             "Lethargy/unresponsiveness",
#             "Unable to keep down fluids",
#             "Capillary refill >3 seconds"
#         ]
#     },
#     "NECK_STIFFNESS": {
#         "follow_up": [
#             {"question": "Severity", "type": "radio",
#              "options": ["Mild discomfort", "Moderate stiffness", "Severe (chin can't touch chest)"],
#              "weights": {"Mild discomfort": 1.5, "Moderate stiffness": 2.0, "Severe (chin can't touch chest)": 3.0},
#              "note": "Severe neck stiffness with fever suggests meningitis"}
#         ],
#         "red_flags": [
#             "Inability to flex neck",
#             "Neck stiffness with fever",
#             "Opisthotonus (arching backward)"
#         ]
#     },
#     "PHOTOPHOBIA": {
#         "follow_up": [
#             {"question": "Severity", "type": "radio",
#              "options": ["Mild light sensitivity", "Moderate (avoids light)", "Severe (eyes tightly closed)"],
#              "weights": {"Mild light sensitivity": 1.5, "Moderate (avoids light)": 2.0, "Severe (eyes tightly closed)": 2.5},
#              "note": "Photophobia with headache may indicate meningitis"}
#         ],
#         "red_flags": [
#             "Photophobia with headache",
#             "Photophobia with neck stiffness"
#         ]
#     },
#     "COUGH_POST_TUSSIVE": {
#         "follow_up": [
#             {"question": "Occurs after coughing", "type": "radio",
#              "options": ["Never", "Sometimes", "Always"],
#              "weights": {"Never": 0.0, "Sometimes": 1.5, "Always": 2.0},
#              "note": "Post-tussive vomiting is classic for pertussis"}
#         ],
#         "red_flags": [
#             "Recurrent post-tussive vomiting"
#         ]
#     },
#     "COUGH_PAROXYSMAL": {
#         "follow_up": [
#             {"question": "Coughing fits", "type": "radio",
#              "options": ["None", "Occasional fits", "Frequent prolonged fits"],
#              "weights": {"None": 0.0, "Occasional fits": 1.8, "Frequent prolonged fits": 2.5},
#              "note": "Paroxysmal coughing is characteristic of pertussis"}
#         ],
#         "red_flags": [
#             "Paroxysms followed by whoop",
#             "Cyanosis during coughing fits"
#         ]
#     },
#     "STRAWBERRY_TONGUE": {
#         "follow_up": [
#             {"question": "Tongue appearance", "type": "radio",
#              "options": ["Normal", "White coating", "Red bumps", "Bright red with bumps"],
#              "weights": {"Normal": 0.0, "White coating": 0.5, "Red bumps": 1.5, "Bright red with bumps": 2.5},
#              "note": "Strawberry tongue is seen in scarlet fever and Kawasaki disease"}
#         ],
#         "red_flags": [
#             "Bright red tongue with prominent papillae"
#         ]
#     },
#     "KOPLIK_SPOTS": {
#         "follow_up": [
#             {"question": "Oral lesions", "type": "radio",
#              "options": ["None", "Small white spots on buccal mucosa"],
#              "weights": {"None": 0.0, "Small white spots on buccal mucosa": 2.5},
#              "note": "Koplik spots are pathognomonic for measles"}
#         ],
#         "red_flags": [
#             "White spots on buccal mucosa with fever"
#         ]
#     },
#     "STOMATITIS": {
#         "follow_up": [
#             {"question": "Mouth ulcers", "type": "radio",
#              "options": ["None", "1-3 ulcers", ">3 ulcers"],
#              "weights": {"None": 0.0, "1-3 ulcers": 1.5, ">3 ulcers": 2.0},
#              "note": "Painful oral ulcers are characteristic of hand-foot-mouth disease"}
#         ],
#         "red_flags": [
#             "Painful mouth ulcers preventing eating/drinking"
#         ]
#     }
# }

# # Enhanced dataset with more conditions and refined weights based on medical literature
# MEDICAL_DATA = """
# CONDITION,FEVER,COUGH,RUNNY_NOSE,SNEEZING,FEVER_SEVERITY,COUGH_TYPE,MUSCLE_ACHES,HEADACHE,WHEEZING,RESPIRATORY_DISTRESS,RASH,VOMITING,DIARRHEA,EAR_PAIN,SORE_THROAT,ABDOMINAL_PAIN,DEHYDRATION,NECK_STIFFNESS,PHOTOPHOBIA,CONJUNCTIVITIS,LYMPH_NODES,URINARY_FREQUENCY,DYSURIA,COUGH_POST_TUSSIVE,APNEA,COUGH_PAROXYSMAL,COUGH_NIGHTTIME,STRAWBERRY_TONGUE,KOPLIK_SPOTS,STOMATITIS
# Common Cold,0.3,1.0,1.8,1.5,0.5,1.0,0.2,0.3,0.0,0.0,0.0,0.0,0.0,0.0,0.2,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
# Influenza (Flu),1.8,1.5,0.5,0.3,1.5,1.2,1.8,1.7,0.0,0.3,0.0,0.8,0.3,0.0,0.3,0.5,0.3,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
# Bronchiolitis,0.8,2.0,0.8,0.5,0.8,1.8,0.3,0.2,2.5,2.2,0.0,0.5,0.3,0.0,0.0,0.0,0.5,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.8,0.0,1.5,0.0,0.0,0.0
# Pneumonia,2.0,2.2,0.3,0.1,1.8,2.0,1.0,1.2,1.5,2.5,0.0,0.3,0.0,0.0,0.0,0.0,0.8,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
# Meningitis,2.2,0.3,0.1,0.0,2.2,0.3,1.8,2.8,0.0,0.5,1.5,1.8,0.3,0.0,0.0,0.0,1.5,3.0,2.5,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
# Asthma,0.3,1.8,0.5,0.7,0.3,1.5,0.0,0.3,3.0,2.5,0.0,0.0,0.0,0.0,0.0,0.0,0.3,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,2.0,0.0,0.0,0.0
# Allergic Rhinitis,0.0,0.5,2.0,2.2,0.0,0.5,0.0,0.0,1.5,0.0,0.8,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.5,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
# COVID-19,1.7,1.8,0.7,0.5,1.5,1.7,1.5,1.7,0.8,1.5,0.5,0.8,0.5,0.0,0.3,0.5,0.7,0.0,0.0,0.3,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
# Strep Throat,1.5,0.5,0.3,0.1,1.2,0.3,0.8,1.5,0.0,0.0,0.0,0.5,0.0,0.0,2.2,0.5,0.0,0.0,0.0,0.0,1.5,0.0,0.0,0.0,0.0,0.0,0.0,1.8,0.0,0.0
# Croup,0.8,2.5,0.5,0.3,0.8,2.2,0.3,0.5,2.2,2.0,0.0,0.3,0.0,0.0,0.0,0.0,0.3,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.5,0.0,0.0,0.0,0.0
# Gastroenteritis,0.5,0.0,0.0,0.0,0.3,0.0,0.5,0.3,0.0,0.0,0.0,2.2,2.5,0.0,0.0,0.5,1.8,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
# UTI,1.5,0.0,0.0,0.0,1.2,0.0,0.3,0.5,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.8,1.2,0.0,0.0,0.0,0.0,2.0,2.2,0.0,0.0,0.0,0.0,0.0,0.0,0.0
# Appendicitis,0.8,0.0,0.0,0.0,0.5,0.0,0.0,0.5,0.0,0.0,0.0,1.8,0.5,0.0,0.0,2.5,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
# Hand-Foot-Mouth,1.0,0.3,0.5,0.3,0.8,0.3,0.5,0.8,0.0,0.0,2.2,0.8,0.3,0.0,0.5,1.2,0.5,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,2.0
# Roseola,2.0,0.0,0.3,0.0,1.8,0.0,0.3,0.5,0.0,0.0,1.8,0.3,0.0,0.0,0.0,0.0,0.3,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
# Pertussis,0.5,3.0,0.5,0.3,0.3,3.0,0.0,0.0,0.0,1.8,0.0,1.5,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,1.5,0.0,2.5,0.0,0.0,0.0,0.0
# Measles,2.2,1.5,1.0,0.5,2.0,1.2,1.0,1.5,0.0,0.5,2.5,0.8,0.3,0.0,0.5,1.0,1.2,0.0,1.5,1.0,0.5,0.0,0.0,0.0,0.0,0.0,0.0,0.0,2.0,0.0
# Chickenpox,1.5,0.3,0.3,0.0,1.2,0.3,0.8,1.0,0.0,0.0,2.8,0.5,0.0,0.0,0.0,0.5,0.8,0.0,0.0,0.3,0.3,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
# Otitis Media,1.0,0.0,0.5,0.0,0.8,0.0,0.0,0.5,0.0,0.0,0.0,0.3,0.0,1.8,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
# Sinusitis,1.2,0.8,1.5,0.8,1.0,0.8,0.5,1.5,0.0,0.0,0.0,0.3,0.0,0.0,1.5,0.0,0.0,0.0,0.5,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
# RSV,1.5,2.2,1.0,0.5,1.2,2.0,0.3,0.5,2.5,2.2,0.0,0.5,0.3,0.0,0.0,0.0,0.5,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.8,0.0,0.0,0.0,0.0
# Scarlet Fever,2.0,0.3,0.3,0.0,1.8,0.3,1.0,1.5,0.0,0.0,2.5,0.8,0.0,0.0,1.8,0.5,0.0,0.0,0.0,0.0,1.5,0.0,0.0,0.0,0.0,0.0,0.0,2.0,0.0,0.0
# Fifth Disease,1.0,0.3,0.5,0.3,0.8,0.3,0.5,0.8,0.0,0.0,2.0,0.3,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.3,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
# Impetigo,0.3,0.0,0.0,0.0,0.3,0.0,0.0,0.0,0.0,0.0,2.5,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.5,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
# Conjunctivitis,0.3,0.0,0.5,0.3,0.3,0.0,0.0,0.0,0.0,0.0,0.5,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.5,2.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
# Pharyngitis,1.2,0.5,0.5,0.3,1.0,0.5,0.5,1.0,0.0,0.0,0.0,0.3,0.0,0.0,1.5,0.0,0.0,0.0,0.0,0.3,0.8,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
# Pyloric Stenosis,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,2.5,0.0,0.0,0.0,0.0,1.5,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
# Intussusception,0.8,0.0,0.0,0.0,0.5,0.0,0.0,0.0,0.0,0.0,0.0,2.2,1.5,0.0,0.0,0.0,2.5,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
# Kawasaki Disease,2.5,0.5,0.8,0.0,2.2,0.5,0.5,1.5,0.0,0.5,2.0,0.5,0.3,0.0,0.0,1.5,0.8,0.5,0.0,1.5,1.8,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.5
# Rheumatic Fever,1.5,0.5,0.3,0.0,1.2,0.5,1.5,1.8,0.0,0.5,1.5,0.3,0.0,0.0,0.0,1.8,0.5,0.3,0.0,0.5,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
# Epiglottitis,2.0,0.8,0.0,0.0,1.8,0.8,1.0,1.2,0.0,2.5,0.0,0.5,0.0,0.0,0.0,2.5,0.0,1.5,0.0,0.0,1.5,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
# Cellulitis,1.5,0.0,0.0,0.0,1.2,0.0,0.5,0.8,0.0,0.0,1.8,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
# Mononucleosis,1.8,0.5,0.3,0.0,1.5,0.5,1.5,2.0,0.0,0.0,0.8,0.5,0.0,0.0,0.0,1.8,0.8,0.0,0.5,0.5,2.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
# Rotavirus,0.5,0.0,0.0,0.0,0.3,0.0,0.3,0.5,0.0,0.0,0.0,1.5,2.5,0.0,0.0,0.0,1.8,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
# Pinworms,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.3,0.0,0.0,0.0,0.0,0.0,1.5,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
# """

# @st.cache_data
# def load_data():
#     from io import StringIO
#     df = pd.read_csv(StringIO(MEDICAL_DATA))
#     # Fill NaN values with 0 for all symptoms
#     symptom_cols = [col for col in df.columns if col != "CONDITION"]
#     df[symptom_cols] = df[symptom_cols].fillna(0)
#     return df

# def calculate_age_risk_factor(age):
#     """Calculate risk factor based on age (higher risk for infants and immunocompromised)"""
#     if age < 3: return 1.5  # Higher weight for infants
#     elif age < 12: return 1.2  # Moderate weight for young children
#     else: return 1.0  # Standard weight for older children

# def apply_clinical_overrides(prediction, symptoms, age):
#     """Apply clinical rules to override model predictions when specific patterns are detected"""
#     # Meningitis override
#     if "NECK_STIFFNESS" in symptoms and "FEVER" in symptoms and "PHOTOPHOBIA" in symptoms and age < 5:
#         return "Meningitis (clinical override)", 0.95
    
#     # Pertussis pattern
#     if "COUGH_PAROXYSMAL" in symptoms and "COUGH_POST_TUSSIVE" in symptoms:
#         return "Pertussis (clinical override)", 0.9
        
#     # Kawasaki criteria
#     if "FEVER" in symptoms and "STRAWBERRY_TONGUE" in symptoms and "RASH" in symptoms and age < 5:
#         return "Kawasaki Disease (clinical override)", 0.85
    
#     # Scarlet fever
#     if "STRAWBERRY_TONGUE" in symptoms and "SORE_THROAT" in symptoms and "RASH" in symptoms:
#         return "Scarlet Fever (clinical override)", 0.85
    
#     # Measles
#     if "KOPLIK_SPOTS" in symptoms and "FEVER" in symptoms and "RASH" in symptoms:
#         return "Measles (clinical override)", 0.9
    
#     return prediction, None

# def main():
#     st.set_page_config(page_title="Pediatric Symptom Checker", page_icon="👶", layout="wide")
#     st.title("👶 Pediatric Symptom Checker")
    
#     # Load data
#     df = load_data()
    
#     # Get all available symptoms from dataset
#     all_symptoms = [col for col in df.columns if col != "CONDITION"]
    
#     # Age input
#     with st.expander("Patient Information", expanded=True):
#         col1, col2 = st.columns(2)
#         with col1:
#             age = st.number_input("Age (months)", min_value=0, max_value=216, value=24, step=1)
#         with col2:
#             medical_history = st.multiselect(
#                 "Medical History (select all that apply)",
#                 options=["Asthma", "Diabetes", "Heart Condition", "Immunocompromised", "Prematurity"],
#                 default=[]
#             )
    
#     # Step 1: Primary symptom selection
#     with st.expander("Step 1: Select main symptoms", expanded=True):
#         primary_symptoms = st.multiselect(
#             "What symptoms is your child experiencing?",
#             options=all_symptoms,
#             placeholder="Select symptoms..."
#         )
    
#     # Step 2: Detailed symptom questions
#     symptom_details = {}
#     if primary_symptoms:
#         with st.expander("Step 2: Provide symptom details", expanded=True):
#             for symptom in primary_symptoms:
#                 if symptom in SYMPTOM_DEFINITIONS:
#                     st.subheader(f"Details about {symptom.lower().replace('_', ' ')}")
                    
#                     symptom_weight = 1.0  # Base weight
                    
#                     for question in SYMPTOM_DEFINITIONS[symptom]["follow_up"]:
#                         response = None
#                         if question["type"] == "radio":
#                             response = st.radio(
#                                 question["question"],
#                                 options=question["options"],
#                                 key=f"{symptom}_{question['question']}"
#                             )
#                         elif question["type"] == "selectbox":
#                             response = st.selectbox(
#                                 question["question"],
#                                 options=question["options"],
#                                 key=f"{symptom}_{question['question']}"
#                             )
#                         elif question["type"] == "checkbox":
#                             response = st.multiselect(
#                                 question["question"],
#                                 options=question["options"],
#                                 key=f"{symptom}_{question['question']}"
#                             )
                        
#                         if response:
#                             if isinstance(response, list):  # For checkbox questions
#                                 for item in response:
#                                     symptom_weight *= question["weights"][item]
#                             else:  # For radio/selectbox
#                                 symptom_weight *= question["weights"][response]
                    
#                     symptom_details[symptom] = {
#                         "value": 1.0,  # Base value
#                         "weight": symptom_weight
#                     }
                    
#                     # Show clinical notes if available
#                     if "note" in SYMPTOM_DEFINITIONS[symptom]:
#                         st.info(SYMPTOM_DEFINITIONS[symptom]["note"])
#                 else:
#                     # For symptoms without follow-up questions
#                     severity = st.slider(
#                         f"Severity of {symptom.lower().replace('_', ' ')}",
#                         min_value=0.1,
#                         max_value=3.0,
#                         value=1.0,
#                         step=0.1,
#                         key=symptom
#                     )
#                     symptom_details[symptom] = {
#                         "value": severity,
#                         "weight": 1.0
#                     }
    
#     # Step 3: Predict
#     if st.button("Analyze Symptoms", type="primary", use_container_width=True):
#         if not primary_symptoms:
#             st.warning("Please select at least one symptom")
#             return
        
#         # Prepare features (only numerical columns)
#         numerical_cols = [col for col in df.columns if col != "CONDITION"]
#         X = df[numerical_cols]
#         y = df["CONDITION"]
        
#         # Train model - using Stacked Ensemble
#         base_models = [
#             ('rf', RandomForestClassifier(n_estimators=100, random_state=42)),
#             ('gb', GradientBoostingClassifier(n_estimators=200, learning_rate=0.1, max_depth=4, random_state=42)),
#             ('svm', SVC(kernel='linear', probability=True, random_state=42))
#         ]
        
#         meta_model = LogisticRegression()
        
#         model = StackingClassifier(
#             estimators=base_models,
#             final_estimator=meta_model,
#             stack_method='predict_proba',
#             passthrough=True,
#             cv=5
#         )
        
#         model.fit(X, y)
        
#         # Prepare input features
#         input_features = {col: 0.0 for col in numerical_cols}
        
#         # Apply symptom weights and age factor
#         age_factor = calculate_age_risk_factor(age)
#         for symptom, details in symptom_details.items():
#             if symptom in input_features:
#                 input_features[symptom] = details["value"] * details["weight"] * age_factor
        
#         # Additional weight for concerning medical history
#         if "Immunocompromised" in medical_history:
#             for symptom in input_features:
#                 if input_features[symptom] > 0:
#                     input_features[symptom] *= 1.5
        
#         # Convert to DataFrame
#         input_df = pd.DataFrame([input_features])[numerical_cols]
        
#         # Make prediction
#         prediction = model.predict(input_df)[0]
#         probabilities = model.predict_proba(input_df)[0]
        
#         # Apply clinical overrides
#         override_prediction, override_prob = apply_clinical_overrides(prediction, primary_symptoms, age)
#         if override_prediction:
#             prediction = override_prediction
        
#         # Display results
#         col1, col2 = st.columns([1, 2])
        
#         with col1:
#             st.success(f"### Most likely condition: **{prediction}**")
            
#             # Show probabilities
#             st.subheader("Top Possible Conditions")
#             prob_df = pd.DataFrame({
#                 "Condition": model.classes_,
#                 "Probability": probabilities
#             }).sort_values("Probability", ascending=False).head(5)
            
#             # Highlight overridden condition if applicable
#             if override_prediction:
#                 prob_df.loc[prob_df['Condition'] == override_prediction.split(' (')[0], 'Probability'] = override_prob
            
#             # Format probabilities with colors
#             def color_probs(val):
#                 color = 'red' if val > 0.7 else 'orange' if val > 0.3 else 'green'
#                 return f'color: {color}; font-weight: bold'
            
#             st.dataframe(
#                 prob_df.style.format({"Probability": "{:.2%}"})
#                       .applymap(color_probs, subset=['Probability']),
#                 hide_index=True
#             )
        
#         with col2:
#             # Show red flags
#             st.subheader("⚠️ Red Flags to Watch For")
#             red_flags_found = False
            
#             # Check symptom-specific red flags
#             for symptom in primary_symptoms:
#                 if symptom in SYMPTOM_DEFINITIONS and "red_flags" in SYMPTOM_DEFINITIONS[symptom]:
#                     for flag in SYMPTOM_DEFINITIONS[symptom]["red_flags"]:
#                         st.error(f"• {flag}")
#                         red_flags_found = True
            
#             # Age-specific red flags
#             if age < 3 and "FEVER" in primary_symptoms:
#                 st.error("• Fever in infants <3 months requires immediate evaluation")
#                 red_flags_found = True
                
#             if age < 6 and "COUGH" in primary_symptoms and "WHEEZING" in primary_symptoms:
#                 st.error("• Wheezing in infants <6 months may indicate serious illness")
#                 red_flags_found = True
                
#             if "PETECHIAL/PURPURIC" in primary_symptoms and "FEVER" in primary_symptoms:
#                 st.error("• Petechial rash with fever may indicate meningococcemia - seek IMMEDIATE care")
#                 red_flags_found = True
            
#             if not red_flags_found:
#                 st.info("No urgent red flags identified based on current symptoms")
            
#             # General advice
#             st.subheader("ℹ️ Recommended Actions")
#             if "Meningitis" in prediction:
#                 st.error("""
#                 **EMERGENCY: Seek immediate medical attention**
#                 - This is a medical emergency requiring IV antibiotics
#                 - Go to nearest ER immediately
#                 - Do not wait for symptoms to worsen
#                 """)
#             elif "Epiglottitis" in prediction:
#                 st.error("""
#                 **EMERGENCY: Do not examine throat**
#                 - Risk of complete airway obstruction
#                 - Keep child calm and upright
#                 - Call emergency services immediately
#                 """)
#             elif prediction in ["Bronchiolitis", "Pneumonia", "Dehydration"]:
#                 st.warning("""
#                 **Urgent: Contact your pediatrician within 4-6 hours**
#                 - Monitor respiratory rate closely
#                 - Keep child hydrated
#                 - Watch for signs of worsening distress
#                 """)
#             elif prediction in ["Influenza (Flu)", "Strep Throat", "Pertussis"]:
#                 st.warning("""
#                 **Contact your pediatrician within 24 hours**
#                 - Rest and fluids
#                 - Monitor fever pattern
#                 - Watch for complications
#                 - May need specific testing/treatment
#                 """)
#             else:
#                 st.info("""
#                 **Monitor at home**
#                 - Symptomatic treatment as needed
#                 - Contact doctor if symptoms worsen or persist >3 days
#                 - Ensure adequate hydration
#                 - Watch for new symptoms
#                 """)
            
#             # Special considerations based on age and history
#             if age < 6:
#                 st.info("ℹ️ For infants under 6 months, always consult a doctor for any significant symptoms")
            
#             if "Immunocompromised" in medical_history:
#                 st.warning("⚠️ Immunocompromised children may need earlier evaluation for fever or infection")

# if __name__ == "__main__":
#     main()




#MAPS
# import streamlit as st
# import pandas as pd
# import numpy as np
# from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
# from sklearn.preprocessing import LabelEncoder
# import requests
# import json
# import folium
# from streamlit_folium import folium_static
# from geopy.geocoders import Nominatim

# # Enhanced medical knowledge base with more pediatric symptoms and refined weights
# SYMPTOM_DEFINITIONS = {
#     "FEVER": {
#         "follow_up": [
#             {"question": "Temperature", "type": "radio", 
#              "options": ["<100.4°F (normal)", "100.4-102.2°F (low-grade)", "102.2-104°F (moderate)", ">104°F (high)"],
#              "weights": {"<100.4°F (normal)": 0.5, "100.4-102.2°F (low-grade)": 1.0, "102.2-104°F (moderate)": 1.8, ">104°F (high)": 2.5},
#              "note": "In infants <3 months, any fever >100.4°F requires immediate evaluation"},
#             {"question": "Duration", "type": "selectbox",
#              "options": ["<24 hours", "1-3 days", "3-7 days", ">7 days"],
#              "weights": {"<24 hours": 0.8, "1-3 days": 1.0, "3-7 days": 1.5, ">7 days": 2.0}}
#         ],
#         "red_flags": [
#             "Fever >100.4°F in infant <3 months",
#             "Fever >104°F",
#             "Fever with stiff neck or photophobia",
#             "Fever with petechial rash",
#             "Fever lasting >5 days"
#         ],
#         "who_notes": "Fever patterns can help differentiate diseases - sustained in typhoid, quotidian in malaria"
#     },
#     "COUGH": {
#         "follow_up": [
#             {"question": "Type", "type": "selectbox",
#              "options": ["Dry", "Productive", "Barking", "Whooping", "Staccato"],
#              "weights": {"Dry": 1.0, "Productive": 1.2, "Barking": 1.8, "Whooping": 2.2, "Staccato": 2.0},
#              "note": "Barking cough suggests croup, whooping suggests pertussis"},
#             {"question": "Timing", "type": "radio",
#              "options": ["Daytime", "Nighttime", "With feeding", "After exercise", "All day"],
#              "weights": {"Daytime": 1.0, "Nighttime": 1.3, "With feeding": 1.5, "After exercise": 1.7, "All day": 1.5}}
#         ],
#         "red_flags": [
#             "Whooping sound on inspiration",
#             "Cough causing vomiting",
#             "Cough with cyanosis",
#             "Cough lasting >3 weeks",
#             "Sudden onset cough (possible aspiration)"
#         ]
#     },
#     "RESPIRATORY_DISTRESS": {
#         "follow_up": [
#             {"question": "Severity", "type": "radio",
#              "options": ["None", "Mild (intercostal retractions)", "Moderate (nasal flaring)", "Severe (grunting, head bobbing)"],
#              "weights": {"None": 0, "Mild (intercostal retractions)": 1.5, "Moderate (nasal flaring)": 2.0, "Severe (grunting, head bobbing)": 3.0},
#              "note": "WHO defines tachypnea as RR >60 in <2mo, >50 in 2-12mo, >40 in 1-5y"}
#         ],
#         "red_flags": [
#             "Respiratory rate >60/min",
#             "Cyanosis",
#             "Grunting",
#             "Severe retractions",
#             "Inability to speak/cry"
#         ]
#     },
#     "RASH": {
#         "follow_up": [
#             {"question": "Type", "type": "selectbox",
#              "options": ["Maculopapular", "Vesicular", "Petechial/Purpuric", "Urticarial", "Erythematous"],
#              "weights": {"Maculopapular": 1.0, "Vesicular": 1.5, "Petechial/Purpuric": 2.5, "Urticarial": 1.3, "Erythematous": 1.2},
#              "note": "Petechial rash requires immediate evaluation for meningococcemia"},
#             {"question": "Distribution", "type": "radio",
#              "options": ["Face", "Trunk", "Extremities", "Palms/soles", "Generalized"],
#              "weights": {"Face": 1.0, "Trunk": 1.2, "Extremities": 1.1, "Palms/soles": 1.8, "Generalized": 1.5}}
#         ],
#         "red_flags": [
#             "Petechial/purpuric rash",
#             "Rash with fever",
#             "Rash with mucosal involvement",
#             "Rapidly spreading rash",
#             "Rash with blistering"
#         ]
#     },
#     "VOMITING": {
#         "follow_up": [
#             {"question": "Frequency", "type": "radio",
#              "options": ["1-2 times", "3-5 times", ">5 times", "Projectile"],
#              "weights": {"1-2 times": 1.0, "3-5 times": 1.5, ">5 times": 2.0, "Projectile": 2.2},
#              "note": "Projectile vomiting in infants suggests pyloric stenosis"},
#             {"question": "Content", "type": "selectbox",
#              "options": ["Food", "Bile (green)", "Blood", "Coffee-ground"],
#              "weights": {"Food": 1.0, "Bile (green)": 1.8, "Blood": 2.5, "Coffee-ground": 2.3}}
#         ],
#         "red_flags": [
#             "Bilious vomiting",
#             "Hematemesis",
#             "Projectile vomiting in infants",
#             "Vomiting with severe abdominal pain",
#             "Vomiting with altered mental status"
#         ]
#     },
#     "DIARRHEA": {
#         "follow_up": [
#             {"question": "Frequency", "type": "radio",
#              "options": ["2-4 loose stools/day", "5-8 loose stools/day", ">8 loose stools/day", "Watery"],
#              "weights": {"2-4 loose stools/day": 1.0, "5-8 loose stools/day": 1.5, ">8 loose stools/day": 2.0, "Watery": 2.2},
#              "note": "WHO defines diarrhea as ≥3 loose stools/day"},
#             {"question": "Appearance", "type": "selectbox",
#              "options": ["Loose", "Mucoid", "Bloody", "Rice-water"],
#              "weights": {"Loose": 1.0, "Mucoid": 1.3, "Bloody": 2.0, "Rice-water": 2.2}}
#         ],
#         "red_flags": [
#             "Bloody diarrhea",
#             "Signs of dehydration (no tears, sunken eyes)",
#             "Diarrhea >2 weeks",
#             "Diarrhea with high fever",
#             ">8 watery stools/day"
#         ]
#     },
#     "EAR_PAIN": {
#         "follow_up": [
#             {"question": "Severity", "type": "radio",
#              "options": ["Mild", "Moderate", "Severe", "Disrupting sleep"],
#              "weights": {"Mild": 1.0, "Moderate": 1.3, "Severe": 1.7, "Disrupting sleep": 1.9},
#              "note": "Pulling ears in infants may indicate otitis media"},
#             {"question": "Duration", "type": "selectbox",
#              "options": ["<24 hours", "1-3 days", ">3 days"],
#              "weights": {"<24 hours": 1.0, "1-3 days": 1.2, ">3 days": 1.5}}
#         ],
#         "red_flags": [
#             "Ear pain with fever >102°F",
#             "Swelling behind ear",
#             "Facial weakness",
#             "Severe pain with sudden relief (possible rupture)"
#         ]
#     },
#     "SORE_THROAT": {
#         "follow_up": [
#             {"question": "Severity", "type": "radio",
#              "options": ["Mild", "Moderate", "Severe", "Unable to swallow"],
#              "weights": {"Mild": 1.0, "Moderate": 1.3, "Severe": 1.8, "Unable to swallow": 2.5},
#              "note": "Consider strep if >3 years with fever and no cough"},
#             {"question": "Appearance", "type": "selectbox",
#              "options": ["Red", "Exudate", "Ulcers", "Swollen tonsils"],
#              "weights": {"Red": 1.0, "Exudate": 1.5, "Ulcers": 1.8, "Swollen tonsils": 1.7}}
#         ],
#         "red_flags": [
#             "Drooling/inability to swallow",
#             "Neck stiffness with sore throat",
#             "Trismus (difficulty opening mouth)",
#             "Voice changes (hot potato voice)"
#         ]
#     },
#     "ABDOMINAL_PAIN": {
#         "follow_up": [
#             {"question": "Location", "type": "selectbox",
#              "options": ["Diffuse", "Periumbilical", "Right lower quadrant", "Epigastric", "Left lower quadrant"],
#              "weights": {"Diffuse": 1.0, "Periumbilical": 1.2, "Right lower quadrant": 2.0, "Epigastric": 1.5, "Left lower quadrant": 1.8},
#              "note": "RLQ pain suggests appendicitis, rebound tenderness is concerning"},
#             {"question": "Severity", "type": "radio",
#              "options": ["Mild", "Moderate", "Severe", "Doubled over"],
#              "weights": {"Mild": 1.0, "Moderate": 1.5, "Severe": 2.0, "Doubled over": 2.5}}
#         ],
#         "red_flags": [
#             "Right lower quadrant pain",
#             "Pain with vomiting",
#             "Rebound tenderness",
#             "Pain waking child from sleep",
#             "Abdominal rigidity"
#         ]
#     },
#     "DEHYDRATION": {
#         "follow_up": [
#             {"question": "Signs", "type": "checkbox",
#              "options": ["Dry mouth", "No tears", "Sunken eyes", "Decreased urine output", "Lethargy"],
#              "weights": {"Dry mouth": 1.0, "No tears": 1.3, "Sunken eyes": 1.5, "Decreased urine output": 1.7, "Lethargy": 2.0},
#              "note": "WHO dehydration classification: none/some/severe"}
#         ],
#         "red_flags": [
#             "No urine >12 hours",
#             "Sunken fontanelle in infants",
#             "Lethargy/unresponsiveness",
#             "Unable to keep down fluids",
#             "Capillary refill >3 seconds"
#         ]
#     },
#     "NECK_STIFFNESS": {
#         "follow_up": [
#             {"question": "Severity", "type": "radio",
#              "options": ["Mild discomfort", "Moderate stiffness", "Severe (chin can't touch chest)"],
#              "weights": {"Mild discomfort": 1.5, "Moderate stiffness": 2.0, "Severe (chin can't touch chest)": 3.0},
#              "note": "Severe neck stiffness with fever suggests meningitis"}
#         ],
#         "red_flags": [
#             "Inability to flex neck",
#             "Neck stiffness with fever",
#             "Opisthotonus (arching backward)"
#         ]
#     },
#     "PHOTOPHOBIA": {
#         "follow_up": [
#             {"question": "Severity", "type": "radio",
#              "options": ["Mild light sensitivity", "Moderate (avoids light)", "Severe (eyes tightly closed)"],
#              "weights": {"Mild light sensitivity": 1.5, "Moderate (avoids light)": 2.0, "Severe (eyes tightly closed)": 2.5},
#              "note": "Photophobia with headache may indicate meningitis"}
#         ],
#         "red_flags": [
#             "Photophobia with headache",
#             "Photophobia with neck stiffness"
#         ]
#     },
#     "COUGH_POST_TUSSIVE": {
#         "follow_up": [
#             {"question": "Occurs after coughing", "type": "radio",
#              "options": ["Never", "Sometimes", "Always"],
#              "weights": {"Never": 0.0, "Sometimes": 1.5, "Always": 2.0},
#              "note": "Post-tussive vomiting is classic for pertussis"}
#         ],
#         "red_flags": [
#             "Recurrent post-tussive vomiting"
#         ]
#     },
#     "COUGH_PAROXYSMAL": {
#         "follow_up": [
#             {"question": "Coughing fits", "type": "radio",
#              "options": ["None", "Occasional fits", "Frequent prolonged fits"],
#              "weights": {"None": 0.0, "Occasional fits": 1.8, "Frequent prolonged fits": 2.5},
#              "note": "Paroxysmal coughing is characteristic of pertussis"}
#         ],
#         "red_flags": [
#             "Paroxysms followed by whoop",
#             "Cyanosis during coughing fits"
#         ]
#     },
#     "STRAWBERRY_TONGUE": {
#         "follow_up": [
#             {"question": "Tongue appearance", "type": "radio",
#              "options": ["Normal", "White coating", "Red bumps", "Bright red with bumps"],
#              "weights": {"Normal": 0.0, "White coating": 0.5, "Red bumps": 1.5, "Bright red with bumps": 2.5},
#              "note": "Strawberry tongue is seen in scarlet fever and Kawasaki disease"}
#         ],
#         "red_flags": [
#             "Bright red tongue with prominent papillae"
#         ]
#     },
#     "KOPLIK_SPOTS": {
#         "follow_up": [
#             {"question": "Oral lesions", "type": "radio",
#              "options": ["None", "Small white spots on buccal mucosa"],
#              "weights": {"None": 0.0, "Small white spots on buccal mucosa": 2.5},
#              "note": "Koplik spots are pathognomonic for measles"}
#         ],
#         "red_flags": [
#             "White spots on buccal mucosa with fever"
#         ]
#     },
#     "STOMATITIS": {
#         "follow_up": [
#             {"question": "Mouth ulcers", "type": "radio",
#              "options": ["None", "1-3 ulcers", ">3 ulcers"],
#              "weights": {"None": 0.0, "1-3 ulcers": 1.5, ">3 ulcers": 2.0},
#              "note": "Painful oral ulcers are characteristic of hand-foot-mouth disease"}
#         ],
#         "red_flags": [
#             "Painful mouth ulcers preventing eating/drinking"
#         ]
#     }
# }

# # Enhanced dataset with more conditions and refined weights based on medical literature
# MEDICAL_DATA = """
# CONDITION,FEVER,COUGH,RUNNY_NOSE,SNEEZING,FEVER_SEVERITY,COUGH_TYPE,MUSCLE_ACHES,HEADACHE,WHEEZING,RESPIRATORY_DISTRESS,RASH,VOMITING,DIARRHEA,EAR_PAIN,SORE_THROAT,ABDOMINAL_PAIN,DEHYDRATION,NECK_STIFFNESS,PHOTOPHOBIA,CONJUNCTIVITIS,LYMPH_NODES,URINARY_FREQUENCY,DYSURIA,COUGH_POST_TUSSIVE,APNEA,COUGH_PAROXYSMAL,COUGH_NIGHTTIME,STRAWBERRY_TONGUE,KOPLIK_SPOTS,STOMATITIS
# Common Cold,0.3,1.0,1.8,1.5,0.5,1.0,0.2,0.3,0.0,0.0,0.0,0.0,0.0,0.0,0.2,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
# Influenza (Flu),1.8,1.5,0.5,0.3,1.5,1.2,1.8,1.7,0.0,0.3,0.0,0.8,0.3,0.0,0.3,0.5,0.3,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
# Bronchiolitis,0.8,2.0,0.8,0.5,0.8,1.8,0.3,0.2,2.5,2.2,0.0,0.5,0.3,0.0,0.0,0.0,0.5,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.8,0.0,1.5,0.0,0.0,0.0
# Pneumonia,2.0,2.2,0.3,0.1,1.8,2.0,1.0,1.2,1.5,2.5,0.0,0.3,0.0,0.0,0.0,0.0,0.8,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
# Meningitis,2.2,0.3,0.1,0.0,2.2,0.3,1.8,2.8,0.0,0.5,1.5,1.8,0.3,0.0,0.0,0.0,1.5,3.0,2.5,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
# Asthma,0.3,1.8,0.5,0.7,0.3,1.5,0.0,0.3,3.0,2.5,0.0,0.0,0.0,0.0,0.0,0.0,0.3,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,2.0,0.0,0.0,0.0
# Allergic Rhinitis,0.0,0.5,2.0,2.2,0.0,0.5,0.0,0.0,1.5,0.0,0.8,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.5,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
# COVID-19,1.7,1.8,0.7,0.5,1.5,1.7,1.5,1.7,0.8,1.5,0.5,0.8,0.5,0.0,0.3,0.5,0.7,0.0,0.0,0.3,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
# Strep Throat,1.5,0.5,0.3,0.1,1.2,0.3,0.8,1.5,0.0,0.0,0.0,0.5,0.0,0.0,2.2,0.5,0.0,0.0,0.0,0.0,1.5,0.0,0.0,0.0,0.0,0.0,0.0,1.8,0.0,0.0
# Croup,0.8,2.5,0.5,0.3,0.8,2.2,0.3,0.5,2.2,2.0,0.0,0.3,0.0,0.0,0.0,0.0,0.3,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.5,0.0,0.0,0.0,0.0
# Gastroenteritis,0.5,0.0,0.0,0.0,0.3,0.0,0.5,0.3,0.0,0.0,0.0,2.2,2.5,0.0,0.0,0.5,1.8,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
# UTI,1.5,0.0,0.0,0.0,1.2,0.0,0.3,0.5,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.8,1.2,0.0,0.0,0.0,0.0,2.0,2.2,0.0,0.0,0.0,0.0,0.0,0.0,0.0
# Appendicitis,0.8,0.0,0.0,0.0,0.5,0.0,0.0,0.5,0.0,0.0,0.0,1.8,0.5,0.0,0.0,2.5,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
# Hand-Foot-Mouth,1.0,0.3,0.5,0.3,0.8,0.3,0.5,0.8,0.0,0.0,2.2,0.8,0.3,0.0,0.5,1.2,0.5,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,2.0
# Roseola,2.0,0.0,0.3,0.0,1.8,0.0,0.3,0.5,0.0,0.0,1.8,0.3,0.0,0.0,0.0,0.0,0.3,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
# Pertussis,0.5,3.0,0.5,0.3,0.3,3.0,0.0,0.0,0.0,1.8,0.0,1.5,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,1.5,0.0,2.5,0.0,0.0,0.0,0.0
# Measles,2.2,1.5,1.0,0.5,2.0,1.2,1.0,1.5,0.0,0.5,2.5,0.8,0.3,0.0,0.5,1.0,1.2,0.0,1.5,1.0,0.5,0.0,0.0,0.0,0.0,0.0,0.0,0.0,2.0,0.0
# Chickenpox,1.5,0.3,0.3,0.0,1.2,0.3,0.8,1.0,0.0,0.0,2.8,0.5,0.0,0.0,0.0,0.5,0.8,0.0,0.0,0.3,0.3,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
# Otitis Media,1.0,0.0,0.5,0.0,0.8,0.0,0.0,0.5,0.0,0.0,0.0,0.3,0.0,1.8,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
# Sinusitis,1.2,0.8,1.5,0.8,1.0,0.8,0.5,1.5,0.0,0.0,0.0,0.3,0.0,0.0,1.5,0.0,0.0,0.0,0.5,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
# RSV,1.5,2.2,1.0,0.5,1.2,2.0,0.3,0.5,2.5,2.2,0.0,0.5,0.3,0.0,0.0,0.0,0.5,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.8,0.0,0.0,0.0,0.0
# Scarlet Fever,2.0,0.3,0.3,0.0,1.8,0.3,1.0,1.5,0.0,0.0,2.5,0.8,0.0,0.0,1.8,0.5,0.0,0.0,0.0,0.0,1.5,0.0,0.0,0.0,0.0,0.0,0.0,2.0,0.0,0.0
# Fifth Disease,1.0,0.3,0.5,0.3,0.8,0.3,0.5,0.8,0.0,0.0,2.0,0.3,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.3,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
# Impetigo,0.3,0.0,0.0,0.0,0.3,0.0,0.0,0.0,0.0,0.0,2.5,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.5,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
# Conjunctivitis,0.3,0.0,0.5,0.3,0.3,0.0,0.0,0.0,0.0,0.0,0.5,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.5,2.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
# Pharyngitis,1.2,0.5,0.5,0.3,1.0,0.5,0.5,1.0,0.0,0.0,0.0,0.3,0.0,0.0,1.5,0.0,0.0,0.0,0.0,0.3,0.8,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
# Pyloric Stenosis,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,2.5,0.0,0.0,0.0,0.0,1.5,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
# Intussusception,0.8,0.0,0.0,0.0,0.5,0.0,0.0,0.0,0.0,0.0,0.0,2.2,1.5,0.0,0.0,0.0,2.5,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
# Kawasaki Disease,2.5,0.5,0.8,0.0,2.2,0.5,0.5,1.5,0.0,0.5,2.0,0.5,0.3,0.0,0.0,1.5,0.8,0.5,0.0,1.5,1.8,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.5
# Rheumatic Fever,1.5,0.5,0.3,0.0,1.2,0.5,1.5,1.8,0.0,0.5,1.5,0.3,0.0,0.0,0.0,1.8,0.5,0.3,0.0,0.5,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
# Epiglottitis,2.0,0.8,0.0,0.0,1.8,0.8,1.0,1.2,0.0,2.5,0.0,0.5,0.0,0.0,0.0,2.5,0.0,1.5,0.0,0.0,1.5,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
# Cellulitis,1.5,0.0,0.0,0.0,1.2,0.0,0.5,0.8,0.0,0.0,1.8,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
# Mononucleosis,1.8,0.5,0.3,0.0,1.5,0.5,1.5,2.0,0.0,0.0,0.8,0.5,0.0,0.0,0.0,1.8,0.8,0.0,0.5,0.5,2.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
# Rotavirus,0.5,0.0,0.0,0.0,0.3,0.0,0.3,0.5,0.0,0.0,0.0,1.5,2.5,0.0,0.0,0.0,1.8,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
# Pinworms,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.3,0.0,0.0,0.0,0.0,0.0,1.5,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
# """

# @st.cache_data
# def load_data():
#     from io import StringIO
#     df = pd.read_csv(StringIO(MEDICAL_DATA))
#     # Fill NaN values with 0 for all symptoms
#     symptom_cols = [col for col in df.columns if col != "CONDITION"]
#     df[symptom_cols] = df[symptom_cols].fillna(0)
#     return df

# def calculate_age_risk_factor(age):
#     """Calculate risk factor based on age (higher risk for infants and immunocompromised)"""
#     if age < 3: return 1.5  # Higher weight for infants
#     elif age < 12: return 1.2  # Moderate weight for young children
#     else: return 1.0  # Standard weight for older children

# def apply_clinical_overrides(prediction, symptoms, age):
#     """Apply clinical rules to override model predictions when specific patterns are detected"""
#     # Meningitis override
#     if "NECK_STIFFNESS" in symptoms and "FEVER" in symptoms and "PHOTOPHOBIA" in symptoms and age < 5:
#         return "Meningitis (clinical override)", 0.95
    
#     # Pertussis pattern
#     if "COUGH_PAROXYSMAL" in symptoms and "COUGH_POST_TUSSIVE" in symptoms:
#         return "Pertussis (clinical override)", 0.9
        
#     # Kawasaki criteria
#     if "FEVER" in symptoms and "STRAWBERRY_TONGUE" in symptoms and "RASH" in symptoms and age < 5:
#         return "Kawasaki Disease (clinical override)", 0.85
    
#     # Scarlet fever
#     if "STRAWBERRY_TONGUE" in symptoms and "SORE_THROAT" in symptoms and "RASH" in symptoms:
#         return "Scarlet Fever (clinical override)", 0.85
    
#     # Measles
#     if "KOPLIK_SPOTS" in symptoms and "FEVER" in symptoms and "RASH" in symptoms:
#         return "Measles (clinical override)", 0.9
    
#     return prediction, None

# def find_nearby_doctors(lat, lon, radius=5000):
#     """
#     Find nearby doctors and pediatricians using Overpass API
#     Returns a DataFrame with name, address, and coordinates
#     """
#     overpass_url = "https://overpass-api.de/api/interpreter"
    
#     # Query for doctors and pediatricians
#     #pediatricians checker
#     query = f"""
#     [out:json];
#     (
#       node["amenity"="doctors"](around:{radius},{lat},{lon});
#       node["amenity"="clinic"](around:{radius},{lat},{lon});
#       node["healthcare"="doctor"](around:{radius},{lat},{lon});
#       node["healthcare"="pediatrician"](around:{radius},{lat},{lon}); 
#     );
#     out center;
#     """
    
#     try:
#         response = requests.get(overpass_url, params={'data': query})
#         response.raise_for_status()
#         data = response.json()
        
#         doctors = []
#         for element in data['elements']:
#             name = element.get('tags', {}).get('name', 'Unknown')
#             address = element.get('tags', {}).get('addr:full', 
#                       element.get('tags', {}).get('addr:street', 'Address not available'))
#             specialty = element.get('tags', {}).get('healthcare:speciality', 'General Practitioner')
            
#             # Get coordinates
#             if 'lat' in element and 'lon' in element:
#                 lat = element['lat']
#                 lon = element['lon']
#             elif 'center' in element:
#                 lat = element['center']['lat']
#                 lon = element['center']['lon']
#             else:
#                 continue
                
#             doctors.append({
#                 'name': name,
#                 'address': address,
#                 'specialty': specialty,
#                 'latitude': lat,
#                 'longitude': lon
#             })
            
#         return pd.DataFrame(doctors)
    
#     except Exception as e:
#         st.error(f"Error fetching nearby doctors: {e}")
#         return pd.DataFrame()

# def show_nearby_doctors():
#     """Show interface for finding nearby doctors"""
#     with st.expander("🚑 Find Nearby Doctors & Pediatricians", expanded=False):
#         st.write("Locate nearby healthcare providers based on your location")
        
#         # Location input options
#         location_method = st.radio("Select location method:", 
#                                  ["Use my current location", "Enter address manually"])
        
#         if location_method == "Use my current location":
#             # Note: In a real app, you would use the browser's geolocation API
#             # This is a simplified version for demonstration
#             lat = st.number_input("Latitude", value=40.7128, format="%.6f")
#             lon = st.number_input("Longitude", value=-74.0060, format="%.6f")
#         else:
#             address = st.text_input("Enter full address:")
#             if address:
#                 geolocator = Nominatim(user_agent="pediatric_symptom_checker")
#                 try:
#                     location = geolocator.geocode(address)
#                     if location:
#                         lat, lon = location.latitude, location.longitude
#                         st.success(f"Found location: {location.address}")
#                     else:
#                         st.warning("Could not find location. Using default coordinates.")
#                         lat, lon = 40.7128, -74.0060  # Default to NYC
#                 except Exception as e:
#                     st.error(f"Geocoding error: {e}")
#                     lat, lon = 40.7128, -74.0060
        
#         search_radius = st.slider("Search radius (meters)", 500, 10000, 2000)
        
#         if st.button("Find Nearby Doctors", key="find_doctors"):
#             with st.spinner("Searching for nearby doctors..."):
#                 doctors_df = find_nearby_doctors(lat, lon, search_radius)
                
#                 if not doctors_df.empty:
#                     st.success(f"Found {len(doctors_df)} doctors/clinics nearby")
                    
#                     # Create map centered at user's location
#                     m = folium.Map(location=[lat, lon], zoom_start=13)
                    
#                     # Add marker for user's location
#                     folium.Marker(
#                         [lat, lon],
#                         popup="Your Location",
#                         icon=folium.Icon(color="blue", icon="user")
#                     ).add_to(m)
                    
#                     # Add markers for each doctor
#                     for idx, row in doctors_df.iterrows():
#                         popup_text = f"""
#                         <b>{row['name']}</b><br>
#                         <i>{row['specialty']}</i><br>
#                         {row['address']}
#                         """
                        
#                         icon_color = "green" if "pediatric" in row['specialty'].lower() else "red"
                        
#                         folium.Marker(
#                             [row['latitude'], row['longitude']],
#                             popup=popup_text,
#                             icon=folium.Icon(color=icon_color, icon="medkit")
#                         ).add_to(m)
                    
#                     # Display the map
#                     folium_static(m)
                    
#                     # Show the data in a table
#                     st.subheader("Nearby Healthcare Providers")
#                     st.dataframe(doctors_df[['name', 'specialty', 'address']])
#                 else:
#                     st.warning("No doctors found in the specified area. Try increasing the search radius.")

# def main():
#     st.set_page_config(page_title="Pediatric Symptom Checker", page_icon="👶", layout="wide")
#     st.title("👶 Pediatric Symptom Checker")
    
#     # Load data
#     df = load_data()
    
#     # Get all available symptoms from dataset
#     all_symptoms = [col for col in df.columns if col != "CONDITION"]
    
#     # Age input
#     with st.expander("Patient Information", expanded=True):
#         col1, col2 = st.columns(2)
#         with col1:
#             age = st.number_input("Age (months)", min_value=0, max_value=216, value=24, step=1)
#         with col2:
#             medical_history = st.multiselect(
#                 "Medical History (select all that apply)",
#                 options=["Asthma", "Diabetes", "Heart Condition", "Immunocompromised", "Prematurity"],
#                 default=[]
#             )
    
#     # Step 1: Primary symptom selection
#     with st.expander("Step 1: Select main symptoms", expanded=True):
#         primary_symptoms = st.multiselect(
#             "What symptoms is your child experiencing?",
#             options=all_symptoms,
#             placeholder="Select symptoms..."
#         )
    
#     # Step 2: Detailed symptom questions
#     symptom_details = {}
#     if primary_symptoms:
#         with st.expander("Step 2: Provide symptom details", expanded=True):
#             for symptom in primary_symptoms:
#                 if symptom in SYMPTOM_DEFINITIONS:
#                     st.subheader(f"Details about {symptom.lower().replace('_', ' ')}")
                    
#                     symptom_weight = 1.0  # Base weight
                    
#                     for question in SYMPTOM_DEFINITIONS[symptom]["follow_up"]:
#                         response = None
#                         if question["type"] == "radio":
#                             response = st.radio(
#                                 question["question"],
#                                 options=question["options"],
#                                 key=f"{symptom}_{question['question']}"
#                             )
#                         elif question["type"] == "selectbox":
#                             response = st.selectbox(
#                                 question["question"],
#                                 options=question["options"],
#                                 key=f"{symptom}_{question['question']}"
#                             )
#                         elif question["type"] == "checkbox":
#                             response = st.multiselect(
#                                 question["question"],
#                                 options=question["options"],
#                                 key=f"{symptom}_{question['question']}"
#                             )
                        
#                         if response:
#                             if isinstance(response, list):  # For checkbox questions
#                                 for item in response:
#                                     symptom_weight *= question["weights"][item]
#                             else:  # For radio/selectbox
#                                 symptom_weight *= question["weights"][response]
                    
#                     symptom_details[symptom] = {
#                         "value": 1.0,  # Base value
#                         "weight": symptom_weight
#                     }
                    
#                     # Show clinical notes if available
#                     if "note" in SYMPTOM_DEFINITIONS[symptom]:
#                         st.info(SYMPTOM_DEFINITIONS[symptom]["note"])
#                 else:
#                     # For symptoms without follow-up questions
#                     severity = st.slider(
#                         f"Severity of {symptom.lower().replace('_', ' ')}",
#                         min_value=0.1,
#                         max_value=3.0,
#                         value=1.0,
#                         step=0.1,
#                         key=symptom
#                     )
#                     symptom_details[symptom] = {
#                         "value": severity,
#                         "weight": 1.0
#                     }
    
#     # Step 3: Predict
#     if st.button("Analyze Symptoms", type="primary", use_container_width=True):
#         if not primary_symptoms:
#             st.warning("Please select at least one symptom")
#             return
        
#         # Prepare features (only numerical columns)
#         numerical_cols = [col for col in df.columns if col != "CONDITION"]
#         X = df[numerical_cols]
#         y = df["CONDITION"]
        
#         # Train model - using GradientBoosting for better performance
#         model = GradientBoostingClassifier(
#             n_estimators=200,
#             learning_rate=0.1,
#             max_depth=4,
#             min_samples_leaf=3,
#             random_state=42
#         )
#         model.fit(X, y)
        
#         # Prepare input features
#         input_features = {col: 0.0 for col in numerical_cols}
        
#         # Apply symptom weights and age factor
#         age_factor = calculate_age_risk_factor(age)
#         for symptom, details in symptom_details.items():
#             if symptom in input_features:
#                 input_features[symptom] = details["value"] * details["weight"] * age_factor
        
#         # Additional weight for concerning medical history
#         if "Immunocompromised" in medical_history:
#             for symptom in input_features:
#                 if input_features[symptom] > 0:
#                     input_features[symptom] *= 1.5
        
#         # Convert to DataFrame
#         input_df = pd.DataFrame([input_features])[numerical_cols]
        
#         # Make prediction
#         prediction = model.predict(input_df)[0]
#         probabilities = model.predict_proba(input_df)[0]
        
#         # Apply clinical overrides
#         override_prediction, override_prob = apply_clinical_overrides(prediction, primary_symptoms, age)
#         if override_prediction:
#             prediction = override_prediction
        
#         # Display results
#         col1, col2 = st.columns([1, 2])
        
#         with col1:
#             st.success(f"### Most likely condition: **{prediction}**")
            
#             # Show probabilities
#             st.subheader("Top Possible Conditions")
#             prob_df = pd.DataFrame({
#                 "Condition": model.classes_,
#                 "Probability": probabilities
#             }).sort_values("Probability", ascending=False).head(5)
            
#             # Highlight overridden condition if applicable
#             if override_prediction:
#                 prob_df.loc[prob_df['Condition'] == override_prediction.split(' (')[0], 'Probability'] = override_prob
            
#             # Format probabilities with colors
#             def color_probs(val):
#                 color = 'red' if val > 0.7 else 'orange' if val > 0.3 else 'green'
#                 return f'color: {color}; font-weight: bold'
            
#             st.dataframe(
#                 prob_df.style.format({"Probability": "{:.2%}"})
#                       .applymap(color_probs, subset=['Probability']),
#                 hide_index=True
#             )
        
#         with col2:
#             # Show red flags
#             st.subheader("⚠️ Red Flags to Watch For")
#             red_flags_found = False
            
#             # Check symptom-specific red flags
#             for symptom in primary_symptoms:
#                 if symptom in SYMPTOM_DEFINITIONS and "red_flags" in SYMPTOM_DEFINITIONS[symptom]:
#                     for flag in SYMPTOM_DEFINITIONS[symptom]["red_flags"]:
#                         st.error(f"• {flag}")
#                         red_flags_found = True
            
#             # Age-specific red flags
#             if age < 3 and "FEVER" in primary_symptoms:
#                 st.error("• Fever in infants <3 months requires immediate evaluation")
#                 red_flags_found = True
                
#             if age < 6 and "COUGH" in primary_symptoms and "WHEEZING" in primary_symptoms:
#                 st.error("• Wheezing in infants <6 months may indicate serious illness")
#                 red_flags_found = True
                
#             if "PETECHIAL/PURPURIC" in primary_symptoms and "FEVER" in primary_symptoms:
#                 st.error("• Petechial rash with fever may indicate meningococcemia - seek IMMEDIATE care")
#                 red_flags_found = True
            
#             if not red_flags_found:
#                 st.info("No urgent red flags identified based on current symptoms")
            
#             # General advice
#             st.subheader("ℹ️ Recommended Actions")
#             if "Meningitis" in prediction:
#                 st.error("""
#                 **EMERGENCY: Seek immediate medical attention**
#                 - This is a medical emergency requiring IV antibiotics
#                 - Go to nearest ER immediately
#                 - Do not wait for symptoms to worsen
#                 """)
#             elif "Epiglottitis" in prediction:
#                 st.error("""
#                 **EMERGENCY: Do not examine throat**
#                 - Risk of complete airway obstruction
#                 - Keep child calm and upright
#                 - Call emergency services immediately
#                 """)
#             elif prediction in ["Bronchiolitis", "Pneumonia", "Dehydration"]:
#                 st.warning("""
#                 **Urgent: Contact your pediatrician within 4-6 hours**
#                 - Monitor respiratory rate closely
#                 - Keep child hydrated
#                 - Watch for signs of worsening distress
#                 """)
#             elif prediction in ["Influenza (Flu)", "Strep Throat", "Pertussis"]:
#                 st.warning("""
#                 **Contact your pediatrician within 24 hours**
#                 - Rest and fluids
#                 - Monitor fever pattern
#                 - Watch for complications
#                 - May need specific testing/treatment
#                 """)
#             else:
#                 st.info("""
#                 **Monitor at home**
#                 - Symptomatic treatment as needed
#                 - Contact doctor if symptoms worsen or persist >3 days
#                 - Ensure adequate hydration
#                 - Watch for new symptoms
#                 """)
            
#             # Special considerations based on age and history
#             if age < 6:
#                 st.info("ℹ️ For infants under 6 months, always consult a doctor for any significant symptoms")
            
#             if "Immunocompromised" in medical_history:
#                 st.warning("⚠️ Immunocompromised children may need earlier evaluation for fever or infection")
    
#     # Show the nearby doctors feature (always visible)
#     show_nearby_doctors()

# if __name__ == "__main__":
#     main()




#MAPS
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.preprocessing import LabelEncoder
import requests
import json
import folium
from streamlit_folium import folium_static
from geopy.geocoders import Nominatim
from fpdf import FPDF
import base64
from datetime import datetime

# Enhanced medical knowledge base with more pediatric symptoms and refined weights
SYMPTOM_DEFINITIONS = {
    "FEVER": {
        "follow_up": [
            {"question": "Temperature", "type": "radio", 
             "options": ["<100.4°F (normal)", "100.4-102.2°F (low-grade)", "102.2-104°F (moderate)", ">104°F (high)"],
             "weights": {"<100.4°F (normal)": 0.5, "100.4-102.2°F (low-grade)": 1.0, "102.2-104°F (moderate)": 1.8, ">104°F (high)": 2.5},
             "note": "In infants <3 months, any fever >100.4°F requires immediate evaluation"},
            {"question": "Duration", "type": "selectbox",
             "options": ["<24 hours", "1-3 days", "3-7 days", ">7 days"],
             "weights": {"<24 hours": 0.8, "1-3 days": 1.0, "3-7 days": 1.5, ">7 days": 2.0}}
        ],
        "red_flags": [
            "Fever >100.4°F in infant <3 months",
            "Fever >104°F",
            "Fever with stiff neck or photophobia",
            "Fever with petechial rash",
            "Fever lasting >5 days"
        ],
        "who_notes": "Fever patterns can help differentiate diseases - sustained in typhoid, quotidian in malaria"
    },
    "COUGH": {
        "follow_up": [
            {"question": "Type", "type": "selectbox",
             "options": ["Dry", "Productive", "Barking", "Whooping", "Staccato"],
             "weights": {"Dry": 1.0, "Productive": 1.2, "Barking": 1.8, "Whooping": 2.2, "Staccato": 2.0},
             "note": "Barking cough suggests croup, whooping suggests pertussis"},
            {"question": "Timing", "type": "radio",
             "options": ["Daytime", "Nighttime", "With feeding", "After exercise", "All day"],
             "weights": {"Daytime": 1.0, "Nighttime": 1.3, "With feeding": 1.5, "After exercise": 1.7, "All day": 1.5}}
        ],
        "red_flags": [
            "Whooping sound on inspiration",
            "Cough causing vomiting",
            "Cough with cyanosis",
            "Cough lasting >3 weeks",
            "Sudden onset cough (possible aspiration)"
        ]
    },
    "RESPIRATORY_DISTRESS": {
        "follow_up": [
            {"question": "Severity", "type": "radio",
             "options": ["None", "Mild (intercostal retractions)", "Moderate (nasal flaring)", "Severe (grunting, head bobbing)"],
             "weights": {"None": 0, "Mild (intercostal retractions)": 1.5, "Moderate (nasal flaring)": 2.0, "Severe (grunting, head bobbing)": 3.0},
             "note": "WHO defines tachypnea as RR >60 in <2mo, >50 in 2-12mo, >40 in 1-5y"}
        ],
        "red_flags": [
            "Respiratory rate >60/min",
            "Cyanosis",
            "Grunting",
            "Severe retractions",
            "Inability to speak/cry"
        ]
    },
    "RASH": {
        "follow_up": [
            {"question": "Type", "type": "selectbox",
             "options": ["Maculopapular", "Vesicular", "Petechial/Purpuric", "Urticarial", "Erythematous"],
             "weights": {"Maculopapular": 1.0, "Vesicular": 1.5, "Petechial/Purpuric": 2.5, "Urticarial": 1.3, "Erythematous": 1.2},
             "note": "Petechial rash requires immediate evaluation for meningococcemia"},
            {"question": "Distribution", "type": "radio",
             "options": ["Face", "Trunk", "Extremities", "Palms/soles", "Generalized"],
             "weights": {"Face": 1.0, "Trunk": 1.2, "Extremities": 1.1, "Palms/soles": 1.8, "Generalized": 1.5}}
        ],
        "red_flags": [
            "Petechial/purpuric rash",
            "Rash with fever",
            "Rash with mucosal involvement",
            "Rapidly spreading rash",
            "Rash with blistering"
        ]
    },
    "VOMITING": {
        "follow_up": [
            {"question": "Frequency", "type": "radio",
             "options": ["1-2 times", "3-5 times", ">5 times", "Projectile"],
             "weights": {"1-2 times": 1.0, "3-5 times": 1.5, ">5 times": 2.0, "Projectile": 2.2},
             "note": "Projectile vomiting in infants suggests pyloric stenosis"},
            {"question": "Content", "type": "selectbox",
             "options": ["Food", "Bile (green)", "Blood", "Coffee-ground"],
             "weights": {"Food": 1.0, "Bile (green)": 1.8, "Blood": 2.5, "Coffee-ground": 2.3}}
        ],
        "red_flags": [
            "Bilious vomiting",
            "Hematemesis",
            "Projectile vomiting in infants",
            "Vomiting with severe abdominal pain",
            "Vomiting with altered mental status"
        ]
    },
    "DIARRHEA": {
        "follow_up": [
            {"question": "Frequency", "type": "radio",
             "options": ["2-4 loose stools/day", "5-8 loose stools/day", ">8 loose stools/day", "Watery"],
             "weights": {"2-4 loose stools/day": 1.0, "5-8 loose stools/day": 1.5, ">8 loose stools/day": 2.0, "Watery": 2.2},
             "note": "WHO defines diarrhea as ≥3 loose stools/day"},
            {"question": "Appearance", "type": "selectbox",
             "options": ["Loose", "Mucoid", "Bloody", "Rice-water"],
             "weights": {"Loose": 1.0, "Mucoid": 1.3, "Bloody": 2.0, "Rice-water": 2.2}}
        ],
        "red_flags": [
            "Bloody diarrhea",
            "Signs of dehydration (no tears, sunken eyes)",
            "Diarrhea >2 weeks",
            "Diarrhea with high fever",
            ">8 watery stools/day"
        ]
    },
    "EAR_PAIN": {
        "follow_up": [
            {"question": "Severity", "type": "radio",
             "options": ["Mild", "Moderate", "Severe", "Disrupting sleep"],
             "weights": {"Mild": 1.0, "Moderate": 1.3, "Severe": 1.7, "Disrupting sleep": 1.9},
             "note": "Pulling ears in infants may indicate otitis media"},
            {"question": "Duration", "type": "selectbox",
             "options": ["<24 hours", "1-3 days", ">3 days"],
             "weights": {"<24 hours": 1.0, "1-3 days": 1.2, ">3 days": 1.5}}
        ],
        "red_flags": [
            "Ear pain with fever >102°F",
            "Swelling behind ear",
            "Facial weakness",
            "Severe pain with sudden relief (possible rupture)"
        ]
    },
    "SORE_THROAT": {
        "follow_up": [
            {"question": "Severity", "type": "radio",
             "options": ["Mild", "Moderate", "Severe", "Unable to swallow"],
             "weights": {"Mild": 1.0, "Moderate": 1.3, "Severe": 1.8, "Unable to swallow": 2.5},
             "note": "Consider strep if >3 years with fever and no cough"},
            {"question": "Appearance", "type": "selectbox",
             "options": ["Red", "Exudate", "Ulcers", "Swollen tonsils"],
             "weights": {"Red": 1.0, "Exudate": 1.5, "Ulcers": 1.8, "Swollen tonsils": 1.7}}
        ],
        "red_flags": [
            "Drooling/inability to swallow",
            "Neck stiffness with sore throat",
            "Trismus (difficulty opening mouth)",
            "Voice changes (hot potato voice)"
        ]
    },
    "ABDOMINAL_PAIN": {
        "follow_up": [
            {"question": "Location", "type": "selectbox",
             "options": ["Diffuse", "Periumbilical", "Right lower quadrant", "Epigastric", "Left lower quadrant"],
             "weights": {"Diffuse": 1.0, "Periumbilical": 1.2, "Right lower quadrant": 2.0, "Epigastric": 1.5, "Left lower quadrant": 1.8},
             "note": "RLQ pain suggests appendicitis, rebound tenderness is concerning"},
            {"question": "Severity", "type": "radio",
             "options": ["Mild", "Moderate", "Severe", "Doubled over"],
             "weights": {"Mild": 1.0, "Moderate": 1.5, "Severe": 2.0, "Doubled over": 2.5}}
        ],
        "red_flags": [
            "Right lower quadrant pain",
            "Pain with vomiting",
            "Rebound tenderness",
            "Pain waking child from sleep",
            "Abdominal rigidity"
        ]
    },
    "DEHYDRATION": {
        "follow_up": [
            {"question": "Signs", "type": "checkbox",
             "options": ["Dry mouth", "No tears", "Sunken eyes", "Decreased urine output", "Lethargy"],
             "weights": {"Dry mouth": 1.0, "No tears": 1.3, "Sunken eyes": 1.5, "Decreased urine output": 1.7, "Lethargy": 2.0},
             "note": "WHO dehydration classification: none/some/severe"}
        ],
        "red_flags": [
            "No urine >12 hours",
            "Sunken fontanelle in infants",
            "Lethargy/unresponsiveness",
            "Unable to keep down fluids",
            "Capillary refill >3 seconds"
        ]
    },
    "NECK_STIFFNESS": {
        "follow_up": [
            {"question": "Severity", "type": "radio",
             "options": ["Mild discomfort", "Moderate stiffness", "Severe (chin can't touch chest)"],
             "weights": {"Mild discomfort": 1.5, "Moderate stiffness": 2.0, "Severe (chin can't touch chest)": 3.0},
             "note": "Severe neck stiffness with fever suggests meningitis"}
        ],
        "red_flags": [
            "Inability to flex neck",
            "Neck stiffness with fever",
            "Opisthotonus (arching backward)"
        ]
    },
    "PHOTOPHOBIA": {
        "follow_up": [
            {"question": "Severity", "type": "radio",
             "options": ["Mild light sensitivity", "Moderate (avoids light)", "Severe (eyes tightly closed)"],
             "weights": {"Mild light sensitivity": 1.5, "Moderate (avoids light)": 2.0, "Severe (eyes tightly closed)": 2.5},
             "note": "Photophobia with headache may indicate meningitis"}
        ],
        "red_flags": [
            "Photophobia with headache",
            "Photophobia with neck stiffness"
        ]
    },
    "COUGH_POST_TUSSIVE": {
        "follow_up": [
            {"question": "Occurs after coughing", "type": "radio",
             "options": ["Never", "Sometimes", "Always"],
             "weights": {"Never": 0.0, "Sometimes": 1.5, "Always": 2.0},
             "note": "Post-tussive vomiting is classic for pertussis"}
        ],
        "red_flags": [
            "Recurrent post-tussive vomiting"
        ]
    },
    "COUGH_PAROXYSMAL": {
        "follow_up": [
            {"question": "Coughing fits", "type": "radio",
             "options": ["None", "Occasional fits", "Frequent prolonged fits"],
             "weights": {"None": 0.0, "Occasional fits": 1.8, "Frequent prolonged fits": 2.5},
             "note": "Paroxysmal coughing is characteristic of pertussis"}
        ],
        "red_flags": [
            "Paroxysms followed by whoop",
            "Cyanosis during coughing fits"
        ]
    },
    "STRAWBERRY_TONGUE": {
        "follow_up": [
            {"question": "Tongue appearance", "type": "radio",
             "options": ["Normal", "White coating", "Red bumps", "Bright red with bumps"],
             "weights": {"Normal": 0.0, "White coating": 0.5, "Red bumps": 1.5, "Bright red with bumps": 2.5},
             "note": "Strawberry tongue is seen in scarlet fever and Kawasaki disease"}
        ],
        "red_flags": [
            "Bright red tongue with prominent papillae"
        ]
    },
    "KOPLIK_SPOTS": {
        "follow_up": [
            {"question": "Oral lesions", "type": "radio",
             "options": ["None", "Small white spots on buccal mucosa"],
             "weights": {"None": 0.0, "Small white spots on buccal mucosa": 2.5},
             "note": "Koplik spots are pathognomonic for measles"}
        ],
        "red_flags": [
            "White spots on buccal mucosa with fever"
        ]
    },
    "STOMATITIS": {
        "follow_up": [
            {"question": "Mouth ulcers", "type": "radio",
             "options": ["None", "1-3 ulcers", ">3 ulcers"],
             "weights": {"None": 0.0, "1-3 ulcers": 1.5, ">3 ulcers": 2.0},
             "note": "Painful oral ulcers are characteristic of hand-foot-mouth disease"}
        ],
        "red_flags": [
            "Painful mouth ulcers preventing eating/drinking"
        ]
    }
}

# Enhanced dataset with more conditions and refined weights based on medical literature
MEDICAL_DATA = """
CONDITION,FEVER,COUGH,RUNNY_NOSE,SNEEZING,FEVER_SEVERITY,COUGH_TYPE,MUSCLE_ACHES,HEADACHE,WHEEZING,RESPIRATORY_DISTRESS,RASH,VOMITING,DIARRHEA,EAR_PAIN,SORE_THROAT,ABDOMINAL_PAIN,DEHYDRATION,NECK_STIFFNESS,PHOTOPHOBIA,CONJUNCTIVITIS,LYMPH_NODES,URINARY_FREQUENCY,DYSURIA,COUGH_POST_TUSSIVE,APNEA,COUGH_PAROXYSMAL,COUGH_NIGHTTIME,STRAWBERRY_TONGUE,KOPLIK_SPOTS,STOMATITIS
Common Cold,0.3,1.0,1.8,1.5,0.5,1.0,0.2,0.3,0.0,0.0,0.0,0.0,0.0,0.0,0.2,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
Influenza (Flu),1.8,1.5,0.5,0.3,1.5,1.2,1.8,1.7,0.0,0.3,0.0,0.8,0.3,0.0,0.3,0.5,0.3,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
Bronchiolitis,0.8,2.0,0.8,0.5,0.8,1.8,0.3,0.2,2.5,2.2,0.0,0.5,0.3,0.0,0.0,0.0,0.5,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.8,0.0,1.5,0.0,0.0,0.0
Pneumonia,2.0,2.2,0.3,0.1,1.8,2.0,1.0,1.2,1.5,2.5,0.0,0.3,0.0,0.0,0.0,0.0,0.8,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
Meningitis,2.2,0.3,0.1,0.0,2.2,0.3,1.8,2.8,0.0,0.5,1.5,1.8,0.3,0.0,0.0,0.0,1.5,3.0,2.5,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
Asthma,0.3,1.8,0.5,0.7,0.3,1.5,0.0,0.3,3.0,2.5,0.0,0.0,0.0,0.0,0.0,0.0,0.3,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,2.0,0.0,0.0,0.0
Allergic Rhinitis,0.0,0.5,2.0,2.2,0.0,0.5,0.0,0.0,1.5,0.0,0.8,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.5,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
COVID-19,1.7,1.8,0.7,0.5,1.5,1.7,1.5,1.7,0.8,1.5,0.5,0.8,0.5,0.0,0.3,0.5,0.7,0.0,0.0,0.3,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
Strep Throat,1.5,0.5,0.3,0.1,1.2,0.3,0.8,1.5,0.0,0.0,0.0,0.5,0.0,0.0,2.2,0.5,0.0,0.0,0.0,0.0,1.5,0.0,0.0,0.0,0.0,0.0,0.0,1.8,0.0,0.0
Croup,0.8,2.5,0.5,0.3,0.8,2.2,0.3,0.5,2.2,2.0,0.0,0.3,0.0,0.0,0.0,0.0,0.3,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.5,0.0,0.0,0.0,0.0
Gastroenteritis,0.5,0.0,0.0,0.0,0.3,0.0,0.5,0.3,0.0,0.0,0.0,2.2,2.5,0.0,0.0,0.5,1.8,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
UTI,1.5,0.0,0.0,0.0,1.2,0.0,0.3,0.5,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.8,1.2,0.0,0.0,0.0,0.0,2.0,2.2,0.0,0.0,0.0,0.0,0.0,0.0,0.0
Appendicitis,0.8,0.0,0.0,0.0,0.5,0.0,0.0,0.5,0.0,0.0,0.0,1.8,0.5,0.0,0.0,2.5,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
Hand-Foot-Mouth,1.0,0.3,0.5,0.3,0.8,0.3,0.5,0.8,0.0,0.0,2.2,0.8,0.3,0.0,0.5,1.2,0.5,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,2.0
Roseola,2.0,0.0,0.3,0.0,1.8,0.0,0.3,0.5,0.0,0.0,1.8,0.3,0.0,0.0,0.0,0.0,0.3,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
Pertussis,0.5,3.0,0.5,0.3,0.3,3.0,0.0,0.0,0.0,1.8,0.0,1.5,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,1.5,0.0,2.5,0.0,0.0,0.0,0.0
Measles,2.2,1.5,1.0,0.5,2.0,1.2,1.0,1.5,0.0,0.5,2.5,0.8,0.3,0.0,0.5,1.0,1.2,0.0,1.5,1.0,0.5,0.0,0.0,0.0,0.0,0.0,0.0,0.0,2.0,0.0
Chickenpox,1.5,0.3,0.3,0.0,1.2,0.3,0.8,1.0,0.0,0.0,2.8,0.5,0.0,0.0,0.0,0.5,0.8,0.0,0.0,0.3,0.3,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
Otitis Media,1.0,0.0,0.5,0.0,0.8,0.0,0.0,0.5,0.0,0.0,0.0,0.3,0.0,1.8,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
Sinusitis,1.2,0.8,1.5,0.8,1.0,0.8,0.5,1.5,0.0,0.0,0.0,0.3,0.0,0.0,1.5,0.0,0.0,0.0,0.5,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
RSV,1.5,2.2,1.0,0.5,1.2,2.0,0.3,0.5,2.5,2.2,0.0,0.5,0.3,0.0,0.0,0.0,0.5,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.8,0.0,0.0,0.0,0.0
Scarlet Fever,2.0,0.3,0.3,0.0,1.8,0.3,1.0,1.5,0.0,0.0,2.5,0.8,0.0,0.0,1.8,0.5,0.0,0.0,0.0,0.0,1.5,0.0,0.0,0.0,0.0,0.0,0.0,2.0,0.0,0.0
Fifth Disease,1.0,0.3,0.5,0.3,0.8,0.3,0.5,0.8,0.0,0.0,2.0,0.3,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.3,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
Impetigo,0.3,0.0,0.0,0.0,0.3,0.0,0.0,0.0,0.0,0.0,2.5,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.5,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
Conjunctivitis,0.3,0.0,0.5,0.3,0.3,0.0,0.0,0.0,0.0,0.0,0.5,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.5,2.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
Pharyngitis,1.2,0.5,0.5,0.3,1.0,0.5,0.5,1.0,0.0,0.0,0.0,0.3,0.0,0.0,1.5,0.0,0.0,0.0,0.0,0.3,0.8,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
Pyloric Stenosis,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,2.5,0.0,0.0,0.0,0.0,1.5,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
Intussusception,0.8,0.0,0.0,0.0,0.5,0.0,0.0,0.0,0.0,0.0,0.0,2.2,1.5,0.0,0.0,0.0,2.5,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
Kawasaki Disease,2.5,0.5,0.8,0.0,2.2,0.5,0.5,1.5,0.0,0.5,2.0,0.5,0.3,0.0,0.0,1.5,0.8,0.5,0.0,1.5,1.8,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.5
Rheumatic Fever,1.5,0.5,0.3,0.0,1.2,0.5,1.5,1.8,0.0,0.5,1.5,0.3,0.0,0.0,0.0,1.8,0.5,0.3,0.0,0.5,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
Epiglottitis,2.0,0.8,0.0,0.0,1.8,0.8,1.0,1.2,0.0,2.5,0.0,0.5,0.0,0.0,0.0,2.5,0.0,1.5,0.0,0.0,1.5,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
Cellulitis,1.5,0.0,0.0,0.0,1.2,0.0,0.5,0.8,0.0,0.0,1.8,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
Mononucleosis,1.8,0.5,0.3,0.0,1.5,0.5,1.5,2.0,0.0,0.0,0.8,0.5,0.0,0.0,0.0,1.8,0.8,0.0,0.5,0.5,2.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
Rotavirus,0.5,0.0,0.0,0.0,0.3,0.0,0.3,0.5,0.0,0.0,0.0,1.5,2.5,0.0,0.0,0.0,1.8,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
Pinworms,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.3,0.0,0.0,0.0,0.0,0.0,1.5,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
"""

@st.cache_data
def load_data():
    from io import StringIO
    df = pd.read_csv(StringIO(MEDICAL_DATA))
    # Fill NaN values with 0 for all symptoms
    symptom_cols = [col for col in df.columns if col != "CONDITION"]
    df[symptom_cols] = df[symptom_cols].fillna(0)
    return df

def calculate_age_risk_factor(age):
    """Calculate risk factor based on age (higher risk for infants and immunocompromised)"""
    if age < 3: return 1.5  # Higher weight for infants
    elif age < 12: return 1.2  # Moderate weight for young children
    else: return 1.0  # Standard weight for older children

def apply_clinical_overrides(prediction, symptoms, age):
    """Apply clinical rules to override model predictions when specific patterns are detected"""
    # Meningitis override
    if "NECK_STIFFNESS" in symptoms and "FEVER" in symptoms and "PHOTOPHOBIA" in symptoms and age < 5:
        return "Meningitis (clinical override)", 0.95
    
    # Pertussis pattern
    if "COUGH_PAROXYSMAL" in symptoms and "COUGH_POST_TUSSIVE" in symptoms:
        return "Pertussis (clinical override)", 0.9
        
    # Kawasaki criteria
    if "FEVER" in symptoms and "STRAWBERRY_TONGUE" in symptoms and "RASH" in symptoms and age < 5:
        return "Kawasaki Disease (clinical override)", 0.85
    
    # Scarlet fever
    if "STRAWBERRY_TONGUE" in symptoms and "SORE_THROAT" in symptoms and "RASH" in symptoms:
        return "Scarlet Fever (clinical override)", 0.85
    
    # Measles
    if "KOPLIK_SPOTS" in symptoms and "FEVER" in symptoms and "RASH" in symptoms:
        return "Measles (clinical override)", 0.9
    
    return prediction, None

def find_nearby_doctors(lat, lon, radius=5000):
    """
    Find nearby doctors and pediatricians using Overpass API
    Returns a DataFrame with name, address, and coordinates
    """
    overpass_url = "https://overpass-api.de/api/interpreter"
    
    # Query for doctors and pediatricians
    #pediatricians checker
    query = f"""
    [out:json];
    (
      node["amenity"="doctors"](around:{radius},{lat},{lon});
      node["amenity"="clinic"](around:{radius},{lat},{lon});
      node["healthcare"="doctor"](around:{radius},{lat},{lon});
      node["healthcare"="pediatrician"](around:{radius},{lat},{lon}); 
    );
    out center;
    """
    
    try:
        response = requests.get(overpass_url, params={'data': query})
        response.raise_for_status()
        data = response.json()
        
        doctors = []
        for element in data['elements']:
            name = element.get('tags', {}).get('name', 'Unknown')
            address = element.get('tags', {}).get('addr:full', 
                      element.get('tags', {}).get('addr:street', 'Address not available'))
            specialty = element.get('tags', {}).get('healthcare:speciality', 'General Practitioner')
            
            # Get coordinates
            if 'lat' in element and 'lon' in element:
                lat = element['lat']
                lon = element['lon']
            elif 'center' in element:
                lat = element['center']['lat']
                lon = element['center']['lon']
            else:
                continue
                
            doctors.append({
                'name': name,
                'address': address,
                'specialty': specialty,
                'latitude': lat,
                'longitude': lon
            })
            
        return pd.DataFrame(doctors)
    
    except Exception as e:
        st.error(f"Error fetching nearby doctors: {e}")
        return pd.DataFrame()

def show_nearby_doctors():
    """Show interface for finding nearby doctors"""
    with st.expander("🚑 Find Nearby Doctors & Pediatricians", expanded=False):
        st.write("Locate nearby healthcare providers based on your location")
        
        # Location input options
        location_method = st.radio("Select location method:", 
                                 ["Use my current location", "Enter address manually"])
        
        if location_method == "Use my current location":
            # Note: In a real app, you would use the browser's geolocation API
            # This is a simplified version for demonstration
            lat = st.number_input("Latitude", value=40.7128, format="%.6f")
            lon = st.number_input("Longitude", value=-74.0060, format="%.6f")
        else:
            address = st.text_input("Enter full address:")
            if address:
                geolocator = Nominatim(user_agent="pediatric_symptom_checker")
                try:
                    location = geolocator.geocode(address)
                    if location:
                        lat, lon = location.latitude, location.longitude
                        st.success(f"Found location: {location.address}")
                    else:
                        st.warning("Could not find location. Using default coordinates.")
                        lat, lon = 40.7128, -74.0060  # Default to NYC
                except Exception as e:
                    st.error(f"Geocoding error: {e}")
                    lat, lon = 40.7128, -74.0060
        
        search_radius = st.slider("Search radius (meters)", 500, 10000, 2000)
        
        if st.button("Find Nearby Doctors", key="find_doctors"):
            with st.spinner("Searching for nearby doctors..."):
                doctors_df = find_nearby_doctors(lat, lon, search_radius)
                
                if not doctors_df.empty:
                    st.success(f"Found {len(doctors_df)} doctors/clinics nearby")
                    
                    # Create map centered at user's location
                    m = folium.Map(location=[lat, lon], zoom_start=13)
                    
                    # Add marker for user's location
                    folium.Marker(
                        [lat, lon],
                        popup="Your Location",
                        icon=folium.Icon(color="blue", icon="user")
                    ).add_to(m)
                    
                    # Add markers for each doctor
                    for idx, row in doctors_df.iterrows():
                        popup_text = f"""
                        <b>{row['name']}</b><br>
                        <i>{row['specialty']}</i><br>
                        {row['address']}
                        """
                        
                        icon_color = "green" if "pediatric" in row['specialty'].lower() else "red"
                        
                        folium.Marker(
                            [row['latitude'], row['longitude']],
                            popup=popup_text,
                            icon=folium.Icon(color=icon_color, icon="medkit")
                        ).add_to(m)
                    
                    # Display the map
                    folium_static(m)
                    
                    # Show the data in a table
                    st.subheader("Nearby Healthcare Providers")
                    st.dataframe(doctors_df[['name', 'specialty', 'address']])
                else:
                    st.warning("No doctors found in the specified area. Try increasing the search radius.")

def create_pdf_report(patient_info, symptoms, prediction, probabilities, red_flags, recommendations):
    """Create a PDF report of the symptom analysis"""
    pdf = FPDF()
    pdf.add_page()
    
    # Set font for the title
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Pediatric Symptom Checker Report", ln=True, align='C')
    pdf.ln(10)
    
    # Add date and time
    pdf.set_font("Arial", '', 10)
    pdf.cell(0, 10, f"Report generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
    pdf.ln(5)
    
    # Patient Information section
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Patient Information", ln=True)
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, f"Age: {patient_info['age']} months", ln=True)
    pdf.cell(0, 10, f"Medical History: {', '.join(patient_info['medical_history']) if patient_info['medical_history'] else 'None'}", ln=True)
    pdf.ln(5)
    
    # Symptoms section
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Reported Symptoms", ln=True)
    pdf.set_font("Arial", '', 12)
    for symptom, details in symptoms.items():
        pdf.cell(0, 10, f"- {symptom.replace('_', ' ').title()}: Severity {details['value']:.1f} (Weight {details['weight']:.1f})", ln=True)
    pdf.ln(5)
    
    # Diagnosis section
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Diagnosis", ln=True)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, f"Most likely condition: {prediction}", ln=True)
    pdf.ln(3)
    
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, "Top Possible Conditions:", ln=True)
    for i, (condition, prob) in enumerate(probabilities.items(), 1):
        pdf.cell(0, 10, f"{i}. {condition}: {prob:.1%}", ln=True)
    pdf.ln(5)
    
    # Red Flags section
    if red_flags:
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "Red Flags Identified", ln=True)
        pdf.set_font("Arial", '', 12)
        for flag in red_flags:
            pdf.cell(0, 10, f"- {flag}", ln=True)
        pdf.ln(5)
    
    # Recommendations section
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Recommended Actions", ln=True)
    pdf.set_font("Arial", '', 12)
    for rec in recommendations:
        pdf.multi_cell(0, 10, rec)
    pdf.ln(5)
    
    # Disclaimer
    pdf.set_font("Arial", 'I', 10)
    pdf.multi_cell(0, 10, "Disclaimer: This report is generated by an AI system and is not a substitute for professional medical advice. Always consult with a qualified healthcare provider for diagnosis and treatment.")
    
    return pdf.output(dest='S').encode('latin1')

def get_recommendations(prediction, age, medical_history):
    """Generate recommendations based on the prediction"""
    recommendations = []
    
    if "Meningitis" in prediction:
        recommendations.append("""
        EMERGENCY: Seek immediate medical attention
        - This is a medical emergency requiring IV antibiotics
        - Go to nearest ER immediately
        - Do not wait for symptoms to worsen
        """)
    elif "Epiglottitis" in prediction:
        recommendations.append("""
        EMERGENCY: Do not examine throat
        - Risk of complete airway obstruction
        - Keep child calm and upright
        - Call emergency services immediately
        """)
    elif prediction in ["Bronchiolitis", "Pneumonia", "Dehydration"]:
        recommendations.append("""
        Urgent: Contact your pediatrician within 4-6 hours
        - Monitor respiratory rate closely
        - Keep child hydrated
        - Watch for signs of worsening distress
        """)
    elif prediction in ["Influenza (Flu)", "Strep Throat", "Pertussis"]:
        recommendations.append("""
        Contact your pediatrician within 24 hours
        - Rest and fluids
        - Monitor fever pattern
        - Watch for complications
        - May need specific testing/treatment
        """)
    else:
        recommendations.append("""
        Monitor at home
        - Symptomatic treatment as needed
        - Contact doctor if symptoms worsen or persist >3 days
        - Ensure adequate hydration
        - Watch for new symptoms
        """)
    
    # Age-specific recommendations
    if age < 6:
        recommendations.append("For infants under 6 months, always consult a doctor for any significant symptoms")
    
    if "Immunocompromised" in medical_history:
        recommendations.append("Immunocompromised children may need earlier evaluation for fever or infection")
    
    return recommendations

def main():
    st.set_page_config(page_title="Pediatric Symptom Checker", page_icon="👶", layout="wide")
    st.title("👶 Pediatric Symptom Checker")
    
    # Load data
    df = load_data()
    
    # Get all available symptoms from dataset
    all_symptoms = [col for col in df.columns if col != "CONDITION"]
    
    # Age input
    with st.expander("Patient Information", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("Age (months)", min_value=0, max_value=216, value=24, step=1)
        with col2:
            medical_history = st.multiselect(
                "Medical History (select all that apply)",
                options=["Asthma", "Diabetes", "Heart Condition", "Immunocompromised", "Prematurity"],
                default=[]
            )
    
    # Step 1: Primary symptom selection
    with st.expander("Step 1: Select main symptoms", expanded=True):
        primary_symptoms = st.multiselect(
            "What symptoms is your child experiencing?",
            options=all_symptoms,
            placeholder="Select symptoms..."
        )
    
    # Step 2: Detailed symptom questions
    symptom_details = {}
    if primary_symptoms:
        with st.expander("Step 2: Provide symptom details", expanded=True):
            for symptom in primary_symptoms:
                if symptom in SYMPTOM_DEFINITIONS:
                    st.subheader(f"Details about {symptom.lower().replace('_', ' ')}")
                    
                    symptom_weight = 1.0  # Base weight
                    
                    for question in SYMPTOM_DEFINITIONS[symptom]["follow_up"]:
                        response = None
                        if question["type"] == "radio":
                            response = st.radio(
                                question["question"],
                                options=question["options"],
                                key=f"{symptom}_{question['question']}"
                            )
                        elif question["type"] == "selectbox":
                            response = st.selectbox(
                                question["question"],
                                options=question["options"],
                                key=f"{symptom}_{question['question']}"
                            )
                        elif question["type"] == "checkbox":
                            response = st.multiselect(
                                question["question"],
                                options=question["options"],
                                key=f"{symptom}_{question['question']}"
                            )
                        
                        if response:
                            if isinstance(response, list):  # For checkbox questions
                                for item in response:
                                    symptom_weight *= question["weights"][item]
                            else:  # For radio/selectbox
                                symptom_weight *= question["weights"][response]
                    
                    symptom_details[symptom] = {
                        "value": 1.0,  # Base value
                        "weight": symptom_weight
                    }
                    
                    # Show clinical notes if available
                    if "note" in SYMPTOM_DEFINITIONS[symptom]:
                        st.info(SYMPTOM_DEFINITIONS[symptom]["note"])
                else:
                    # For symptoms without follow-up questions
                    severity = st.slider(
                        f"Severity of {symptom.lower().replace('_', ' ')}",
                        min_value=0.1,
                        max_value=3.0,
                        value=1.0,
                        step=0.1,
                        key=symptom
                    )
                    symptom_details[symptom] = {
                        "value": severity,
                        "weight": 1.0
                    }
    
    # Initialize session state for prediction results
    if 'prediction_results' not in st.session_state:
        st.session_state.prediction_results = None
    
    # Step 3: Predict
    if st.button("Analyze Symptoms", type="primary", use_container_width=True):
        if not primary_symptoms:
            st.warning("Please select at least one symptom")
            return
        
        # Prepare features (only numerical columns)
        numerical_cols = [col for col in df.columns if col != "CONDITION"]
        X = df[numerical_cols]
        y = df["CONDITION"]
        
        # Train model - using GradientBoosting for better performance
        model = GradientBoostingClassifier(
            n_estimators=200,
            learning_rate=0.1,
            max_depth=4,
            min_samples_leaf=3,
            random_state=42
        )
        model.fit(X, y)
        
        # Prepare input features
        input_features = {col: 0.0 for col in numerical_cols}
        
        # Apply symptom weights and age factor
        age_factor = calculate_age_risk_factor(age)
        for symptom, details in symptom_details.items():
            if symptom in input_features:
                input_features[symptom] = details["value"] * details["weight"] * age_factor
        
        # Additional weight for concerning medical history
        if "Immunocompromised" in medical_history:
            for symptom in input_features:
                if input_features[symptom] > 0:
                    input_features[symptom] *= 1.5
        
        # Convert to DataFrame
        input_df = pd.DataFrame([input_features])[numerical_cols]
        
        # Make prediction
        prediction = model.predict(input_df)[0]
        probabilities = model.predict_proba(input_df)[0]
        
        # Apply clinical overrides
        override_prediction, override_prob = apply_clinical_overrides(prediction, primary_symptoms, age)
        if override_prediction:
            prediction = override_prediction
        
        # Get top 5 conditions with probabilities
        prob_df = pd.DataFrame({
            "Condition": model.classes_,
            "Probability": probabilities
        }).sort_values("Probability", ascending=False).head(5)
        
        # Highlight overridden condition if applicable
        if override_prediction:
            prob_df.loc[prob_df['Condition'] == override_prediction.split(' (')[0], 'Probability'] = override_prob
        
        # Get red flags
        red_flags = []
        for symptom in primary_symptoms:
            if symptom in SYMPTOM_DEFINITIONS and "red_flags" in SYMPTOM_DEFINITIONS[symptom]:
                red_flags.extend(SYMPTOM_DEFINITIONS[symptom]["red_flags"])
        
        # Age-specific red flags
        if age < 3 and "FEVER" in primary_symptoms:
            red_flags.append("Fever in infants <3 months requires immediate evaluation")
            
        if age < 6 and "COUGH" in primary_symptoms and "WHEEZING" in primary_symptoms:
            red_flags.append("Wheezing in infants <6 months may indicate serious illness")
            
        if "PETECHIAL/PURPURIC" in primary_symptoms and "FEVER" in primary_symptoms:
            red_flags.append("Petechial rash with fever may indicate meningococcemia - seek IMMEDIATE care")
        
        # Get recommendations
        recommendations = get_recommendations(prediction, age, medical_history)
        
        # Store results in session state
        st.session_state.prediction_results = {
            "prediction": prediction,
            "probabilities": dict(zip(prob_df['Condition'], prob_df['Probability'])),
            "red_flags": red_flags,
            "recommendations": recommendations,
            "patient_info": {
                "age": age,
                "medical_history": medical_history
            },
            "symptoms": symptom_details
        }
    
    # Display results if available
    if st.session_state.prediction_results:
        results = st.session_state.prediction_results
        
        # Create PDF report
        pdf_report = create_pdf_report(
            results['patient_info'],
            results['symptoms'],
            results['prediction'],
            results['probabilities'],
            results['red_flags'],
            results['recommendations']
        )
        
        # Add download button at the top right
        col1, col2 = st.columns([4, 1])
        with col1:
            st.success(f"### Most likely condition: **{results['prediction']}**")
        with col2:
            st.download_button(
                label="📄 Download Report",
                data=pdf_report,
                file_name=f"pediatric_symptom_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        
        # Display results in two columns
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # Show probabilities
            st.subheader("Top Possible Conditions")
            prob_df = pd.DataFrame({
                "Condition": results['probabilities'].keys(),
                "Probability": results['probabilities'].values()
            }).sort_values("Probability", ascending=False)
            
            # Format probabilities with colors
            def color_probs(val):
                color = 'red' if val > 0.7 else 'orange' if val > 0.3 else 'green'
                return f'color: {color}; font-weight: bold'
            
            st.dataframe(
                prob_df.style.format({"Probability": "{:.2%}"})
                      .applymap(color_probs, subset=['Probability']),
                hide_index=True
            )
        
        with col2:
            # Show red flags
            if results['red_flags']:
                st.subheader("⚠️ Red Flags to Watch For")
                for flag in results['red_flags']:
                    st.error(f"• {flag}")
            else:
                st.subheader("ℹ️ No Urgent Red Flags")
                st.info("No urgent red flags identified based on current symptoms")
            
            # Show recommendations
            st.subheader("ℹ️ Recommended Actions")
            for rec in results['recommendations']:
                st.warning(rec)
    
    # Show the nearby doctors feature (always visible)
    show_nearby_doctors()

if __name__ == "__main__":
    main()