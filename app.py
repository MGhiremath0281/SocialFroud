import streamlit as st
from utils.otp_auth import send_email_otp, send_sms_otp, verify_otp
from utils.insta_scraper import get_profile_data
from utils.fraud_logic import is_suspicious
from utils.alert import send_alerts

# Page Config
st.set_page_config(
    page_title="Insta Fraud Detector",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for aesthetics (natural colors)
st.markdown("""
    <style>
    .title { color: #2c3e50; font-size: 36px; font-weight: 700; text-align: center; margin-bottom: 20px; }
    .step { font-size: 24px; font-weight: 600; margin-top: 30px; color: #34495e; }
    .info-box { border-radius: 10px; padding: 15px; background-color: #ecf0f1; color: #2c3e50; margin-bottom: 20px; }
    div.stButton > button {
        background-color: #2980b9;
        color: white;
        padding: 10px 24px;
        border-radius: 8px;
        font-weight: 600;
        border: none;
        transition: background-color 0.3s ease;
    }
    div.stButton > button:hover {
        background-color: #1f6391;
        cursor: pointer;
    }
    </style>
""", unsafe_allow_html=True)

# Rerun workaround function for Streamlit versions without experimental_rerun()
def rerun():
    # Update query params to force rerun
    st.experimental_set_query_params = None  # disable old function if present
    current_params = st.session_state.get('query_params', {})
    # Setting a unique param to trigger rerun
    st.experimental_set_query_params = None
    st.session_state['rerun_key'] = st.session_state.get('rerun_key', 0) + 1
    st.experimental_set_query_params = None
    st.session_state.query_params = {"_rerun": st.session_state['rerun_key']}
    st.experimental_rerun = None
    # Use new st.query_params method to update parameters
    st.query_params.update({"_rerun": str(st.session_state['rerun_key'])})

# Actually, Streamlit's st.query_params is a dict-like object:
# You can assign to it directly like this:
def rerun():
    rerun_key = st.session_state.get("rerun_key", 0) + 1
    st.session_state["rerun_key"] = rerun_key
    st.query_params = {"_rerun": str(rerun_key)}

# Initialize session state
if 'verified' not in st.session_state:
    st.session_state.verified = False
if 'email' not in st.session_state:
    st.session_state.email = ""
if 'phone' not in st.session_state:
    st.session_state.phone = ""

st.markdown('<p class="title">Insta Fraud Detector</p>', unsafe_allow_html=True)

if not st.session_state.verified:
    st.markdown('<p class="step">Step 1: Verify Your Identity</p>', unsafe_allow_html=True)
    with st.form("otp_form"):
        st.markdown('<div class="info-box">Enter your email and phone to receive an OTP.</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        email = col1.text_input("Email")
        phone = col2.text_input("Phone Number (with country code, e.g. +1234567890)")

        submitted_otp_request = st.form_submit_button("Send OTP")

        if submitted_otp_request:
            if not email or not phone:
                st.error("Both email and phone number are required.")
            elif not phone.startswith('+'):
                st.error("Phone number must include country code and start with '+'.")
            else:
                st.session_state.email = email
                st.session_state.phone = phone
                try:
                    send_email_otp(email)
                    send_sms_otp(phone)
                    st.success("OTPs sent! Check your inbox and SMS.")
                except Exception as e:
                    st.error(f"Failed to send OTP: {e}")

    if st.session_state.email and st.session_state.phone:
        otp = st.text_input("Enter OTP")
        if st.button("Verify OTP"):
            try:
                if verify_otp(st.session_state.email, otp) or verify_otp(st.session_state.phone, otp):
                    st.session_state.verified = True
                    st.success("Verification successful!")
                    rerun()
                else:
                    st.error("Invalid OTP. Please try again.")
            except Exception as e:
                st.error(f"OTP verification failed: {e}")

else:
    st.markdown('<p class="step">Step 2: Enter Instagram Username</p>', unsafe_allow_html=True)
    username = st.text_input("Instagram Username")
    if st.button("Check Profile"):
        if username:
            with st.spinner("Fetching profile data..."):
                profile = get_profile_data(username)
            if profile is None:
                st.warning(f"Could not fetch profile for '{username}'. It might be private or does not exist.")
            elif profile.get("is_private", False):
                st.info(f"The profile '{username}' is private. Unable to perform fraud analysis.")
            else:
                is_fraud, reasons = is_suspicious(profile)
                send_alerts(st.session_state.email, st.session_state.phone, username, is_fraud)

                st.subheader("Profile Analysis Result:")
                st.json(profile)
                if is_fraud:
                    st.error("Suspicious Profile Detected!")
                    st.write("Reasons:")
                    for reason in reasons:
                        st.write(f"- {reason}")
                else:
                    st.success("This profile appears legitimate.")
        else:
            st.warning("Please enter a username.")
