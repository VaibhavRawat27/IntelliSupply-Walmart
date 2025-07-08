import streamlit as st
import pandas as pd
import os

def edit_and_save_csv(label, filepath):
    st.subheader(f"✏️ Edit: {label}")
    try:
        df = pd.read_csv(filepath)
        edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)

        if st.button(f"💾 Save {label}", key=label):
            edited_df.to_csv(filepath, index=False)
            st.success(f"{label} saved successfully to {filepath}")

        return edited_df

    except Exception as e:
        st.error(f"Failed to load {label}: {e}")
        return pd.DataFrame()
