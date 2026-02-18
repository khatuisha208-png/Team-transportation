import streamlit as st
import pandas as pd
import numpy as np

# --- PAGE CONFIG ---
st.set_page_config(page_title="TransitFreight AI", layout="wide")

st.title("🚌 TransitFreight: AI-Driven Logistics")
st.markdown("### Bulletproof Dynamic Pricing Model (Native Framework)")

# --- SIDEBAR: VARIABLES ---
st.sidebar.header("📦 Package & Bus Settings")
n_boxes = st.sidebar.slider("Number of Boxes", 1, 100, 30)
avg_weight = st.sidebar.number_input("Avg Weight (kg)", value=5.0)
avg_vol = st.sidebar.number_input("Avg Volume (L)", value=10.0)
bus_capacity = st.sidebar.slider("Bus Hold Capacity (L)", 100, 1000, 500)

st.sidebar.header("💰 Financials")
base_fee = st.sidebar.number_input("Base Handling Fee ($)", value=10.0)
op_cost_per_box = st.sidebar.number_input("Op Cost/Box ($)", value=3.0)
bus_cut_pct = st.sidebar.slider("Bus Partner Cut (%)", 0, 100, 35)

# --- PRICING LOGIC ---
def get_metrics(n, w, v, cap):
    total_v = n * v
    utilization = min(total_v / cap, 1.0)
    
    # Base Price calculation
    unit_base = base_fee + (w * 1.5) + (v * 0.4)
    
    # Simple Surge Multiplier
    if utilization < 0.5:
        surge = 1.0
    else:
        # Increase price as capacity fills up
        surge = 1.0 + (utilization - 0.5) * 4 
    
    final_unit_price = unit_base * surge
    rev = final_unit_price * n
    cost = (op_cost_per_box * n) + (rev * (bus_cut_pct / 100))
    prof = rev - cost
    
    return round(final_unit_price, 2), round(prof, 2), round(utilization * 100, 1)

# --- EXECUTION ---
u_price, u_profit, u_util = get_metrics(n_boxes, avg_weight, avg_vol, bus_capacity)

# --- KPI DISPLAY ---
col1, col2, col3 = st.columns(3)
col1.metric("Price / Box", f"${u_price}")
col2.metric("Total Profit", f"${u_profit:,.2f}")
col3.metric("Capacity Used", f"{u_util}%")

st.divider()

# --- CHART 1: PROFIT SCALING (Native Line Chart) ---
st.subheader("📈 Profit Growth vs. Number of Boxes")
st.write("Notice how profit accelerates as the bus fills up (Dynamic Pricing Effect).")

box_counts = range(1, 101)
scaling_data = []
for b in box_counts:
    _, p, _ = get_metrics(b, avg_weight, avg_vol, bus_capacity)
    scaling_data.append(p)

# Streamlit Native Line Chart
chart_df = pd.DataFrame(scaling_data, index=box_counts, columns=["Net Profit ($)"])
st.line_chart(chart_df)

# --- CHART 2: WEEKLY FORECAST (Native Bar Chart) ---
st.subheader("📅 7-Day Demand Forecast")
days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
# Weekend spikes in demand
demand_curve = [15, 12, 20, 25, 60, 85, 40]

weekly_profits = []
for d in demand_curve:
    _, p, _ = get_metrics(d, avg_weight, avg_vol, bus_capacity)
    weekly_profits.append(p)

forecast_df = pd.DataFrame({
    "Day": days,
    "Box Demand": demand_curve,
    "Daily Profit ($)": weekly_profits
}).set_index("Day")

st.bar_chart(forecast_df)

st.info("💡 This dashboard uses Streamlit Native components. No Matplotlib or Plotly required.")
