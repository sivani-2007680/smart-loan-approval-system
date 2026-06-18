import streamlit as st
import pandas as pd
import joblib

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Smart Loan Approval Predictor",
    page_icon="🏦",
    layout="wide"
)

# ---------------- LOAD MODEL ----------------

model = joblib.load("loan_model.pkl")
scaler = joblib.load("scaler.pkl")

# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>

.main {
    padding-top: 1rem;
}

.stButton > button {
    width: 100%;
    height: 60px;
    font-size: 22px;
    font-weight: bold;
    border-radius: 12px;
}

.block-container {
    padding-top: 1rem;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------

st.markdown("""
# 🏦 Smart Loan Approval Predictor

Predict loan approval using Machine Learning.

Fill in the details below and click **Check Eligibility**.
""")

# ---------------- SIDEBAR ----------------

st.sidebar.title("📌 About")

st.sidebar.info("""
Built Using:

✅ Streamlit  
✅ Scikit-Learn  
✅ Gaussian Naive Bayes  
✅ Python  

Created by Sivani
""")

# ---------------- FORM ----------------

with st.form("loan_form"):

    st.subheader("👤 Personal Information")

    col1, col2 = st.columns(2)

    with col1:
        age = float(st.text_input("Age", "30"))
        dependents = float(st.text_input("Dependents", "1"))

        gender = st.selectbox(
            "Gender",
            ["Female", "Male"]
        )

        marital_status = st.selectbox(
            "Marital Status",
            ["Married", "Single"]
        )

        education = st.selectbox(
            "Education Level",
            ["No", "Yes"]
        )

    with col2:

        employment_status = st.selectbox(
            "Employment Status",
            [
                "Contract",
                "Salaried",
                "Self-employed",
                "Unemployed"
            ]
        )

        employer_category = st.selectbox(
            "Employer Category",
            [
                "Business",
                "Government",
                "MNC",
                "Private",
                "Unemployed"
            ]
        )

        property_area = st.selectbox(
            "Property Area",
            [
                "Rural",
                "Semiurban",
                "Urban"
            ]
        )

    st.subheader("💰 Financial Information")

    col3, col4 = st.columns(2)

    with col3:

        applicant_income = float(
            st.text_input("Applicant Income", "10000")
        )

        coapplicant_income = float(
            st.text_input("Coapplicant Income", "5000")
        )

        savings = float(
            st.text_input("Savings", "50000")
        )

        collateral_value = float(
            st.text_input("Collateral Value", "100000")
        )

    with col4:

        loan_amount = float(
            st.text_input("Loan Amount", "20000")
        )

        loan_term = float(
            st.text_input("Loan Term (Months)", "12")
        )

        existing_loans = float(
            st.text_input("Existing Loans", "0")
        )

    st.subheader("📊 Credit Details")

    credit_score = st.slider(
        "Credit Score",
        300,
        900,
        700
    )

    dti_ratio = st.slider(
        "Debt-To-Income Ratio",
        0.0,
        1.0,
        0.30,
        0.01
    )

    loan_purpose = st.selectbox(
        "Loan Purpose",
        [
            "Business",
            "Car",
            "Education",
            "Home",
            "Personal"
        ]
    )

    submitted = st.form_submit_button(
        "🔍 Check Eligibility"
    )

# ---------------- PREDICTION ----------------

if submitted:

    Education_Level = 1 if education == "Yes" else 0

    Employment_Status_Salaried = 1 if employment_status == "Salaried" else 0
    Employment_Status_Self_employed = 1 if employment_status == "Self-employed" else 0
    Employment_Status_Unemployed = 1 if employment_status == "Unemployed" else 0

    Marital_Status_Single = 1 if marital_status == "Single" else 0

    Loan_Purpose_Car = 1 if loan_purpose == "Car" else 0
    Loan_Purpose_Education = 1 if loan_purpose == "Education" else 0
    Loan_Purpose_Home = 1 if loan_purpose == "Home" else 0
    Loan_Purpose_Personal = 1 if loan_purpose == "Personal" else 0

    Property_Area_Semiurban = 1 if property_area == "Semiurban" else 0
    Property_Area_Urban = 1 if property_area == "Urban" else 0

    Gender_Male = 1 if gender == "Male" else 0

    Employer_Category_Government = 1 if employer_category == "Government" else 0
    Employer_Category_MNC = 1 if employer_category == "MNC" else 0
    Employer_Category_Private = 1 if employer_category == "Private" else 0
    Employer_Category_Unemployed = 1 if employer_category == "Unemployed" else 0

    DTI_Ratio_sq = dti_ratio ** 2
    Credit_Score_sq = credit_score ** 2

    data = [[
        applicant_income,
        coapplicant_income,
        age,
        dependents,
        existing_loans,
        savings,
        collateral_value,
        loan_amount,
        loan_term,
        Education_Level,
        Employment_Status_Salaried,
        Employment_Status_Self_employed,
        Employment_Status_Unemployed,
        Marital_Status_Single,
        Loan_Purpose_Car,
        Loan_Purpose_Education,
        Loan_Purpose_Home,
        Loan_Purpose_Personal,
        Property_Area_Semiurban,
        Property_Area_Urban,
        Gender_Male,
        Employer_Category_Government,
        Employer_Category_MNC,
        Employer_Category_Private,
        Employer_Category_Unemployed,
        DTI_Ratio_sq,
        Credit_Score_sq
    ]]

    data_scaled = scaler.transform(data)

    prediction = model.predict(data_scaled)

    probability = model.predict_proba(data_scaled)[0][1]

    st.subheader("📈 Prediction Result")

    st.metric(
        "Approval Probability",
        f"{probability*100:.2f}%"
    )

    st.progress(float(probability))

    if prediction[0] == 1:

        st.success("🎉 Loan Approved")

        st.balloons()

    else:

        st.error("❌ Loan Rejected")