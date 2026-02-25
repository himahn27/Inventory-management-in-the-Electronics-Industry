import pandas as pd
import numpy as np
import joblib
from feature_engineering import create_features
from sklearn.metrics import mean_absolute_error, mean_squared_error
from tensorflow.keras.models import load_model

def evaluate():

    df = pd.read_excel("data/daily_sales.xlsx")
    df = create_features(df)

    X = df.drop(columns=['Date', 'Daily_Sales'])
    y = df['Daily_Sales']

    split = int(len(df) * 0.8)

    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]

    results = []

    # ------------------ XGBOOST ------------------
    xgb_model = joblib.load("models/xgb_model.pkl")
    xgb_pred = xgb_model.predict(X_test)

    xgb_mae = mean_absolute_error(y_test, xgb_pred)
    xgb_rmse = np.sqrt(mean_squared_error(y_test, xgb_pred))
    xgb_mape = np.mean(np.abs((y_test - xgb_pred) / y_test)) * 100

    results.append(["XGBoost", xgb_mae, xgb_rmse, xgb_mape])


    # ------------------ SARIMAX ------------------
    sarimax_model = joblib.load("models/sarimax_model.pkl")
    sarimax_pred = sarimax_model.forecast(steps=len(y_test))

    sarimax_mae = mean_absolute_error(y_test, sarimax_pred)
    sarimax_rmse = np.sqrt(mean_squared_error(y_test, sarimax_pred))
    sarimax_mape = np.mean(np.abs((y_test - sarimax_pred) / y_test)) * 100

    results.append(["SARIMAX", sarimax_mae, sarimax_rmse, sarimax_mape])


    # ------------------ LSTM ------------------
    lstm_model = load_model("models/lstm_model.h5", compile=False)
    scaler = joblib.load("models/lstm_scaler.pkl")

    y_scaled = scaler.transform(y.values.reshape(-1,1))

    X_lstm = []
    y_lstm = []

    for i in range(30, len(y_scaled)):
        X_lstm.append(y_scaled[i-30:i])
        y_lstm.append(y_scaled[i])

    X_lstm = np.array(X_lstm)
    y_lstm = np.array(y_lstm)

    split_lstm = int(len(X_lstm) * 0.8)

    X_test_lstm = X_lstm[split_lstm:]
    y_test_lstm = y_lstm[split_lstm:]

    lstm_pred_scaled = lstm_model.predict(X_test_lstm)
    lstm_pred = scaler.inverse_transform(lstm_pred_scaled)
    y_test_actual = scaler.inverse_transform(y_test_lstm)

    lstm_mae = mean_absolute_error(y_test_actual, lstm_pred)
    lstm_rmse = np.sqrt(mean_squared_error(y_test_actual, lstm_pred))
    lstm_mape = np.mean(np.abs((y_test_actual - lstm_pred) / y_test_actual)) * 100

    results.append(["LSTM", lstm_mae, lstm_rmse, lstm_mape])


    # ------------------ Store Results ------------------

    results_df = pd.DataFrame(results,
                              columns=["Model", "MAE", "RMSE", "MAPE"])

    # Round values
    results_df[["MAE", "RMSE", "MAPE"]] = results_df[["MAE", "RMSE", "MAPE"]].round(2)

    # Identify best model (lowest RMSE)
    best_model = results_df.loc[results_df["RMSE"].idxmin(), "Model"]

    print("\n===== Model Comparison Results =====\n")
    print(results_df)
    print(f"\nBest Model Based on RMSE: {best_model}")

    # Save neatly
    results_df.to_csv("model_comparison_results.csv", index=False)

    print("\nResults saved to:")
    print("model_comparison_results.csv")


if __name__ == "__main__":
    evaluate()