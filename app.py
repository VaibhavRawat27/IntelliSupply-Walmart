# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
from modules.route_optimizer import optimize_route
from modules.forecaster import forecast_inventory
from modules.rebalancer import suggest_rebalance
from modules.visualizer import show_inventory_charts
from modules.data_editor import edit_and_save_csv
from modules.alert import generate_low_stock_alerts, display_alert_log

if "alert_log" not in st.session_state:
    st.session_state.alert_log = pd.DataFrame(columns=["timestamp", "product_id", "product_name", "quantity", "alert"])
# Set Streamlit page config
st.set_page_config(page_title="IntelliSupply Dashboard", layout="wide")

# Title and Overview
st.title("📦 IntelliSupply: Smart Retail Supply Chain Platform")
st.markdown("""
Welcome to **IntelliSupply**, your smart dashboard for transforming retail supply chain management.

This application performs:
- **Inventory Forecasting** using historical stock data.
- **Warehouse Stock Rebalancing** for optimal distribution.
- **Last-Mile Delivery Optimization** using geospatial route calculations.
- **Interactive Visualizations** for KPIs and trends.

Try with your own datasets or explore with the demo use-case below.
""")

# --- Data Loading Section ---
st.sidebar.header("📂 Load and Inspect Data")
st.sidebar.markdown("Upload or use default datasets for analysis.")
with st.sidebar.expander("📊 Preview Loaded Data Files"):
    inv_df = pd.read_csv("data/inventory_data.csv")
    sales_df = pd.read_csv("data/sales_history.csv")
    delivery_df = pd.read_csv("data/delivery_data.csv")
    supplier_df = pd.read_csv("data/supplier_data.csv")
    warehouse_df = pd.read_csv("data/warehouse_locations.csv")
    restock_df = pd.read_csv("data/restock_requests.csv")

    st.success("✅ Data loaded successfully.")
    st.write("**🧾 Inventory Data:**", inv_df.head())
    st.write("**📈 Sales History:**", sales_df.head())
    st.write("**🚚 Delivery Data:**", delivery_df.head())
    st.write("**🏭 Supplier Data:**", supplier_df.head())
    st.write("**📦 Warehouse Locations:**", warehouse_df.head())
    st.write("**📋 Restock Requests:**", restock_df.head())

# --- Inventory Forecasting ---
st.header("📈 Inventory Forecasting")
st.markdown("""
**Goal**: Estimate future stock needs based on sales trends and current inventory.

**Scenario**: Warehouse A is running low on Product X. Based on sales history, we forecast it will run out in 5 days.

**Solution**: This section uses ML/statistical methods to project demand.
""")
forecast = forecast_inventory(inv_df)
st.subheader("🔍 Forecasted Inventory Table")
st.dataframe(forecast, use_container_width=True)

st.subheader("📉 Forecast Visualization")
if 'product_id' in forecast.columns:
    sample_prod = forecast['product_id'].iloc[0]
    fig = px.line(forecast[forecast['product_id'] == sample_prod], x='date', y='forecast_qty', title=f"Forecast for Product ID {sample_prod}")
    st.plotly_chart(fig, use_container_width=True)

# --- Rebalancing Suggestions ---
st.header("🔄 Stock Rebalancing Suggestions")
st.markdown("""
**Goal**: Prevent overstocking and stockouts.

**Scenario**: Warehouse B is overstocked on Product Y, while Warehouse D is nearly empty.

**Solution**: Suggest transferring 500 units of Product Y from B to D.
""")
rebalance = suggest_rebalance(inv_df)
st.subheader("🔁 Rebalance Table")
st.dataframe(rebalance, use_container_width=True)

if not rebalance.empty and {'from_warehouse', 'to_warehouse', 'quantity'}.issubset(rebalance.columns):
    st.subheader("📊 Rebalance Heatmap")
    fig2 = px.sunburst(rebalance, path=['from_warehouse', 'to_warehouse'], values='quantity', title="Stock Movement Suggestions")
    st.plotly_chart(fig2, use_container_width=True)

# --- Route Optimization ---
st.header("🚚 Last-Mile Delivery Optimization")
st.markdown("""
**Goal**: Minimize delivery times and fuel costs.

**Scenario**: Deliver orders to 10 customers in Mumbai.

**Solution**: Use OSRM API to compute the most efficient route.
""")
locations = delivery_df.to_dict(orient="records")
route_geo = optimize_route(locations)

if route_geo and 'coordinates' in route_geo:
    st.subheader("🗺️ Optimized Route Map")
    st.map(pd.DataFrame([{"lat": lat, "lon": lon} for lon, lat in route_geo['coordinates']]))
    st.success("✅ Route plotted successfully.")
else:
    st.warning("⚠️ Unable to fetch route. Please verify delivery data format.")

# --- Visual Insights ---
st.header("📊 Visual Insights")
st.markdown("""
**Goal**: Understand performance and trends.

**Scenario**: Product Z has high weekend demand. Warehouse C has low turnover.
""")
show_inventory_charts(inv_df, sales_df)

# --- Restocking Requests ---
st.header("📋 Restocking Requests")
st.markdown("""
**Goal**: Manage incoming restocking needs from various warehouses.
""")
st.dataframe(restock_df, use_container_width=True)

# --- Footer ---
st.success("✅ IntelliSupply Dashboard Loaded Successfully")
st.markdown("""
---
### 🛠️ How This Works
1. Upload/stream inventory, sales, and delivery data.
2. IntelliSupply analyzes data using forecasting, rebalancing logic, and OSRM-based routing.
3. You get interactive tables, visual charts, and delivery route maps.

### 📦 Modules Summary
- `forecast_inventory`: Inventory demand prediction.
- `suggest_rebalance`: Smart redistribution logic.
- `optimize_route`: Real-time delivery optimization.
- `show_inventory_charts`: Visual analytics module.

### 🔍 Demo: Try This
- Modify `inventory_data.csv` and refresh.
- Observe changes in forecast, stock movement, and delivery maps.
- Watch the analytics reflect real-time updates.
""")

# --- Full CSV Management Section ---
st.header("🗃️ Data Manager & Editor")
st.markdown("Edit any CSV file interactively and save changes.")

inv_df = edit_and_save_csv("Inventory Data", "data/inventory_data.csv")
sales_df = edit_and_save_csv("Sales History", "data/sales_history.csv")
delivery_df = edit_and_save_csv("Delivery Data", "data/delivery_data.csv")
supplier_df = edit_and_save_csv("Supplier Data", "data/supplier_data.csv")
warehouse_df = edit_and_save_csv("Warehouse Locations", "data/warehouse_locations.csv")
restock_df = edit_and_save_csv("Restock Requests", "data/restock_requests.csv")

st.header("🚨 Inventory Alerts & Notifications")
alerts = generate_low_stock_alerts(inv_df)

if alerts:
    st.session_state.alert_log = pd.concat([st.session_state.alert_log, pd.DataFrame(alerts)], ignore_index=True)

display_alert_log(st.session_state.alert_log)\

