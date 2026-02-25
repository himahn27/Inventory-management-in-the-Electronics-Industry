import pandas as pd
import joblib
from xgboost import XGBRegressor
from feature_engineering import create_features

def train_final_model():

    df = pd.read_excel("data/daily_sales.xlsx")
    df = create_features(df)

    X = df.drop(columns=['Date', 'Daily_Sales'])
    y = df['Daily_Sales']

    model = XGBRegressor(
        n_estimators=300,
        learning_rate=0.05,
        max_depth=5
    )

    model.fit(X, y)

    joblib.dump(model, "final_xgb_model.pkl")

    print("Final XGBoost model trained and saved!")

if __name__ == "__main__":
    train_final_model()