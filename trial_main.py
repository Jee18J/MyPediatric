
import streamlit as st
import google.generativeai as genai
import speech_recognition as sr
from transformers import BertTokenizerFast
from datetime import datetime
import time

# Set page config
st.set_page_config(
    page_title="Pediatric Health Assistant", 
    page_icon="👶",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern UI (copied from trial.py)
def local_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Lexend:wght@500&display=swap');
        html, body, [class*="stApp"] {
            font-family: 'Lexend', Arial, sans-serif !important;
            font-weight: 500 !important;
            font-size: 1.08rem;
            color: #22304a;
        }
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
        hr, .stMarkdown hr {
            border: none;
            border-top: 2px solid #e3eaf3;
            margin: 1.2rem 0 1.2rem 0;
            height: 0;
            background: none;
        }
        .disclaimer-card {
            background: #fff !important;
            border-radius: 18px !important;
            box-shadow: 0 4px 24px rgba(37, 99, 235, 0.10) !important;
            border-left: 6px solid #fbbf24 !important;
            padding: 1.5rem 1.5rem 1.2rem 1.5rem !important;
            margin-top: 2.5rem !important;
            margin-bottom: 1.5rem !important;
            border: 1px solid #e3eaf3 !important;
        }
        .disclaimer-title {
            font-size: 1.2rem;
            font-weight: 700;
            color: #b45309;
            margin-bottom: 0.7rem;
            letter-spacing: 0.01em;
        }
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

# Configure Gemini AI 
genai.configure(api_key="AIzaSyClwCo8aIpV8gieeDQ5HsjiASODhGkxt-0")

# Model configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction="""
You are a helpful and friendly pediatrician chatbot designed to assist parents with common child health concerns.
Your responsibilities:
- Answer questions related to common symptoms in children such as cold, cough, fever, stomach pain, rashes, vomiting, etc.
- Provide general explanations for possible causes in simple and reassuring language.
- Suggest commonly used over-the-counter (OTC) medications, only by generic names (e.g., paracetamol, cetirizine).
- Mention age-appropriateness or dosage ranges when necessary, but avoid giving exact dosages.
- Recommend seeing a pediatrician for persistent, severe, or unclear symptoms.
- Keep answers brief, clear, and non-technical.
- Avoid giving deep medical advice, prescription-level detail, or suggesting specific brands.
Example:
User: My child has had a cough for 3 days.
You: It sounds like your child might have a common cold or viral infection, which often causes cough. Make sure they get enough fluids and rest. You can consider giving a children's cough syrup with a mild antihistamine like cetirizine. If the cough worsens or lasts more than a week, it's best to see a pediatrician.
Always include a gentle reminder to consult a doctor for personalized care.
""",
)

# Load BERT tokenizer
@st.cache_resource
def load_bert_tokenizer():
    tokenizer = BertTokenizerFast.from_pretrained("bert-base-cased")
    return tokenizer

tokenizer = load_bert_tokenizer()

# Function to extract medical terms using LLM
def extract_medical_terms(prompt):
    # First tokenize the prompt
    tokens = tokenizer.tokenize(prompt)
    tokenized_text = tokenizer.convert_tokens_to_string(tokens)
    
    # Send tokenized text to LLM for term extraction
    extraction_prompt = f"""
    Extract ONLY medical terms from this tokenized text: '{tokenized_text}'. 
    Follow these rules:
    1. Return only medical terms separated by commas
    2. Ignore non-medical words
    3. Include symptoms, body parts, conditions
    4. Keep terms in their original form
    Example Output: fever, cough, headache
    """
    
    response = model.generate_content(extraction_prompt)
    medical_terms = [term.strip() for term in response.text.split(",") if term.strip()]
    return medical_terms, tokenized_text  # Return both terms and tokenized text

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm your pediatric health assistant. How can I help?"}
    ]

local_css()

# Header with gradient
st.markdown("""
<div class="header-container">
    <h1 style="margin:0;padding:0;">👶 Pediatric Health Assistant</h1>
    <p style="margin:0;padding-top:0.5rem;font-size:1.1rem;">Get quick pediatric advice for your child's health concerns</p>
</div>
""", unsafe_allow_html=True)

# Introduction card
st.markdown("""
<div class="card">
    <p>This assistant provides general pediatric health information. You can either type your question or use voice input.</p>
    <p><strong>Remember:</strong> This is not a substitute for professional medical advice.</p>
</div>
""", unsafe_allow_html=True)

# Input prompt and chat messages in a card
st.markdown('<div class="card">', unsafe_allow_html=True)

# Options for input: Text or Voice
input_mode = st.radio(
    "Choose your input method:",
    ("Text", "Voice"),
    horizontal=True,
    label_visibility="collapsed"
)

if input_mode == "Text":
    if prompt := st.chat_input("Ask about your child's symptoms..."):
        # Extract medical terms using LLM (which now handles tokenization internally)
        medical_terms, tokenized_text = extract_medical_terms(prompt)
        st.info(f"Extracted Medical Terms: {', '.join(medical_terms) if medical_terms else 'None'}")
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)
        with st.chat_message("assistant", avatar="👨‍⚕️"):
            message_placeholder = st.empty()
            full_response = ""
            with st.spinner("Analyzing your question..."):
                try:
                    enhanced_prompt = f"Original query: {prompt}\nIdentified medical terms: {', '.join(medical_terms)}"
                    response = model.generate_content(enhanced_prompt)
                    for chunk in response.text.split(" "):
                        full_response += chunk + " "
                        time.sleep(0.05)
                        message_placeholder.markdown(full_response + "▌")
                    message_placeholder.markdown(full_response)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    st.error(f"Error: {str(e)}")

elif input_mode == "Voice":
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("🎤 Click to Speak", use_container_width=True):
            prompt = voice_input()
            if prompt:
                medical_terms, tokenized_text = extract_medical_terms(prompt)
                st.info(f"Extracted Medical Terms: {', '.join(medical_terms) if medical_terms else 'None'}")
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("user", avatar="👤"):
                    st.markdown(prompt)
                with st.chat_message("assistant", avatar="👨‍⚕️"):
                    with st.spinner("Analyzing your question..."):
                        try:
                            enhanced_prompt = f"Original query: {prompt}\nIdentified medical terms: {', '.join(medical_terms)}"
                            response = model.generate_content(enhanced_prompt)
                            st.markdown(response.text)
                            st.session_state.messages.append({"role": "assistant", "content": response.text})
                        except Exception as e:
                            st.error(f"Error: {str(e)}")

# Display chat messages with enhanced styling (for initial messages)
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="👨‍⚕️" if message["role"] == "assistant" else "👤"):
        st.markdown(message["content"])

st.markdown('</div>', unsafe_allow_html=True)

# Navigation button
st.markdown("---")
if st.button("Detailed Symptom Checker", type="primary", use_container_width=True):
    st.switch_page("pages/trial.py")

# Disclaimer card
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








