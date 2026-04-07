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
    background: linear-gradient(135deg, #0f172a, #1e293b);
}

/* ANIMATION */
@keyframes popIn {
    0% {opacity:0; transform:scale(0.7);}
    100% {opacity:1; transform:scale(1);}
}

.welcome-box {
    background: rgba(255,255,255,0.08);
    padding: 1.5rem;
    border-radius: 20px;
    text-align: center;
    animation: popIn 1s ease-out;
}

.welcome-title {
    font-size: 2.5rem;
    color: white;
    font-weight: bold;
}

.welcome-subtitle {
    color: #cbd5e1;
}

.glass-card {
    background: rgba(255,255,255,0.07);
    padding: 2rem;
    border-radius: 20px;
}

.metric {
    background: rgba(255,255,255,0.06);
    padding: 1rem;
    border-radius: 15px;
    text-align: center;
    color: white;
}

.metric-value {
    font-size: 1.8rem;
    font-weight: bold;
    color: #38bdf8;
}

.stButton>button, .stDownloadButton>button {
    width: 100%;
    background: linear-gradient(90deg,#2563eb,#38bdf8);
    color: white;
    font-weight: bold;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

# ---------- WELCOME ----------
st.markdown("""
<div class="welcome-box">
    <div class="welcome-title">✨ Welcome to Diabetes Analyzer</div>
    <div class="welcome-subtitle">AI-powered diabetes risk prediction system</div>
</div>
""", unsafe_allow_html=True)

st.markdown("## 🩺 Diabetes Prediction System")

# ---------- LAYOUT ----------
left, right = st.columns([1.2,1])

with left:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)

    with st.form("form"):
        name = st.text_input("Patient Name")

        col1, col2 = st.columns(2)

        with col1:
            age = st.number_input("Age", 1, 120, value=30, help="Normal adult: 18–65")
            bp = st.number_input("Blood Pressure", value=80.0, help="70–120 mmHg")
            glucose = st.number_input("Glucose", value=100.0, help="70–100 normal")

        with col2:
            bmi = st.number_input("BMI", value=24.5, help="18.5–24.9 normal")
            insulin = st.number_input("Insulin", value=80.0, help="16–166 normal")

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

    avg = (glucose + bmi + bp)/3 if (glucose + bmi + bp)!=0 else 0

    st.markdown("### Risk Indicator")

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

    st.markdown("## Result")

    if name:
        st.write(f"Patient: **{name}**")

    if prediction == 1:
        st.error("⚠️ High chance of Diabetes")
    else:
        st.success("✅ Low chance of Diabetes")

    # ---------- REPORT ----------
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

    st.download_button(
        "Download Report",
        report,
        file_name="report.txt"
    )

# ---------- FOOTER ----------
st.markdown("This tool is for educational purposes only.")
