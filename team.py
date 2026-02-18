import requests
import pandas as pd
from datetime import datetime
from sklearn.ensemble import RandomForestRegressor

# --- SIMULATED TRANSIT API CONFIG ---
# In reality, this would be your City's Transport API (e.g., Delhi Transit, Transport for London)
TRANSIT_API_URL = "https://api.citytransit.com/v1/live_bus_status"

class LogisticsAI:
    def __init__(self):
        # The model is pre-trained on historical "Bus Occupancy vs Cargo Space"
        self.model = RandomForestRegressor(n_estimators=100)
        self._train_mock_model()

    def _train_mock_model(self):
        # Simulated historical training data: [Route_ID, Hour, Day, Pax_Count]
        # Target: Available_Cargo_Volume (Cubic Feet)
        train_x = [[101, 8, 0, 45], [101, 14, 0, 10], [102, 9, 1, 50], [102, 21, 1, 5]]
        train_y = [2.5, 15.0, 1.0, 18.5]
        self.model.fit(train_x, train_y)

    def get_live_bus_data(self, route_id):
        """
        Scenario: Fetching real-time passenger load from the Bus API.
        If the bus is 90% full of people, cargo space is low.
        """
        # Mocking an API Response
        response = {
            "status": "success",
            "data": {
                "bus_id": "BUS-99",
                "current_pax_count": 38,  # Data from electronic ticketing/sensors
                "eta_minutes": 12
            }
        }
        return response['data']

    def predict_responsiveness(self, route_id):
        """
        The Core Logic: Decide if we should send the shipment on THIS bus
        or wait for the next one to ensure 'Responsiveness'.
        """
        live_data = self.get_live_bus_data(route_id)
        now = datetime.now()
        
        # Prepare feature vector for AI
        features = [[route_id, now.hour, now.weekday(), live_data['current_pax_count']]]
        
        predicted_space = self.model.predict(features)[0]
        
        # Business Logic: We need at least 5 cubic feet for a standard shipment
        if predicted_space >= 5.0:
            return {
                "decision": "PROCEED",
                "bus_id": live_data['bus_id'],
                "eta": live_data['eta_minutes'],
                "predicted_space": f"{predicted_space} cu ft"
            }
        else:
            return {
                "decision": "REROUTE",
                "reason": "Insufficient Space",
                "next_best_route": "Route-102 (ETA 25m)"
            }

# --- EXECUTION ---
startup_ai = LogisticsAI()
shipment_plan = startup_ai.predict_responsiveness(route_id=101)

print(f"--- Shipment Dispatch Control ---")
print(f"Action: {shipment_plan['decision']}")
if shipment_plan['decision'] == "PROCEED":
    print(f"Assign to: {shipment_plan['bus_id']} (Arriving in {shipment_plan['eta']} mins)")
else:
    print(f"Wait: {shipment_plan['reason']}. Strategy: {shipment_plan['next_best_route']}")
