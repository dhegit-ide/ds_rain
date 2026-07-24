import streamlit as st
import pandas as pd

def render(df):
    st.divider()

    if not pd.api.types.is_datetime64_any_dtype(df['ds']):
        df['ds'] = pd.to_datetime(df['ds'], errors='coerce')

    n_rows, n_cols = df.shape
    start_date = df['ds'].min()
    end_date = df['ds'].max()

    col1, col2, col3, col4 = st.columns(4)    
    with col1:
        with st.container(border=True, gap="xxsmall"):
            st.metric(
                label=":orange-badge[:material/table_rows: Rows]", 
                value=f"**{n_rows}**",
            )
    with col2:
        with st.container(border=True, gap="xxsmall"):
            st.metric(
                label=":orange-badge[:material/view_column: Columns]",
                value=f"**{n_cols}**",
            )
    with col3:
        with st.container(border=True, gap="xxsmall"):
            st.metric(
                label=":orange-badge[:material/calendar_today: Start Date]",
                value=start_date.strftime("**%d %b %Y**")
            )
    with col4:
        with st.container(border=True, gap="xxsmall"):
            st.metric(
                label=":orange-badge[:material/event: End Date]",
                value=end_date.strftime("**%d %b %Y**")
            )

    st.divider()