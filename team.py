import streamlit as st
import pandas as pd
import numpy as np

# --- PAGE CONFIG ---
st.set_page_config(page_title="TransitFreight India AI", layout="wide")

st.title("🚌 TransitFreight: Indian Bus-Logistics AI")
st.markdown("### Dynamic Pricing & Profit Optimizer (₹ / $ft^3$)")

# --- SIDEBAR: LOCALIZED VARIABLES ---
st.sidebar.header("📦 Package Details")
n_boxes = st.sidebar.slider("Number of Boxes", 1, 100, 20)
avg_weight = st.sidebar.number_input("Avg Weight (kg)", value=10.0)
avg_vol = st.sidebar.number_input("Avg Volume (Cubic Feet - $ft^3$)", value=2.0)
bus_capacity = st.sidebar.slider("Bus Hold Capacity ($ft^3$)", 100, 500, 300)

st.sidebar.header("💰 Financials (INR)")
base_fee = st.sidebar.number_input("Base Handling Fee (₹)", value=150.0)
op_cost_per_box = st.sidebar.number_input("Our Handling Cost/Box (₹)", value=40.0)
bus_cut_pct = st.sidebar.slider("Bus Operator Commission (%)", 0, 100, 30)

# --- PRICING LOGIC ---
def get_india_metrics(n, w, v, cap):
    total_v = n * v
    utilization = min(total_v / cap, 1.0)
    
    # Base Price calculation: Base + (Weight * ₹10) + (Vol * ₹50)
    # In India, volume takes priority in buses due to space constraints
    unit_base = base_fee + (w * 10) + (v * 50)
    
    # Dynamic Surge Logic
    # If the bus is more than 60% full, prices spike to prioritize high-value goods
    if utilization < 0.6:
        surge = 1.0
    elif utilization < 0.9:
        surge = 1.25 # 25% Surge
    else:
        surge = 1.25 + (utilization - 0.9) * 10 # Exponential Spike up to 2x+
    
    final_unit_price = unit_base * surge
    rev = final_unit_price * n
    partner_payout = rev * (bus_cut_pct / 100)
    cost = (op_cost_per_box * n) + partner_payout
    prof = rev - cost
    
    return round(final_unit_price, 2), round(prof, 2), round(utilization * 100, 1)

# --- EXECUTION ---
u_price, u_profit, u_util = get_metrics = get_india_metrics(n_boxes, avg_weight, avg_vol, bus_capacity)

# --- KPI DISPLAY ---
col1, col2, col3 = st.columns(3)
col1.metric("Price per Box", f"₹{u_price}")
col2.metric("Est. Net Profit", f"₹{u_profit:,.2f}")
col3.metric("Bus Space Used", f"{u_util}%")

st.divider()

# --- CHART 1: THE PROFIT "KICK" ---
st.subheader("📈 Profit Scalability (Dynamic Surge Effect)")
st.write("As more boxes are booked, the price per box increases, leading to non-linear profit growth.")

box_counts = range(1, 101)
data_points = []
for b in box_counts:
    p_box, p_total, _ = get_india_metrics(b, avg_weight, avg_vol, bus_capacity)
    data_points.append({"Boxes": b, "Total Profit (₹)": p_total, "Unit Price (₹)": p_box})

df_scaling = pd.DataFrame(data_points).set_index("Boxes")
st.line_chart(df_scaling[["Total Profit (₹)"]])

# --- CHART 2: REVENUE VS VOLUME ---
st.subheader("📊 Space Utilization vs. Unit Price")
st.write("This bar chart shows how the AI raises prices as the $ft^3$ capacity hits the limit.")
st.bar_chart(df_scaling[["Unit Price (₹)"]])

st.info("💡 Note: In this model, Volume ($ft^3$) is the primary driver of surge pricing because bus luggage space is a finite physical constraint.")
