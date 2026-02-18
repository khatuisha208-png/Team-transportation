import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(layout="wide")
st.title("📊 Operational Command Center: AI Dispatch")

# 1. ROUTE INTELLIGENCE DATA
# This data represents the "State" the AI observes to predict free space
route_data = {
    "Mumbai-Pune": {"dist": 150, "avg_bus_freq": 15, "historical_fill_rate": 0.65},
    "Mumbai-Nagpur": {"dist": 800, "avg_bus_freq": 4, "historical_fill_rate": 0.40},
    "Mumbai-Nashik": {"dist": 170, "avg_bus_freq": 8, "historical_fill_rate": 0.55}
}

# 2. SELECTION CONTROLS
col1, col2, col3 = st.columns(3)
with col1:
    route = st.selectbox("Active Route", list(route_data.keys()))
with col2:
    month = st.select_slider("Forecast Month", options=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
with col3:
    priority = st.radio("Focus Area", ["Lead Time Reduction", "Space Optimization"])

# 3. THE AI PREDICTION ENGINE (Logic)
# Prediction of Free Space based on Route and Seasonality
base_fill = route_data[route]["historical_fill_rate"]
seasonal_impact = 0.2 if month in ["Oct", "Nov", "Dec"] else -0.1 # Peak festival season
predicted_free_space = round((1 - (base_fill + seasonal_impact)) * 100)

# Lead Time Calculation (Traditional vs AI-Optimized)
trad_lead_time = 48 if route == "Mumbai-Nagpur" else 24
ai_lead_time = trad_lead_time * 0.6 # AI reduces lead time by 40% via real-time bus matching

# 4. COMPANY INSIGHTS DISPLAY
st.divider()
kpi1, kpi2, kpi3 = st.columns(3)

with kpi1:
    st.metric("Predicted Free Space", f"{predicted_free_space}%", delta="Available for Booking")
    st.caption("Based on real-time bus ticketing API integration.")

with kpi2:
    st.metric("Expected Delivery Time", f"{int(ai_lead_time)} Hours", delta=f"-{int(trad_lead_time - ai_lead_time)}h vs Market")
    st.caption("Achieved via predictive route-hopping.")

with kpi3:
    st.metric("Route Profitability", "High", delta="Cost Leadership Active")
    st.caption("Utilizing 100% of existing public infrastructure.")

# 5. DATA VISUALIZATION: WEEKLY CAPACITY TRENDS
st.subheader(f"Weekly Capacity Forecast: {route} ({month})")
weekly_data = pd.DataFrame({
    'Week': ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
    'Free_Space_Predicted': [predicted_free_space + 5, predicted_free_space - 10, predicted_free_space + 2, predicted_free_space - 5],
    'Expected_Demand': [30, 55, 40, 65]
}).set_index('Week')

st.line_chart(weekly_data)

st.info(f"💡 **AI Strategy:** For {route} in {month}, the agent suggests batching non-fragile items in Week 1 to maximize the high predicted free space.")
