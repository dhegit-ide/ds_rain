import streamlit as st

def render(df):
    with st.expander(":material/table_view: Dataset"):
        st.dataframe(df)

    st.divider()