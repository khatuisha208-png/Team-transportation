import streamlit as st
import pandas as pd
import numpy as np
import random

st.set_page_config(layout="wide", page_title="Admin Logistics Command")

# 1. DATA INFRASTRUCTURE (The Environment)
routes = ["Mumbai-Pune", "Mumbai-Nagpur", "Mumbai-Nashik"]
months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
weeks = ["Week 1", "Week 2", "Week 3", "Week 4"]

# Mocking historical RL Data: Space Availability & Reliability per Route/Month/Week
# In reality, this would be a trained model saved as a .pkl file
data_log = []
for r in routes:
    for m in months:
        for w in weeks:
            # Logic: Nagpur is less reliable in Monsoon (July); Pune is busy on Weekends
            base_space = random.randint(20, 100)
            if r == "Mumbai-Nagpur" and m in ["July", "August"]:
                base_space -= 15 # Weather delays
            data_log.append([r, m, w, base_space, random.uniform(0.7, 0.98)])

df_master = pd.DataFrame(data_log, columns=['Route', 'Month', 'Week', 'Available_Space', 'Reliability'])

# 2. COMPANY ADMIN DASHBOARD
st.title("🚛 Regional Network Optimization: Admin View")
st.sidebar.header("Network Filters")

selected_route = st.sidebar.selectbox("Select Core Route", routes)
selected_month = st.sidebar.select_slider("Review Month", options=months)

# 3. RL INSIGHT GENERATION (The "Brain")
st.header(f"Strategy Analysis: {selected_route} in {selected_month}")

# Filter data for the view
filtered_df = df_master[(df_master['Route'] == selected_route) & (df_master['Month'] == selected_month)]

# Display Weekly Performance
cols = st.columns(4)
for i, row in enumerate(filtered_df.itertuples()):
    with cols[i]:
        st.metric(label=row.Week, value=f"{row.Available_Space} cuft", delta=f"{round(row.Reliability*100)}% Reliable")
        
        # RL Decision Logic (Company POV)
        if row.Available_Space > 70:
            st.success("Decision: AGGRESSIVE PRICING")
            st.caption("Action: Lower rates by 15% to fill empty space.")
        elif row.Available_Space < 30:
            st.error("Decision: CAPACITY CRUNCH")
            st.caption("Action: Increase price; prioritize fragile/premium.")
        else:
            st.warning("Decision: OPTIMIZE LOAD")
            st.caption("Action: Consolidate small parcels.")

# 4. REVENUE & DOCUMENTATION SUMMARY
st.divider()
st.subheader("Route-Specific Logistics Requirements")

doc_col1, doc_col2 = st.columns(2)

with doc_col1:
    st.markdown("""
    ### 📑 Mandatory Compliance
    * **Inter-City E-Way Bill:** Required for Mumbai-Nagpur/Nashik (high-value agri/industrial).
    * **Octroi/Local Body Tax Forms:** Essential for Pune-Mumbai entry points.
    * **Transit Insurance (High-Speed):** Specifically for the Expressway (Mumbai-Pune).
    """)

with doc_col2:
    st.markdown(f"""
    ### 📈 Strategic Focus for {selected_route}
    * **Responsiveness:** Use AI to predict Pune Expressway traffic during 'Week 4' (End of month rush).
    * **Differentiation:** Offer 'Cold-Chain' tracking for Mumbai-Nashik (Agri-logistics focus).
    * **Cost Leadership:** Target Mumbai-Nagpur night buses for heavy, non-urgent bulk cargo.
    """)
