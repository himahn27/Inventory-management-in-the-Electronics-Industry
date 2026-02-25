import pandas as pd
import numpy as np

def create_features(df):
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date')

    # Time features
    df['day_of_week'] = df['Date'].dt.dayofweek
    df['month'] = df['Date'].dt.month
    df['is_weekend'] = df['day_of_week'].apply(lambda x: 1 if x >= 5 else 0)

    # Lag features
    df['lag_1'] = df['Daily_Sales'].shift(1)
    df['lag_7'] = df['Daily_Sales'].shift(7)
    df['lag_30'] = df['Daily_Sales'].shift(30)

    # Rolling mean
    df['rolling_mean_7'] = df['Daily_Sales'].rolling(7).mean()

    df = df.dropna()

    return df