import streamlit as st
import datetime
import mysql.connector
import streamlit_authenticator as stauth
import bcrypt
from functions import insert_into_table, display_time, get_values, customize_query, on_change_id, update_table, users
import os
from dotenv import load_dotenv


load_dotenv()

db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('db_host')
database = os.getenv('DB_NAME')



conn = mysql.connector.connect(user=db_user, password=db_password,
                              host=db_host, database=database)
st.session_state["conn"] = conn
st.session_state["authenticator"] = False
today = datetime.datetime.now()
st.session_state['today'] = today
st.session_state["time_id"] = None
credentials = users(conn)


#st.write(bcrypt.hashpw('pwd1'.encode(), bcrypt.gensalt()).decode())

authenticator = stauth.Authenticate(credentials, "hours_times", "abcdet", cookie_expiry_days= 1)



name, authentication_status, username = authenticator.login('Login', 'main')


if st.session_state["authentication_status"]:
    st.session_state["authenticator"] = authenticator
 
    authenticator.logout('Logout', 'main')
    st.write(f'#### Hi, *{st.session_state["name"]}*')
  
    employer_choice = st.selectbox("Employer", get_values(conn, "employer", ["employer_name"]),on_change=on_change_id,key="employer_push")
    st.session_state["employer_id"] = employer_choice

    query_id =  f"select employer_id from employer where employer_name = '{employer_choice}'"
    employer_id = customize_query(conn,query_id)[0]["employer_id"]



    query = f" select * from time_entries where DATE(start_time) = '{today.date()}' and employer_id = '{employer_id}' "
    times = customize_query(conn,query)



    st.write(f"### {today.strftime('%A, %B %d, %Y')}")
    with st.container():
        push_in, push_out = st.columns(2)
        with push_in:
            st.write("#### Start Time")
            if len(times) > 0:
                start_date = times[0]["start_time"]
                st.write(start_date.strftime('%H:%M'))
            else:
                push_in_button = st.button(label="Start")
                st.write(f"#### Manual start")
                start_hour = st.number_input(label="Hour", min_value=0, max_value=23, step=1)
                start_minute =  st.number_input(label="Minutes", min_value=0, max_value=59, step=1)
                manual_push_in_button = st.button(label="Manual Start")
                
                if push_in_button:
                    insert_into_table(conn,"time_entries",["employer_id","start_time"],[employer_id,datetime.datetime.now()])
                    st.experimental_rerun()
                if manual_push_in_button:
                    insert_into_table(conn,"time_entries",["employer_id","start_time"],[
                                    employer_id,datetime.datetime(today.year, today.month, today.day, start_hour, start_minute)])
                    st.experimental_rerun()
                

        with push_out:
            st.write("#### End Day")
            if len(times) > 0:
                end_date = times[0]["end_time"]
                if end_date is None:    
                    push_out_button = st.button(label="End")
                    st.write(f"#### Manual end")
                    end_hour = st.number_input(label="Hours", min_value=0, max_value=23, step=1)
                    end_minute =  st.number_input(label="Minute", min_value=0, max_value=59, step=1)
                    manual_push_out_button = st.button(label="Manual End")
                    
                    if push_out_button:
                        update_query = f"UPDATE time_entries SET end_time = '{datetime.datetime.now()}' WHERE employer_id = '{employer_id}' and Date(start_time) = '{today.date()}'"
                        update_table(conn,update_query)
                        st.experimental_rerun()
                    if manual_push_out_button:
                        update_query = f"UPDATE time_entries SET end_time = '{datetime.datetime(today.year, today.month, today.day, end_hour, end_minute)}' WHERE employer_id = '{employer_id}' and Date(start_time) = '{today.date()}'"
                        update_table(conn,update_query)
                        st.experimental_rerun()
                else:
                    st.write(end_date.strftime('%H:%M'))

elif st.session_state["authentication_status"] == False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] == None:
    st.warning('Please enter your username and password')






