import streamlit as st
import pandas as pd


# FDA 2005 Guidance Table 1 km factors
FDA_KM = {
    "Human (60 kg)": 37,
    "Mouse": 3,
    "Hamster": 5,
    "Rat": 6,
    "Ferret": 7,
    "Guinea pig": 8,
    "Rabbit": 12,
    "Dog": 20,
    "Monkey (cynomolgus/rhesus)": 12,
    "Marmoset": 6,
    "Squirrel monkey": 7,
    "Baboon": 20,
    "Micro-pig": 27,
    "Mini-pig": 35
}


# -------------------------------
# Calculation functions
# -------------------------------

def hed_km_conversion(animal_dose, species):
    """
    FDA BSA conversion:
    HED = Animal dose × (Km animal / Km human)
    """

    km_animal = FDA_KM[species]
    km_human = FDA_KM["Human (60 kg)"]

    hed = animal_dose * (km_animal / km_human)

    return hed



def hed_weight_formula(animal_dose,
                       animal_weight,
                       human_weight):

    """
    FDA Appendix B formula:

    HED = Animal dose × (Wanimal/Whuman)^0.33
    """

    hed = animal_dose * (
        animal_weight / human_weight
    ) ** 0.33

    return hed



def calculate_mrsd(hed, safety_factor):

    return hed / safety_factor



# -------------------------------
# Streamlit UI
# -------------------------------

st.title(
    "FDA Animal-to-Human Dose Conversion Calculator"
)

st.markdown(
"""
Based on:

**FDA Guidance for Industry (2005)**  
Estimating the Maximum Safe Starting Dose in Initial Clinical Trials

Calculations:
- Body Surface Area (BSA) conversion
- Human Equivalent Dose (HED)
- Maximum Recommended Starting Dose (MRSD)
"""
)


st.sidebar.header("Input Parameters")


animal_species = st.sidebar.selectbox(
    "Animal species",
    list(FDA_KM.keys())[1:]
)


animal_dose = st.sidebar.number_input(
    "Animal dose (mg/kg)",
    min_value=0.001,
    value=10.0
)


method = st.sidebar.radio(
    "Conversion method",
    [
        "FDA BSA (Km factor)",
        "Custom weight formula"
    ]
)


if method == "FDA BSA (Km factor)":

    hed = hed_km_conversion(
        animal_dose,
        animal_species
    )


else:

    animal_weight = st.sidebar.number_input(
        "Animal weight (kg)",
        min_value=0.001,
        value=0.025
    )


    human_weight = st.sidebar.number_input(
        "Human weight (kg)",
        min_value=1.0,
        value=60.0
    )


    hed = hed_weight_formula(
        animal_dose,
        animal_weight,
        human_weight
    )



safety_factor = st.sidebar.number_input(
    "Safety factor",
    min_value=1,
    value=10
)


mrsd = calculate_mrsd(
    hed,
    safety_factor
)



# -------------------------------
# Results
# -------------------------------

st.header("Results")


col1, col2, col3 = st.columns(3)


with col1:
    st.metric(
        "Animal dose",
        f"{animal_dose:.3f} mg/kg"
    )


with col2:
    st.metric(
        "Human Equivalent Dose (HED)",
        f"{hed:.3f} mg/kg"
    )


with col3:
    st.metric(
        "MRSD",
        f"{mrsd:.3f} mg/kg"
    )



st.divider()


st.subheader("Human Dose Example")


human_weight = st.number_input(
    "Human body weight (kg)",
    value=60.0
)


total_mg = mrsd * human_weight


st.write(
    f"""
Maximum starting amount:

**{total_mg:.2f} mg total**

for a {human_weight:.1f} kg human
"""
)



# -------------------------------
# Injection calculator
# -------------------------------

st.divider()

st.header("Injection Volume Calculator")


drug_concentration = st.number_input(
    "Drug concentration (mg/mL)",
    value=1.0
)


volume = total_mg / drug_concentration


st.success(
    f"Injection volume = {volume:.3f} mL"
)



# -------------------------------
# Reference table
# -------------------------------

st.divider()

st.subheader("FDA Km Conversion Table")


df = pd.DataFrame(
    FDA_KM.items(),
    columns=[
        "Species",
        "Km factor"
    ]
)


st.dataframe(df)
