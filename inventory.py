import numpy as np

def calculate_inventory(
    forecast_demand,
    current_stock,
    units_per_board
):

    # 1️⃣ Total components required for next month
    total_required = forecast_demand * units_per_board

    # 2️⃣ How many more components needed
    order_quantity = max(0, total_required - current_stock)

    # 3️⃣ Stock status
    if current_stock >= total_required:
        status = "Sufficient Stock ✅"
    else:
        status = "Need to Order ❌"

    return {
        "Total Required": round(total_required),
        "Current Stock": round(current_stock),
        "Order Quantity": round(order_quantity),
        "Status": status
    }