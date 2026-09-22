import streamlit as st
import pandas as pd
from components.tab2_forecast import (
    row1_dataset,
    row2_prediksi_vs_aktual,
    row3_metric_card,
)
from utils.data_loader import validate_cv_df

st.title(":material/bar_chart: Forecast", help="Atur pilihan dataset dan Unique ID melalui kontrol di sidebar")
st.write("Halaman ini menyajikan evaluasi hasil peramalan (*forecasting*) berdasarkan performa model pada data uji (*test set*)")

cv_df = None

# --- Sidebar: semua kontrol di sini ---
with st.sidebar:
    st.markdown("### :material/folder_open: Dataset", help="Dataset hasil cross validation harus memiliki kolom `unique_id`, `ds`, `cutoff`, `y`, dan minimal satu kolom tambahan sebagai hasil prediksi.",)

    # Sumber data
    data_source = st.radio(
        "Pilih sumber dataset cross validation", 
        ["Upload CSV", "Gunakan contoh dataset"], 
        index=1
    )
    if data_source == "Upload CSV":
        uploaded_file = st.file_uploader("Upload file CSV", type=["csv"])
        if uploaded_file:
            cv_df = pd.read_csv(uploaded_file)
            is_valid, message = validate_cv_df(cv_df)
            if not is_valid:
                st.error(message)
                st.stop()
            else:
                st.success(message)
                st.session_state['cv_df'] = cv_df
                st.session_state['cv_loaded'] = True
    else:
        try:
            cv_df = pd.read_csv("data/cv_df_nhits.csv")
            st.info("Menggunakan hasil cross validation contoh bawaan.")
            st.session_state['cv_df'] = cv_df
            st.session_state['cv_loaded'] = True
        except FileNotFoundError:
            st.error("File contoh dataset tidak ditemukan di folder data/")
    
    st.divider()

    st.markdown("#### :material/settings: Others")
    if cv_df is not None:
        # Pilih unique_id
        unique_ids = cv_df['unique_id'].unique()
        st.selectbox(
            "Pilih Unique ID",
            options=unique_ids,
            key="selected_unique_id",
        )


if cv_df is not None:
    row1_dataset.render(cv_df)
    row2_prediksi_vs_aktual.render(cv_df)
    row3_metric_card.render(cv_df)
    