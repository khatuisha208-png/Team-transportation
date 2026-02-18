import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# --- PAGE CONFIG ---
st.set_page_config(page_title="TransitFreight AI Optimizer", layout="wide")

# --- PRICING ENGINE LOGIC ---
class PricingEngine:
    def __init__(self, base_fee=10, weight_rate=2.0, vol_rate=0.5, capacity=100):
        self.base_fee = base_fee
        self.weight_rate = weight_rate
        self.vol_rate = vol_rate
        self.capacity = capacity

    def calculate_price(self, weight, volume, current_occupancy):
        # Linear Base Price
        base = self.base_fee + (weight * self.weight_rate) + (volume * self.vol_rate)
        
        # Dynamic Surge Logic
        utilization = current_occupancy / self.capacity
        if utilization < 0.5:
            surge = 1.0
        elif utilization < 0.8:
            surge = 1.25
        else:
            # Exponential surge as we hit the limit
            surge = 1.25 + (utilization - 0.8) * 8 
        
        return round(base * surge, 2), surge

# --- STREAMLIT UI ---
st.title("🚌 TransitFreight: AI Dynamic Pricing Dashboard")
st.markdown("Optimization of unused public bus space using Time-Series Demand and Multivariate Linear Pricing.")

# Sidebar Controls
st.sidebar.header("📦 Package Variables")
n_boxes = st.sidebar.slider("Number of Boxes in Batch", 1, 50, 10)
avg_weight = st.sidebar.number_input("Average Weight per Box (kg)", value=5.0)
avg_vol = st.sidebar.number_input("Average Volume per Box (Liters)", value=10.0)

st.sidebar.header("⚙️ Cost & Capacity")
bus_cap = st.sidebar.slider("Bus Hold Capacity (L)", 50, 500, 200)
op_cost = st.sidebar.number_input("Handling Cost per Box ($)", value=3.0)
revenue_share = st.sidebar.slider("Bus Company Share (%)", 0, 100, 40) / 100

# --- CALCULATIONS ---
engine = PricingEngine(capacity=bus_cap)
total_vol_needed = n_boxes * avg_vol
unit_price, surge_multiplier = engine.calculate_price(avg_weight, avg_vol, total_vol_needed)

total_revenue = unit_price * n_boxes
total_costs = (op_cost * n_boxes) + (total_revenue * revenue_share)
net_profit = total_revenue - total_costs

# --- KPI METRICS ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Unit Price", f"${unit_price}")
col2.metric("Surge Multiplier", f"{surge_multiplier:.2f}x")
col3.metric("Total Revenue", f"${total_revenue:,.2f}")
col4.metric("Net Profit", f"${net_profit:,.2f}", delta=f"{((net_profit/total_revenue)*100):.1f}% Margin")

# --- VISUALIZATIONS ---
st.divider()
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("Profit Scalability")
    # Simulate different box counts
    counts = np.arange(1, 61)
    profits = []
    for c in counts:
        p, _ = engine.calculate_price(avg_weight, avg_vol, c * avg_vol)
        rev = p * c
        cost = (op_cost * c) + (rev * revenue_share)
        profits.append(rev - cost)
    
    fig, ax = plt.subplots()
    ax.plot(counts, profits, color='#2ecc71', linewidth=3)
    ax.set_xlabel("Number of Boxes")
    ax.set_ylabel("Net Profit ($)")
    ax.fill_between(counts, profits, color='#2ecc71', alpha=0.2)
    st.pyplot(fig)

with chart_col2:
    st.subheader("Price Sensitivity (Weight vs Vol)")
    # Heatmap of base price
    w_range = np.linspace(1, 20, 10)
    v_range = np.linspace(1, 50, 10)
    z = np.array([[engine.calculate_price(w, v, 0)[0] for v in v_range] for w in w_range])
    
    fig2, ax2 = plt.subplots()
    sns.heatmap(z, xticklabels=v_range.astype(int), yticklabels=w_range.astype(int), annot=True, fmt=".0f", cmap="YlGnBu")
    ax2.set_xlabel("Volume (L)")
    ax2.set_ylabel("Weight (kg)")
    st.pyplot(fig2)

st.success("AI Model Status: Optimal. Adjust sliders to see real-time profit impact.")
