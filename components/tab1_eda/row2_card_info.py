import streamlit as st
import pandas as pd
from utils.detect_freq import detect_and_summary

def render(df):
    st.subheader(":material/dashboard: Karakteristik Dataset")
    if not pd.api.types.is_datetime64_any_dtype(df['ds']):
        df['ds'] = pd.to_datetime(df['ds'], errors='coerce')
    
     # --- Card 1: Unique ID ---
    unique_ids = df['unique_id'].unique()
    total_uid = len(unique_ids)
    if total_uid > 5:
        sample_uid = ", ".join(unique_ids[:5]) + ", ..."
    else:
        sample_uid = ", ".join(unique_ids)

    # --- Card 2: Frekuensi Data ---
    freq, start, end, total, unit = detect_and_summary(df)
    st.session_state['data_freq'] = freq
    st.session_state['data_total'] = total
    st.session_state['data_unit'] = unit
    
    # --- Card 3: Shape ---
    rows, cols = df.shape
    dtypes = df.dtypes.value_counts()
    type_summary = " | ".join([f"{count} {dtype}" for dtype, count in dtypes.items()])
    
    # --- Card 4: Kelengkapan Data ---
    total_cells = rows * cols
    missing_cells = df.isna().sum().sum()
    completeness = 100 * (1 - missing_cells / total_cells)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        with st.container(border=True, gap="xxsmall"):
            st.metric(label="Unique ID (Grup)", value=total_uid)
            st.write(f":blue-badge[{sample_uid}]")
    
    with col2:
        with st.container(border=True, gap="xxsmall"):
            st.metric(label=f"Frekuensi Data ({freq})", value=f"{total}")
            st.write(f":blue-badge[{start.year} - {end.year} ({end.year - start.year + 1} tahun)]")
    
    with col3:
        with st.container(border=True, gap="xxsmall"):
            st.metric(label="Shape (Baris, Kolom)", value=f"{rows}, {cols}")
            st.write(f":blue-badge[{type_summary}]")

    with col4:
        with st.container(border=True, gap="xxsmall"):
            st.metric(label="Kelengkapan Data", value=f"{round(completeness, 3):g}%")
            st.write(f":blue-badge[{missing_cells} sel nilai hilang]")