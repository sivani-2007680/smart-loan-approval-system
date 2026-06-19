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


        # ===================== LOAN COMPARISON TOOL (MANUAL INPUT FIXED) =====================

st.markdown("---")
st.subheader("💰 Loan Comparison Tool (HDFC vs Your Loan)")

# ---------------- HDFC RATES ----------------
hdfc_rates = {
    "Short Term (1-2 yrs)": 6.25,
    "Medium Term (2-5 yrs)": 6.45,
    "Long Term (5-10 yrs)": 6.15
}

# ---------------- EMI FUNCTION ----------------
def emi(P, r, years):
    r = r / (12 * 100)
    n = years * 12
    if r == 0:
        return P / n
    return (P * r * (1 + r)**n) / ((1 + r)**n - 1)

# ---------------- GET PRINCIPAL FROM ML FORM ----------------
try:
    principal = loan_amount
except:
    principal = 20000

# ---------------- INPUT SECTION (NO + / - BUTTONS) ----------------

col1, col2 = st.columns(2)

with col1:
    years_input = st.text_input(
        "Loan Tenure (Years)",
        value=str(st.session_state.get("years", 5))
    )

    hdfc_type = st.selectbox(
        "HDFC Rate Type",
        list(hdfc_rates.keys()),
        index=1
    )

with col2:
    custom_rate_input = st.text_input(
        "Your Interest Rate (%)",
        value=str(st.session_state.get("rate", 10.0))
    )

# ---------------- SAFE CONVERSION ----------------
try:
    years = float(years_input)
except:
    years = 5

try:
    custom_rate = float(custom_rate_input)
except:
    custom_rate = 10.0

# ---------------- SAVE STATE ----------------
st.session_state["years"] = years
st.session_state["rate"] = custom_rate

# ---------------- CALCULATIONS ----------------
hdfc_rate = hdfc_rates[hdfc_type]

hdfc_emi = emi(principal, hdfc_rate, years)
user_emi = emi(principal, custom_rate, years)

hdfc_total = hdfc_emi * years * 12
user_total = user_emi * years * 12

# ---------------- DISPLAY ----------------

st.markdown("### 📊 Comparison Result")

col1, col2 = st.columns(2)

with col1:
    st.subheader("🏦 HDFC Bank")
    st.write(f"Rate: {hdfc_rate}%")
    st.metric("EMI", f"₹{hdfc_emi:,.2f}")
    st.metric("Total Payment", f"₹{hdfc_total:,.2f}")

with col2:
    st.subheader("📊 Your Loan")
    st.write(f"Rate: {custom_rate}%")
    st.metric("EMI", f"₹{user_emi:,.2f}")
    st.metric("Total Payment", f"₹{user_total:,.2f}")

# ---------------- RESULT ----------------
diff = user_total - hdfc_total

st.markdown("---")

if diff > 0:
    st.error(f"❌ HDFC is cheaper by ₹{diff:,.2f}")
else:
    st.success(f"🎉 You save ₹{abs(diff):,.2f}")

# ---------------- VISUAL ----------------
st.bar_chart({
    "HDFC": [hdfc_total],
    "Your Loan": [user_total]
})