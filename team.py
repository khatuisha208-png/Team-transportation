import streamlit as st
import pandas as pd
import numpy as np

# --- PAGE CONFIG ---
st.set_page_config(page_title="TransitFreight AI: Yield Optimizer", layout="wide")

st.title("🚌 TransitFreight: AI Exponential Yield Model")
st.markdown("### Dynamic Pricing for Indian Bus Logistics (₹ / $ft^3$)")

# --- SIDEBAR: INPUTS ---
st.sidebar.header("📦 Logistics Parameters")
n_boxes = st.sidebar.slider("Number of Boxes", 1, 100, 20)
avg_weight = st.sidebar.number_input("Avg Weight (kg)", value=10.0)
avg_vol = st.sidebar.number_input("Avg Volume (Cubic Feet - $ft^3$)", value=2.0)
bus_capacity = st.sidebar.slider("Bus Hold Capacity ($ft^3$)", 100, 500, 300)

st.sidebar.header("⚙️ Model Sensitivity")
# 'k' controls how aggressively the price rises as space disappears
k_sensitivity = st.sidebar.slider("Price Sensitivity (k)", 0.5, 3.0, 1.5)

st.sidebar.header("💰 Financials (INR)")
base_fee = st.sidebar.number_input("Base Fee (₹)", value=200.0)
op_cost = st.sidebar.number_input("Handling Cost/Box (₹)", value=50.0)
bus_cut_pct = st.sidebar.slider("Bus Operator Cut (%)", 10, 50, 30) / 100

# --- THE EXPONENTIAL YIELD ENGINE ---
def calculate_yield_price(n, w, v, cap, k):
    # 1. Calculate Base Price (Linear Cost-Plus)
    # Using India-specific rates (₹15 per kg, ₹60 per cubic foot)
    unit_base = base_fee + (w * 15) + (v * 60)
    
    # 2. Utilization Ratio (Current Space / Total Space)
    total_volume_needed = n * v
    utilization = total_volume_needed / cap
    
    # 3. Exponential Scarcity Function: Price = Base * e^(k * util)
    # This replaces "if/else" heuristic logic with a continuous curve
    surge_multiplier = np.exp(k * utilization)
    
    # Ensure utilization doesn't break math if it exceeds 100%
    clamped_util = min(utilization, 1.0)
    
    final_price = unit_base * surge_multiplier
    
    # 4. Profit Calculation
    revenue = final_price * n
    # Costs = Handling + Bus Owner's Share
    total_costs = (op_cost * n) + (revenue * bus_cut_pct)
    net_profit = revenue - total_costs
    
    return {
        "unit_price": round(final_price, 2),
        "total_revenue": round(revenue, 2),
        "profit": round(net_profit, 2),
        "utilization": round(clamped_util * 100, 1),
        "multiplier": round(surge_multiplier, 2)
    }

# --- EXECUTION ---
results = calculate_yield_price(n_boxes, avg_weight, avg_vol, bus_capacity, k_sensitivity)

# --- KPI DASHBOARD ---
c1, c2, c3, c4 = st.columns(4)
c1.metric("Current Price", f"₹{results['unit_price']}")
c2.metric("Yield Multiplier", f"{results['multiplier']}x")
c3.metric("Net Profit", f"₹{results['profit']:,.2f}")
c4.metric("Capacity Used", f"{results['utilization']}%")

st.divider()

# --- VISUALIZATION: THE YIELD CURVE ---
st.subheader("📈 Yield Curve: Price vs. Capacity Utilization")
st.write("This graph shows how the Exponential Model automatically manages scarcity.")

# Generate data for the curve
sim_n = np.arange(1, int(bus_capacity/avg_vol) + 5)
curve_data = []
for n in sim_n:
    res = calculate_yield_price(n, avg_weight, avg_vol, bus_capacity, k_sensitivity)
    curve_data.append({
        "Boxes": n,
        "Price per Box (₹)": res['unit_price'],
        "Total Profit (₹)": res['profit']
    })

df = pd.DataFrame(curve_data).set_index("Boxes")

# Native Streamlit Charts (Failsafe)
col_left, col_right = st.columns(2)
with col_left:
    st.write("**Unit Price Growth (₹)**")
    st.line_chart(df["Price per Box (₹)"])
with col_right:
    st.write("**Cumulative Profit Scalability (₹)**")
    st.area_chart(df["Total Profit (₹)"])

st.success(f"Model Summary: At {results['utilization']}% capacity, the scarcity multiplier is {results['multiplier']}x.")
