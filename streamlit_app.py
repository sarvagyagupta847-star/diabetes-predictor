import streamlit as st
import pickle
import numpy as np

st.set_page_config(page_title="Diabetes Predictor", page_icon="🩺", layout="centered")

st.title("🩺 Diabetes Risk Predictor")
st.caption("Enter patient details and click Predict.")

st.divider()

age     = st.slider("Age", 1, 120, 35)
bp      = st.slider("Blood Pressure (mmHg)", 0, 200, 72)
glucose = st.slider("Glucose (mg/dL)", 0, 300, 110)
bmi     = st.slider("BMI", 0.0, 70.0, 24.5, step=0.1)
insulin = st.slider("Insulin (µU/mL)", 0, 900, 80)

st.divider()

if st.button("Predict", use_container_width=True):
    try:
        model = pickle.load(open("model.pkl", "rb"))
        pred  = model.predict(np.array([[age, bp, glucose, bmi, insulin]]))[0]
    except FileNotFoundError:
        score = (2 if glucose > 140 else 1 if glucose > 100 else 0) \
              + (2 if bmi > 30 else 1 if bmi > 25 else 0) \
              + (1 if age > 50 else 0) \
              + (1 if bp > 90 else 0) \
              + (1 if insulin > 200 else 0)
        pred = 1 if score >= 4 else 0

    if pred == 1:
        st.error("⚠️ High Risk of Diabetes Detected")
    else:
        st.success("✅ Low Risk — Vitals Look Healthy")

st.caption("⚠️ This is an ML-based tool, not a medical diagnosis.")
