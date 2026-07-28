import streamlit as st
import pandas as pd
from components.tab2_forecast import (
    row1_card_cv,
    row2_preview_cv,
    row3_describe_cv,
    row4_evaluate
)
from utils.data_loader import validate_cv_df

st.title(":material/bar_chart: Forecasting")
st.info("Gunakan kontrol di sidebar untuk memilih dataset dan pengaturan.")

cv_df = None

# --- Sidebar: semua kontrol di sini ---
with st.sidebar:
    st.markdown("### :material/tune: Settings")

    # Sumber data
    data_source = st.radio("Pilih sumber dataset cross validation", ["Upload CSV", "Gunakan contoh dataset"])
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
            cv_df = pd.read_csv("data/cv_df.csv")
            st.info("Menggunakan hasil cross validation contoh bawaan.")
            st.session_state['cv_df'] = cv_df
            st.session_state['cv_loaded'] = True
        except FileNotFoundError:
            st.error("File contoh dataset tidak ditemukan di folder data/")

    if cv_df is not None:
        # Pilih unique_id
        unique_ids = cv_df['unique_id'].unique()
        st.selectbox(
            "Pilih Unique ID",
            options=unique_ids,
            key="selected_unique_id",
        )

        # Pilih prediksi
        pred_cols = [c for c in cv_df.columns if c not in ['unique_id','ds','cutoff','y']]
        st.selectbox(
            "Pilih Prediksi",
            options=pred_cols,
            key="selected_pred",
        )


if cv_df is not None:
    row1_card_cv.render(cv_df)
    row2_preview_cv.render(cv_df)
    row3_describe_cv.render(cv_df)
    row4_evaluate.render(cv_df)

    