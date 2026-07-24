import streamlit as st
import pandas as pd

def render(cv_df):
    st.divider()

    n_unique_ids = cv_df['unique_id'].nunique()
    horizon = cv_df.groupby(['unique_id','cutoff']).size().mean().round(0)  # rata-rata panjang forecast per cutoff
    n_folds = cv_df['cutoff'].nunique()
    pred_cols = [c for c in cv_df.columns if c not in ['unique_id','ds','cutoff','y']]

    if len(pred_cols) == 1: model_info = pred_cols[0]
    else: model_info = f"{len(pred_cols)} models"

    col1, col2, col3, col4 = st.columns(4)    
    with col1:
        with st.container(border=True, gap="xxsmall"):
            st.metric(
                label=":orange-badge[:material/location_city: Unique ID]", 
                value=f"**{n_unique_ids}**",
            )
    with col2:
        with st.container(border=True, gap="xxsmall"):
            st.metric(
                label=":orange-badge[:material/timeline: Horizon]",
                value=f"**{horizon}**",
            )
    with col3:
        with st.container(border=True, gap="xxsmall"):
            st.metric(
                label=":orange-badge[:material/content_cut: Folds]",
                value=f"**{n_folds}**"
            )
    with col4:
        with st.container(border=True, gap="xxsmall"):
            st.metric(
                label=":orange-badge[:material/insights: Model]",
                value=f"**{model_info}**"
            )

    st.divider()