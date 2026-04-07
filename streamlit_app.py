import streamlit as st
import pickle
import numpy as np

st.set_page_config(
    page_title="Diabetes Prediction System",
    page_icon="🩺",
    layout="wide"
)

@st.cache_resource
def load_model():
    with open("model.pkl", "rb") as f:
        return pickle.load(f)

model = load_model()

st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f172a, #1e293b, #111827);
}
[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a, #111827);
}
.main-title {
    font-size: 3rem;
    font-weight: 800;
    color: white;
    text-align: center;
    margin-bottom: 0.4rem;
}
.sub-title {
    font-size: 1.1rem;
    color: #cbd5e1;
    text-align: center;
    margin-bottom: 2rem;
}
.glass-card {
    background: rgba(255,255,255,0.08);
    padding: 2rem;
    border-radius: 24px;
    border: 1px solid rgba(255,255,255,0.12);
    box-shadow: 0 8px 32px rgba(0,0,0,0.25);
}
.metric-box {
    background: rgba(255,255,255,0.07);
    padding: 1rem;
    border-radius: 18px;
    text-align: center;
    color: white;
    border: 1px solid rgba(255,255,255,0.08);
}
.metric-value {
    font-size: 1.8rem;
    font-weight: 700;
    color: #38bdf8;
}
.metric-label {
    color: #cbd5e1;
    font-size: 0.95rem;
}
.note-box {
    background: rgba(59,130,246,0.14);
    border-left: 5px solid #38bdf8;
    padding: 1rem;
    border-radius: 14px;
    color: #e2e8f0;
    margin-top: 1.5rem;
}
.section-heading {
    color: white;
    font-size: 1.3rem;
    font-weight: 700;
    margin-bottom: 1rem;
}
.footer-text {
    text-align: center;
    color: #94a3b8;
    margin-top: 1.5rem;
    font-size: 0.9rem;
}
.stButton > button {
    width: 100%;
    background: linear-gradient(90deg, #2563eb, #06b6d4);
    color: white;
    font-size: 1.05rem;
    font-weight: 700;
    border: none;
    border-radius: 14px;
    padding: 0.75rem 1rem;
    box-shadow: 0 6px 20px rgba(37,99,235,0.3);
}
.stButton > button:hover {
    background: linear-gradient(90deg, #1d4ed8, #0891b2);
    color: white;
}
label, .stNumberInput label {
    color: #e2e8f0 !important;
    font-weight: 600 !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🩺 Diabetes Prediction System</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">A smart healthcare web app that estimates diabetes risk using machine learning</div>',
    unsafe_allow_html=True
)

left, right = st.columns([1.2, 1])

with left:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">Enter Patient Details</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input("Age", min_value=1, max_value=120, value=25, step=1)
        bp = st.number_input("Blood Pressure", min_value=0.0, value=80.0, step=1.0)
        glucose = st.number_input("Glucose", min_value=0.0, value=100.0, step=1.0)

    with col2:
        bmi = st.number_input("BMI", min_value=0.0, value=24.5, step=0.1, format="%.1f")
        insulin = st.number_input("Insulin", min_value=0.0, value=80.0, step=1.0)

    predict = st.button("Predict Diabetes Risk")
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">Health Snapshot</div>', unsafe_allow_html=True)

    m1, m2 = st.columns(2)
    with m1:
        st.markdown(
            f'<div class="metric-box"><div class="metric-label">Age</div><div class="metric-value">{age}</div></div>',
            unsafe_allow_html=True
        )
    with m2:
        st.markdown(
            f'<div class="metric-box"><div class="metric-label">BMI</div><div class="metric-value">{bmi}</div></div>',
            unsafe_allow_html=True
        )

    m3, m4 = st.columns(2)
    with m3:
        st.markdown(
            f'<div class="metric-box"><div class="metric-label">Glucose</div><div class="metric-value">{glucose}</div></div>',
            unsafe_allow_html=True
        )
    with m4:
        st.markdown(
            f'<div class="metric-box"><div class="metric-label">BP</div><div class="metric-value">{bp}</div></div>',
            unsafe_allow_html=True
        )

    st.markdown('</div>', unsafe_allow_html=True)

if predict:
    data = np.array([[age, bp, glucose, bmi, insulin]])
    prediction = model.predict(data)[0]

    st.markdown("### Prediction Result")
    if prediction == 1:
        st.error("⚠️ High chance of diabetes detected")
    else:
        st.success("✅ Low chance of diabetes detected")

    if hasattr(model, "predict_proba"):
        probability = model.predict_proba(data)[0][1] * 100
        st.info(f"Estimated diabetes risk score: {probability:.2f}%")

st.markdown(
    """
    <div class="note-box">
    <b>Note:</b> This tool uses machine learning for awareness and educational purposes.
    It should support healthcare decisions, not replace a doctor's diagnosis.
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="footer-text">Built with Streamlit + Machine Learning + Decision Tree Model</div>', unsafe_allow_html=True)
