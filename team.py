import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

# 1. MOCK DATA GENERATION 
# In a real scenario, this comes from your GPS/Ticketing API
data = {
    'route_id': np.random.randint(101, 110, 1000),
    'hour_of_day': np.random.randint(6, 22, 1000), # 6 AM to 10 PM
    'day_of_week': np.random.randint(0, 7, 1000), # 0=Monday
    'is_holiday': np.random.choice([0, 1], 1000, p=[0.9, 0.1]),
    'historical_passenger_count': np.random.randint(5, 50, 1000),
    'available_cargo_volume_sqft': np.random.uniform(5.0, 25.0, 1000) # Target Variable
}

df = pd.DataFrame(data)

# 2. FEATURE ENGINEERING
X = df[['route_id', 'hour_of_day', 'day_of_week', 'is_holiday', 'historical_passenger_count']]
y = df['available_cargo_volume_sqft']

# Split data: 80% Training, 20% Testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. MODEL INITIALIZATION
# RandomForest is robust for logistics forecasting
model = RandomForestRegressor(n_estimators=100, random_state=42)

# 4. TRAINING
model.fit(X_train, y_train)

# 5. PREDICTION LOGIC
def predict_bus_space(route, hour, day, passengers):
    """
    Predicts if a bus on a specific route will have enough space for a shipment.
    """
    input_data = pd.DataFrame([[route, hour, day, 0, passengers]], 
                              columns=X.columns)
    prediction = model.predict(input_data)
    return round(prediction[0], 2)

# Example: Predict space for Route 105 at 5 PM on a Wednesday
space_available = predict_bus_space(105, 17, 2, 35)
print(f"Predicted Available Space for Route 105: {space_available} sq ft")

# 6. EVALUATION
predictions = model.predict(X_test)
print(f"Model Mean Absolute Error: {mean_absolute_error(y_test, predictions):.2f} sq ft")
