import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
import joblib
import os

# ── Step 1: Load dataset ──────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_path = os.path.join(BASE_DIR, "datasets", "pest_data.csv")

df = pd.read_csv(data_path)
print("Dataset loaded successfully!")
print(df.head())
print(f"\nTotal rows: {len(df)}")

# ── Step 2: Encode Crop_Type (text → number) ──────────────────────────────────
# Machine learning models only understand numbers, not words like "Rice"
# LabelEncoder converts: Maize=0, Rice=1, Sugarcane=2, Vegetables=3, Wheat=4
encoder = LabelEncoder()
df["Crop_Type_Encoded"] = encoder.fit_transform(df["Crop_Type"])

print(f"\nCrop types found: {list(encoder.classes_)}")

# ── Step 3: Prepare features and labels ──────────────────────────────────────
X = df[["Temperature", "Humidity", "Rainfall", "Crop_Type_Encoded"]]
y = df["Pest_Risk"]

# ── Step 4: Split into training and testing sets ──────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print(f"\nTraining samples: {len(X_train)}")
print(f"Testing samples:  {len(X_test)}")

# ── Step 5: Train the model ───────────────────────────────────────────────────
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
print("\nModel training complete!")

# ── Step 6: Check accuracy ────────────────────────────────────────────────────
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model accuracy: {accuracy * 100:.1f}%")

# ── Step 7: Save BOTH the model AND the encoder ───────────────────────────────
# We must save the encoder too so the Streamlit app can convert crop names
model_path   = os.path.join(BASE_DIR, "models", "pest_model.pkl")
encoder_path = os.path.join(BASE_DIR, "models", "pest_encoder.pkl")

joblib.dump(model,   model_path)
joblib.dump(encoder, encoder_path)

print(f"\nModel saved at:   {model_path}")
print(f"Encoder saved at: {encoder_path}")
print("\nDone! Phase 3 model is ready.")