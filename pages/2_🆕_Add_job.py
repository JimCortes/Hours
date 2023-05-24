import streamlit as st

from functions import get_values, customize_query, insert_into_table



conn = st.session_state["conn"]
today = st.session_state['today'] 
authenticator = st.session_state["authenticator"]

if st.session_state["authentication_status"]:
    authenticator.logout('Logout', 'main')

    st.write(f"### {today.strftime('%A, %B %d, %Y')}")


    with st.form("my_form", clear_on_submit=True):
        employer_name = st.selectbox("Employer", get_values(conn, "employer", ["employer_name"]))
        job_number = st.text_input("Job number", max_chars=255)
        employees = st.number_input("No. Workers", min_value=0, max_value=50, step=1)
        tip = st.number_input('Tip', format="%.2f", min_value=0.00, max_value=1000.00, step=0.01)
        job_description = st.text_input("Coments", max_chars=255)
        submit_button = st.form_submit_button(label="Submit")
        net_tip = tip / employees if employees != 0 else 0


    if submit_button:
        query_id =  f"select employer_id from employer where employer_name = '{employer_name}'"
        employer_id = customize_query(conn,query_id)[0]["employer_id"]
        query = f" select * from time_entries where DATE(start_time) = '{today.date()}' and employer_id = '{employer_id}' "
        times = customize_query(conn,query)
        if len(times) > 0:
            end_date = times[0]["end_time"]
            times_id =  times[0]["time_id"]
            if end_date is None:
                insert_into_table(conn,"jobs",["employer_id", "day_id", "job_number", "employees", "tip", "job_description"],
                                        [employer_id, times_id,job_number, employees,tip,job_description])
                st.success(f"Job {job_number} added tip {tip} for you {net_tip}") 
            else:
                st.error(f"You finished your turn, Nothing added", icon="🚨")       
        
        else:
            st.warning(f"Push in  for {employer_name}", icon='⚠️')
            st.error(f"Nothing added", icon="🚨")
        

else:
     st.warning('Please enter your username and password') 