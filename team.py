import streamlit as st
import numpy as np
import pandas as pd
import random

# --- 1. THE ENVIRONMENT (Historical Bus Data) ---
# Simulating a database of bus slots: [Hour, Day_of_Week, Avg_Occupancy, Reliability_Score]
bus_slots = []
for day in range(7): # 0-6 (Mon-Sun)
    for hour in range(6, 22): # 6 AM to 10 PM
        occupancy = random.uniform(0.1, 0.9)
        reliability = random.uniform(0.7, 0.99)
        bus_slots.append([hour, day, occupancy, reliability])

bus_df = pd.DataFrame(bus_slots, columns=['hour', 'day', 'occupancy', 'reliability'])

# --- 2. THE RL AGENT (Q-Learning) ---
# State: (Day, Hour) | Action: (Accept Slot, Reject & Try Next)
q_table = np.zeros((len(bus_slots), 2))
learning_rate = 0.1
discount = 0.95

# Training the agent to recognize "Good" slots
for _ in range(500):
    idx = random.randint(0, len(bus_slots)-1)
    # Reward logic: High reward for low occupancy (cheap) and high reliability (fast)
    reward = (1 - bus_df.iloc[idx]['occupancy']) * 10 + (bus_df.iloc[idx]['reliability'] * 5)
    q_table[idx, 1] = reward # Action 1 is "Suggest this slot"

# --- 3. STREAMLIT UI: CUSTOMER BOOKING ---
st.title("🚌 AI-Powered Smart Bus Booking")
st.subheader("Strategy A: Responsiveness via RL Optimization")

with st.sidebar:
    st.header("Shipment Details")
    d_date = st.date_input("Expected Delivery Date")
    weight = st.number_input("Weight (kg)", 1.0, 50.0, 5.0)
    vol = st.number_input("Volume (cu ft)", 1.0, 20.0, 2.0)
    fragile = st.toggle("Fragile Item")

# Input for Booking
st.write("### Find Best Delivery Window")
col1, col2 = st.columns(2)
with col1:
    pref_day = st.selectbox("Preferred Pickup Day", 
                            ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
with col2:
    pref_time = st.slider("Earliest Pickup Hour", 6, 20, 9)

# Convert Day to Index
day_map = {"Monday":0, "Tuesday":1, "Wednesday":2, "Thursday":3, "Friday":4, "Saturday":5, "Sunday":6}
day_idx = day_map[pref_day]

if st.button("Optimize Booking"):
    # Filter bus slots based on customer day and time
    possible_slots = bus_df[(bus_df['day'] == day_idx) & (bus_df['hour'] >= pref_time)]
    
    # RL Agent picks the slot with the highest Q-value
    best_slot_idx = possible_slots.index[np.argmax(q_table[possible_slots.index, 1])]
    result = bus_df.iloc[best_slot_idx]
    
    # Calculate Dynamic Price (Base + Weight/Vol + Fragility Premium - Efficiency Discount)
    base_price = 50 
    fragile_fee = 20 if fragile else 0
    # RL Reward influences price: More efficient slots = Cheaper for customer
    efficiency_discount = (1 - result['occupancy']) * 15
    final_price = base_price + (weight * 2) + (vol * 5) + fragile_fee - efficiency_discount

    st.divider()
    st.success(f"### Suggested Pickup: {pref_day} at {int(result['hour'])}:00")
    
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("Dynamic Price", f"₹{round(final_price, 2)}")
    kpi2.metric("Space Availability", f"{round((1-result['occupancy'])*100)}%")
    kpi3.metric("Reliability Score", f"{round(result['reliability']*100)}%")
    
    st.info("💡 **Why this slot?** Our RL agent identified this as a low-congestion window, reducing the risk of delay and lowering your transit cost.")
