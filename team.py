import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(layout="wide", page_title="Logistics Command Center")

# --- 1. THE DATA ENGINE (Industry-Standard Demand Points) ---
routes = ["Mumbai-Pune", "Mumbai-Nagpur", "Mumbai-Nashik"]
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# Simulated Monthly Demand and Space Data
# Avg_Volume: Units per month | Lead_Reduction: % improvement over traditional 3PL
monthly_stats = []
for r in routes:
    for m in months:
        # Scenario: Oct-Dec is peak season (less free space, higher demand)
        peak_factor = 1.4 if m in ["Oct", "Nov", "Dec"] else 1.0
        demand = np.random.randint(2000, 5000) * peak_factor
        free_space = max(10, 80 - (demand / 100)) # Space drops as demand rises
        lead_red = 45 if r == "Mumbai-Pune" else 30 # Pune has higher frequency, so better lead reduction
        monthly_stats.append([r, m, int(demand), round(free_space, 1), lead_red])

df_admin = pd.DataFrame(monthly_stats, columns=['Route', 'Month', 'Total_Demand', 'Predicted_Free_Space', 'Lead_Time_Reduction_%'])

# --- 2. COMPANY DASHBOARD UI ---
st.title("🏢 Startup Admin: Regional Capacity Planning")
st.markdown("### Strategy A: Maximize Responsiveness via Predictive Load Smoothing")

# Filters
selected_route = st.sidebar.selectbox("Select Route", routes)

# 3. MONTHLY AGGREGATE VIEW
st.subheader(f"12-Month Forecast: {selected_route}")
route_df = df_admin[df_admin['Route'] == selected_route]

# Displaying the "Prediction vs Demand" Trend
st.line_chart(route_df.set_index('Month')[['Total_Demand', 'Predicted_Free_Space']])

# 4. WEEKLY OPERATIONAL VIEW (Deep Dive)
st.divider()
st.subheader(f"Current Month Weekly Breakdown (Lead Time Analytics)")

# Simulating the 4 weeks of the current month
weekly_data = pd.DataFrame({
    'Week': ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
    'Incoming_Load': [450, 600, 320, 800],
    'AI_Lead_Time_Hrs': [6, 8, 5, 12],
    'Market_Lead_Time_Hrs': [18, 18, 18, 18]
})

col1, col2 = st.columns([2, 1])

with col1:
    st.bar_chart(weekly_data.set_index('Week')[['AI_Lead_Time_Hrs', 'Market_Lead_Time_Hrs']])
    st.caption("Comparison: AI-Optimized Bus Hopping vs. Traditional Courier Lead Times")

with col2:
    st.write("#### AI Dispatch Strategy")
    avg_reduction = weekly_data['AI_Lead_Time_Hrs'].mean()
    st.metric("Avg. Target Lead Time", f"{avg_reduction} Hrs")
    
    if selected_route == "Mumbai-Nagpur":
        st.info("💡 **Strategy:** Long-haul route. Agent suggests 'Direct-to-Hub' dispatch in Week 4 to avoid 12hr congestion delays.")
    else:
        st.success("💡 **Strategy:** High-frequency route. Agent suggests 'Instant Dispatch' to maintain <8hr lead time.")
