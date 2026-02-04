
import streamlit as st
import joblib
import pandas as pd

# Load the trained Random Forest model

model = joblib.load('random_forest_model.pkl')

CORRECTION_SUGGESTIONS = {
    "Total Coliform": "Improve sewage treatment, prevent untreated waste discharge, and apply disinfection methods such as chlorination or UV treatment.",
    "pH": "Control industrial effluents and regulate chemical discharge to maintain neutral pH levels.",
    "DO": "Increase aeration, improve water flow, and reduce organic waste inflow.",
    "BOD": "Reduce organic pollution by improving wastewater treatment and limiting domestic and industrial waste discharge."
}


# Define the prediction function
def predict_water_quality(PH, DO, BOD, TotalColiform):
    input_data = pd.DataFrame([[
        PH, DO, BOD, TotalColiform
    ]], columns=[
        'PH',
        'D.O. (mg/l)',
        'B.O.D. (mg/l)',
        'TOTAL COLIFORM (MPN/100ml)Mean'
    ])

    prediction = model.predict(input_data)[0]

    violations = []
    suggestions = []

    if TotalColiform > 50:
        violations.append("Total Coliform > 50")
        suggestions.append(CORRECTION_SUGGESTIONS["Total Coliform"])

    if not (6.5 <= PH <= 8.5):
        violations.append("pH outside 6.5–8.5")
        suggestions.append(CORRECTION_SUGGESTIONS["pH"])

    if DO < 6:
        violations.append("Dissolved Oxygen < 6 mg/l")
        suggestions.append(CORRECTION_SUGGESTIONS["DO"])

    if BOD > 2:
        violations.append("BOD > 2 mg/l")
        suggestions.append(CORRECTION_SUGGESTIONS["BOD"])

    if prediction == 0 and not violations:
        return "Safe", "All parameters are within CPCB safe limits.", []

    return "Polluted", ", ".join(violations), suggestions


# Streamlit App Interface
st.set_page_config(page_title="Water Quality Prediction", layout="centered")

st.title("💧 Water Quality Prediction App")
st.markdown("Enter the water quality parameters to predict if the water is safe or polluted according to CPCB guidelines.")

st.header("Input Parameters")

# Input widgets
ph = st.slider("pH", min_value=0.0, max_value=14.0, value=7.0, step=0.1)
do = st.slider("Dissolved Oxygen (D.O. mg/l)", min_value=0.0, max_value=20.0, value=7.0, step=0.1)
bod = st.slider("Biochemical Oxygen Demand (B.O.D. mg/l)", min_value=0.0, max_value=10.0, value=2.0, step=0.1)
total_coliform = st.slider("Total Coliform (MPN/100ml)", min_value=0, max_value=5000, value=50, step=10)


if st.button("Predict Water Quality"):
    status, reasons, suggestions = predict_water_quality(
        ph, do, bod, total_coliform
    )

    st.subheader("Prediction Result")

    if status == "Safe":
        st.success("✅ Water is SAFE")
        st.info(reasons)
    else:
        st.error("❌ Water is POLLUTED")
        st.warning("Reasons:")
        st.write(reasons)

        st.subheader("Suggested Corrective Actions")
        for i, s in enumerate(suggestions, 1):
            st.write(f"{i}. {s}")
