import streamlit as st
import numpy as np
import pandas as pd

# --- 1. COMPANY REVENUE LOGIC ---
st.set_page_config(layout="wide")
st.title("🚛 Startup Admin: Network Load Orchestrator")
st.markdown("### Focus: Strategy A (Responsiveness) & Cost Leadership Optimization")

# Simulated System Stats
col_a, col_b, col_c, col_d = st.columns(4)
col_a.metric("Total Active Shipments", "1,240")
col_b.metric("Avg. Bus Utilization", "42%", "+5% vs Last Week")
col_c.metric("On-Time Delivery", "98.2%", "AI Optimized")
col_d.metric("Daily Revenue", "₹45,200", "High Margin")

# --- 2. ADMIN INPUT: THE GLOBAL DEMAND POOL ---
st.sidebar.header("Batch Processing Controls")
target_day = st.sidebar.selectbox("View Strategy for:", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
urgency_filter = st.sidebar.slider("Minimum Priority Score", 0, 100, 50)

# --- 3. REINFORCEMENT LEARNING: BATCH ALLOCATOR ---
# The Agent analyzes all pending orders and assigns them to the "Best" bus routes
st.write(f"## {target_day} Allocation Strategy")

# Mock data representing the "Environment" the RL Agent manages
data = {
    "Route_ID": ["RT-101", "RT-202", "RT-303", "RT-105", "RT-404"],
    "Pending_Volume_cuft": [15.5, 42.0, 10.2, 5.0, 22.1],
    "Predicted_Bus_Space": [20.0, 35.0, 15.0, 5.0, 25.0],
    "Fragile_Count": [2, 12, 1, 0, 5],
    "Profit_Potential": [0.85, 0.40, 0.92, 0.60, 0.75] # Agent's calculated reward
}
df = pd.DataFrame(data)

# RL Logic: The agent flags routes that are "High Risk" (Low space vs High Volume)
df['AI_Decision'] = df.apply(lambda x: "🚀 AUTHORIZE" if x['Predicted_Bus_Space'] > x['Pending_Volume_cuft'] else "⚠️ REROUTE", axis=1)

# Display the "Company Command Center"
st.table(df)

# --- 4. STRATEGIC ANALYSIS ---
st.write("### RL Agent Insights")
st.info("""
**Agent Note:** Route **RT-202** has a bottleneck. The RL model suggests offloading 7.0 cuft to **RT-303** at the Central Interchange to maintain our **Responsiveness** guarantee without increasing costs.
""")
