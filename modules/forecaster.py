# modules/forecaster.py
import pandas as pd

def forecast_inventory(inv_df):
    forecast_list = []
    for _, row in inv_df.iterrows():
        avg_daily_sales = row['CurrentStock'] / 15  # mock logic: assume current stock lasts 15 days
        days_left = row['CurrentStock'] / avg_daily_sales
        forecast_list.append({
            "ProductID": row['ProductID'],
            "ProductName": row['ProductName'],
            "CurrentStock": row['CurrentStock'],
            "ForecastedDaysLeft": round(days_left, 1),
            "RestockNeeded": "Yes" if days_left < 7 else "No"
        })
    return pd.DataFrame(forecast_list)
