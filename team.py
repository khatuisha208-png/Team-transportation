import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# --- PAGE CONFIG ---
st.set_page_config(page_title="TransitFreight AI", layout="wide")

# --- APP TITLE ---
st.title("🚌 TransitFreight: AI-Driven Logistics")
st.markdown("### Dynamic Pricing & Profit Optimizer (Interactive Model)")

# --- SIDEBAR INPUTS ---
st.sidebar.header("📦 Package & Bus Parameters")
n_boxes = st.sidebar.slider("Number of Boxes", 1, 100, 25)
avg_weight = st.sidebar.number_input("Avg Weight (kg)", value=5.0)
avg_vol = st.sidebar.number_input("Avg Volume (Liters)", value=12.0)
bus_capacity = st.sidebar.slider("Bus Hold Capacity (L)", 100, 1000, 500)

st.sidebar.header("💰 Financials")
base_fee = st.sidebar.number_input("Base Handling Fee ($)", value=10.0)
op_cost_per_box = st.sidebar.number_input("Operating Cost/Box ($)", value=4.0)
bus_cut = st.sidebar.slider("Bus Partner Cut (%)", 0, 100, 35) / 100

# --- AI PRICING LOGIC ---
def calculate_dynamic_price(n, w, v, cap):
    total_v = n * v
    utilization = total_v / cap
    
    # Linear base: $10 base + $1.5/kg + $0.3/L
    unit_base = base_fee + (w * 1.5) + (v * 0.3)
    
    # Dynamic Surge Logic (Non-linear)
    if utilization < 0.6:
        surge = 1.0
    elif utilization < 0.9:
        surge = 1.0 + (utilization - 0.6) * 2  # Gradual rise
    else:
        surge = 1.6 + (utilization - 0.9) * 10 # Exponential spike
        
    return round(unit_base * surge, 2), round(surge, 2), utilization

# --- DATA PROCESSING ---
price, surge, util = calculate_dynamic_price(n_boxes, avg_weight, avg_vol, bus_capacity)
revenue = price * n_boxes
costs = (op_cost_per_box * n_boxes) + (revenue * bus_cut)
profit = revenue - costs

# --- KPI DASHBOARD ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Price per Box", f"${price}")
col2.metric("Surge Multiplier", f"{surge}x")
col3.metric("Total Profit", f"${profit:,.2f}")
col4.metric("Capacity Used", f"{util*100:.1f}%")

st.divider()

# --- TIME SERIES SIMULATION (7-Day Forecast) ---
st.subheader("📅 7-Day Demand & Profit Forecast")
days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
# Simulated demand based on typical transit patterns (higher on weekends)
daily_demand = [20, 18, 25, 30, 55, 65, 45] 

forecast_data = []
for day, demand in zip(days, daily_demand):
    p, s, u = calculate_dynamic_price(demand, avg_weight, avg_vol, bus_capacity)
    rev = p * demand
    cst = (op_cost_per_box * demand) + (rev * bus_cut)
    forecast_data.append({"Day": day, "Demand": demand, "Profit": rev - cst, "Price": p})

df = pd.DataFrame(forecast_data)

# PLOTLY CHART: Demand vs Profit
fig = go.Figure()
fig.add_trace(go.Bar(x=df['Day'], y=df['Demand'], name='Box Demand', marker_color='#636EFA'))
fig.add_trace(go.Scatter(x=df['Day'], y=df['Profit'], name='Net Profit ($)', yaxis='y2', line=dict(color='#00CC96', width=4)))

fig.update_layout(
    title="Demand Spikes vs. Profit Margin",
    yaxis=dict(title="Number of Boxes"),
    yaxis2=dict(title="Profit ($)", overlaying='y', side='right'),
    legend=dict(x=0, y=1.1, orientation='h')
)
st.plotly_chart(fig, use_container_width=True)

# --- MULTIVARIATE ANALYSIS ---
st.subheader("🧪 Variable Sensitivity Analysis")
st.write("How **Volume** and **Weight** impact your Unit Price:")

# Create a grid for the heatmap
v_range = np.linspace(5, 50, 10)
w_range = np.linspace(1, 30, 10)
matrix = []
for w in w_range:
    row = []
    for v in v_range:
        p, _, _ = calculate_dynamic_price(1, w, v, bus_capacity)
        row.append(p)
    matrix.append(row)

fig_heat = px.imshow(matrix, 
                labels=dict(x="Volume (L)", y="Weight (kg)", color="Price ($)"),
                x=v_range.round(1), y=w_range.round(1),
                color_continuous_scale='Viridis')
st.plotly_chart(fig_heat, use_container_width=True)
