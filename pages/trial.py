import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.pipeline import Pipeline
import requests
import folium
from streamlit_folium import folium_static
from geopy.geocoders import Nominatim
from fpdf import FPDF
import base64
from datetime import datetime
import time
import random


# Custom CSS for modern UI
def local_css():
    st.markdown("""
    <style>
        /* Import Lexend Medium font */
        @import url('https://fonts.googleapis.com/css2?family=Lexend:wght@500&display=swap');
        html, body, [class*="stApp"] {
            font-family: 'Lexend', Arial, sans-serif !important;
            font-weight: 500 !important;
            font-size: 1.08rem;
            color: #22304a;
        }
        /* Highlight section headings (expander/step titles/section-title class) */
        section[data-testid="stExpander"] > div > label,
        div[role="heading"]:has(> .emoji),
        .section-title,
        .stMarkdown h3,
        .stMarkdown h2 {
            font-size: 2rem !important;
            font-weight: 700 !important;
            color: var(--primary) !important;
            margin-bottom: 0.5rem !important;
            letter-spacing: 0.01em;
            line-height: 1.2;
        }
        /* General card style for all major sections and expanders */
        .card, .section-card,
        section[data-testid="stExpander"],
        div[data-testid="stExpander"],
        .st-expander, .streamlit-expander,
        .stMarkdown > div, .stMarkdown > p {
            background: #fff !important;
            border-radius: 18px !important;
            box-shadow: 0 4px 24px rgba(37, 99, 235, 0.10) !important;
            padding: 1.5rem 1.5rem 1.2rem 1.5rem !important;
            margin-bottom: 1.5rem !important;
            border: 1px solid #e3eaf3 !important;
        }
        /* Remove card styling from horizontal rules and their containers */
        .stMarkdown > hr,
        .stMarkdown > div:has(> hr),
        .stMarkdown > p:has(> hr),
        .stMarkdown > div:empty,
        .stMarkdown > p:empty {
            background: none !important;
            box-shadow: none !important;
            border: none !important;
            padding: 0 !important;
            margin: 0.5rem 0 !important;
        }
        /* Style the horizontal rule itself for a clean line */
        hr, .stMarkdown hr {
            border: none;
            border-top: 2px solid #e3eaf3;
            margin: 1.2rem 0 1.2rem 0;
            height: 0;
            background: none;
        }
        /* Disclaimer card styling */
        .disclaimer-card {
            background-color:#b45309;
            background: #fff !important;
            border-radius: 18px !important;
            box-shadow: 0 4px 24px rgba(37, 99, 235, 0.10) !important;
            border-left: 6px solid #fbbf24 !important; /* Amber/Yellow */
            padding: 1.5rem 1.5rem 1.2rem 1.5rem !important;
            margin-top: 2.5rem !important;
            margin-bottom: 1.5rem !important;
            border: 1px solid #e3eaf3 !important;
        }
        .disclaimer-title {
            font-size: 1.2rem;
            font-weight: 700;
            color: #b45309; /* Dark amber */
            margin-bottom: 0.7rem;
            letter-spacing: 0.01em;
            text-align: center;
        }
        /* Root Variables - Medical Theme */
        :root {
            --primary: #2563eb;
            --secondary: #38bdf8;
            --accent: #22c55e;
            --background: #f4faff;
            --card: #ffffff;
            --text: #22304a;
            --text-light: #4A5568;
            --warning: #ef4444;
            --success: #22c55e;
            --info: #2563eb;
            --border-radius: 16px;
            --box-shadow: 0 4px 24px rgba(37, 99, 235, 0.08);
            --transition: all 0.2s cubic-bezier(.4,0,.2,1);
        }
        .stApp {
            background-color: var(--background) !important;
        }
        .main .block-container {
            background-color: var(--background);
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        .css-1d391kg {
            background-color: #eaf3fb;
        }
        .header-container {
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            padding: 2.5rem 1.5rem;
            border-radius: var(--border-radius);
            margin-bottom: 2rem;
            box-shadow: var(--box-shadow);
            color: #fff;
            text-align: center;
            position: relative;
            overflow: hidden;
        }
        .header-container h1, .header-container p {
            color: #fff !important;
            font-family: 'Lexend', Arial, sans-serif !important;
            font-weight: 500 !important;
        }
        .card, .streamlit-expanderContent {
            background: var(--card);
            border-radius: var(--border-radius);
            box-shadow: var(--box-shadow);
            padding: 1.5rem 1.5rem 1.2rem 1.5rem;
            margin-bottom: 1.2rem;
            border: 1px solid #e3eaf3;
            font-family: 'Lexend', Arial, sans-serif !important;
            font-weight: 500 !important;
        }
        .streamlit-expanderHeader {
            font-weight: 600;
            color: var(--primary);
            font-size: 1.15rem;
            font-family: 'Lexend', Arial, sans-serif !important;
        }
        .stButton>button {
            background: linear-gradient(90deg, var(--primary) 60%, var(--secondary) 100%);
            color: #fff !important;
            font-size: 1.13rem;
            font-weight: 700;
            border-radius: var(--border-radius);
            padding: 0.85rem 2.2rem;
            border: none;
            box-shadow: 0 2px 8px rgba(37, 99, 235, 0.10);
            transition: var(--transition);
            letter-spacing: 0.01em;
            outline: none !important;
            font-family: 'Lexend', Arial, sans-serif !important;
        }
        .stButton>button:hover, .stButton>button:focus {
            background: linear-gradient(90deg, var(--secondary) 0%, var(--primary) 100%);
            color: #fff !important;
            box-shadow: 0 4px 16px rgba(37, 99, 235, 0.18);
            transform: translateY(-2px) scale(1.03);
        }
        .stButton>button:active {
            transform: scale(0.98);
        }
        .step-indicator {
            font-size: 1.1rem;
            font-weight: 600;
            color: var(--primary);
            font-family: 'Lexend', Arial, sans-serif !important;
        }
        .symptom-card {
            background: var(--card);
            border-radius: var(--border-radius);
            padding: 1.25rem;
            margin-bottom: 1rem;
            box-shadow: 0 2px 8px rgba(37, 99, 235, 0.06);
            border-left: 5px solid var(--accent);
            color: var(--text);
            font-family: 'Lexend', Arial, sans-serif !important;
        }
        .symptom-card h4 {
            font-size: 1.15rem;
            font-weight: 600;
            color: var(--primary);
            font-family: 'Lexend', Arial, sans-serif !important;
        }
        .red-flag {
            background: rgba(239, 68, 68, 0.08);
            border-left: 5px solid var(--warning);
            padding: 1rem;
            margin: 0.5rem 0;
            border-radius: 0 var(--border-radius) var(--border-radius) 0;
            color: var(--warning);
            font-weight: 600;
            font-family: 'Lexend', Arial, sans-serif !important;
        }
        .recommendation {
            background: rgba(34, 197, 94, 0.08);
            border-left: 5px solid var(--success);
            padding: 1rem;
            margin: 0.5rem 0;
            border-radius: 0 var(--border-radius) var(--border-radius) 0;
            color: var(--success);
            font-weight: 600;
            font-family: 'Lexend', Arial, sans-serif !important;
        }
        .info-card {
            background: rgba(37, 99, 235, 0.07);
            border-left: 5px solid var(--info);
            padding: 1rem;
            margin: 0.5rem 0;
            border-radius: 0 var(--border-radius) var(--border-radius) 0;
            color: var(--primary);
            font-weight: 600;
            font-family: 'Lexend', Arial, sans-serif !important;
        }
        .stTextInput input, .stNumberInput input, .stSelectbox select {
            border-radius: var(--border-radius) !important;
            padding: 12px 14px !important;
            border: 1.5px solid #dbeafe !important;
            font-size: 1.08rem;
            color: var(--text);
            background: #fff;
            transition: var(--transition);
            font-family: 'Lexend', Arial, sans-serif !important;
            font-weight: 500 !important;
        }
        .stTextInput input:focus, .stNumberInput input:focus, .stSelectbox select:focus {
            border-color: var(--primary) !important;
            box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.13) !important;
        }
        .stRadio [role="radiogroup"] {
            gap: 15px;
        }
        .stRadio [role="radio"] {
            padding: 8px 16px;
            border-radius: var(--border-radius);
            border: 1.5px solid #dbeafe;
            font-size: 1.05rem;
            color: var(--text);
            transition: var(--transition);
            font-family: 'Lexend', Arial, sans-serif !important;
        }
        .stRadio [role="radio"][aria-checked="true"] {
            background: var(--primary);
            color: #fff;
            border-color: var(--primary);
        }
        .stProgress > div > div > div > div {
            background: var(--accent);
            border-radius: 4px;
        }
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        ::-webkit-scrollbar-track {
            background: #eaf3fb;
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb {
            background: var(--primary);
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: var(--secondary);
        }
        h1, h2, h3, h4, h5, h6 {
            color: var(--primary);
            font-family: 'Lexend', Arial, sans-serif !important;
            font-weight: 500 !important;
        }
        p, li, span, label, div, input, select {
            color: var(--text);
            font-family: 'Lexend', Arial, sans-serif !important;
            font-weight: 500 !important;
        }
        @media (max-width: 768px) {
            .header-container {
                padding: 1.5rem 0.5rem;
            }
            .card, .symptom-card, .streamlit-expanderContent {
                padding: 1rem;
            }
            .stButton>button {
                padding: 0.7rem 1.2rem;
                font-size: 1rem;
            }
        }
    </style>
    """, unsafe_allow_html=True)

# PDF Report Generator
def generate_pdf_report(patient_info, symptoms, prediction, probabilities_df, red_flags, recommendations):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    
    # Header with color
    pdf.set_fill_color(74, 111, 165)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 10, "Pediatric Health Report", 0, 1, 'C', 1)
    pdf.set_font("Arial", '', 10)
    pdf.cell(0, 8, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}", 0, 1, 'C', 1)
    pdf.ln(10)
    
    # Reset colors
    pdf.set_fill_color(255, 255, 255)
    pdf.set_text_color(0, 0, 0)
    
    # Patient Information
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Patient Information", 0, 1)
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 8, f"Age: {patient_info['age']} months", 0, 1)
    pdf.cell(0, 8, f"Medical History: {', '.join(patient_info['medical_history']) if patient_info['medical_history'] else 'None'}", 0, 1)
    pdf.ln(5)
    
    # Symptoms
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Reported Symptoms", 0, 1)
    pdf.set_font("Arial", '', 12)
    for symptom, details in symptoms.items():
        pdf.cell(0, 8, f"- {symptom.replace('_', ' ').title()}: Severity score {details}", 0, 1)
    pdf.ln(5)
    
    # Diagnosis
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Diagnostic Assessment", 0, 1)
    pdf.set_font("Arial", 'B', 12)
    pdf.set_text_color(74, 111, 165)  # Primary color
    pdf.cell(0, 8, f"Most Likely Condition: {prediction}", 0, 1)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", '', 12)
    
    # Probability table
    pdf.cell(0, 8, "Condition Probabilities:", 0, 1)
    col_width = pdf.w / 3
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(col_width, 8, "Condition", 1)
    pdf.cell(col_width, 8, "Probability", 1, 1)
    pdf.set_font("Arial", '', 12)
    
    for _, row in probabilities_df.iterrows():
        pdf.cell(col_width, 8, row['Condition'], 1)
        pdf.cell(col_width, 8, f"{row['Probability']:.2%}", 1, 1)
    pdf.ln(5)
    
    # Red Flags
    if red_flags:
        pdf.set_font("Arial", 'B', 14)
        pdf.set_text_color(255, 107, 107)  # Warning color
        pdf.cell(0, 10, "Red Flags", 0, 1)
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", '', 12)
        for flag in red_flags:
            pdf.cell(0, 8, f"- {flag}", 0, 1)
        pdf.ln(5)
    
    # Recommendations
    if recommendations:
        pdf.set_font("Arial", 'B', 14)
        pdf.set_text_color(72, 219, 180)  # Success color
        pdf.cell(0, 10, "Recommendations", 0, 1)
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", '', 12)
        for rec in recommendations:
            pdf.cell(0, 8, f"- {rec}", 0, 1)
        pdf.ln(5)
    
    # Disclaimer
    pdf.set_font("Arial", 'I', 10)
    pdf.multi_cell(0, 8, "Disclaimer: This report is generated by an AI system and should not replace professional medical advice. Always consult with a qualified healthcare provider for diagnosis and treatment.")
    
    return pdf

# Load and preprocess the dataset
@st.cache_data
def load_data(file_path):
    df = pd.read_csv(file_path)
    symptom_cols = [col for col in df.columns if col != "CONDITION"]
    df[symptom_cols] = df[symptom_cols].fillna(0)
    return df

# Enhanced medical knowledge base with all symptoms from the dataset
SYMPTOM_DEFINITIONS = {
    "FEVER": {
        "follow_up": [
            {"question": "Temperature", "type": "radio",
             "options": ["<100.4°F", "100.4-102.2°F", "102.2-104°F", ">104°F"],
             "weights": {"<100.4°F": 1, "100.4-102.2°F": 2, "102.2-104°F": 3, ">104°F": 4}},
            {"question": "Duration", "type": "selectbox",
             "options": ["<24 hours", "1-3 days", "3-7 days", ">7 days"],
             "weights": {"<24 hours": 1, "1-3 days": 2, "3-7 days": 3, ">7 days": 4}}
        ],
        "red_flags": ["Fever >100.4°F in infants <3 months", "Fever >104°F"],
        "icon": "🌡️"
    },
    "COUGH": {
        "follow_up": [
            {"question": "Type", "type": "selectbox",
             "options": ["Dry", "Productive", "Barking", "Whooping"],
             "weights": {"Dry": 1, "Productive": 2, "Barking": 3, "Whooping": 4}},
            {"question": "Timing", "type": "radio",
             "options": ["Daytime", "Nighttime", "With feeding", "After exercise", "All day"],
             "weights": {"Daytime": 1, "Nighttime": 2, "With feeding": 2, "After exercise": 2, "All day": 3}}
        ],
        "red_flags": ["Whooping sound on inspiration", "Cough causing vomiting"],
        "icon": "🤧"
    },
    "RUNNY_NOSE": {
        "follow_up": [
            {"question": "Severity", "type": "radio",
             "options": ["Mild", "Moderate", "Severe"],
             "weights": {"Mild": 1, "Moderate": 2, "Severe": 3}}
        ],
        "red_flags": ["Nasal discharge with foul odor"],
        "icon": "👃"
    },
    "SNEEZING": {
        "follow_up": [
            {"question": "Frequency", "type": "radio",
             "options": ["Occasional", "Frequent", "Constant"],
             "weights": {"Occasional": 1, "Frequent": 2, "Constant": 3}}
        ],
        "icon": "🤧"
    },
    "DIARRHEA": {
        "follow_up": [
            {"question": "Frequency", "type": "radio",
             "options": ["2-4 loose stools/day", "5-8 loose stools/day", ">8 loose stools/day", "Watery"],
             "weights": {"2-4 loose stools/day": 1, "5-8 loose stools/day": 2, ">8 loose stools/day": 3, "Watery": 3}},
            {"question": "Appearance", "type": "selectbox",
             "options": ["Loose", "Mucoid", "Bloody", "Rice-water"],
             "weights": {"Loose": 1, "Mucoid": 2, "Bloody": 3, "Rice-water": 3}}
        ],
        "red_flags": ["Blood in stool", "Signs of dehydration"],
        "icon": "💩"
    },
    "DEHYDRATION": {
        "follow_up": [
            {"question": "Signs", "type": "checkbox",
             "options": ["Dry mouth", "No tears", "Sunken eyes", "Decreased urine output", "Lethargy"],
             "weights": {"Dry mouth": 1, "No tears": 2, "Sunken eyes": 3, "Decreased urine output": 3, "Lethargy": 4}}
        ],
        "red_flags": ["Severe dehydration signs"],
        "icon": "💧"
    },
    "ABDOMINAL_PAIN": {
        "follow_up": [
            {"question": "Severity", "type": "radio",
             "options": ["Mild", "Moderate", "Severe", "Doubled over"],
             "weights": {"Mild": 1, "Moderate": 2, "Severe": 3, "Doubled over": 4}},
            {"question": "Location", "type": "selectbox",
             "options": ["Generalized", "Upper abdomen", "Lower abdomen", "Right side", "Left side"],
             "weights": {"Generalized": 1, "Upper abdomen": 2, "Lower abdomen": 2, "Right side": 3, "Left side": 3}}
        ],
        "red_flags": ["Severe localized pain", "Pain lasting >6 hours"],
        "icon": "🤢"
    },
    "RASH": {
        "follow_up": [
            {"question": "Appearance", "type": "selectbox",
             "options": ["Macular", "Papular", "Vesicular", "Petechial/Purpuric"],
             "weights": {"Macular": 1, "Papular": 2, "Vesicular": 3, "Petechial/Purpuric": 4}},
            {"question": "Distribution", "type": "checkbox",
             "options": ["Face", "Trunk", "Extremities", "Palms/Soles", "Generalized"],
             "weights": {"Face": 1, "Trunk": 1, "Extremities": 1, "Palms/Soles": 2, "Generalized": 2}}
        ],
        "red_flags": ["Rash with fever", "Non-blanching rash"],
        "icon": "🔴"
    },
    "HEADACHE": {
        "follow_up": [
            {"question": "Severity", "type": "radio",
             "options": ["Mild", "Moderate", "Severe"],
             "weights": {"Mild": 1, "Moderate": 2, "Severe": 3}},
            {"question": "Duration", "type": "selectbox",
             "options": ["<1 hour", "1-4 hours", "4-24 hours", ">24 hours"],
             "weights": {"<1 hour": 1, "1-4 hours": 2, "4-24 hours": 3, ">24 hours": 4}}
        ],
        "red_flags": ["Severe headache with fever", "Headache with neck stiffness"],
        "icon": "🤕"
    },
    "CHEST_PAIN": {
        "follow_up": [
            {"question": "Type", "type": "selectbox",
             "options": ["Sharp", "Dull", "Burning", "Pressure"],
             "weights": {"Sharp": 1, "Dull": 2, "Burning": 2, "Pressure": 3}},
            {"question": "Associated Symptoms", "type": "checkbox",
             "options": ["Shortness of breath", "Palpitations", "Cough", "Fever"],
             "weights": {"Shortness of breath": 2, "Palpitations": 2, "Cough": 1, "Fever": 1}}
        ],
        "red_flags": ["Chest pain with shortness of breath", "Chest pain with palpitations"],
        "icon": "💔"
    },
    "ITCHING": {
        "follow_up": [
            {"question": "Severity", "type": "radio",
             "options": ["Mild", "Moderate", "Severe"],
             "weights": {"Mild": 1, "Moderate": 2, "Severe": 3}},
            {"question": "Location", "type": "checkbox",
             "options": ["Face", "Trunk", "Extremities", "Generalized"],
             "weights": {"Face": 1, "Trunk": 1, "Extremities": 1, "Generalized": 2}}
        ],
        "icon": "🦠"
    },
    "MUSCLE_ACHES": {
        "follow_up": [
            {"question": "Severity", "type": "radio",
             "options": ["Mild", "Moderate", "Severe"],
             "weights": {"Mild": 1, "Moderate": 2, "Severe": 3}},
            {"question": "Duration", "type": "selectbox",
             "options": ["<24 hours", "1-3 days", ">3 days"],
             "weights": {"<24 hours": 1, "1-3 days": 2, ">3 days": 3}}
        ],
        "icon": "💪"
    },
    "NAUSEA": {
        "follow_up": [
            {"question": "Severity", "type": "radio",
             "options": ["Mild", "Moderate", "Severe"],
             "weights": {"Mild": 1, "Moderate": 2, "Severe": 3}},
            {"question": "Associated Symptoms", "type": "checkbox",
             "options": ["Vomiting", "Dizziness", "Headache", "Fever"],
             "weights": {"Vomiting": 2, "Dizziness": 1, "Headache": 1, "Fever": 1}}
        ],
        "icon": "🤢"
    },
    "NECK_STIFFNESS": {
        "follow_up": [
            {"question": "Severity", "type": "radio",
             "options": ["Mild", "Moderate", "Severe"],
             "weights": {"Mild": 1, "Moderate": 2, "Severe": 3}},
            {"question": "Associated Symptoms", "type": "checkbox",
             "options": ["Fever", "Headache", "Photophobia"],
             "weights": {"Fever": 3, "Headache": 2, "Photophobia": 2}}
        ],
        "red_flags": ["Neck stiffness with fever"],
        "icon": "🦴"
    },
    "PHOTOPHOBIA": {
        "follow_up": [
            {"question": "Severity", "type": "radio",
             "options": ["Mild", "Moderate", "Severe"],
             "weights": {"Mild": 1, "Moderate": 2, "Severe": 3}}
        ],
        "red_flags": ["Photophobia with headache and fever"],
        "icon": "👁️"
    },
    "POLYDIPSIA": {
        "follow_up": [
            {"question": "Severity", "type": "radio",
             "options": ["Mild", "Moderate", "Severe"],
             "weights": {"Mild": 1, "Moderate": 2, "Severe": 3}}
        ],
        "icon": "🚰"
    },
    "POLYURIA": {
        "follow_up": [
            {"question": "Severity", "type": "radio",
             "options": ["Mild", "Moderate", "Severe"],
             "weights": {"Mild": 1, "Moderate": 2, "Severe": 3}}
        ],
        "icon": "🚽"
    },
    "RESPIRATORY_DISTRESS": {
        "follow_up": [
            {"question": "Severity", "type": "radio",
             "options": ["Mild", "Moderate", "Severe"],
             "weights": {"Mild": 1, "Moderate": 2, "Severe": 3}},
            {"question": "Signs", "type": "checkbox",
             "options": ["Nasal flaring", "Retractions", "Grunting", "Cyanosis"],
             "weights": {"Nasal flaring": 2, "Retractions": 3, "Grunting": 3, "Cyanosis": 4}}
        ],
        "red_flags": ["Respiratory distress with cyanosis"],
        "icon": "😮‍💨"
    },
    "SORE_THROAT": {
        "follow_up": [
            {"question": "Severity", "type": "radio",
             "options": ["Mild", "Moderate", "Severe"],
             "weights": {"Mild": 1, "Moderate": 2, "Severe": 3}},
            {"question": "Duration", "type": "selectbox",
             "options": ["<24 hours", "1-3 days", ">3 days"],
             "weights": {"<24 hours": 1, "1-3 days": 2, ">3 days": 3}}
        ],
        "icon": "👄"
    },
    "STRIDOR": {
        "follow_up": [
            {"question": "Timing", "type": "radio",
             "options": ["Inspiratory", "Expiratory", "Both"],
             "weights": {"Inspiratory": 2, "Expiratory": 3, "Both": 4}}
        ],
        "red_flags": ["Stridor at rest"],
        "icon": "🎵"
    },
    "VOMITING": {
        "follow_up": [
            {"question": "Frequency", "type": "radio",
             "options": ["1-2 times", "3-5 times", ">5 times"],
             "weights": {"1-2 times": 1, "3-5 times": 2, ">5 times": 3}},
            {"question": "Content", "type": "selectbox",
             "options": ["Food", "Bile", "Blood"],
             "weights": {"Food": 1, "Bile": 2, "Blood": 3}}
        ],
        "red_flags": ["Projectile vomiting", "Vomiting blood"],
        "icon": "🤮"
    },
    "WEIGHT_LOSS": {
        "follow_up": [
            {"question": "Amount", "type": "radio",
             "options": ["<5% body weight", "5-10% body weight", ">10% body weight"],
             "weights": {"<5% body weight": 1, "5-10% body weight": 2, ">10% body weight": 3}},
            {"question": "Duration", "type": "selectbox",
             "options": ["<1 week", "1-4 weeks", ">4 weeks"],
             "weights": {"<1 week": 1, "1-4 weeks": 2, ">4 weeks": 3}}
        ],
        "red_flags": ["Rapid weight loss"],
        "icon": "⚖️"
    },
    "WHEEZING": {
        "follow_up": [
            {"question": "Severity", "type": "radio",
             "options": ["Mild", "Moderate", "Severe"],
             "weights": {"Mild": 1, "Moderate": 2, "Severe": 3}},
            {"question": "Timing", "type": "selectbox",
             "options": ["Occasional", "With activity", "At rest"],
             "weights": {"Occasional": 1, "With activity": 2, "At rest": 3}}
        ],
        "red_flags": ["Wheezing at rest"],
        "icon": "🎵"
    }
}

# Find nearby doctors using Overpass API
def find_nearby_doctors(lat, lon, radius=5000):
    overpass_url = "https://overpass-api.de/api/interpreter"
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
            address = element.get('tags', {}).get('addr:full', element.get('tags', {}).get('addr:street', 'Address not available'))
            specialty = element.get('tags', {}).get('healthcare:speciality', 'General Practitioner')
            lat = element.get('lat', element.get('center', {}).get('lat'))
            lon = element.get('lon', element.get('center', {}).get('lon'))
            if lat and lon:
                doctors.append({'name': name, 'address': address, 'specialty': specialty, 'latitude': lat, 'longitude': lon})
        return pd.DataFrame(doctors)
    except Exception as e:
        st.error(f"Error fetching nearby doctors: {e}")
        return pd.DataFrame()

# Show nearby doctors interface
def show_nearby_doctors():
    with st.expander("🚑 Find Nearby Pediatricians & Clinics", expanded=False):
        st.markdown("### 🔍 Locate healthcare providers near you")
        
        # Initialize default location (New York)
        lat, lon = 40.7128, -74.0060
        
        # Address input section
        address = st.text_input("Enter your full address:", 
                              placeholder="e.g., 123 Main St, City, Country",
                              key="doctor_search_address")
        
        if address:
            geolocator = Nominatim(user_agent="pediatric-symptom-checker")
            try:
                location = geolocator.geocode(address)
                if location:
                    lat, lon = location.latitude, location.longitude
                    st.success(f"Found location: {lat:.4f}, {lon:.4f}")
                else:
                    st.warning("Address not found. Using default location.")
            except Exception as e:
                st.error(f"Geocoding error: {e}")
                st.warning("Using default location.")
        
        search_radius = st.slider("Search radius (meters)", 
                                500, 10000, 2000, 
                                help="Wider radius may show more options")
        
        if st.button("🔍 Search for Doctors", type="primary", use_container_width=True):
            with st.spinner("Searching nearby..."):
                doctors_df = find_nearby_doctors(lat, lon, search_radius)
                
                if not doctors_df.empty:
                    st.success(f"✅ Found {len(doctors_df)} healthcare providers nearby")
                    
                    # Create map
                    m = folium.Map(location=[lat, lon], zoom_start=13, tiles="cartodbpositron")
                    folium.Marker(
                        [lat, lon], 
                        popup="Your Location", 
                        icon=folium.Icon(color="blue", icon="user", prefix="fa")
                    ).add_to(m)
                    
                    # Add doctors
                    for idx, row in doctors_df.iterrows():
                        is_pediatric = "pediatric" in str(row['specialty']).lower()
                        icon_color = "green" if is_pediatric else "red"
                        icon_type = "child" if is_pediatric else "user-md"
                        
                        folium.Marker(
                            [row['latitude'], row['longitude']],
                            popup=f"<b>{row['name']}</b><br><i>{row['specialty']}</i><br>{row['address']}",
                            icon=folium.Icon(color=icon_color, icon=icon_type, prefix="fa")
                        ).add_to(m)
                    
                    # Display map
                    folium_static(m, width=700, height=500)
                    
                    # Show table
                    st.markdown("### 🏥 Nearby Healthcare Providers")
                    st.dataframe(
                        doctors_df[['name', 'specialty', 'address']].rename(columns={
                            'name': 'Name',
                            'specialty': 'Specialty',
                            'address': 'Address'
                        }),
                        hide_index=True,
                        use_container_width=True
                    )
                else:
                    st.warning("No doctors found in this area. Try increasing the search radius.")

# Train the model
@st.cache_resource
def train_model(df):
    df["AGE_FEATURE"] = 0
    df["IMMUNOCOMPROMISED_FEATURE"] = 0
    label_encoder = LabelEncoder()
    df["CONDITION"] = label_encoder.fit_transform(df["CONDITION"])
    X = df.drop(columns=["CONDITION"])
    y = df["CONDITION"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("classifier", RandomForestClassifier(n_estimators=200, max_depth=10, random_state=42))
    ])
    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    return pipeline, label_encoder

# Step indicator component using Streamlit columns
def show_step_indicator(current_step):
    steps = [
        {"title": "Patient Info", "number": 1},
        {"title": "Select Symptoms", "number": 2},
        {"title": "Symptom Details", "number": 3},
        {"title": "Analysis", "number": 4}
    ]


    
    cols = st.columns(len(steps))
    for i, step in enumerate(steps):
        with cols[i]:
            # Determine the step state
            if step["number"] < current_step:
                step_state = "✅"  # Completed
                step_color = "#48dbb4"  # Success color
            elif step["number"] == current_step:
                step_state = "➡️"  # Current
                step_color = "#4a6fa5"  # Primary color
            else:
                step_state = str(step["number"])  # Not started
                step_color = "#e0e0e0"  # Gray
            
            # Create a container for each step
            st.markdown(
                f"""
                <div style="text-align: center; margin-bottom: 10px;">
                    <div style="
                        background-color: {step_color};
                        color: white;
                        width: 30px;
                        height: 30px;
                        border-radius: 50%;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        margin: 0 auto;
                        font-weight: bold;
                    ">{step_state}</div>
                    <div style="font-weight: {'bold' if step['number'] == current_step else 'normal'};">
                        {step['title']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

# Define symptom conflicts
conflicting_symptoms = {
    "FEVER": ["HYPOTHERMIA"],
    "WHEEZING": ["STRIDOR"],
    "STRIDOR": ["WHEEZING"],
    "NECK_STIFFNESS": ["PHOTOPHOBIA"],
    "PHOTOPHOBIA": ["NECK_STIFFNESS"],
    "RESPIRATORY_DISTRESS": ["SORE_THROAT"],
    "VOMITING": ["NAUSEA"],
    # add more conflicts if needed
}

# Helper function to filter options based on conflicts
def filter_conflicting_options(all_options, current_selection, conflicts_dict):
    filtered = []
    for opt in all_options:
        conflicts = conflicts_dict.get(opt, [])
        # Exclude if any conflicting symptom is already selected
        if not any(conflict in current_selection for conflict in conflicts):
            filtered.append(opt)
    return filtered

# Main application
def main():
    st.set_page_config(
        page_title="Pediatric Symptom Checker", 
        page_icon="👶", 
        layout="wide",
        initial_sidebar_state="expanded"
    )
    local_css()
    
    # Header with gradient
    st.markdown("""
    <div class="header-container">
        <h1 style="margin:0;padding:0;">👶 Pediatric Symptom Checker</h1>
        <p style="margin:0;padding-top:0.5rem;font-size:1.1rem;">A smart tool to help parents assess their child's symptoms and get guidance</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Introduction
    st.markdown("""
    <div class="card">
        <p>Welcome to the Pediatric Symptom Checker. This tool helps you evaluate your child's symptoms and provides 
        guidance on possible conditions. Please follow these steps:</p>
        <ol>
            <li>Provide basic information about your child</li>
            <li>Select all symptoms your child is experiencing</li>
            <li>Provide details about each symptom</li>
            <li>Get an assessment with recommendations</li>
        </ol>
        <p><strong>Remember:</strong> This tool doesn't replace professional medical advice.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load data and model
    file_path = "pages/pediatric_dataset_30k.csv"
    df = load_data(file_path)
    model, label_encoder = train_model(df)
    all_symptoms = [col for col in df.columns if col != "CONDITION"]
    
    # Step 1: Patient Information
    with st.expander("👤 Step 1: Patient Information", expanded=True):
        show_step_indicator(1)
        st.markdown("### Tell us about your child")
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input(
                "Age (months)", 
                min_value=0, 
                max_value=216, 
                value=24, 
                step=1,
                help="Child's age in months (0-18 years)"
            )
            
            # Age category indicator
            if age < 12:
                st.info("👶 Infant (0-12 months)")
            elif age < 36:
                st.info("🧒 Toddler (1-3 years)")
            elif age < 60:
                st.info("👦 Preschooler (3-5 years)")
            else:
                st.info("👧 Child (5+ years)")
                
        with col2:
            medical_history = st.multiselect(
                "Medical History (select all that apply)",
                options=["Allergies (Food, Environmental, Medication)", "Asthma", 
                         "Immunocompromised Status", "Prematurity or Neonatal Complications"],
                default=[]
            )
             # Set red flags based on medical history and age
            red_flags = []
            if "Immunocompromised Status" in medical_history:
                red_flags.append("Caution: Child with immunocompromised status.")
            if (age < 12) and ("Asthma" in medical_history):
                red_flags.append("Caution: Children with asthma are more vulnerable.")
            if (age < 3) and ("Allergies (Food, Environmental, Medication)" in medical_history):
                red_flags.append("Caution: Allergies may be more dangerous in infants.")
            
            # if "Immunocompromised" in medical_history:
            #     st.warning("⚠️ Children with compromised immune systems may need special medical attention")
    
    # Step 2: Symptom Selection
    with st.expander("🤒 Step 2: Select Symptoms", expanded=False):
        show_step_indicator(2)
        st.markdown("### What symptoms is your child experiencing?")
        
        # Updated symptom categories with five tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "🌡️ General Symptoms", 
            "🤢 Digestive Symptoms", 
            "🔴 Skin Symptoms", 
            "💨 Respiratory Symptoms", 
            "🧠 Neurological Symptoms"
        ])
        
        with tab1:
            general_symptoms = ["FEVER", "COUGH", "RUNNY_NOSE", "SNEEZING", "CHEST_PAIN", "MUSCLE_ACHES"]
            selected_general = st.multiselect(
                "General symptoms:",
                options=general_symptoms,
                format_func=lambda x: x.replace("_", " ").title(),
                placeholder="Select general symptoms...",
                key="general_symptoms"
            )

        with tab2:
            digestive_symptoms = ["DIARRHEA", "DEHYDRATION", "ABDOMINAL_PAIN", "NAUSEA", "VOMITING", "POLYDIPSIA", "POLYURIA", "WEIGHT_LOSS"]
            selected_digestive = st.multiselect(
                "Digestive symptoms:",
                options=digestive_symptoms,
                format_func=lambda x: x.replace("_", " ").title(),
                placeholder="Select digestive symptoms...",
                key="digestive_symptoms"
            )

        with tab3:
            skin_symptoms = ["RASH", "ITCHING"]
            selected_skin = st.multiselect(
                "Skin symptoms:",
                options=skin_symptoms,
                format_func=lambda x: x.replace("_", " ").title(),
                placeholder="Select skin symptoms...",
                key="skin_symptoms"
            )

        with tab4:
            respiratory_symptoms = ["COUGH", "WHEEZING", "STRIDOR", "RESPIRATORY_DISTRESS"]
            selected_respiratory = st.multiselect(
                "Respiratory symptoms:",
                options=respiratory_symptoms,
                format_func=lambda x: x.replace("_", " ").title(),
                placeholder="Select respiratory symptoms...",
                key="respiratory_symptoms"
            )

        with tab5:
            neurological_symptoms = ["HEADACHE", "NECK_STIFFNESS", "PHOTOPHOBIA"]
            selected_neurological = st.multiselect(
                "Neurological symptoms:",
                options=neurological_symptoms,
                format_func=lambda x: x.replace("_", " ").title(),
                placeholder="Select neurological symptoms...",
                key="neurological_symptoms"
            )

        # Combine all selected symptoms
        primary_symptoms = (selected_general + selected_digestive + selected_skin + 
                            selected_respiratory + selected_neurological)

        if primary_symptoms:
            st.markdown(f"<div class='info-card'>Selected symptoms: {', '.join([s.replace('_', ' ').title() for s in primary_symptoms])}</div>", unsafe_allow_html=True)

        # Check total number of symptoms
        total_symptoms = len(primary_symptoms)
        can_proceed = True
        if total_symptoms > 5:
            st.warning("Please select no more than 5 symptoms.")
            can_proceed = False
    
    # Step 3: Symptom Details
    symptom_details = {}
    if primary_symptoms:
        with st.expander("📝 Step 3: Symptom Details", expanded=False):
            show_step_indicator(3)
            st.markdown("### Provide more details about each symptom")
            progress_bar = st.progress(0)
            total_symptoms = len(primary_symptoms)
            
            for i, symptom in enumerate(primary_symptoms):
                with st.container():
                    icon = SYMPTOM_DEFINITIONS.get(symptom, {}).get("icon", "ℹ️")
                    st.markdown(f"<div class='symptom-card'><h4>{icon} {symptom.replace('_', ' ').title()}</h4></div>", unsafe_allow_html=True)
                    
                    if symptom in SYMPTOM_DEFINITIONS:
                        symptom_score = 0
                        for question in SYMPTOM_DEFINITIONS[symptom]["follow_up"]:
                            if question["type"] == "radio":
                                response = st.radio(
                                    question["question"],
                                    options=question["options"],
                                    key=f"{symptom}_{question['question']}",
                                    horizontal=True
                                )
                                symptom_score += question["weights"][response]
                            elif question["type"] == "selectbox":
                                response = st.selectbox(
                                    question["question"],
                                    options=question["options"],
                                    key=f"{symptom}_{question['question']}"
                                )
                                symptom_score += question["weights"][response]
                            elif question["type"] == "checkbox":
                                response = st.multiselect(
                                    question["question"],
                                    options=question["options"],
                                    key=f"{symptom}_{question['question']}"
                                )
                                for item in response:
                                    symptom_score += question["weights"][item]
                        symptom_details[symptom] = symptom_score
                    else:
                        severity = st.slider(
                            f"Severity of {symptom.replace('_', ' ')}",
                            min_value=0.1, 
                            max_value=3.0, 
                            value=1.0, 
                            step=0.1, 
                            key=symptom,
                            help="1 = Mild, 3 = Severe"
                        )
                        symptom_details[symptom] = severity
                    
                    progress_bar.progress((i + 1) / total_symptoms)
                    if i < total_symptoms - 1:
                        st.divider()
    
    # Step 4: Analysis
    show_step_indicator(4 if primary_symptoms else 3)
    if st.button("🔍 Analyze Symptoms", type="primary", use_container_width=True):
        if not primary_symptoms:
            st.warning("Please select at least one symptom")
            st.stop()
        elif not can_proceed:
            st.error("Too many symptoms selected. Please reduce to 5 or fewer.")
            st.stop()
        else:
            with st.spinner("Analyzing symptoms..."):
                time.sleep(1)
            
            # Prepare input features
            input_features = {col: 0.0 for col in all_symptoms}
            input_features["AGE_FEATURE"] = 3 if age < 3 else (2 if age < 12 else 1)
            input_features["IMMUNOCOMPROMISED_FEATURE"] = 1 if "Immunocompromised" in medical_history else 0
            
            for symptom, score in symptom_details.items():
                if symptom in input_features:
                    input_features[symptom] = score
            
            # Make prediction
            input_df = pd.DataFrame([input_features])
            prediction = model.predict(input_df)[0]
            probabilities = model.predict_proba(input_df)[0]
            prediction = label_encoder.inverse_transform([prediction])[0]

            # red_flags = []
            if age < 3:
                red_flags.append("⚠️ Infants under 3 months are at higher risk for complicating conditions.")
            if "Asthma" in medical_history:
                red_flags.append("⚠️ Caution: Child has a history of asthma.")
            if "Prematurity or Neonatal Complications" in medical_history:
                red_flags.append("⚠️ Caution: Child was born prematurely or had neonatal complications, may need extra observation.")
            if "Allergies (Food, Environmental, Medication)" in medical_history:
                red_flags.append("⚠️ Caution: Child has allergies which may complicate symptoms.")
            
            # Get red flags
            red_flags = []
            for symptom in primary_symptoms:
                if symptom in SYMPTOM_DEFINITIONS and "red_flags" in SYMPTOM_DEFINITIONS[symptom]:
                    red_flags.extend(SYMPTOM_DEFINITIONS[symptom]["red_flags"])
                    
            
            # Generate recommendations
            recommendations = []
            if "Meningitis" in prediction:
                recommendations.append("EMERGENCY: Seek immediate medical attention - This is a medical emergency requiring IV antibiotics.")
            if "Immunocompromised" in medical_history:
                recommendations.append("Children with compromised immune systems should be evaluated earlier for infections.")
            if "FEVER" in primary_symptoms and age < 3:
                recommendations.append("Infants under 3 months with fever should be evaluated by a doctor immediately.")
            if "DEHYDRATION" in primary_symptoms:
                recommendations.append("Ensure adequate fluid intake and monitor for worsening signs of dehydration.")
            if "RESPIRATORY_DISTRESS" in primary_symptoms:
                recommendations.append("Respiratory distress requires immediate medical evaluation.")
            if "STRIDOR" in primary_symptoms:
                recommendations.append("Stridor may indicate airway obstruction - seek medical attention.")
            if "NECK_STIFFNESS" in primary_symptoms:
                recommendations.append("Neck stiffness with fever requires urgent medical evaluation.")

            # Create the DataFrame for top probabilities
            prob_df = pd.DataFrame({
                "Condition": label_encoder.classes_,
                "Probability": probabilities
                }).sort_values("Probability", ascending=False).head(3)
            
            # Display results
            st.markdown("---")
            st.markdown(f"""
            <div class='diagnosis-highlight'>
                <h2 style='text-align:center;margin-bottom:0.5rem;'>Diagnostic Results</h2>
                <h3 style='text-align:center;color:#4a6fa5;margin-top:0;'>Most likely condition: {prediction}</h3>
            </div>
            """, unsafe_allow_html=True)
            
            # Define descriptions for each condition
            condition_descriptions = {
                "Common Cold": "A viral infection causing runny nose, sneezing, and cough.",
                "Influenza": "Flu with fever, body aches, cough, and fatigue.",
                "Bronchiolitis": "Lung infection in infants with breathing difficulty.",
                "Pneumonia": "Lung infection with cough, fever, and difficulty breathing.",
                "Meningitis": "Inflammation of membranes around brain/spinal cord, serious.",
                "Asthma": "Chronic airway inflammation causing wheezing and breathlessness.",
                "Gastroenteritis": "Stomach infection with diarrhea, vomiting, dehydration.",
                "Croup": "Viral infection causing barking cough and breathing issues.",
                "Appendicitis": "Inflammation of appendix, requires urgent care.",
                "Scarlet Fever": "Bacterial infection with rash and sore throat.",
                "Eczema": "Skin condition with itchy rashes.",
                "Type 1 Diabetes": "Autoimmune disease affecting blood sugar regulation."
                }
            def create_condition_html(condition_name):
                description = condition_descriptions.get(condition_name, "No description available.")
                return f"""
                <span style='margin-left:8px; font-size:1.2em; cursor:pointer;' title="{description}">ℹ️</span>
                """
            # Select top 3 conditions
            top_conditions = prob_df['Condition'].head(3).tolist()
            top_probs = prob_df['Probability'].head(3).tolist()
            # Add a heading for clarity
            st.markdown("### Top Possible Conditions:")
            cols = st.columns(3)
            for i, col in enumerate(cols):
                cond = top_conditions[i]
                prob = top_probs[i]
                icon_html = create_condition_html(cond)
                col.markdown(f"**{cond}** {icon_html}", unsafe_allow_html=True)
                col.progress(int(prob * 100))
                col.write(f"{prob:.2%}")
            
            # Red flags
            if red_flags:
                st.markdown("### ⚠️ Red Flags")
                for flag in red_flags:
                    st.markdown(f"""
                    <div class='red-flag'>
                        <p style='margin:0;'><strong>{flag}</strong></p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class='card' style='background-color:#e8f5e9;'>
                    <h4 style='color:#2e7d32;margin:0;'>No urgent red flags identified</h4>
                </div>
                """, unsafe_allow_html=True)
            
            # Recommendations
            if recommendations:
                st.markdown("### Recommended Actions")
                for rec in recommendations:
                    st.markdown(f"""
                    <div class='recommendation'>
                        <p style='margin:0;'>{rec}</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Additional advice based on condition
            st.markdown("### ℹ️ Additional Information")
            if "Common Cold" in prediction:
                st.markdown("""
                <div class='info-card'>
                    <p><strong>For common cold:</strong></p>
                    <ul>
                        <li>Ensure your child gets plenty of rest</li>
                        <li>Use saline nasal drops to relieve congestion</li>
                        <li>Offer warm fluids to soothe throat irritation</li>
                        <li>Use a cool-mist humidifier in the room</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            elif "Gastroenteritis" in prediction:
                st.markdown("""
                <div class='info-card'>
                    <p><strong>For gastroenteritis:</strong></p>
                    <ul>
                        <li>Offer small, frequent amounts of oral rehydration solution</li>
                        <li>Avoid sugary drinks and dairy products</li>
                        <li>Gradually reintroduce bland foods (BRAT diet: bananas, rice, applesauce, toast)</li>
                        <li>Watch for signs of dehydration</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            elif "Asthma" in prediction:
                st.markdown("""
                <div class='info-card'>
                    <p><strong>For asthma:</strong></p>
                    <ul>
                        <li>Use prescribed inhalers as directed</li>
                        <li>Avoid known triggers (dust, pollen, smoke)</li>
                        <li>Seek emergency care if breathing becomes difficult</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            elif "Meningitis" in prediction:
                st.markdown("""
                <div class='info-card'>
                    <p><strong>For suspected meningitis:</strong></p>
                    <ul>
                        <li>This is a medical emergency - seek immediate care</li>
                        <li>Do not wait - go to the nearest emergency department</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            
            # PDF Report
            st.markdown("---")
            st.markdown("### 📄 Download Report")
            pdf = generate_pdf_report(
                patient_info={"age": age, "medical_history": medical_history},
                symptoms=symptom_details,
                prediction=prediction,
                probabilities_df=prob_df,
                red_flags=red_flags,
                recommendations=recommendations
            )
            
            pdf_output = pdf.output(dest='S').encode('latin-1')
            b64 = base64.b64encode(pdf_output).decode()
            href = f"""
            <a href="data:application/octet-stream;base64,{b64}" download="pediatric_health_report.pdf" style='
                display: inline-block;
                background-color: #4a6fa5;
                color: white;
                padding: 12px 24px;
                text-align: center;
                text-decoration: none;
                font-size: 16px;
                margin: 4px 2px;
                cursor: pointer;
                border-radius: 8px;
                border: none;
                transition: all 0.3s ease;
            ' onmouseover="this.style.backgroundColor='#166088'" onmouseout="this.style.backgroundColor='#4a6fa5'">📥 Download Full Medical Report</a>
            """
            st.markdown(href, unsafe_allow_html=True)
    
    # Nearby doctors section
    st.markdown("---")
    show_nearby_doctors()


    st.markdown("---")
    st.markdown("### 👪 Connect with Other Parents")
    st.markdown("Share your experiences and ask questions in our community forum.")
    if st.button("Open Parents Forum", type="secondary", use_container_width=True):
        st.switch_page("pages/chat.py") # This is the key line to switch pages


    st.markdown("---")
    st.markdown("### Growth Chart")
    st.markdown("Understand the growth of your child")
    if st.button("Open Growth Chart", type="secondary", use_container_width=True):
        st.switch_page("pages/growth.py") # This is the key line to switch pages
    
    # Footer
    st.markdown('''
    <div class="disclaimer-card">
        <div class="disclaimer-title">⚠️ <b>Disclaimer</b></div>
        <div>
            <p style="text-align: center;">This tool is for informational purposes only and does not provide medical advice.</p>
            <p style="text-align: center;">Always consult a qualified healthcare provider for diagnosis and treatment.</p>
            <p style="text-align: center; font-size:0.95em; margin-top:1.5em;">Version 1.1.0 | Last updated: 2025-05-12</p>
        </div>
    </div>
    ''', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
