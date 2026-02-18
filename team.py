import streamlit as st
import pandas as pd
import numpy as np

# Simulate 24 hours of Bus Data
# 'Passenger_Load': 0 (empty) to 100 (full)
# 'Shipment_Demand': Number of packages waiting
hours = list(range(24))
passenger_load = [10, 5, 5, 20, 60, 95, 80, 50, 40, 35, 30, 45, 55, 60, 85, 90, 70, 40, 30, 20, 15, 10, 5, 5]
shipment_demand = [2, 1, 5, 10, 15, 20, 18, 12, 10, 8, 15, 20, 25, 30, 20, 15, 10, 5, 5, 5, 3, 2, 1, 1]

df = pd.DataFrame({
    'Hour': hours,
    'Passenger_Load': passenger_load,
    'Shipment_Demand': shipment_demand
})

# Logic: Calculate 'Shipping_Cost' based on Bus Fullness
# Cost Leadership Strategy: We pay a penalty for shipping during peak hours
df['Calculated_Cost'] = df['Passenger_Load'].apply(lambda x: 1.0 if x < 40 else (2.5 if x < 75 else 5.0))

# Logic: Calculate 'Transit_Time_Score' (Traffic during day increases time)
df['Time_Efficiency'] = [90, 95, 95, 80, 60, 40, 50, 70, 80, 85, 90, 85, 75, 65, 50, 40, 60, 80, 90, 95, 95, 95, 95, 95]

st.title("🚌 Logi-Bus: Cost & Time Optimizer")
st.write("This AI model aligns **Shipment Demand** with **Bus Capacity** to find the cheapest windows.")

# Display Cost vs Time Graph
st.line_chart(df.set_index('Hour')[['Calculated_Cost', 'Time_Efficiency']])

# Strategy Selection
st.subheader("Strategy Recommendation")
best_hour = df[df['Calculated_Cost'] == df['Calculated_Cost'].min()]['Time_Efficiency'].idxmax()

st.success(f"""
**AI Optimization Result:** * **Target Window:** {best_hour}:00 - {best_hour+2}:00
* **Why:** This window has the lowest **Passenger Load** (Cost Leadership) while maintaining high **Time Efficiency**.
* **Action:** Direct couriers to consolidate all morning shipments for the {best_hour}:00 bus.
""")
