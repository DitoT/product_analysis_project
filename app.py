import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# Load data
# -----------------------------
users = pd.read_csv("./data/clean_users.csv")
tasks = pd.read_csv("./data/clean_tasks.csv")
events = pd.read_csv("./data/clean_events.csv")
ab = pd.read_csv("./data/clean_ab_test_results.csv")

# Convert dates
users['signup_date'] = pd.to_datetime(users['signup_date'])
tasks['created_at'] = pd.to_datetime(tasks['created_at'])
tasks['completed_at'] = pd.to_datetime(tasks['completed_at'], errors='coerce')
events['event_date'] = pd.to_datetime(events['event_date'])

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("Filters")

# Country filter
countries = users['country'].unique()
selected_country = st.sidebar.multiselect("Country", countries, default=list(countries))

# Device filter
devices = users['device'].unique()
selected_device = st.sidebar.multiselect("Device", devices, default=list(devices))

# Date filter (signup_date)
min_date = users['signup_date'].min()
max_date = users['signup_date'].max()
start_date, end_date = st.sidebar.date_input("Signup Date Range", [min_date, max_date])

# Filter users
filtered_users = users[
    (users['country'].isin(selected_country)) &
    (users['device'].isin(selected_device)) &
    (users['signup_date'].between(pd.to_datetime(start_date), pd.to_datetime(end_date)))
]

# Filter tasks, events, ab test based on filtered users
filtered_tasks = tasks[tasks['user_id'].isin(filtered_users['user_id'])]
filtered_events = events[events['user_id'].isin(filtered_users['user_id'])]
filtered_ab = ab[ab['user_id'].isin(filtered_users['user_id'])]

# -----------------------------
# KPIs
# -----------------------------
st.title("Product Analytics Dashboard")

completion_rate = filtered_tasks['status'].value_counts(normalize=True).get('completed', 0)
avg_duration = filtered_tasks['task_duration_hours'].mean()
active_users = filtered_events['user_id'].nunique()

col1, col2, col3 = st.columns(3)
col1.metric("Completion Rate", f"{completion_rate:.2%}")
col2.metric("Average Task Duration (hours)", f"{avg_duration:.2f}")
col3.metric("Active Users", active_users)

# -----------------------------
# Task Status Distribution (Plotly)
# -----------------------------
st.subheader("Task Status Distribution")
status_counts = filtered_tasks['status'].value_counts().reset_index()
status_counts.columns = ['Status', 'Count']  # Fix column names
fig_status = px.bar(
    status_counts,
    x='Status',
    y='Count',
    title="Tasks by Status",
    text='Count'
)
st.plotly_chart(fig_status, use_container_width=True)

# -----------------------------
# Task Duration Distribution (Plotly)
# -----------------------------
st.subheader("Task Duration Distribution")
fig_duration = px.histogram(
    filtered_tasks,
    x='task_duration_hours',
    nbins=10,
    title="Task Duration Distribution (hours)"
)
st.plotly_chart(fig_duration, use_container_width=True)

# -----------------------------
# A/B Test Analysis (Plotly)
# -----------------------------
st.subheader("A/B Test Conversion Rates")
ab_summary = filtered_ab.groupby('variant')['converted'].mean().reset_index()
ab_summary.columns = ['Variant', 'Conversion']  # Fix column names
ab_summary['Conversion'] = ab_summary['Conversion'] * 100  # percentage
fig_ab = px.bar(
    ab_summary,
    x='Variant',
    y='Conversion',
    text='Conversion',
    title="Conversion Rate by Variant (%)"
)
fig_ab.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
st.plotly_chart(fig_ab, use_container_width=True)

# -----------------------------
# CSV Export
# -----------------------------
st.subheader("Download Filtered Tasks")
@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

csv = convert_df(filtered_tasks)
st.download_button(
    label="Download Filtered Tasks as CSV",
    data=csv,
    file_name='filtered_tasks.csv',
    mime='text/csv'
)

st.success("Dashboard ready! Use filters to explore data dynamically.")
