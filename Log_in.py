import streamlit as st
from time import sleep
from navigation import make_sidebar

make_sidebar()

st.title("Welcome to Dashboard -- Tanzania Organizational Effectiveness Survey")

st.write("Please log in to continue.")

username = st.text_input("Username")
password = st.text_input("Password", type="password")


if st.button("Log in", type="primary"):
    if username == "cghpi-tanzania" and password in ['NACP', 'NTLP', 'NMCP', 'RSSH']:
        st.session_state.logged_in = True
        st.success("Logged in successfully!")
        st.session_state['password'] = password
        # Navigate to the score filtering page
        #st.experimental_rerun()
        sleep(0.5)
        st.switch_page("pages/1-Introduction.py")
    else:
        st.error("Incorrect username or password")
