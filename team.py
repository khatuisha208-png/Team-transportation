import streamlit as st
import pandas as pd
import numpy as np

# 1. SETUP
st.set_page_config(page_title="Responsive Startup Sim", layout="wide")
st.title("🚀 Strategic Logistics: Cost Leadership + Responsiveness")

# 2. STRATEGY CONTROLS
st.sidebar.header("Strategy Settings")
# How 'Aggressive' are we at catching every bus?
response_aggression = st.sidebar.slider("Responsiveness (Bus Catching Rate %)", 50, 100, 90)

col1, col2, col3 = st.columns(3)
with col1:
    avg_orders = st.number_input("Average Daily Orders", value=1000)
with col2:
    num_buses = st.number_input("Buses passing Hub per Day", value=150)
with col3:
    bus_capacity_pkg = st.number_input("Avg Slack Space (Packages/Bus)", value=10)

# 3. ENGINE: MEASURING DWELL TIME
data = []
inventory = [] # List to track 'age' of each package for responsiveness
backlog_count = 0
total_shipped = 0

for day in range(1, 31):
    # New Arrivals
    new_pkgs = np.random.poisson(avg_orders)
    backlog_count += new_pkgs
    
    # Calculate Today's Available 'Hitchhiker' Capacity
    # We factor in our 'Aggression' (Responsiveness)
    available_slots = num_buses * bus_capacity_pkg * (response_aggression / 100)
    # Adding some randomness to bus availability
    available_slots = int(available_slots * np.random.uniform(0.7, 1.2))
    
    # Shipment Action
    shipped = min(backlog_count, available_slots)
    backlog_count -= shipped
    total_shipped += shipped
    
    # Calculate Dwell Time (Simple proxy: Backlog / Daily Capacity)
    dwell_time_hrs = (backlog_count / max(1, available_slots)) * 24
    
    data.append({
        "Day": day,
        "Backlog": backlog_count,
        "Hours of Delay": dwell_time_hrs,
        "Throughput": shipped
    })

df = pd.DataFrame(data)

# 4. DASHBOARD
st.divider()
k1, k2, k3 = st.columns(3)
k1.metric("Total Throughput", f"{total_shipped:,} Pkgs")
k2.metric("Avg. Response Delay", f"{round(df['Hours of Delay'].mean(), 1)} Hours")
k3.metric("Cost Efficiency", "MAX (Shared Asset Model)")

st.subheader("Response Speed (Wait Time at Bus Stand)")
st.line_chart(df.set_index("Day")["Hours of Delay"])

st.subheader("Inventory Pressure (Backlog)")
st.area_chart(df.set_index("Day")["Backlog"])
