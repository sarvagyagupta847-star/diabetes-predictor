import streamlit as st
import pickle
import numpy as np

st.set_page_config(page_title="Diabetes Predictor", page_icon="🩺")

# Load model
model = pickle.load(open("model.pkl", "rb"))

st.title("🩺 Diabetes Prediction System")

st.write("Enter patient details:")

age = st.number_input("Age", 1, 120)
bp = st.number_input("Blood Pressure")
glucose = st.number_input("Glucose")
bmi = st.number_input("BMI")
insulin = st.number_input("Insulin")

if st.button("Predict"):
    data = np.array([[age, bp, glucose, bmi, insulin]])
    prediction = model.predict(data)

    if prediction[0] == 1:
        st.error("⚠️ High Risk of Diabetes")
    else:
        st.success("✅ Low Risk of Diabetes")
