# ml_model.py
# Machine Learning model for predicting traffic congestion

from sklearn.tree import DecisionTreeClassifier

# Training dataset
# Vehicle count -> Traffic level

X = [[10], [20], [30], [40], [50], [60], [70]]
y = ["Low", "Low", "Medium", "Medium", "High", "High", "High"]

# Create the model
model = DecisionTreeClassifier()

# Train the model
model.fit(X, y)


# Function to predict traffic level
def predict_traffic(vehicle_count):

    prediction = model.predict([[vehicle_count]])

    return prediction[0]