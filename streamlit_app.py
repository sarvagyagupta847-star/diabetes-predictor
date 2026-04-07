import streamlit as st
import pickle
import numpy as np
from datetime import datetime

st.set_page_config(page_title="Diabetes Analyzer", page_icon="🩺", layout="wide")

# ---------- LOAD MODEL ----------
@st.cache_resource
def load_model():
    return pickle.load(open("model.pkl", "rb"))

model = load_model()

# ---------- CSS ----------
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #1a0f2e, #2a1b4d, #102542);
}

/* FULL PAGE INTRO */
@keyframes splash {
    0% {opacity:1;}
    80% {opacity:1;}
    100% {opacity:0; visibility:hidden;}
}

.intro {
    position: fixed;
    inset: 0;
    backdrop-filter: blur(18px);
    display:flex;
    align-items:center;
    justify-content:center;
    z-index:9999;
    animation:splash 3.5s forwards;
}

.intro-text {
    font-size:3rem;
    font-weight:bold;
    color:white;
}

/* UI */
.glass-card {
    background: rgba(255,255,255,0.08);
    padding:2rem;
    border-radius:20px;
}

.metric {
    background: rgba(255,255,255,0.06);
    padding:1rem;
    border-radius:15px;
    text-align:center;
    color:white;
    margin-bottom:10px;
}

.metric-value {
    font-size:1.7rem;
    color:#38bdf8;
}

.stButton>button, .stDownloadButton>button {
    width:100%;
    background: linear-gradient(90deg,#7c3aed,#06b6d4);
    color:white;
    font-weight:bold;
}
</style>
""", unsafe_allow_html=True)

# ---------- INTRO ----------
st.markdown("""
<div class="intro">
    <div class="intro-text">✨ Welcome to Diabetes Analyzer</div>
</div>
""", unsafe_allow_html=True)

st.title("🩺 Diabetes Prediction System")

# ---------- LAYOUT ----------
left, right = st.columns([1.2,1])

with left:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)

    with st.form("form"):
        name = st.text_input("Patient Name")

        col1, col2 = st.columns(2)

        with col1:
            age = st.number_input("Age (1–120 years)", 1, 120, 30)

            bp = st.number_input(
                "Blood Pressure (70–120 mmHg)",
                min_value=70.0,
                max_value=200.0,
                value=80.0
            )

            glucose = st.number_input(
                "Glucose (70–100 mg/dL normal)",
                min_value=50.0,
                max_value=300.0,
                value=100.0
            )

        with col2:
            bmi = st.number_input(
                "BMI (18.5–24.9 normal)",
                min_value=10.0,
                max_value=50.0,
                value=24.5
            )

            insulin = st.number_input(
                "Insulin (16–166 normal)",
                min_value=0.0,
                max_value=300.0,
                value=80.0
            )

        submit = st.form_submit_button("Predict & Generate Report")

    st.markdown('</div>', unsafe_allow_html=True)

# ---------- SNAPSHOT ----------
with right:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("Health Snapshot")

    st.markdown(f'<div class="metric">Age<br><div class="metric-value">{age}</div></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric">BMI<br><div class="metric-value">{bmi}</div></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric">Glucose<br><div class="metric-value">{glucose}</div></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric">BP<br><div class="metric-value">{bp}</div></div>', unsafe_allow_html=True)

    avg = (glucose + bmi + bp)/3

    st.subheader("Risk Indicator")

    if avg > 120:
        st.error("High Risk")
    elif avg > 80:
        st.warning("Moderate Risk")
    else:
        st.success("Low Risk")

    st.markdown('</div>', unsafe_allow_html=True)

# ---------- PREDICTION ----------
if submit:
    data = np.array([[age, bp, glucose, bmi, insulin]])
    prediction = model.predict(data)[0]

    result = "HIGH RISK" if prediction==1 else "LOW RISK"

    st.subheader("Result")

    if name:
        st.write(f"Patient: **{name}**")

    if prediction == 1:
        st.error("⚠️ High chance of Diabetes")
    else:
        st.success("✅ Low chance of Diabetes")

    report = f"""
DIABETES REPORT
----------------
Name: {name}
Date: {datetime.now()}

Age: {age}
BP: {bp}
Glucose: {glucose}
BMI: {bmi}
Insulin: {insulin}

Result: {result}
"""

    st.text(report)

    st.download_button("Download Report", report, file_name="report.txt")

# ---------- FOOTER ----------
st.info("""
Normal Ranges:
- BP: 70–120 mmHg
- Glucose: 70–100 mg/dL
- BMI: 18.5–24.9
- Insulin: 16–166
""")

st.write("⚠️ This tool is for educational use only.")
