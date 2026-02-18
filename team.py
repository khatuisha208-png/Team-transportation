import streamlit as st
import pandas as pd
import numpy as np

# --- INDUSTRY STANDARD DEMAND DATA (Small Scale) ---
# Routes: Mumbai-Pune (Fast/Frequent), Mumbai-Nagpur (Long-haul), Mumbai-Nashik (Agri-Industrial)
data = {
    "Route": ["Mumbai-Pune", "Mumbai-Nagpur", "Mumbai-Nashik"],
    "Daily_Demand_Units": [120, 45, 85],       # Standard daily parcel count for a startup
    "Avg_Weight_kg": [5.2, 12.5, 8.0],          # Industry average for bus-hold parcels
    "Current_Lead_Time_hr": [4, 18, 5],         # AI-optimized time
    "Market_Lead_Time_hr": [12, 48, 15],        # Traditional courier time
    "Free_Space_Forecast": [35, 60, 42]         # % of bus hold available
}

df = pd.DataFrame(data)

st.title("🚛 Startup Admin: Strategic Dispatch Hub")
st.subheader("Inventory & Lead Time Optimization (Company POV)")

# 1. STRATEGIC METRICS
st.markdown("### 📈 Key Performance Indicators (KPIs)")
m1, m2, m3 = st.columns(3)
with m1:
    # Calculating lead time reduction percentage
    reduction = ((df['Market_Lead_Time_hr'] - df['Current_Lead_Time_hr']) / df['Market_Lead_Time_hr']).mean() * 100
    st.metric("Avg. Lead Time Reduction", f"{int(reduction)}%", delta="Responsiveness Edge")
with m2:
    st.metric("System Utilization", "68%", delta="Target 85%")
with m3:
    st.metric("Cost Saving vs 3PL", "32%", delta="Cost Leadership")

# 2. ROUTE-WISE PREDICTION TABLE
st.markdown("### 📍 Route Forecast & Capacity Planning")

# Industry Logic: If Free Space > 50%, the AI triggers "Consolidation Mode"
df['AI_Recommendation'] = np.where(df['Free_Space_Forecast'] > 50, "Bulk Batching", "Express Dispatch")

st.dataframe(df.style.highlight_max(axis=0, subset=['Free_Space_Forecast'], color='#d1e7dd'))

# 3. DEMAND TRENDS (Weekly View for Resource Allocation)
st.markdown("### 📊 Demand Volatility (Weekly)")
# Industry standard: Demand peaks on Tuesday/Wednesday; dips on Sunday
weekly_demand = pd.DataFrame({
    'Day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
    'Mumbai-Pune': [110, 140, 135, 120, 150, 90, 60],
    'Mumbai-Nagpur': [40, 45, 50, 42, 48, 30, 20]
}).set_index('Day')

st.line_chart(weekly_demand)

st.info("💡 **Strategy Insight:** The RL model suggests increasing the 'Mumbai-Pune' frequency on Saturdays to handle the weekend e-commerce surge while passenger seats are full but cargo holds are often under-utilized.")
