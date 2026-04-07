import streamlit as st

st.title("Antibody Injection Volume Calculator")

st.markdown("Calculate injection volume based on dose, mouse weight, and antibody concentration.")


weight_g = st.number_input("Mouse weight (grams)", min_value=0.1, value=10.0)
dose_mg_per_kg = st.number_input("Dose (mg/kg)", min_value=0.0, value=15.0)
stock_conc = st.number_input("Stock concentration (mg/mL)", min_value=0.0, value=1.0)

use_dilution = st.checkbox("Use diluted working concentration?")

if use_dilution:
    working_conc = st.number_input("Working concentration (mg/mL)", min_value=0.0, value=0.5)
else:
    working_conc = stock_conc


weight_kg = weight_g / 1000
dose_mg = dose_mg_per_kg * weight_kg

if working_conc > 0:
    volume_ml = dose_mg / working_conc
    volume_ul = volume_ml * 1000
else:
    volume_ml = 0
    volume_ul = 0


st.subheader("Results")
st.write(f"Required dose: **{dose_mg:.4f} mg**")
st.write(f"Injection volume: **{volume_ul:.1f} µL**")


if use_dilution and stock_conc > 0:
    dilution_factor = stock_conc / working_conc
    st.write(f"Dilution factor: **{dilution_factor:.2f}x**")
