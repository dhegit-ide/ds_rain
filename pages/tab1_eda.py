import streamlit as st
import pandas as pd
from components.tab1_eda import (
    row1_card,
    row2_preview_dataset,
    row3_info_dataset,
    row4_describe_dataset,
    row5_feature_selection,
)
from utils.data_loader import validate_csv, get_numeric_columns

st.title(":material/tile_small: Overview Dataset")
st.info("Gunakan kontrol di sidebar untuk memilih dataset dan pengaturan.")

df = None

# --- Sidebar: semua kontrol di sini ---
with st.sidebar:
    st.markdown("### :material/tune: Settings")

    # Sumber data
    data_source = st.radio("Pilih sumber dataset", ["Upload CSV", "Gunakan contoh dataset"])
    if data_source == "Upload CSV":
        uploaded_file = st.file_uploader("Upload file CSV", type=["csv"])
        if uploaded_file:
            df = pd.read_csv(uploaded_file)
            is_valid, message = validate_csv(df)
            if not is_valid:
                st.error(message)
                st.stop()
            else:
                st.success(message)
                st.session_state['df_raw'] = df
                st.session_state['data_loaded'] = True
    else:
        try:
            df = pd.read_csv("data/bone_wajo_pinrang_sidrap_encoded.csv")
            st.info("Menggunakan dataset contoh bawaan.")
            st.session_state['df_raw'] = df
            st.session_state['data_loaded'] = True
        except FileNotFoundError:
            st.error("File contoh dataset tidak ditemukan di folder data/")

    # Target kolom
    if df is not None:
        numeric_cols = get_numeric_columns(df)
        if numeric_cols:
            st.selectbox(
                "Pilih target kolom",
                options=numeric_cols,
                key="target_column",
            )
        else:
            st.warning(":material/warning: Tidak ada kolom numerik!")
            st.session_state['target_column'] = None

    # Seleksi fitur
    st.selectbox(
        "Pilih Metode Korelasi",
        options=["Pearson", "Spearman", "Kendall", "Mutual Information"],
        key="corr_method",
    )

if df is not None:
    row1_card.render(df)
    row2_preview_dataset.render(df)
    row3_info_dataset.render(df)
    row4_describe_dataset.render(df)
    row5_feature_selection.render(df)
