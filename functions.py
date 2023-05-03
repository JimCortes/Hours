import mysql.connector
import datetime
import streamlit as st


def insert_into_table(conn,table_name, columns, values, where_clause=None):
    mycursor = conn.cursor()
    query = f"INSERT INTO {table_name} ({','.join(columns)}) VALUES ({','.join(['%s' for _ in values])})"
    if where_clause:
        query += f" WHERE {where_clause}"
    mycursor.execute(query, values)
    conn.commit()
    return mycursor.lastrowid 

def customize_query(conn, query):
    mycursor = conn.cursor()
    mycursor.execute(query)
    results = mycursor.fetchall()
    columns = [desc[0] for desc in mycursor.description]
    return [dict(zip(columns, row)) for row in results]


def users(conn):
    query = "select user_name, user, password_hash from users;"
    mycursor = conn.cursor()
    mycursor.execute(query)
    results = mycursor.fetchall()
    users_dict = {}
    for row in results:
        username = row[0]
        user_data = {
            "name": row[1],
            "password": row[2]
        }
        users_dict[username] = user_data
    return {"usernames": users_dict}

def on_change_list():
    if st.session_state["employer1"]:
        st.session_state["employer"] = st.session_state["employer1"]

def on_change_id():
    if st.session_state["employer_push"]:
        st.session_state["employer_id"] = st.session_state["employer_push"]

def on_click_push():
    conn = st.session_state["conn"]
    query = f" select * from time_entries where DATE(start_time) = '{datetime.datetime.now().date()}' and employer_id = '{employer_id}' "
    st.session_state["start_date"] = customize_query(conn, query)
    st.write(st.session_state["start_date"])

       

def get_values(conn, table_name,columns):
    mycursor = conn.cursor()
    query = f"select DISTINCT {','.join(columns)} from {table_name}"
    mycursor.execute(query)
    return [item[0] for item in mycursor.fetchall()]



def today():
    return time.strftime("%A, %B %d")

def check_push_in(conn):
    mydb = conn
    mycursor = mydb.cursor()
    query = f"select start_time from time_entries where start_time == {today()} "
    mycursor.execute(query)
    return mycursor

def update_table(conn,update_query):     
    mycursor = conn.cursor()
    mycursor.execute(update_query)
    conn.commit()


def make_float(value):
    if value is None:
        return 0
    else:
        return float(value) 


def display_time():
    return datetime.datetime.now().strftime("%H:%M")

def delta_metric(initial, last):
    return initial - last


