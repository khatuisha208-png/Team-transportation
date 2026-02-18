import streamlit as st
import pandas as pd
try:
    from prophet import Prophet
except ImportError:
    st.error("Prophet is not installed. Please add 'prophet' to your requirements.txt")

# Rest of your demand-to-schedule aligner code...

# 1. Create Mock Data: Monthly Average Demand
# 'ds' = datestamp, 'y' = number of shipment requests
data = {
    'ds': pd.date_range(start='2024-01-01', periods=24, freq='MS'),
    'y': [120, 135, 150, 145, 160, 190, 210, 205, 180, 170, 240, 280, # 2024
          140, 155, 175, 165, 190, 220, 250, 245, 210, 200, 290, 330]  # 2025
}

df = pd.DataFrame(data)

# 2. Initialize and Fit the Prophet Model
# Prophet handles seasonality (like year-end spikes) automatically
model = Prophet(yearly_seasonality=True, weekly_seasonality=False, daily_seasonality=False)
model.fit(df)

# 3. Create a future dataframe for the next 6 months
future = model.make_future_dataframe(periods=6, freq='MS')

# 4. Predict demand
forecast = model.predict(future)

# 5. Visualize the Forecast
fig1 = model.plot(forecast)
plt.title("Logistics Demand Forecast (Monthly)")
plt.xlabel("Date")
plt.ylabel("Shipment Volume")
plt.show()

# Display the specific predicted values for the next 6 months
print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(6))
