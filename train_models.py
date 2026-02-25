import pandas as pd
import numpy as np
import os
from feature_engineering import create_features
from xgboost import XGBRegressor
from statsmodels.tsa.statespace.sarimax import SARIMAX
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler
import joblib

def train_models():

    #Create models folder
    os.makedirs("models" , exist_ok=True)
    df = pd.read_excel("data/daily_sales.xlsx")
    df = create_features(df)

    X = df.drop(columns=['Date', 'Daily_Sales'])
    y = df['Daily_Sales']

    split = int(len(df) * 0.8)

    X_train = X[:split]
    y_train = y[:split]

    # ---------- XGBoost ----------
    xgb_model = XGBRegressor()
    xgb_model.fit(X_train, y_train)

    joblib.dump(xgb_model, "models/xgb_model.pkl")

    # ---------- SARIMAX ----------
    sarimax_model = SARIMAX(y_train, order=(1,1,1), seasonal_order=(1,1,1,7))
    sarimax_result = sarimax_model.fit()

    joblib.dump(sarimax_result, "models/sarimax_model.pkl")

    # ---------- LSTM ----------
    scaler = MinMaxScaler()
    y_scaled = scaler.fit_transform(y.values.reshape(-1,1))

    X_lstm = []
    y_lstm = []

    for i in range(30, len(y_scaled)):
        X_lstm.append(y_scaled[i-30:i])
        y_lstm.append(y_scaled[i])

    X_lstm, y_lstm = np.array(X_lstm), np.array(y_lstm)

    split_lstm = int(len(X_lstm)*0.8)

    X_train_lstm = X_lstm[:split_lstm]
    y_train_lstm = y_lstm[:split_lstm]

    model_lstm = Sequential()
    model_lstm.add(LSTM(50, return_sequences=False, input_shape=(30,1)))
    model_lstm.add(Dense(1))

    model_lstm.compile(optimizer='adam', loss='mse')
    model_lstm.fit(X_train_lstm, y_train_lstm, epochs=10, batch_size=16)

    model_lstm.save("models/lstm_model.h5")
    joblib.dump(scaler, "models/lstm_scaler.pkl")

    print("All models trained and saved successfully!")

if __name__ == "__main__":
    train_models()