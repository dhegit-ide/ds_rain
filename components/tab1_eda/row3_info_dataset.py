import streamlit as st
import pandas as pd

def render(df):
    st.subheader(":material/data_table: Informasi Dataset")
    
    st.dataframe(
        pd.DataFrame({
            "Feature": df.columns,
            "Data Type": df.dtypes.astype(str),
            "Null Count": df.isnull().sum().values,
            "Unique Count": df.nunique().values
        }).reset_index(drop=True)
    )

    st.divider()