import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX

# 1. Generate 24 months of synthetic demand data
# Base demand + seasonal peak (December) + general growth trend
np.random.seed(42)
months = pd.date_range(start='2024-01-01', periods=24, freq='MS')
base_demand = np.array([100, 110, 120, 115, 130, 150, 170, 160, 140, 130, 190, 250,
                        120, 130, 145, 140, 160, 185, 210, 200, 175, 165, 240, 310])
df = pd.DataFrame({'Date': months, 'Demand': base_demand})
df.set_index('Date', inplace=True)

# 2. Fit the SARIMA Model (Order: p,d,q)(P,D,Q,s)
# s=12 for monthly seasonality
model = SARIMAX(df['Demand'], 
                order=(1, 1, 1), 
                seasonal_order=(1, 1, 1, 12))
model_fit = model.fit(disp=False)

# 3. Forecast the next 6 months
forecast = model_fit.get_forecast(steps=6)
forecast_df = forecast.summary_frame()

# 4. Plotting the results
plt.figure(figsize=(10, 5))
plt.plot(df.index, df['Demand'], label='Historical Demand', marker='o')
plt.plot(forecast_df.index, forecast_df['mean'], label='AI Forecast', color='red', linestyle='--')
plt.fill_between(forecast_df.index, forecast_df['mean_ci_lower'], forecast_df['mean_ci_upper'], color='pink', alpha=0.3)
plt.title("Logistics Shipment Demand: 6-Month AI Projection")
plt.legend()
plt.show()

print("Forecasted Demand for next 3 months:")
print(forecast_df['mean'].head(3))
