import streamlit as st
import pickle
import numpy as np
from datetime import datetime

st.set_page_config(page_title="Diabetes Analyzer", page_icon="🩺", layout="wide")

@st.cache_resource
def load_model():
    with open("model.pkl", "rb") as f:
        return pickle.load(f)

model = load_model()

st.markdown("""
<style>
/* -------- Main background -------- */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #1a0f2e, #2a1b4d, #102542);
    background-attachment: fixed;
}

/* Hide default header background */
[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}

/* -------- Full-page intro animation -------- */
@keyframes fullSplash {
    0% {
        opacity: 1;
        visibility: visible;
    }
    70% {
        opacity: 1;
        visibility: visible;
    }
    100% {
        opacity: 0;
        visibility: hidden;
    }
}

@keyframes zoomText {
    0% {
        opacity: 0;
        transform: scale(0.7) translateY(20px);
    }
    30% {
        opacity: 1;
        transform: scale(1.08) translateY(0);
    }
    60% {
        opacity: 1;
        transform: scale(1) translateY(0);
    }
    100% {
        opacity: 1;
        transform: scale(1) translateY(0);
    }
}

@keyframes blurRelease {
    0% {
        filter: blur(10px);
    }
    70% {
        filter: blur(10px);
    }
    100% {
        filter: blur(0px);
    }
}

.intro-overlay {
    position: fixed;
    inset: 0;
    z-index: 999999;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(8, 10, 25, 0.45);
    backdrop-filter: blur(18px);
    animation: fullSplash 3.5s ease forwards;
}

.intro-box {
    text-align: center;
    padding: 2.5rem 3rem;
    border-radius: 28px;
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255,255,255,0.12);
    box-shadow: 0 15px 45px rgba(0,0,0,0.35);
}

.intro-title {
    font-size: 3.2rem;
    font-weight: 800;
    color: #ffffff;
    letter-spacing: 1px;
    animation: zoomText 1.2s ease-out;
}

.intro-subtitle {
    margin-top: 0.8rem;
    color: #dbeafe;
    font-size: 1.1rem;
    animation: zoomText 1.6s ease-out;
}

/* Blur the app briefly while intro is active */
.main .block-container {
    animation: blurRelease 3.5s ease forwards;
}

/* -------- Main UI -------- */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1200px;
}

.main-title {
    font-size: 2.6rem;
    font-weight: 800;
    color: white;
    text-align: center;
    margin-bottom: 0.35rem;
}

.sub-title {
    text-align: center;
    color: #d8ddee;
    margin-bottom: 2rem;
    font-size: 1.05rem;
}

.glass-card {
    background: rgba(255,255,255,0.08);
    padding: 2rem;
    border-radius: 24px;
    border: 1px solid rgba(255,255,255,0.1);
    box-shadow: 0 10px 30px rgba(0,0,0,0.22);
    margin-bottom: 1rem;
}

.metric {
    background: rgba(255,255,255,0.07);
    padding: 1rem;
    border-radius: 18px;
    text-align: center;
    color: white;
    margin-bottom: 0.8rem;
    border: 1px solid rgba(255,255,255,0.08);
}

.metric-value {
    font-size: 1.8rem;
    font-weight: bold;
    color: #7dd3fc;
    margin-top: 0.3rem;
}

label, .stNumberInput label, .stTextInput label {
    color: #edf2ff !important;
    font-weight: 600 !important;
}

.stButton>button, .stDownloadButton>button, div[data-testid="stFormSubmitButton"] button {
    width: 100%;
    background: linear-gradient(90deg, #7c3aed, #06b6d4);
    color: white;
    font-weight: 700;
    border-radius: 14px;
    border: none;
    padding: 0.75rem 1rem;
    box-shadow: 0 8px 24px rgba(124,58,237,0.3);
}

.stButton>button:hover, .stDownloadButton>button:hover, div[data-testid="stFormSubmitButton"] button:hover {
    color: white;
    background: linear-gradient(90deg, #6d28d9, #0891b2);
}

.note-box {
    background: rgba(255,255,255,0.08);
    border-left: 5px solid #7c3aed;
    padding: 1rem;
    border-radius: 14px;
    color: #e5e7eb;
    margin-top: 1rem;
}

.report-box {
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,255,255,0.09);
    padding: 1rem;
    border-radius: 16px;
    color: white;
}

.footer-text {
    text-align: center;
    color: #cbd5e1;
    font-size: 0.92rem;
    margin-top: 1rem;
}
</style>
""", unsafe_allow_html=True)

# Full-page animated overlay
st.markdown("""
<div class="intro-overlay">
    <div class="intro-box">
        <div class="intro-title">✨ WELCOME TO DIABETES ANALYZER</div>
        <div class="intro-subtitle">Smart ML-based diabetes risk prediction system</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🩺 Diabetes Prediction System</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">Enter patient details to predict diabetes risk and generate a patient report</div>',
    unsafe_allow_html=True
)

left, right = st.columns([1.25, 1])

with left:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("Patient Details")

    with st.form("patient_form"):
        name = st.text_input("Patient Name", placeholder="Enter full name")

        col1, col2 = st.columns(2)

        with col1:
            age = st.number_input(
    "Age (1–120 years)",
    min_value=1,
    max_value=120,
    value=30
)
           bp = st.number_input(
    "Blood Pressure (70–120 mmHg)",
    min_value=70.0,
    max_value=200.0,
    value=80.0,
    step=1.0
)
glucose = st.number_input(
    "Glucose (70–100 mg/dL normal)",
    min_value=50.0,
    max_value=300.0,
    value=100.0,
    step=1.0
)

        with col2:
     bmi = st.number_input(
    "BMI (18.5–24.9 normal)",
    min_value=10.0,
    max_value=50.0,
    value=24.5,
    step=0.1
)
            
            insulin = st.number_input(
    "Insulin (16–166 normal)",
    min_value=0.0,
    max_value=300.0,
    value=80.0,
    step=1.0
)

        submitted = st.form_submit_button("Predict and Generate Report")

    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("Health Snapshot")

    m1, m2 = st.columns(2)
    with m1:
        st.markdown(
            f'<div class="metric">Age<div class="metric-value">{age}</div></div>',
            unsafe_allow_html=True
        )
    with m2:
        st.markdown(
            f'<div class="metric">BMI<div class="metric-value">{bmi}</div></div>',
            unsafe_allow_html=True
        )

    m3, m4 = st.columns(2)
    with m3:
        st.markdown(
            f'<div class="metric">Glucose<div class="metric-value">{glucose}</div></div>',
            unsafe_allow_html=True
        )
    with m4:
        st.markdown(
            f'<div class="metric">Blood Pressure<div class="metric-value">{bp}</div></div>',
            unsafe_allow_html=True
        )

    st.markdown(
        f'<div class="metric">Insulin<div class="metric-value">{insulin}</div></div>',
        unsafe_allow_html=True
    )

    avg = (glucose + bmi + bp) / 3 if (glucose + bmi + bp) > 0 else 0

    st.markdown("### Risk Indicator")
    if avg > 120:
        st.error("High Risk Zone")
    elif avg > 80:
        st.warning("Moderate Risk Zone")
    else:
        st.success("Low Risk Zone")

    st.markdown('</div>', unsafe_allow_html=True)

if "report_text" not in st.session_state:
    st.session_state.report_text = None

if submitted:
    data = np.array([[age, bp, glucose, bmi, insulin]])
    prediction = model.predict(data)[0]

    risk_score = None
    if hasattr(model, "predict_proba"):
        risk_score = model.predict_proba(data)[0][1] * 100

    if prediction == 1:
        result_text = "High chance of diabetes detected"
        result_short = "HIGH RISK"
    else:
        result_text = "Low chance of diabetes detected"
        result_short = "LOW RISK"

    patient_name = name.strip() if name.strip() else "Unknown Patient"
    report_date = datetime.now().strftime("%d/%m/%Y %H:%M")

    report = f"""
DIABETES PREDICTION PATIENT REPORT
----------------------------------

Patient Name: {patient_name}
Date & Time: {report_date}

Entered Health Values
---------------------
Age: {age}
Blood Pressure: {bp}
Glucose: {glucose}
BMI: {bmi}
Insulin: {insulin}

Prediction Result
-----------------
Status: {result_short}
Interpretation: {result_text}
"""

    if risk_score is not None:
        report += f"Estimated Risk Score: {risk_score:.2f}%\n"

    report += """
Important Note
--------------
This report is generated by a machine learning model for awareness and educational purposes only.
It does not replace professional medical diagnosis or treatment advice.
"""

    st.session_state.report_text = report

    st.markdown("## Prediction Result")
    st.write(f"**Patient Name:** {patient_name}")

    if prediction == 1:
        st.error(f"⚠️ {result_text}")
    else:
        st.success(f"✅ {result_text}")

    if risk_score is not None:
        st.info(f"Estimated diabetes risk score: {risk_score:.2f}%")

if st.session_state.report_text:
    st.markdown("## Patient Report")
    st.markdown('<div class="report-box">', unsafe_allow_html=True)
    st.text(st.session_state.report_text)
    st.markdown('</div>', unsafe_allow_html=True)

    st.download_button(
        label="Download Patient Report",
        data=st.session_state.report_text,
        file_name="patient_report.txt",
        mime="text/plain"
    )

st.markdown(
    """
    <div class="note-box">
    <b>Note:</b> This app is for awareness and educational purposes only. It should support healthcare decisions, not replace a doctor's diagnosis.
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    '<div class="footer-text">Built with Streamlit + Machine Learning + Decision Tree Model</div>',
    unsafe_allow_html=True
)
