# modules/rebalancer.py
import pandas as pd

def suggest_rebalance(inv_df):
    suggestions = []
    grouped = inv_df.groupby('ProductID')

    for product_id, group in grouped:
        max_stock = group.loc[group['CurrentStock'].idxmax()]
        min_stock = group.loc[group['CurrentStock'].idxmin()]

        if max_stock['CurrentStock'] - min_stock['CurrentStock'] > 100:
            suggestions.append({
                "ProductID": product_id,
                "FromStore": max_stock['StoreID'],
                "ToStore": min_stock['StoreID'],
                "QtyToTransfer": int((max_stock['CurrentStock'] - min_stock['CurrentStock']) / 2)
            })
    return pd.DataFrame(suggestions)
