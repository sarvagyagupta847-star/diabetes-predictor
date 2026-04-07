import streamlit as st
import pickle
import numpy as np

st.set_page_config(page_title="Diabetes Predictor", page_icon="🩺", layout="wide")

@st.cache_resource
def load_model():
    return pickle.load(open("model.pkl", "rb"))

model = load_model()

# ---------- UI STYLE ----------
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f172a, #1e293b);
}
.main-title {
    font-size: 3rem;
    font-weight: 800;
    color: white;
    text-align: center;
}
.sub-title {
    text-align: center;
    color: #cbd5e1;
    margin-bottom: 2rem;
}
.glass-card {
    background: rgba(255,255,255,0.07);
    padding: 2rem;
    border-radius: 20px;
    border: 1px solid rgba(255,255,255,0.1);
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
.stButton>button {
    width: 100%;
    background: linear-gradient(90deg,#2563eb,#38bdf8);
    color: white;
    font-weight: bold;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown('<div class="main-title">🩺 Diabetes Prediction System</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Enter patient details to predict diabetes risk</div>', unsafe_allow_html=True)

# ---------- LAYOUT ----------
left, right = st.columns([1.2,1])

with left:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)

    st.subheader("Patient Details")

    # 🔥 NEW: Patient Name
    name = st.text_input("Patient Name")

    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input("Age", 1, 120)
        bp = st.number_input("Blood Pressure")
        glucose = st.number_input("Glucose")

    with col2:
        bmi = st.number_input("BMI")
        insulin = st.number_input("Insulin")

    predict = st.button("Predict")

    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("Health Snapshot")

    m1, m2 = st.columns(2)

    with m1:
        st.markdown(f'<div class="metric"><div>Age</div><div class="metric-value">{age}</div></div>', unsafe_allow_html=True)
    with m2:
        st.markdown(f'<div class="metric"><div>BMI</div><div class="metric-value">{bmi}</div></div>', unsafe_allow_html=True)

    m3, m4 = st.columns(2)

    with m3:
        st.markdown(f'<div class="metric"><div>Glucose</div><div class="metric-value">{glucose}</div></div>', unsafe_allow_html=True)
    with m4:
        st.markdown(f'<div class="metric"><div>BP</div><div class="metric-value">{bp}</div></div>', unsafe_allow_html=True)

    # 🔥 NEW: Risk Level Indicator
    avg = (glucose + bmi + bp) / 3 if (glucose + bmi + bp) != 0 else 0

    st.markdown("### Risk Indicator")

    if avg > 120:
        st.error("High Risk Zone")
    elif avg > 80:
        st.warning("Moderate Risk")
    else:
        st.success("Low Risk")

    st.markdown('</div>', unsafe_allow_html=True)

# ---------- PREDICTION ----------
if predict:
    data = np.array([[age, bp, glucose, bmi, insulin]])
    prediction = model.predict(data)[0]

    st.markdown("## Result")

    # 🔥 Show patient name in result
    if name:
        st.write(f"Patient: **{name}**")

    if prediction == 1:
        st.error("⚠️ High chance of Diabetes")
    else:
        st.success("✅ Low chance of Diabetes")

    if hasattr(model, "predict_proba"):
        prob = model.predict_proba(data)[0][1] * 100
        st.info(f"Risk Score: {prob:.2f}%")

# ---------- FOOTER ----------
st.markdown("This tool is for educational purposes only.")
