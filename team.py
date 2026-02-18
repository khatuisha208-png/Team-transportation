import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(layout="wide")
st.title("🤖 Dynamic RL Cost Orchestrator")

# --- 1. LIVE ENVIRONMENT INPUTS ---
st.sidebar.header("🕹️ Live Environment Control")
route_select = st.sidebar.selectbox("Active Route", ["Mumbai-Pune", "Mumbai-Nashik", "Mumbai-Nagpur"])
demand_surge = st.sidebar.slider("Current Demand Surge (%)", 0, 100, 20)
bus_availability = st.sidebar.slider("Bus Hold Supply (%)", 10, 100, 80)

# --- 2. DYNAMIC RL BRAIN (Decision Logic) ---
# This is the "Inference" part of the RL Agent. 
# It weighs the reward of "Waiting" vs "Dispatching" based on live inputs.

def get_rl_decision(demand, supply):
    # Action 0: Off-Peak Consolidation (High Reward when Demand is low/Supply is high)
    # Action 1: Standard Batching
    # Action 2: Express (Avoided for Cost Leadership)
    
    # Simple logic simulating an RL Agent's Q-value selection:
    if supply > (demand + 20):
        return "Deep Consolidation", 12.5, "🟢 Low Cost Mode"
    elif supply >= demand:
        return "Standard Batching", 28.0, "🟡 Balanced Mode"
    else:
        return "Emergency Injection", 55.0, "🔴 High Cost Mode (Supply Deficit)"

# Execute Decision
decision_name, unit_cost, status = get_rl_decision(demand_surge, bus_availability)

# --- 3. DYNAMIC METRICS ---
st.subheader(f"Current System State: {route_select}")
m1, m2, m3 = st.columns(3)

with m1:
    st.metric("AI-Assigned Strategy", decision_name)
with m2:
    # This value is now dynamic based on your sliders
    st.metric("Dynamic Unit Cost", f"₹{unit_cost}", delta=f"{unit_cost - 30:.2f} vs Market Avg")
with m3:
    st.metric("System Health", status)

# --- 4. THE DYNAMIC FORECAST ---
# We generate a forecast that REACTS to your current slider positions
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
dynamic_forecast = []

for m in months:
    # Add some seasonal noise to your live slider input
    seasonal_demand = demand_surge + np.random.randint(-10, 10)
    seasonal_demand = max(0, min(100, seasonal_demand))
    
    # Agent re-decides for every month based on your input
    _, cost, _ = get_rl_decision(seasonal_demand, bus_availability)
    dynamic_forecast.append([m, seasonal_demand, cost])

df_dynamic = pd.DataFrame(dynamic_forecast, columns=['Month', 'Live_Demand', 'Unit_Cost'])

# --- 5. VISUALIZATION ---
st.divider()
st.write("### AI Behavioral Response (Forecasted)")

# Using a dual-axis style to show how the Agent keeps cost low even as demand moves
c1, c2 = st.columns(2)
with c1:
    st.write("#### Demand Flux")
    st.line_chart(df_dynamic.set_index('Month')['Live_Demand'])
with c2:
    st.write("#### Agent's Cost Response")
    st.area_chart(df_dynamic.set_index('Month')['Unit_Cost'], color="#2ecc71")

st.info("💡 **Why is this dynamic?** Try moving the 'Bus Hold Supply' slider. If supply drops below demand, the AI will immediately switch strategies from 'Consolidation' to 'Emergency Injection,' causing the cost area chart to spike.")
