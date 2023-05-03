import streamlit as st
import datetime
from functions import insert_into_table, display_time, get_values, customize_query,on_change_list, update_table

conn = st.session_state["conn"]
authenticator = st.session_state["authenticator"]

if st.session_state["authentication_status"]:
    authenticator.logout('Logout', 'main')

    with st.container(): 
        employer_names= st.selectbox("Employer", get_values(conn, "employer", ["employer_name"]), on_change=on_change_list, key="employer1")
        st.session_state["employer"] = employer_names 
        query = f"""SELECT employer.employer_name, wage_history.wage, wage_history.start_date, employer.employer_id, id_wage_history
                    FROM employer
                    INNER JOIN wage_history ON employer.employer_id = wage_history.employer_id
                    WHERE employer.employer_name = '{st.session_state["employer"]}'
                    ORDER BY id_wage_history DESC LIMIT 1;"""
        
        employer_id = customize_query(conn, query)[0]['employer_id']
        start_column, wage_column =  st.columns(2)
        with start_column:
            date = customize_query(conn, query)[0]['start_date']
            st.write(f"Last update in {employer_names} was {date.strftime('%Y-%m-%d')}")
        with wage_column:
            current_wage = customize_query(conn, query)[0]['wage']
            id_wage = customize_query(conn, query)[0]['id_wage_history']
            st.write(f"The current wage is: ${current_wage:,.2f}")

    st.write(f" ### Update your wage for {employer_names}")
    with st.form("my_form_docs", clear_on_submit=True):
        end_date = st.date_input("Last date")
        start_date = st.date_input("New start date")
        wage = st.number_input(label="Wage", format="%.2f", min_value=0.00, max_value=100.00, step=0.01)
        update_button = st.form_submit_button(label="Update")



    if update_button:
        update_query = f"UPDATE wage_history SET end_date = '{end_date.strftime('%Y-%m-%d %H:%M:%S')}' WHERE employer_id = {employer_id} and id_wage_history = {id_wage}"
        update_table(conn,update_query)
        st.success("Wage have been update.") 
        insert_into_table(conn,"wage_history",["employer_id",
                                    "start_date, wage",],
                                    [employer_id,start_date,wage])

else:
     st.warning('Please enter your username and password') 