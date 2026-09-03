import streamlit as st

def render(df):
    st.subheader(":material/table_view: Preview Dataset")
    st.dataframe(df)

    st.divider()