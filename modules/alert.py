import streamlit as st
import pandas as pd
import datetime

ALERT_THRESHOLD = 300  # You can adjust this as needed

def generate_low_stock_alerts(inv_df):
    quantity_col = "CurrentStock"  # Updated for your data format

    if quantity_col not in inv_df.columns:
        st.error(f"❌ Column '{quantity_col}' not found in inventory data.")
        return []

    low_stock_items = inv_df[inv_df[quantity_col] < ALERT_THRESHOLD]

    if not low_stock_items.empty:
        st.warning(f"⚠️ {len(low_stock_items)} item(s) have low stock.")
        alert_messages = []
        for _, row in low_stock_items.iterrows():
            message = (
                f"🔔 LOW STOCK: {row['ProductName']} (Product ID: {row['ProductID']}, "
                f"Store: {row['StoreID']}) has only {row[quantity_col]} units."
            )
            st.error(message)
            alert_messages.append({
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "product_id": row['ProductID'],
                "product_name": row['ProductName'],
                "store_id": row['StoreID'],
                "quantity": row[quantity_col],
                "alert": message
            })
        return alert_messages
    else:
        st.success("✅ All stock levels are sufficient.")
        return []

def display_alert_log(alert_log_df):
    if not alert_log_df.empty:
        st.subheader("📜 Alert Log")
        st.dataframe(alert_log_df.sort_values("timestamp", ascending=False), use_container_width=True)
    else:
        st.info("No alerts have been triggered yet.")
