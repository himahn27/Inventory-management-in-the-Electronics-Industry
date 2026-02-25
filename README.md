# 📦 Inventory Management in the Electronics Industry

## 📌 Project Overview

This project focuses on inventory planning and demand forecasting for electronic components used in motherboard manufacturing.

The system predicts next month’s motherboard sales based on historical daily sales data and calculates the required component quantities based on current stock levels.

It integrates sales forecasting with inventory calculation to support production planning decisions.

---

## 🎯 Objective

- Predict next month’s motherboard sales
- Convert board-level demand into component-level requirements
- Compare required components with current stock
- Determine order quantity for each selected component

---

## 🏗️ Project Structure
```
inventory_management/   

│
├── app.py                       # Streamlit UI
├── forecast.py                  # Sales forecasting logic
├── inventory.py                 # Inventory calculation logic
├── feature_engineering.py       # Creates model features
├── train_models.py              # Trains forecasting models
├── evaluate_models.py           # Evaluates model performance
├── final_xgb_model.pkl          # Trained XGBoost model
├── requirements.txt             # Project dependencies
└── .gitignore                   # Git ignored files
```
## 📊 Forecasting Models Used

Three models were trained and evaluated:

### 1️⃣ XGBoost Regressor
- Gradient boosting-based regression model
- Handles non-linear patterns effectively
- Best performing model based on MAE, RMSE, and MAPE

### 2️⃣ SARIMAX
- Statistical time series model
- Captures seasonality and trend
- Used for comparison

### 3️⃣ LSTM (Long Short-Term Memory)
- Deep learning model for sequence prediction
- Captures temporal dependencies in time series data

After evaluation, **XGBoost** was selected as the final model due to superior performance metrics.

---

## ⚙️ How the System Works

### Step 1: Upload Historical Sales Data
User uploads daily motherboard sales data (minimum 30 days recommended).

### Step 2: Forecast Next 30 Days
The trained XGBoost model predicts the next 30 days of sales based on lag features and rolling averages.

### Step 3: Calculate Monthly Forecast
The system sums predicted daily sales to obtain total forecasted boards for the next month.

### Step 4: Component Inventory Calculation
Based on:
- Forecasted boards
- Units required per board (BOM)
- Current stock available

The system calculates:
- Total required components
- Order quantity needed

---

## 📈 Features

- Recursive 30-day sales forecasting
- Feature engineering with lag variables
- Multi-month dataset support
- Component-level inventory calculation
- Interactive Streamlit dashboard
- Visualization:
  - Actual vs Forecast comparison chart
  - Component requirement pie chart

---

## 🛠️ Technologies Used

- Python
- Pandas
- NumPy
- XGBoost
- Statsmodels (SARIMAX)
- TensorFlow / Keras (LSTM)
- Streamlit
- Matplotlib

---
Created by Hima
