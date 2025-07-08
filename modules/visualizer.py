import streamlit as st
import plotly.express as px
import pandas as pd

def show_inventory_charts(inv_df, sales_df):
    st.subheader("📦 Inventory & Sales Visual Insights")

    # 📊 Chart 1: Stock Levels by Product
    fig1 = px.bar(
        inv_df.groupby("ProductName", as_index=False)["CurrentStock"].sum(),
        x="ProductName", y="CurrentStock",
        title="🧊 Current Stock Levels by Product",
        color="CurrentStock", color_continuous_scale="Blues",
        text_auto=True
    )
    st.plotly_chart(fig1, use_container_width=True)

    # 📊 Chart 2: Sales by Product
    fig2 = px.bar(
        sales_df.groupby("ProductName", as_index=False)["UnitsSold"].sum(),
        x="ProductName", y="UnitsSold",
        title="🔥 Total Units Sold by Product",
        color="UnitsSold", color_continuous_scale="Oranges",
        text_auto=True
    )
    st.plotly_chart(fig2, use_container_width=True)

    # 📈 Chart 3: Time Series of Sales (if available)
    if 'Date' in sales_df.columns:
        sales_df['Date'] = pd.to_datetime(sales_df['Date'])
        timeseries = sales_df.groupby(['Date', 'ProductName'], as_index=False)['UnitsSold'].sum()
        fig3 = px.line(
            timeseries, x="Date", y="UnitsSold", color="ProductName",
            title="📆 Sales Trend Over Time",
            markers=True
        )
        st.plotly_chart(fig3, use_container_width=True)

    # 📊 Chart 4: Store-wise Inventory Heatmap
    if 'StoreID' in inv_df.columns:
        heatmap_df = inv_df.groupby(["StoreID", "ProductName"], as_index=False)["CurrentStock"].sum()
        fig4 = px.density_heatmap(
            heatmap_df, x="StoreID", y="ProductName", z="CurrentStock",
            title="🌐 Inventory Heatmap Across Stores",
            color_continuous_scale="Viridis"
        )
        st.plotly_chart(fig4, use_container_width=True)

    # 📉 Chart 5: Top 5 Low Stock Products
    low_stock = inv_df.groupby("ProductName")["CurrentStock"].sum().sort_values().head(5).reset_index()
    fig5 = px.bar(
        low_stock, x="ProductName", y="CurrentStock",
        title="🚨 Top 5 Low Stock Products",
        color="CurrentStock", text_auto=True, color_continuous_scale="reds"
    )
    st.plotly_chart(fig5, use_container_width=True)

    st.success("✅ All visualizations loaded with full interactivity.")
