import streamlit as st
from forecast import forecast_next_30_days
from inventory import calculate_inventory
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Inventory Forecasting System", layout="wide")

st.title("📈 Demand Forecasting and Component Planning System")

# =========================
# 1️⃣ Forecast Section
# =========================

st.subheader("📂 Upload Recent Sales Data")

uploaded_file = st.file_uploader(
    "Upload Excel File (must contain Date and Daily_Sales columns)",
    type=["xlsx"]
)

if uploaded_file is not None:

    input_df = pd.read_excel(uploaded_file)
    st.session_state["uploaded_df"] = input_df

    if st.button("🔮 Predict Next Month Sales"):

        daily_forecast, monthly_forecast = forecast_next_30_days(input_df)

        st.session_state["daily_forecast"] = daily_forecast
        st.session_state["monthly_forecast"] = monthly_forecast

# Always display forecast if already calculated
if "daily_forecast" in st.session_state:

    st.subheader("📅 Next 30 Days Sales Forecast")
    display_df = st.session_state["daily_forecast"].copy()
    display_df["Date"] = pd.to_datetime(display_df["Date"]).dt.strftime("%Y-%m-%d")
    st.dataframe(display_df)
    
    forecast_df = st.session_state["daily_forecast"]
    first_forecast_date = forecast_df["Date"].iloc[0]

    forecast_month_name = pd.to_datetime(first_forecast_date).strftime("%B")

    st.success(
        f"📊 Total Forecasted Boards for {forecast_month_name}: "
        f"{st.session_state['monthly_forecast']}"
    )
if "daily_forecast" in st.session_state and "uploaded_df" in st.session_state:

    uploaded_df = st.session_state["uploaded_df"].copy()
    uploaded_df["Type"] = "Actual"

    forecast_df = st.session_state["daily_forecast"].copy()
    forecast_df.rename(columns={"Predicted_Sales": "Daily_Sales"}, inplace=True)
    forecast_df["Type"] = "Forecast"

    combined = pd.concat([uploaded_df, forecast_df])

    st.subheader("📈 Actual vs Forecast Comparison")

    fig, ax = plt.subplots()

    actual_data = combined[combined["Type"] == "Actual"]
    forecast_data = combined[combined["Type"] == "Forecast"]

    ax.plot(actual_data["Date"], actual_data["Daily_Sales"], label="Actual")
    ax.plot(forecast_data["Date"], forecast_data["Daily_Sales"], label="Forecast")

    ax.legend()
    ax.set_xlabel("Date")
    ax.set_ylabel("Boards Sold")

    st.pyplot(fig)
# =========================
# 2️⃣ Inventory Section
# =========================

if "monthly_forecast" in st.session_state:

    st.subheader("🔧 Component Inventory Calculator")

    components = {
    "1000171-v2 PCB": 1,
    "C6 - 103J100": 1,
    "C8 - D4 1N4007 Diode": 1,
    "C9 - JVS222M2EEELS": 1,
    "C10, C11 - ERF1VM102G250T": 2,
    "C14 - LHK220M50V511": 1,
    "CN2 - A2006-WV09X2": 1,
    "CN3 - A2006-WV07X2": 1,
    "F1 - NTS1630A": 1,
    "HS1 - Heatsink": 1,
    "Heatsink Clip": 1,
    "L2 - BT-L3-SK-0033": 1,
    "L3 - IND-500uH-0.75A-3X12": 1,
    "SW1 - Tact Switch": 1,
    "T1 - BT-T2-SK-0033": 1,
    "T3 - 4000107-V1": 1,
    "U3 - LM78L05": 1,
    "Screw": 1,
    "Shrink Sleeve (Meter)": 0.014,
    "Spring Washer": 1,
    "C2, DC1, DC2, C4 - CAP-104": 4,
    "C1 - LHK101M16V511": 1,
    "C3 - LHK102M16V1015": 1,
    "R1 - RES-2K-0805-SMD": 1,
    "R4 - RES-1R-5%-WWHSH-1W": 1,
    "R7 - RES-4.7K-5%-0805-SMD": 1,
    "R16 - RES-0E-0805-SMD": 1,
    "R8-R20 Group - RES-0E-1206-SMD": 10,
    "LED - CON-2610-03-M-S/T": 1,
    "KEYS - CON-2510-05-M-S/T": 1,
    "DISPLAY - 14PIN HEADER": 1
}
    component_name = st.selectbox(
        "Select Component",
        list(components.keys())
    )

    units_per_board = components[component_name]

    current_stock = st.number_input(
        "Current Stock Available",
        min_value=0
    )

    if st.button("📊 Calculate Inventory Requirement"):

        result = calculate_inventory(
            forecast_demand=st.session_state["monthly_forecast"],
            current_stock=current_stock,
            units_per_board=units_per_board
        )

        st.subheader("📦 Inventory Result")

        st.write("Component Selected:", component_name)
        st.write("Units per Board:", units_per_board)
        st.write("Total Required:", result["Total Required"])
        st.write("Current Stock:", result["Current Stock"])
        st.write("Order Quantity:", result["Order Quantity"])
        st.write("Status:", result["Status"])

    # Pie Chart for Component Requirement
        st.subheader("📊 Component Requirement Distribution")

        total_required = result["Total Required"]
        current_stock = result["Current Stock"]
        order_quantity = result["Order Quantity"]

        labels = ["Available Stock", "Additional Required"]
        sizes = [current_stock, order_quantity]

        fig2, ax2 = plt.subplots()
        ax2.pie(sizes, labels=labels, autopct="%1.1f%%")
        ax2.set_title("Component Requirement Breakdown")

        st.pyplot(fig2)    