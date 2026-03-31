import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import pickle
from sklearn.metrics import accuracy_score

# Load dataset
data = pd.read_csv("parkinsons.csv")

# Remove text column 'name' safely
if "name" in data.columns:
    data = data.drop(columns=["name"])

# Target column
X = data.drop(columns=["status"])
y = data["status"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = LogisticRegression(max_iter=2000)

model.fit(X_train, y_train)

# Accuracy
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print("Parkinson Model Accuracy:", accuracy)

# Save model
pickle.dump(model, open("parkinson_model.sav", "wb"))

print("Parkinson model trained successfully")
