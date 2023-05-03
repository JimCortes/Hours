import streamlit as st
import datetime
from functions import insert_into_table, display_time

conn = st.session_state["conn"]

authenticator = st.session_state["authenticator"]

if st.session_state["authentication_status"]:
    authenticator.logout('Logout', 'main')
    with st.form("my_form", clear_on_submit=True):
        employer_name = st.text_input("Name", max_chars=255)
        employer_description = st.text_input("Description", max_chars=255)
        start_date = st.date_input("start date")
        wage = st.number_input(label="Wage", format="%.2f", min_value=0.00, max_value=100.00, step=0.01)
        submit_button = st.form_submit_button(label="Submit")

    if submit_button:
        employer_id = insert_into_table(conn,"employer",
                                    ["employer_name","employer_description"],
                                    [employer_name,employer_description])
        insert_into_table(conn,"wage_history",["employer_id",
                                    "start_date, wage"],
                                    [employer_id,start_date,wage])
        st.success("Employer and wage information saved successfully.")
else:
     st.warning('Please enter your username and password') 