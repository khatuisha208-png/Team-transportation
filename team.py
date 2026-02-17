import streamlit as st
import pandas as pd
import numpy as np

# 1. PAGE SETUP & THEME
st.set_page_config(page_title="Responsive Logistics Sim", layout="wide")
st.title("⚡ Responsive State-Wide Logistics Strategy")
st.markdown("_Strategy: Maximizing Throughput via Opportunistic Capacity Harvesting_")
# 2. STRATEGIC INPUTS
with st.container():
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("📡 Demand (Pull Signal)")
        avg_orders = st.slider("Daily Demand Volume", 100, 5000, 1200)
        vol_per_pkg = st.number_input("Average Pkg Vol (ft³)", value=0.8)
        
    with col2:
        st.subheader("🚌 Response Fleet")
        total_buses = st.slider("Total Daily Bus Trips", 50, 1000, 300)
        avg_empty_space = st.slider("Avg Empty Vol per Bus", 5, 50, 20)
        
    with col3:
        st.subheader("💰 Lean Financials")
        license_fee_q = st.number_input("Quarterly Govt Fee (₹)", value=750000)
        rev_per_pkg = st.number_input("Service Fee (₹/pkg)", value=100)

# 3. RESPONSIVE ENGINE (The logic of 'Catching the Window')
data = []
backlog = 0
total_shipped = 0
total_revenue = 0

for d in range(1, 91): # 90 Day Quarter
    # 1. Demand Arrival
    daily_inflow = np.random.poisson(avg_orders)
    backlog += daily_inflow
    
    # 2. Capacity Discovery (Responsive Strategy doesn't know capacity until it arrives)
    # We simulate that bus capacity changes every single day based on passenger load
    daily_capacity_ft3 = total_buses * np.random.uniform(avg_empty_space * 0.4, avg_empty_space)
    max_ship_qty = int(daily_capacity_ft3 / vol_per_pkg)
    
    # 3. The Responsive Action
    shipped_today = min(backlog, max_ship_qty)
    backlog -= shipped_today
    total_shipped += shipped_today
    total_revenue += (shipped_today * rev_per_pkg)
    
    # 4. Measure Response Speed (Daily Backlog / Avg Inflow)
    # Higher number means slower response (backlog building up)
    response_delay = backlog / avg_orders if avg_orders > 0 else 0
    
    data.append({
        "Day": d,
        "Backlog": backlog,
        "Response Delay (Days)": response_delay,
        "Daily Revenue": shipped_today * rev_per_pkg
    })

df = pd.DataFrame(data)

# 4. RESPONSIVE DASHBOARD
st.divider()
kpi1, kpi2, kpi3 = st.columns(3)

# Strategic Metric: Quarterly Net
q_profit = total_revenue - license_fee_q - (total_shipped * 5) # Subtracting handling
kpi1.metric("Quarterly Net Profit", f"₹{q_profit:,.0f}")

# Strategic Metric: Agility
avg_delay = df["Response Delay (Days)"].mean()
kpi2.metric("Avg Response Time", f"{round(avg_delay * 24, 1)} Hours", delta_color="inverse")

# Strategic Metric: Coverage
kpi3.metric("Fleet Utilization", f"{round((total_shipped / (total_buses * avg_empty_space/vol_per_pkg * 90))*100, 1)}%")

# Visualizing Agility
st.subheader("📈 Response Agility: Station Backlog over Time")
st.area_chart(df.set_index("Day")["Backlog"])

st.subheader("⏱️ Responsiveness (Wait Time at Hubs)")
# A flat line means high responsiveness. A rising line means the strategy is failing.
st.line_chart(df.set_index("Day")["Response Delay (Days)"])
