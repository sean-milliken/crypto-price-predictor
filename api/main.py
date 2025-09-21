from fastapi import FastAPI
import joblib
import pandas as pd
import yfinance as yf

from fastapi.middleware.cors import CORSMiddleware

# Load trained model and feature list
model, features = joblib.load("models/rf_model.joblib")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins (for demo/hackathon)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_features(symbol: str):
    """Fetch latest feature values for a given crypto symbol."""
    # Get more history (30 days instead of 15)
    df = yf.download(symbol, period="30d", interval="1d")
    
    if df.empty:
        raise ValueError(f"No data returned for {symbol}")
    
    # Feature engineering
    df["Return"] = df["Close"].pct_change()
    df["MA5"] = df["Close"].rolling(5).mean()
    df["MA10"] = df["Close"].rolling(10).mean()
    df["Vol_Change"] = df["Volume"].pct_change()
    df = df.dropna()

    if df.empty:
        raise ValueError(f"Not enough data to build features for {symbol}")
    
    latest = df.iloc[-1]
    return pd.DataFrame([latest[features].to_dict()])

from fastapi.responses import JSONResponse

@app.get("/predict/{symbol}")
def predict(symbol: str):
    try:
        X = get_features(symbol)
        proba = model.predict_proba(X)[0, 1]
        pred = int(proba > 0.5)
        return {
            "symbol": symbol,
            "prediction": "UP" if pred else "DOWN",
            "probability": round(float(proba), 4),
        }
    except Exception as e:
        return JSONResponse(
            status_code=400,  # Bad Request instead of 500
            content={"error": str(e), "symbol": symbol}
        )