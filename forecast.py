import pandas as pd
import joblib
from feature_engineering import create_features

MODEL_PATH = "final_xgb_model.pkl"
BASE_DATA_PATH = "data/daily_sales.xlsx"

def forecast_next_30_days(uploaded_df):

    model = joblib.load(MODEL_PATH)

    # Load full historical data
    base_df = pd.read_excel(BASE_DATA_PATH)

    # Append uploaded recent data
    combined_df = pd.concat([base_df, uploaded_df], ignore_index=True)

    combined_df["Date"] = pd.to_datetime(combined_df["Date"])
    combined_df = combined_df.sort_values("Date")

    # Create features
    df = create_features(combined_df)

    history = df.copy()

    predictions = []

    for _ in range(30):

        last_row = history.iloc[-1]
        next_date = last_row["Date"] + pd.Timedelta(days=1)

        new_row = {}
        new_row["Date"] = next_date
        new_row["day_of_week"] = next_date.dayofweek
        new_row["month"] = next_date.month
        new_row["is_weekend"] = 1 if next_date.dayofweek >= 5 else 0

        new_row["lag_1"] = history["Daily_Sales"].iloc[-1]
        new_row["lag_7"] = history["Daily_Sales"].iloc[-7]
        new_row["lag_30"] = history["Daily_Sales"].iloc[-30]
        new_row["rolling_mean_7"] = history["Daily_Sales"].iloc[-7:].mean()

        feature_df = pd.DataFrame([new_row])
        X_future = feature_df.drop(columns=["Date"])

        pred = model.predict(X_future)[0]

        new_row["Daily_Sales"] = pred

        history = pd.concat(
            [history, pd.DataFrame([new_row])],
            ignore_index=True
        )

        predictions.append({
            "Date": next_date,
            "Predicted_Sales": round(pred)
        })

    forecast_df = pd.DataFrame(predictions)
    monthly_total = forecast_df["Predicted_Sales"].sum()

    return forecast_df, round(monthly_total)