import streamlit as st
import pandas as pd
import numpy as np

# 1. SETUP DATA: 24-hour cycle of a Public Bus System
hours = list(range(24))
# Passenger load spikes during 8am and 5pm (Peak)
passenger_load = [5, 5, 5, 10, 30, 85, 95, 90, 60, 40, 35, 30, 40, 50, 60, 85, 95, 80, 50, 30, 20, 15, 10, 5]
# Shipment demand (packages needing to move)
shipment_demand = [1, 1, 2, 5, 10, 15, 20, 18, 12, 10, 8, 15, 20, 25, 30, 20, 15, 10, 5, 5, 5, 3, 2, 1]

df = pd.DataFrame({
    'Hour': hours,
    'Passenger_Load': passenger_load,
    'Shipment_Demand': shipment_demand
})

# 2. THE AI LOGIC (Time Series Alignment)
# We calculate a 'Cost-Efficiency Index'
# High load = High Cost (Spot pricing / No space)
# Low load = Low Cost (Bulk monthly agreement)
df['Shipping_Cost'] = df['Passenger_Load'].apply(lambda x: 10 if x < 30 else (25 if x < 70 else 60))

# Transit Time Score: High during traffic peaks (morning/evening)
df['Time_Delay_Min'] = [5, 5, 5, 10, 25, 45, 50, 45, 30, 20, 15, 15, 20, 25, 35, 45, 50, 40, 25, 15, 10, 5, 5, 5]

# 3. STREAMLIT DASHBOARD
st.set_page_config(page_title="Logi-Bus Optimizer", layout="wide")
st.title("🚌 Logi-Bus: Cost Leadership AI")
st.write("Aligning **Cargo Demand** with **Bus Capacity** using Multivariate Time Series Logic.")

# Multi-element chart using Streamlit's native engine
st.subheader("Hourly Analysis: Cost vs. Transit Delay")
chart_data = df.set_index('Hour')[['Shipping_Cost', 'Time_Delay_Min']]
st.line_chart(chart_data)

# 4. DECISION ENGINE (The Optimization)
# Find the hour with the lowest cost that also has low delay
optimal_df = df[df['Passenger_Load'] < 40] # Filter for off-peak only
best_row = optimal_df.loc[optimal_df['Time_Delay_Min'].idxmin()]
best_hour = int(best_row['Hour'])

st.divider()

col1, col2 = st.columns(2)
with col1:
    st.metric("Optimal Dispatch Time", f"{best_hour}:00", delta="Off-Peak Window")
    st.write("**Strategy:** Cost Leadership requires using pre-paid 'Void Space'.")

with col2:
    potential_savings = 100 - (best_row['Shipping_Cost'] / df['Shipping_Cost'].max() * 100)
    st.metric("Estimated Cost Savings", f"{int(potential_savings)}%", delta="vs. Traditional Courier")
    st.write("**Impact:** By avoiding peak hours, we reduce variable 'Spot' fees.")

st.success(f"**AI Action Plan:** Direct your couriers to the 'Hub' for the {best_hour}:00 bus. This window provides the lowest cost-per-package while ensuring minimal traffic delay.")
