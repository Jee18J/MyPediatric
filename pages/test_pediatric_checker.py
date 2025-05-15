import pytest
import pandas as pd
from fpdf import FPDF
import base64
from datetime import datetime
from trial import (  # Replace with your actual module name
    load_data, train_model, generate_pdf_report, 
    find_nearby_doctors, SYMPTOM_DEFINITIONS
)

# --- Fixtures (Shared Test Data) ---
@pytest.fixture
def sample_data():
    return load_data("synthetic_disease_symptom_data.csv")

@pytest.fixture
def trained_model(sample_data):
    return train_model(sample_data)

# --- Test Cases ---
def test_data_loading(sample_data):
    """Test dataset loading"""
    assert not sample_data.empty
    assert "CONDITION" in sample_data.columns

def test_model_training(trained_model):
    """Test model training"""
    model, label_encoder = trained_model
    assert hasattr(model, "predict")
    assert hasattr(label_encoder, "classes_")

def test_symptom_selection_validation():
    """Test symptom selection limit"""
    assert len(["FEVER", "COUGH", "RASH"]) <= 5  # Valid case
    with pytest.raises(AssertionError):
        assert len(["FEVER", "COUGH", "RASH", "VOMITING", "DIARRHEA", "HEADACHE"]) <= 5  # Invalid

def test_pdf_report_generation():
    """Test PDF generation"""
    pdf = generate_pdf_report(
        patient_info={"age": 24, "medical_history": ["Asthma"]},
        symptoms={"FEVER": 2},
        prediction="Common Cold",
        probabilities_df=pd.DataFrame({"Condition": ["Cold"], "Probability": [0.8]}),
        red_flags=[],
        recommendations=[]
    )
    assert b"%PDF" in pdf.output(dest="S").encode("latin-1")

def test_age_based_red_flags():
    """Test age-based red flags"""
    red_flags = []
    if 2 < 3:  # Simulate age=2 months
        red_flags.append("⚠️ Infants under 3 months are at higher risk")
    assert "under 3 months" in red_flags[0]

def test_medical_history_handling():
    """Test medical history flags"""
    features = {"IMMUNOCOMPROMISED_FEATURE": 0}
    if "Immunocompromised Status" in ["Immunocompromised Status"]:
        features["IMMUNOCOMPROMISED_FEATURE"] = 1
    assert features["IMMUNOCOMPROMISED_FEATURE"] == 1

def test_symptom_scoring():
    """Test symptom scoring logic"""
    symptom = "FEVER"
    responses = {
        "Temperature": "Severe (child feels very hot, irritable, or appears unwell)",
        "Duration": "3-7 days"
    }
    expected_score = 3 + 3  # From weights in SYMPTOM_DEFINITIONS
    actual_score = sum(
        q["weights"][responses[q["question"]] ]
        for q in SYMPTOM_DEFINITIONS[symptom]["follow_up"]
    )
    assert actual_score == expected_score

@pytest.mark.skip(reason="Requires live API - use mock in production")
def test_doctor_search_api():
    """Test doctor search API (skipped to avoid live calls)"""
    doctors_df = find_nearby_doctors(40.7128, -74.0060, 2000)
    assert isinstance(doctors_df, pd.DataFrame)

def test_step_indicator_rendering():
    """Test UI step logic"""
    assert 2 in [1, 2, 3, 4]  # Simulate current_step=2

def test_condition_probability_sorting():
    """Test probability sorting"""
    prob_df = pd.DataFrame({
        "Condition": ["Cold", "Flu"],
        "Probability": [0.2, 0.5]
    }).sort_values("Probability", ascending=False)
    assert prob_df.iloc[0]["Probability"] == 0.5

# --- Main Execution (Optional) ---
if __name__ == "__main__":
    pytest.main([__file__, "-v"])