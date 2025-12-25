import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
import joblib
import os

# Create model folder if not exists
os.makedirs("model", exist_ok=True)

# Load dataset
data = pd.read_csv("data/student_performance.csv")

# Drop unnecessary columns
data = data.drop(['student_id', 'grade'], axis=1)

# Features and target
X = data[['weekly_self_study_hours', 'attendance_percentage', 'class_participation']]
y = data['total_score']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = LinearRegression()
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

# Evaluation
print("Mean Absolute Error (MAE):", mean_absolute_error(y_test, y_pred))
print("R2 Score:", r2_score(y_test, y_pred))

# Save model
joblib.dump(model, "model/student_performance_model.pkl")
print("Model saved successfully!")
