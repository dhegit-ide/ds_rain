import streamlit as st

def render(df):
    st.divider()
    with st.expander(":material/table_view: Lihat Sampel Data"):
        st.dataframe(df)
    st.divider()