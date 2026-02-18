import streamlit as st
import pandas as pd
import numpy as np

st.title("Logistics Startup: AI Demand Engine")

# Mock data for your monthly demand
data = {
    'Month': pd.date_range(start='2024-01-01', periods=12, freq='MS'),
    'Actual_Demand': [100, 120, 110, 130, 150, 170, 160, 155, 180, 210, 250, 230],
    'AI_Predicted': [105, 115, 115, 135, 155, 165, 170, 160, 185, 200, 240, 225]
}
df = pd.DataFrame(data).set_index('Month')

# Built-in Streamlit Chart (NO MATPLOTLIB NEEDED)
st.line_chart(df)

st.write("### AI Insights for Cost Leadership:")
st.info("Predicted demand is up 15%. Pre-negotiate off-peak bus space for next month to maintain 20% lower costs than traditional couriers.")
