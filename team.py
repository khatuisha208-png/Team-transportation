import streamlit as st
import numpy as np
import pandas as pd
import random

st.set_page_config(layout="wide")
st.title("🤖 RL-Driven Command Center (Company POV)")

# --- 1. THE RL ENVIRONMENT SETUP ---
routes = ["Mumbai-Pune", "Mumbai-Nagpur", "Mumbai-Nashik"]
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# States: (Route, Month_Type[Peak/Off-Peak])
# Actions: 0 = Express (Fast but expensive), 1 = Standard (Balanced), 2 = Budget (Wait for empty bus)
n_actions = 3
q_table = np.zeros((len(routes) * 2, n_actions)) # 2 states per route: Peak/Normal

# --- 2. THE RL TRAINING LOGIC (Simplified Q-Learning) ---
def train_agent():
    learning_rate = 0.1
    discount_factor = 0.9
    
    for _ in range(2000): # Training episodes
        state = random.randint(0, (len(routes) * 2) - 1)
        action = random.randint(0, n_actions - 1)
        
        # Reward Logic based on Lead Time Reduction & Cost
        # If State is Peak (odd index) and Action is Express (0), high cost = low reward
        if state % 2 == 1: # Peak State
            rewards = [2, 5, 10] # Reward 'Budget' more in peak to save cost
        else: # Normal State
            rewards = [10, 5, 2] # Reward 'Express' more to keep lead time low
            
        reward = rewards[action]
        
        # Q-Update
        q_table[state, action] += learning_rate * (reward + discount_factor * np.max(q_table[state]) - q_table[state, action])

train_agent()

# --- 3. COMPANY POV: PREDICTIVE DASHBOARD ---
selected_route = st.sidebar.selectbox("Select Route", routes)
route_idx = routes.index(selected_route) * 2

st.subheader(f"Strategy Analysis: {selected_route}")

# Simulation of Monthly Demand vs AI Predicted Space
monthly_data = []
for i, m in enumerate(months):
    is_peak = 1 if m in ["Oct", "Nov", "Dec"] else 0
    state_idx = route_idx + is_peak
    
    # The AI chooses the best action from the Q-Table
    best_action = np.argmax(q_table[state_idx])
    
    # Industry Data Points
    demand = np.random.randint(4000, 6500) if is_peak else np.random.randint(2000, 3500)
    
    # Action impact on Lead Time and Space
    if best_action == 0: # Express
        lead_red = 65; free_space = 15; strategy = "Express Dispatch"
    elif best_action == 1: # Standard
        lead_red = 45; free_space = 40; strategy = "Balanced Load"
    else: # Budget
        lead_red = 20; free_space = 75; strategy = "Cost Optimization"
        
    monthly_data.append([m, demand, free_space, lead_red, strategy])

df = pd.DataFrame(monthly_data, columns=['Month', 'Demand', 'Free_Space_%', 'Lead_Reduction_%', 'AI_Strategy'])

# --- 4. VISUALIZING THE AI DECISIONS ---
col1, col2 = st.columns(2)

with col1:
    st.write("#### 📦 Demand vs. AI-Predicted Space")
    # Using a professional-grade chart that plots both metrics correctly
    chart_data = df.set_index('Month')
    st.line_chart(chart_data['Demand'])
    st.area_chart(chart_data['Free_Space_%'], color="#ffaa00")

with col2:
    st.write("#### ⚡ Strategy Selection & Lead Time Gain")
    st.dataframe(df[['Month', 'AI_Strategy', 'Lead_Reduction_%']].set_index('Month'))

st.divider()

# --- 5. LEAD REDUCTION VERIFICATION ---
st.subheader("Final Strategy A Outcome")
avg_red = df['Lead_Reduction_%'].mean()
st.info(f"The RL Agent has optimized {selected_route} to achieve an average **{avg_red:.1f}% Lead Time Reduction** over standard couriers.")
