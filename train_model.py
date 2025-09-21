import os
import pandas as pd
import yfinance as yf
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

# 1. Get data
df = yf.download("BTC-USD", start="2022-01-01", end="2023-12-31")

# 2. Feature engineering
df["Return"] = df["Close"].pct_change()
df["MA5"] = df["Close"].rolling(5).mean()
df["MA10"] = df["Close"].rolling(10).mean()
df["Vol_Change"] = df["Volume"].pct_change()
df = df.dropna()

# 3. Target: 1 if tomorrow up, else 0
df["Target"] = (df["Close"].shift(-1) > df["Close"]).astype(int)

features = ["Return", "MA5", "MA10", "Vol_Change"]
X = df[features]
y = df["Target"]

X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, shuffle=False)

# 4. Train
clf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
clf.fit(X_train, y_train)

# 5. Ensure models folder exists
os.makedirs("models", exist_ok=True)

# 6. Save model
joblib.dump((clf, features), "models/rf_model.joblib")
print("✅ Model saved to models/rf_model.joblib")
