import streamlit as st
import datetime
from functions import get_values, on_change_id, customize_query, make_float, delta_metric
from dateutil.relativedelta import relativedelta
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

conn = st.session_state["conn"]
today = st.session_state['today'] 
time_id = st.session_state["time_id"]
start_month = today.replace(day=1)
st.set_page_config(initial_sidebar_state='expanded')

authenticator = st.session_state["authenticator"]

if st.session_state["authentication_status"]:
    authenticator.logout('Logout', 'main')
    st.sidebar.header("Data")

    selected_options = st.sidebar.selectbox('Select Employer:',get_values(conn, "employer",["employer_name"]))

    query =  f"select employer_id from employer where employer_name = '{selected_options}'"
    employer_id = customize_query(conn,query)[0]["employer_id"]
    month_earlier = start_month - relativedelta(months=1)
    month_later = today - relativedelta(months=1)

    query_sum = f"SELECT SUM(total_hours) as total_hours, SUM(first_8_hours) as first_8, SUM(after_8_hours) as last_8  FROM working_hours WHERE employer_id = '{employer_id}' AND start_time >= '{start_month}' AND start_time < '{today}';"
    hours = customize_query(conn,query_sum)
    total_hours =  make_float(hours[0]['total_hours'])
    normal_hours = make_float(hours[0]['first_8'])
    extra_hours = make_float(hours[0]['last_8'])

    query_sum_last = f"SELECT SUM(total_hours) as total_hours, SUM(first_8_hours) as first_8, SUM(after_8_hours) as last_8  FROM working_hours WHERE employer_id = '{employer_id}' AND start_time >= '{month_earlier}' AND start_time < '{month_later}';"
    hours_earlier = customize_query(conn,query_sum_last)
    e_total_hours =  make_float(hours_earlier[0]['total_hours'])
    e_normal_hours = make_float(hours_earlier[0]['first_8'])
    e_extra_hours = make_float(hours_earlier[0]['last_8'])


    query_times = f" select * from time_entries where DATE(start_time) = '{today.date()}' and employer_id = '{employer_id}' "
    times_return = customize_query(conn,query_times)

    if not times_return:
        no_job = 0 
        tips = 0
    else:       
        time_ids = customize_query(conn,query_times)[0]["time_id"]
        query_jobs = f"select count(job_id) as jobs, sum(tip) as tips from jobs WHERE employer_id = '{employer_id}' and day_id = '{time_ids}'"
        jobs= customize_query(conn,query_jobs)
        no_job= jobs[0]["jobs"]
        tips = jobs[0]["tips"]


  
    ## Creating Graphs
    labels = ["Regular", "Overtime"]

    # Create subplots: use 'domain' type for Pie subplot
    fig = make_subplots(rows=1, cols=1, specs=[[{'type':'domain'}]])
    fig.add_trace(go.Pie(labels=labels, values=[normal_hours,extra_hours], name="Working Hours"),1, 1)
    # Use `hole` to create a donut-like pie chart
    fig.update_traces(hole=.5, hoverinfo="label+percent+name")

    fig.update_layout(
        title_text="",
        # Add annotations in the center of the donut pies.
        annotations=[dict(text='Working Time', x=0.5, y=0.5, font_size=18, showarrow=False)])

   

    query_graph = f"SELECT start_time,total_hours, first_8_hours, after_8_hours  FROM working_hours WHERE employer_id = '{employer_id}' AND start_time >= '{start_month}' group by Date(start_time);"
    data_query = customize_query(conn,query_graph)
    data = pd.DataFrame(data_query,dtype=float)
    
    st.write(f"### Today stats")
    st.write(f"{today.strftime('%A, %B %d, %Y')}")
 
        
    if data.empty:
        pass
    else:
        data["start_time"] = pd.to_datetime(data["start_time"]).dt.date
        fig1 = go.Figure(data=[
                go.Bar(x=data["start_time"], y=data["first_8_hours"], name="Regular"),
                go.Bar(x=data["start_time"], y=data["after_8_hours"], name="Extra")],
                layout_title_text="Daily hours",)

        fig1.update_layout(barmode='stack', xaxis=dict(type='date',tickformat='%d %b %Y'))

        with st.container():
            d_jobs,d_tips = st.columns(2)
            with d_jobs:
                st.metric(label="Number of Jobs", value=f"{no_job:,.0f}")
            with d_tips:
                st.metric(label="Tips", value=f"${tips:,.2f}")

        st.write(fig1)
  

    st.write(f"### Monthly stats")
    st.write(f"From {start_month.strftime('%A, %B %d, %Y')} to {today.strftime('%A, %B %d, %Y')}")

    with st.container():
        today,monthly, yearly = st.columns(3)
        with today:
            st.metric(label="Total hours", value=f"{total_hours:,.2f}", delta=delta_metric(total_hours, e_total_hours))
        with monthly:
            st.metric(label="Normal", value=f"{normal_hours:,.2f}", delta=delta_metric(normal_hours, e_normal_hours))
        with yearly:
            st.metric(label="Extra", value=f"{extra_hours:,.2f}", delta=delta_metric(extra_hours, e_extra_hours))
    with st.container():
        st.write(fig)
    
else:
     st.warning('Please enter your username and password') 