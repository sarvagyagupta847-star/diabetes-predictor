import streamlit as st
import pickle
import numpy as np
from datetime import datetime

st.set_page_config(page_title="Diabetes Analyzer", page_icon="🩺", layout="wide")

# ---------- LOAD MODEL ----------
@st.cache_resource
def load_model():
    with open("model.pkl", "rb") as f:
        return pickle.load(f)

model = load_model()

# ---------- CSS ----------
st.markdown("""
<style>
/* ================================
   GLOBAL BACKGROUND
================================ */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(-45deg, #0f172a, #1e1b4b, #0f766e, #7c3aed, #1d4ed8);
    background-size: 400% 400%;
    animation: gradientFlow 15s ease infinite;
    background-attachment: fixed;
}

[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}

@keyframes gradientFlow {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}

/* ================================
   INTRO SCREEN
================================ */
@keyframes fadeOut {
    0% {opacity: 1;}
    82% {opacity: 1;}
    100% {opacity: 0; visibility: hidden;}
}

@keyframes glowPulse {
    0% {
        opacity: 0;
        transform: scale(0.85);
        text-shadow: 0 0 0px rgba(255,255,255,0);
    }
    50% {
        opacity: 1;
        transform: scale(1.08);
        text-shadow:
            0 0 20px #38bdf8,
            0 0 40px #7c3aed,
            0 0 60px #06b6d4;
    }
    100% {
        opacity: 1;
        transform: scale(1);
        text-shadow:
            0 0 10px #38bdf8,
            0 0 25px #7c3aed;
    }
}

@keyframes softRise {
    0% {
        opacity: 0;
        transform: translateY(25px);
    }
    100% {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes floatBox {
    0% {transform: translateY(0px);}
    50% {transform: translateY(-8px);}
    100% {transform: translateY(0px);}
}

.intro {
    position: fixed;
    inset: 0;
    z-index: 99999;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(3, 7, 18, 0.50);
    backdrop-filter: blur(24px);
    animation: fadeOut 4s forwards;
}

.intro-box {
    text-align: center;
    padding: 2.5rem 3rem;
    border-radius: 32px;
    background: rgba(255,255,255,0.10);
    border: 1px solid rgba(255,255,255,0.15);
    box-shadow: 0 20px 60px rgba(0,0,0,0.40);
    animation: floatBox 3s ease-in-out infinite;
}

.intro-text {
    font-size: 3.2rem;
    font-weight: 900;
    color: white;
    letter-spacing: 1px;
    animation: glowPulse 2s ease-in-out;
}

.intro-sub {
    margin-top: 0.75rem;
    color: #dbeafe;
    font-size: 1.08rem;
    animation: softRise 1.2s ease-in-out;
}

/* ================================
   MAIN TITLE
================================ */
@keyframes shimmer {
    0% {background-position: -200% center;}
    100% {background-position: 200% center;}
}

.main-title {
    font-size: 2.9rem;
    font-weight: 900;
    margin-bottom: 0.25rem;
    background: linear-gradient(90deg, #ffffff, #67e8f9, #c4b5fd, #f9a8d4, #ffffff);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shimmer 6s linear infinite;
}

.main-subtitle {
    color: #e2e8f0;
    font-size: 1.05rem;
    margin-bottom: 1.3rem;
    animation: softRise 1s ease-in-out;
}

/* ================================
   HEARTBEAT LINE
================================ */
@keyframes heartbeatMove {
    0% {background-position: 0% 50%;}
    100% {background-position: 200% 50%;}
}

.heartbeat-line {
    height: 5px;
    width: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, #22d3ee, #a78bfa, #f472b6, #22d3ee);
    background-size: 200% 100%;
    animation: heartbeatMove 3s linear infinite;
    margin: 0.6rem 0 1.4rem 0;
    box-shadow: 0 0 18px rgba(56,189,248,0.5);
}

/* ================================
   CARDS
================================ */
@keyframes fadeSlideUp {
    0% {
        opacity: 0;
        transform: translateY(35px);
    }
    100% {
        opacity: 1;
        transform: translateY(0);
    }
}

.glass-card {
    background: rgba(255,255,255,0.10);
    padding: 2rem;
    border-radius: 24px;
    border: 1px solid rgba(255,255,255,0.12);
    box-shadow: 0 12px 34px rgba(0,0,0,0.22);
    margin-bottom: 1rem;
    animation: fadeSlideUp 0.9s ease-in-out;
    transition: transform 0.35s ease, box-shadow 0.35s ease;
}

.glass-card:hover {
    transform: translateY(-8px) scale(1.01);
    box-shadow: 0 18px 40px rgba(0,0,0,0.28);
}

/* ================================
   METRICS
================================ */
.metric {
    background: linear-gradient(135deg, rgba(255,255,255,0.10), rgba(255,255,255,0.06));
    padding: 1rem;
    border-radius: 18px;
    text-align: center;
    color: white;
    margin-bottom: 0.9rem;
    border: 1px solid rgba(255,255,255,0.08);
    animation: fadeSlideUp 1s ease-in-out;
    transition: all 0.28s ease;
}

.metric:hover {
    transform: scale(1.05);
    background: linear-gradient(135deg, rgba(125,211,252,0.18), rgba(196,181,253,0.18));
}

.metric-value {
    font-size: 1.8rem;
    font-weight: 800;
    margin-top: 0.25rem;
    color: #fde68a;
    text-shadow: 0 0 10px rgba(253,230,138,0.35);
}

/* ================================
   BUTTONS
================================ */
@keyframes pulseButton {
    0% {box-shadow: 0 0 0 rgba(124,58,237,0.0);}
    50% {box-shadow: 0 0 24px rgba(56,189,248,0.45);}
    100% {box-shadow: 0 0 0 rgba(124,58,237,0.0);}
}

.stButton>button,
.stDownloadButton>button,
div[data-testid="stFormSubmitButton"] button {
    width: 100%;
    background: linear-gradient(90deg, #ec4899, #7c3aed, #06b6d4);
    color: white;
    font-weight: 800;
    border-radius: 16px;
    border: none;
    padding: 0.85rem 1rem;
    animation: pulseButton 2.3s infinite;
    transition: transform 0.2s ease;
}

.stButton>button:hover,
.stDownloadButton>button:hover,
div[data-testid="stFormSubmitButton"] button:hover {
    transform: scale(1.03);
    color: white;
}

/* ================================
   CONTENT BOXES
================================ */
.recommend-box {
    background: rgba(255,255,255,0.10);
    border-left: 5px solid #22d3ee;
    padding: 1rem;
    border-radius: 14px;
    color: #f8fafc;
    margin-top: 0.8rem;
    animation: fadeSlideUp 0.8s ease-in-out;
}

.report-box {
    background: rgba(255,255,255,0.09);
    border: 1px solid rgba(255,255,255,0.10);
    padding: 1rem;
    border-radius: 18px;
    color: white;
    animation: fadeSlideUp 0.7s ease-in-out;
}

.note-box {
    background: rgba(255,255,255,0.10);
    border-left: 5px solid #f472b6;
    padding: 1rem;
    border-radius: 14px;
    color: #f8fafc;
    margin-top: 1rem;
    animation: fadeSlideUp 1.1s ease-in-out;
}

.footer-text {
    text-align: center;
    color: #e2e8f0;
    font-size: 0.92rem;
    margin-top: 1rem;
    animation: softRise 1.4s ease-in-out;
}

.result-wrap {
    animation: fadeSlideUp 0.6s ease-in-out;
}

h1, h2, h3, h4, p, label {
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# ---------- INTRO ----------
st.markdown("""
<div class="intro">
    <div class="intro-box">
        <div class="intro-text">✨ Welcome to Diabetes Analyzer</div>
        <div class="intro-sub">Smart ML-based diabetes risk prediction system</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown('<div class="main-title">🩺 Diabetes Prediction System</div>', unsafe_allow_html=True)
st.markdown('<div class="main-subtitle">Enter patient details to predict diabetes risk and generate a patient report.</div>', unsafe_allow_html=True)
st.markdown('<div class="heartbeat-line"></div>', unsafe_allow_html=True)

# ---------- LAYOUT ----------
left, right = st.columns([1.2, 1])

with left:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("Patient Details")

    with st.form("patient_form"):
        name = st.text_input("Patient Name", placeholder="Enter full name")

        col1, col2 = st.columns(2)

        with col1:
            age = st.number_input("Age (1–120 years)", min_value=1, max_value=120, value=30, step=1)
            bp = st.number_input("Blood Pressure (70–120 mmHg normal)", min_value=70.0, max_value=200.0, value=80.0, step=1.0)
            glucose = st.number_input("Glucose (70–100 mg/dL fasting normal)", min_value=50.0, max_value=300.0, value=100.0, step=1.0)

        with col2:
            bmi = st.number_input("BMI (18.5–24.9 normal)", min_value=10.0, max_value=50.0, value=24.5, step=0.1)
            insulin = st.number_input("Insulin (16–166 typical range)", min_value=0.0, max_value=300.0, value=80.0, step=1.0)

        submitted = st.form_submit_button("Predict and Generate Report")

    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("Health Snapshot")

    st.markdown(f'<div class="metric">Age<div class="metric-value">{age}</div></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric">BMI<div class="metric-value">{bmi}</div></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric">Glucose<div class="metric-value">{glucose}</div></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric">Blood Pressure<div class="metric-value">{bp}</div></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric">Insulin<div class="metric-value">{insulin}</div></div>', unsafe_allow_html=True)

    avg = (glucose + bmi + bp) / 3

    st.subheader("Risk Indicator")
    if avg > 120:
        st.error("High Risk Zone")
    elif avg > 80:
        st.warning("Moderate Risk Zone")
    else:
        st.success("Low Risk Zone")

    st.markdown('</div>', unsafe_allow_html=True)

if "report_text" not in st.session_state:
    st.session_state.report_text = None

# ---------- PREDICTION ----------
if submitted:
    data = np.array([[age, bp, glucose, bmi, insulin]])
    prediction = model.predict(data)[0]

    patient_name = name.strip() if name.strip() else "Unknown Patient"
    result = "HIGH RISK" if prediction == 1 else "LOW RISK"

    risk_score = None
    if hasattr(model, "predict_proba"):
        try:
            risk_score = model.predict_proba(data)[0][1] * 100
        except Exception:
            risk_score = None

    st.markdown('<div class="result-wrap">', unsafe_allow_html=True)
    st.subheader("Result")
    st.write(f"Patient: **{patient_name}**")

    if prediction == 1:
        st.error("⚠️ High chance of Diabetes")
    else:
        st.success("✅ Low chance of Diabetes")

    if risk_score is not None:
        st.info(f"Estimated diabetes risk score: {risk_score:.2f}%")
    st.markdown('</div>', unsafe_allow_html=True)

    st.subheader("What to Do Next")

    if prediction == 1:
        st.markdown("""
        <div class="recommend-box">
        <b>⚠️ High Risk – Recommended Actions:</b><br><br>
        • Consult a doctor for proper diagnosis<br>
        • Monitor blood sugar regularly<br>
        • Reduce sugar intake<br>
        • Focus on weight management<br>
        • Stay physically active regularly<br>
        </div>
        """, unsafe_allow_html=True)

        st.subheader("🍎 Diet Tips")
        st.markdown("""
        <div class="recommend-box">
        <b>Eat:</b><br>
        • Green vegetables (spinach, broccoli, cucumber)<br>
        • Whole grains (brown rice, oats, whole wheat)<br>
        • Protein (eggs, paneer, dal, chicken, fish)<br>
        • Nuts and seeds in moderation<br><br>
        <b>Avoid:</b><br>
        • Sugary drinks and sweets<br>
        • Fried and junk food<br>
        • Excess white bread, maida, bakery foods<br>
        • Large portions of high-carb food<br>
        </div>
        """, unsafe_allow_html=True)

        st.subheader("🏃 Exercise Tips")
        st.markdown("""
        <div class="recommend-box">
        • Walk at least 30 minutes daily<br>
        • Do light jogging or cycling if comfortable<br>
        • Try yoga or stretching exercises<br>
        • Avoid sitting for very long hours<br>
        • Aim for regular activity at least 5 days a week<br>
        </div>
        """, unsafe_allow_html=True)

    else:
        st.markdown("""
        <div class="recommend-box">
        <b>✅ Low Risk – Maintain Healthy Lifestyle:</b><br><br>
        • Continue healthy eating habits<br>
        • Stay physically active<br>
        • Maintain healthy body weight<br>
        • Get regular health checkups<br>
        </div>
        """, unsafe_allow_html=True)

        st.subheader("🍎 Healthy Diet Tips")
        st.markdown("""
        <div class="recommend-box">
        • Eat fresh fruits and vegetables regularly<br>
        • Prefer home-cooked balanced meals<br>
        • Drink enough water<br>
        • Avoid too much sugar and processed food<br>
        </div>
        """, unsafe_allow_html=True)

        st.subheader("🏃 Exercise Tips")
        st.markdown("""
        <div class="recommend-box">
        • Walk 20–30 minutes daily<br>
        • Stay physically active throughout the day<br>
        • Do stretching, yoga, or light exercise<br>
        • Avoid sedentary lifestyle<br>
        </div>
        """, unsafe_allow_html=True)

    report = f"""
DIABETES REPORT
----------------
Name: {patient_name}
Date: {datetime.now().strftime("%d/%m/%Y %H:%M")}

Age: {age}
Blood Pressure: {bp}
Glucose: {glucose}
BMI: {bmi}
Insulin: {insulin}

Result: {result}
"""

    if risk_score is not None:
        report += f"Estimated Risk Score: {risk_score:.2f}%\n"

    if prediction == 1:
        report += """
Suggested Next Steps:
- Consult a doctor for proper diagnosis
- Monitor blood sugar regularly
- Reduce sugary foods and drinks
- Improve diet and activity level

Diet Tips:
- Eat vegetables, whole grains, and protein
- Avoid junk food, sweets, and refined carbs

Exercise Tips:
- Walk 30 minutes daily
- Try cycling, yoga, or light jogging
"""
    else:
        report += """
Suggested Next Steps:
- Continue healthy habits
- Maintain regular checkups
- Stay active and hydrated

Diet Tips:
- Eat balanced home-cooked meals
- Limit excess sugar and processed food

Exercise Tips:
- Walk 20–30 minutes daily
- Stay active and avoid sitting too long
"""

    report += """
Important Note:
This tool is for awareness and educational use only.
It does not replace medical diagnosis or treatment advice.
"""

    st.session_state.report_text = report

# ---------- REPORT DISPLAY ----------
if st.session_state.report_text:
    st.subheader("Patient Report")
    st.markdown('<div class="report-box">', unsafe_allow_html=True)
    st.text(st.session_state.report_text)
    st.markdown('</div>', unsafe_allow_html=True)

    st.download_button(
        label="Download Patient Report",
        data=st.session_state.report_text,
        file_name="patient_report.txt",
        mime="text/plain"
    )

# ---------- FOOTER ----------
st.info("""
Reference ranges:
- Blood Pressure: 70–120 mmHg
- Glucose (fasting): 70–100 mg/dL
- BMI: 18.5–24.9
- Insulin: 16–166
""")

st.markdown("""
<div class="note-box">
<b>Note:</b> This app is for awareness and educational purposes only.
It should support healthcare decisions, not replace a doctor's diagnosis.
</div>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="footer-text">Built with Streamlit + Machine Learning + Decision Tree Model</div>',
    unsafe_allow_html=True
)
