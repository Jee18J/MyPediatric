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

# Custom CSS for modern UI
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
        .card {
            background: var(--card);
            border-radius: var(--border-radius);
            box-shadow: var(--box-shadow);
            padding: 1.5rem 1.5rem 1.2rem 1.5rem;
            margin-bottom: 1.2rem;
            border: 1px solid #e3eaf3;
            font-family: 'Lexend', Arial, sans-serif !important;
            font-weight: 500 !important;
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
        .stTextInput input, .stTextArea textarea, .stSelectbox select {
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
        .stTextInput input:focus, .stTextArea textarea:focus, .stSelectbox select:focus {
            border-color: var(--primary) !important;
            box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.13) !important;
        }
        .stChatMessage {
            background: var(--card);
            border-radius: var(--border-radius);
            padding: 1.5rem;
            margin: 0.5rem 0;
            box-shadow: var(--box-shadow);
            border: 1px solid #e3eaf3;
            font-family: 'Lexend', Arial, sans-serif !important;
        }
        .stChatMessage.user {
            background-color: rgba(37, 99, 235, 0.05);
            border-left: 4px solid var(--primary);
        }
        .stChatMessage.assistant {
            background-color: rgba(34, 197, 94, 0.05);
            border-left: 4px solid var(--accent);
        }
        .stRadio [role="radiogroup"] {
            gap: 15px;
            margin-bottom: 1rem;
        }
        .stRadio [role="radio"] {
            padding: 8px 16px;
            border-radius: var(--border-radius);
            border: 1.5px solid #dbeafe;
            font-family: 'Lexend', Arial, sans-serif !important;
            font-weight: 500 !important;
        }
        .stRadio [role="radio"][aria-checked="true"] {
            background-color: var(--primary);
            color: white;
            border-color: var(--primary);
        }
        .footer {
            text-align: center;
            padding: 1.5rem;
            color: var(--text-light);
            font-size: 0.95rem;
            font-family: 'Lexend', Arial, sans-serif !important;
        }
        @media (max-width: 768px) {
            .header-container {
                padding: 1.5rem 0.5rem;
            }
            .card {
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

# Display chat messages with enhanced styling
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="👨‍⚕️" if message["role"] == "assistant" else "👤"):
        st.markdown(message["content"])

# Function to process voice input
def voice_input():
    recognizer = sr.Recognizer()
    with st.status("🎤 Listening... Speak now", expanded=True) as status:
        try:
            with sr.Microphone() as source:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                prompt = recognizer.recognize_google(audio)
                status.update(label="✅ Voice captured", state="complete", expanded=False)
                st.success(f"You said: {prompt}")
                return prompt
        except Exception as e:
            st.error(f"Error accessing microphone: {e}")
            return None

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
        
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)
        
        # Generate response from Gemini
        with st.chat_message("assistant", avatar="👨‍⚕️"):
            message_placeholder = st.empty()
            full_response = ""
            with st.spinner("Analyzing your question..."):
                try:
                    # Include medical terms in the prompt to Gemini for better context
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
                # Extract medical terms using LLM (handles tokenization)
                medical_terms, tokenized_text = extract_medical_terms(prompt)
                
                
                st.info(f"Extracted Medical Terms: {', '.join(medical_terms) if medical_terms else 'None'}")
                
                # Add user message to chat history
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("user", avatar="👤"):
                    st.markdown(prompt)
                
                # Generate response from Gemini
                with st.chat_message("assistant", avatar="👨‍⚕️"):
                    with st.spinner("Analyzing your question..."):
                        try:
                            enhanced_prompt = f"Original query: {prompt}\nIdentified medical terms: {', '.join(medical_terms)}"
                            response = model.generate_content(enhanced_prompt)
                            st.markdown(response.text)
                            st.session_state.messages.append({"role": "assistant", "content": response.text})
                        except Exception as e:
                            st.error(f"Error: {str(e)}")

# Navigation button
st.markdown("---")
if st.button("Detailed Symptom Checker", type="primary", use_container_width=True):
    st.switch_page("pages/trial.py")

# Footer
st.markdown("""
<div class="footer">
    <p>This tool is for informational purposes only and does not provide medical advice.</p>
    <p>Always consult a qualified healthcare provider for diagnosis and treatment.</p>
</div>
""", unsafe_allow_html=True)








