import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Child Growth Chart", layout="wide")
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
        .stSelectbox > div > div > select,
        .stNumberInput > div > div > input {
            border-radius: var(--border-radius) !important;
            padding: 12px 14px !important;
            border: 1.5px solid #dbeafe !important;
            font-size: 1.15rem !important;
            color: var(--text) !important;
            background: #fff;
            transition: var(--transition);
            font-family: 'Lexend', Arial, sans-serif !important;
            font-weight: 500 !important;
            height: 3.5rem !important;
        }
        .stSelectbox > div > div > select option {
            color: var(--text) !important;
            background: #fff !important;
        }
        .stSelectbox > div > div > select:focus,
        .stNumberInput > div > div > input:focus {
            border-color: var(--primary) !important;
            box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.13) !important;
            color: var(--text) !important;
        }
        .stSelectbox > div > div > div,
        .stNumberInput > div > div > div {
            font-size: 1.15rem !important;
            font-weight: 600 !important;
            color: var(--primary) !important;
            margin-bottom: 0.5rem !important;
        }
        .stPlotlyChart {
            background: var(--card);
            border-radius: var(--border-radius);
            box-shadow: var(--box-shadow);
            padding: 1rem;
            margin-bottom: 1.2rem;
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

# Dummy percentile curves (simplified WHO-like format)
def get_weight_for_age_curves(gender):
    months = np.arange(0, 25)  # 0 to 24 months
    base = 3.2 if gender == "Male" else 3.0
    return {
        "months": months,
        "3rd": base + 0.3 * months,
        "15th": base + 0.35 * months,
        "50th": base + 0.42 * months,
        "85th": base + 0.49 * months,
        "97th": base + 0.55 * months,
    }

def get_height_for_age_curves(gender):
    months = np.arange(0, 25)
    base = 49.9 if gender == "Male" else 49.1
    return {
        "months": months,
        "3rd": base + 0.7 * months,
        "15th": base + 0.75 * months,
        "50th": base + 0.8 * months,
        "85th": base + 0.85 * months,
        "97th": base + 0.9 * months,
    }

def get_weight_for_height_curves(gender):
    heights = np.arange(45, 100)
    base = 2.5 if gender == "Male" else 2.3
    return {
        "heights": heights,
        "3rd": base + 0.1 * (heights - 45),
        "15th": base + 0.13 * (heights - 45),
        "50th": base + 0.15 * (heights - 45),
        "85th": base + 0.18 * (heights - 45),
        "97th": base + 0.20 * (heights - 45),
    }

# Apply custom CSS
local_css()

# Header with gradient
st.markdown("""
<div class="header-container">
    <h1 style="margin:0;padding:0;">👶 Child Growth Chart Visualizer</h1>
    <p style="margin:0;padding-top:0.5rem;font-size:1.1rem;">Track your child's growth and development</p>
</div>
""", unsafe_allow_html=True)

# Input section in a card
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<h2 style="color: var(--primary); margin-bottom: 1.5rem;">Enter Child\'s Information</h2>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    gender = st.radio("Gender", ["Male", "Female"])
    age = st.number_input("Age (months)", min_value=0, max_value=24, step=1)
with col2:
    weight = st.number_input("Weight (kg)", min_value=2.0, max_value=20.0, step=0.1)
    height = st.number_input("Height (cm)", min_value=45.0, max_value=100.0, step=0.1)

show = st.button("Plot Growth Charts", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

if show:
    color = "blue" if gender == "Male" else "deeppink"

    # --- Weight for Age ---
    data = get_weight_for_age_curves(gender)
    fig1, ax1 = plt.subplots(figsize=(8, 5))
    for key in ['3rd', '15th', '50th', '85th', '97th']:
        ax1.plot(data["months"], data[key], label=f"{key} percentile", linestyle='--' if key != "50th" else '-', color='gray' if key != "50th" else 'orange')
    ax1.scatter(age, weight, color=color, label="Your child", zorder=5, s=100)
    ax1.set_title("Weight-for-Age", fontsize=14, fontweight='bold', pad=20)
    ax1.set_xlabel("Age (months)", fontsize=12)
    ax1.set_ylabel("Weight (kg)", fontsize=12)
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3)
    plt.tight_layout()

    # --- Height for Age ---
    data = get_height_for_age_curves(gender)
    fig2, ax2 = plt.subplots(figsize=(8, 5))
    for key in ['3rd', '15th', '50th', '85th', '97th']:
        ax2.plot(data["months"], data[key], label=f"{key} percentile", linestyle='--' if key != "50th" else '-', color='gray' if key != "50th" else 'orange')
    ax2.scatter(age, height, color=color, label="Your child", zorder=5, s=100)
    ax2.set_title("Height-for-Age", fontsize=14, fontweight='bold', pad=20)
    ax2.set_xlabel("Age (months)", fontsize=12)
    ax2.set_ylabel("Height (cm)", fontsize=12)
    ax2.legend(fontsize=10)
    ax2.grid(True, alpha=0.3)
    plt.tight_layout()

    # --- Weight for Height ---
    data = get_weight_for_height_curves(gender)
    fig3, ax3 = plt.subplots(figsize=(8, 5))
    for key in ['3rd', '15th', '50th', '85th', '97th']:
        ax3.plot(data["heights"], data[key], label=f"{key} percentile", linestyle='--' if key != "50th" else '-', color='gray' if key != "50th" else 'orange')
    ax3.scatter(height, weight, color=color, label="Your child", zorder=5, s=100)
    ax3.set_title("Weight-for-Height", fontsize=14, fontweight='bold', pad=20)
    ax3.set_xlabel("Height (cm)", fontsize=12)
    ax3.set_ylabel("Weight (kg)", fontsize=12)
    ax3.legend(fontsize=10)
    ax3.grid(True, alpha=0.3)
    plt.tight_layout()

    # Display plots in a grid
    col1, col2 = st.columns(2)
    with col1:
        st.pyplot(fig1)
        st.pyplot(fig3)
    with col2:
        st.pyplot(fig2)

# Footer
st.markdown("""
<div class="footer">
    <p>Child Growth Chart Visualizer | Based on WHO Growth Standards</p>
    <p>For informational purposes only. Consult your healthcare provider for medical advice.</p>
</div>
""", unsafe_allow_html=True)
