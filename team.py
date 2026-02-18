import numpy as np
import random
import streamlit as st

# 1. ENVIRONMENT SETUP
# States: 0=Low Traffic, 1=Moderate, 2=Peak Hour
# Actions: 0=Send Now, 1=Wait 15 Mins, 2=Reroute to different line
n_states = 3
n_actions = 3

# Initialize Q-Table with zeros
q_table = np.zeros((n_states, n_actions))

# Hyperparameters
learning_rate = 0.1
discount_factor = 0.9
exploration_rate = 0.2 
epochs = 1000

# 2. SIMULATED REWARD FUNCTION
def get_reward(state, action):
    # If it's Peak Hour (State 2) and we try to 'Send Now' (Action 0), penalty is high
    if state == 2 and action == 0:
        return -10 # Penalty for putting cargo on a crowded bus
    # If it's Peak Hour (State 2) and we 'Wait' (Action 1), small reward
    elif state == 2 and action == 1:
        return 5 
    # If it's Low Traffic (State 0) and we 'Send Now' (Action 0), high reward
    elif state == 0 and action == 0:
        return 10
    else:
        return 1 # Neutral/Small progress

# 3. TRAINING THE AGENT
for i in range(epochs):
    state = random.randint(0, n_states - 1)
    
    # Explore vs Exploit
    if random.uniform(0, 1) < exploration_rate:
        action = random.randint(0, n_actions - 1)
    else:
        action = np.argmax(q_table[state])
    
    reward = get_reward(state, action)
    
    # Q-Table Update (Bellman Equation)
    old_value = q_table[state, action]
    next_max = np.max(q_table[state])
    
    # New Q Value
    q_table[state, action] = (1 - learning_rate) * old_value + \
                             learning_rate * (reward + discount_factor * next_max)

# 4. STREAMLIT INTERFACE
st.title("🤖 RL Dispatcher: Strategy A")
st.write("This model uses **Reinforcement Learning** to decide the most responsive transport action.")

current_env_state = st.select_slider(
    'Select Current Traffic/Bus Load State',
    options=[0, 1, 2],
    value=1,
    help="0: Empty/Night, 1: Moderate, 2: Peak Hour"
)

if st.button("Run RL Dispatcher"):
    best_action = np.argmax(q_table[current_env_state])
    
    action_map = {
        0: "🚀 DISPATCH IMMEDIATELY (High Capacity Available)",
        1: "⏳ HOLD SHIPMENT (Next Bus has better space)",
        2: "🔄 REROUTE (Current line too crowded, switching to alternate route)"
    }
    
    st.subheader("Agent Decision:")
    st.info(action_map[best_action])
    
    st.write("### Q-Table (Agent's Memory)")
    st.dataframe(q_table)
