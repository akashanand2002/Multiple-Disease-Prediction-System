from sklearn.metrics import accuracy_score
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import pickle

# column names
columns = [
    "Pregnancies",
    "Glucose",
    "BloodPressure",
    "SkinThickness",
    "Insulin",
    "BMI",
    "DiabetesPedigreeFunction",
    "Age",
    "Outcome",
]

# load dataset
data = pd.read_csv("diabetes.csv", names=columns)

X = data.drop("Outcome", axis=1)
y = data["Outcome"]

# split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# train model
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# save model
pickle.dump(model, open("diabetes_model.sav", "wb"))

print("Model trained successfully")

# prediction on test data
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("Model Accuracy:", accuracy)
