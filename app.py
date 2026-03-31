import streamlit as st
import numpy as np
import pickle

from auth import register, login
from chatbot import get_response

# ================= PAGE CONFIG =================

st.set_page_config(
    page_title="AI Health Assistant",
    layout="wide"
)

# ================= LOAD MODELS =================

diabetes_model = pickle.load(open("diabetes_model.sav", "rb"))
heart_model = pickle.load(open("heart_model.sav", "rb"))
parkinson_model = pickle.load(open("parkinson_model.sav", "rb"))

# ================= SESSION =================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "chat_open" not in st.session_state:
    st.session_state.chat_open = False

# ================= CSS =================

st.markdown("""
<style>

.main {
    background-color: #0f172a;
}

.header {
    padding: 18px;
    background: linear-gradient(90deg, #2563eb, #1d4ed8);
    color: white;
    text-align: center;
    border-radius: 12px;
    margin-bottom: 25px;
}

.card {
    background-color: #1e293b;
    padding: 25px;
    border-radius: 14px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.4);
    margin-bottom: 20px;
    color: white;
}

section[data-testid="stSidebar"] {
    background-color: #111827;
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

.stButton > button {
    background-color: #2563eb;
    color: white;
    border-radius: 8px;
    font-weight: 600;
}

.chat-box {
    position: fixed;
    bottom: 100px;
    right: 25px;
    width: 340px;
    background-color: #1e293b;
    color: white;
    border-radius: 12px;
    padding: 18px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.5);
}

</style>
""", unsafe_allow_html=True)

# ================= HEADER =================

st.markdown(
    """
    <div class="header">
        <h1>AI Health Assistant</h1>
        <p>Smart Disease Prediction using Artificial Intelligence</p>
    </div>
    """,
    unsafe_allow_html=True
)

# ================= SIDEBAR LOGIN =================

st.sidebar.title("Account")

menu = ["Login", "Register"]
choice = st.sidebar.selectbox("Select Option", menu)

# REGISTER
if choice == "Register":

    st.subheader("Create New Account")

    new_user = st.text_input("Username")
    new_password = st.text_input("Password", type="password")

    if st.button("Register"):
        register(new_user, new_password)
        st.success("Account created successfully")

# LOGIN
elif choice == "Login":

    st.subheader("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        result = login(username, password)

        if result:
            st.session_state.logged_in = True
            st.success("Login successful")

        else:
            st.error("Invalid username or password")

# LOGOUT
if st.session_state.logged_in:

    if st.sidebar.button("Logout"):

        st.session_state.logged_in = False
        st.rerun()

# ================= DASHBOARD =================

if st.session_state.logged_in:

    st.sidebar.title("Disease Prediction")

    selected = st.sidebar.radio(
        "Select Module",
        [
            "Diabetes Prediction",
            "Heart Disease Prediction",
            "Parkinson Prediction"
        ]
    )

    # ================= DIABETES =================

    if selected == "Diabetes Prediction":

        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.header("Diabetes Prediction")

        preg = st.number_input("Pregnancies")
        glucose = st.number_input("Glucose")
        bp = st.number_input("Blood Pressure")
        skin = st.number_input("Skin Thickness")
        insulin = st.number_input("Insulin")
        bmi = st.number_input("BMI")
        age = st.number_input("Age")

        if st.button("Predict Diabetes"):

            input_data = np.array(
                [[preg, glucose, bp, skin, insulin, bmi, age]]
            )

            prediction = diabetes_model.predict(input_data)

            if prediction[0] == 1:
                st.error("⚠️ Person has Diabetes")
            else:
                st.success("✅ Person does not have Diabetes")

        st.markdown('</div>', unsafe_allow_html=True)

    # ================= HEART =================

    elif selected == "Heart Disease Prediction":

        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.header("Heart Disease Prediction")

        age = st.number_input("Age")

        sex = st.selectbox(
            "Sex",
            [0, 1],
            help="0 = Female, 1 = Male"
        )

        cp = st.number_input("Chest Pain Type (0-3)")
        trestbps = st.number_input("Resting Blood Pressure")
        chol = st.number_input("Cholesterol")
        fbs = st.number_input("Fasting Blood Sugar (1 = Yes, 0 = No)")
        restecg = st.number_input("Rest ECG (0-2)")
        thalach = st.number_input("Max Heart Rate")
        exang = st.number_input("Exercise Induced Angina (1/0)")
        oldpeak = st.number_input("ST Depression")
        slope = st.number_input("Slope (0-2)")
        ca = st.number_input("Major Vessels (0-3)")
        thal = st.number_input("Thal (0-3)")

        if st.button("Predict Heart Disease"):

            input_data = np.array([[
                age,
                sex,
                cp,
                trestbps,
                chol,
                fbs,
                restecg,
                thalach,
                exang,
                oldpeak,
                slope,
                ca,
                thal
            ]])

            prediction = heart_model.predict(input_data)

            if prediction[0] == 1:
                st.error("⚠️ Person has Heart Disease")
            else:
                st.success("✅ Person does not have Heart Disease")

        st.markdown('</div>', unsafe_allow_html=True)

    # ================= PARKINSON =================
    elif selected == "Parkinson Prediction":

        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.header("Parkinson Disease Prediction")

        fo = st.number_input("MDVP:Fo(Hz)")
        fhi = st.number_input("MDVP:Fhi(Hz)")
        flo = st.number_input("MDVP:Flo(Hz)")
        jitter_percent = st.number_input("MDVP:Jitter(%)")
        jitter_abs = st.number_input("MDVP:Jitter(Abs)")
        rap = st.number_input("MDVP:RAP")
        ppq = st.number_input("MDVP:PPQ")
        ddp = st.number_input("Jitter:DDP")
        shimmer = st.number_input("MDVP:Shimmer")
        shimmer_db = st.number_input("MDVP:Shimmer(dB)")
        apq3 = st.number_input("Shimmer:APQ3")
        apq5 = st.number_input("Shimmer:APQ5")
        apq = st.number_input("MDVP:APQ")
        dda = st.number_input("Shimmer:DDA")
        nhr = st.number_input("NHR")
        hnr = st.number_input("HNR")
        rpde = st.number_input("RPDE")
        dfa = st.number_input("DFA")
        spread1 = st.number_input("spread1")
        spread2 = st.number_input("spread2")
        d2 = st.number_input("D2")
        ppe = st.number_input("PPE")

        if st.button("Predict Parkinson Disease"):

            input_data = np.array([[
                fo,
                fhi,
                flo,
                jitter_percent,
                jitter_abs,
                rap,
                ppq,
                ddp,
                shimmer,
                shimmer_db,
                apq3,
                apq5,
                apq,
                dda,
                nhr,
                hnr,
                rpde,
                dfa,
                spread1,
                spread2,
                d2,
                ppe
            ]])

            prediction = parkinson_model.predict(input_data)

            if prediction[0] == 1:

                st.error("⚠️ Person has Parkinson Disease")

            else:

                st.success("✅ Person does not have Parkinson Disease")

        st.markdown('</div>', unsafe_allow_html=True)

    # ================= CHAT =================

    if st.button("💬 AI Chat"):
        st.session_state.chat_open = not st.session_state.chat_open

    if st.session_state.chat_open:

        st.markdown(
            """
            <div class="chat-box">
            <h4>AI Health Assistant</h4>
            </div>
            """,
            unsafe_allow_html=True
        )

        user_input = st.text_input("Ask your health question")

        if st.button("Get Answer"):

            response = get_response(user_input)

            st.success(response)

# ================= NOT LOGGED =================

else:

    st.warning(
        "Please login to access the dashboard"
    )

# ================= FOOTER =================

st.markdown("---")

st.caption(
    "Developed by Akash Anand | MCA Final Year Project"
)
