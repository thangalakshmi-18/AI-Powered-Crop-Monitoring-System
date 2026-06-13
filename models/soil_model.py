import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import os

# ── Step 1: Load dataset ──────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_path = os.path.join(BASE_DIR, "datasets", "soil_data.csv")

df = pd.read_csv(data_path)
print("Dataset loaded successfully!")
print(df.head())

# ── Step 2: Prepare features and labels ──────────────────────────────────────
X = df[["Nitrogen", "Phosphorus", "Potassium", "pH", "Moisture"]]
y = df["Soil_Condition"]

# ── Step 3: Split into training and testing sets ──────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ── Step 4: Train the model ───────────────────────────────────────────────────
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
print("\nModel training complete!")

# ── Step 5: Check accuracy ────────────────────────────────────────────────────
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model accuracy: {accuracy * 100:.1f}%")

# ── Step 6: Save the model ────────────────────────────────────────────────────
model_path = os.path.join(BASE_DIR, "models", "soil_model.pkl")
joblib.dump(model, model_path)
print(f"\nModel saved at: {model_path}")
print("Done! You can now use this model in your Streamlit app.")