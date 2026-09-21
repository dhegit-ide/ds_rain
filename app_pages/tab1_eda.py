import streamlit as st
import pandas as pd
from components.tab1_eda import (
    row1_dataset,
    row2_card_info,
    row3_statistik,
    row4_boxplot,
    row5_histogram,
    row6_grafik_series,
    row7_grafik_pola_musiman,
    row8_korelasi_fitur,
)
from utils.data_loader import validate_csv, get_numeric_columns
from utils.sliding_window import init_sliding_window_state, on_window_change, sync_date_widgets, on_start_date_change, on_end_date_change

st.title(":material/tile_small: Overview Dataset")
st.info("Gunakan kontrol di sidebar untuk memilih dataset dan pengaturan.")

df = None

# --- Sidebar: semua kontrol di sini ---
with st.sidebar:
    st.markdown("### :material/folder_open: Dataset")

    # Sumber data
    data_source = st.radio(
        "Pilih sumber dataset", 
        ["Upload CSV", "Gunakan contoh dataset"],
        index=1
    )
    if data_source == "Upload CSV":
        uploaded_file = st.file_uploader("Upload file CSV", type=["csv"])
        if uploaded_file:
            
            file_key = uploaded_file.name
            if st.session_state.get('current_uploaded_file') != file_key:
                st.session_state['current_uploaded_file'] = file_key
                keys_to_clear = [
                    'selected_start_date', 'selected_end_date', 
                    'window_size_input', 'window_size', 
                    'min_idx', 'max_idx'
                ]
                for key in keys_to_clear:
                    st.session_state.pop(key, None)

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
        if st.session_state.get('current_uploaded_file') is not None:
            st.session_state.pop('current_uploaded_file', None)
            for key in ['selected_start_date', 'selected_end_date', 'window_size_input', 'window_size']:
                st.session_state.pop(key, None)

        try:
            df = pd.read_csv("data/df_30_tahun.csv")
            st.info("Menggunakan dataset contoh bawaan.")
            st.session_state['df_raw'] = df
            st.session_state['data_loaded'] = True
        except FileNotFoundError:
            st.error("File contoh dataset tidak ditemukan di folder data/")

    if df is not None:
        st.divider()
        
        # Konversi ke datetime
        if not pd.api.types.is_datetime64_any_dtype(df["ds"]):
            df["ds"] = pd.to_datetime(df["ds"], errors="coerce")

        # Hapus timezone jika ada (misal UTC) agar bisa dibandingkan dengan Timestamp biasa
        if hasattr(df["ds"].dt, "tz") and df["ds"].dt.tz is not None:
            df["ds"] = df["ds"].dt.tz_localize(None)

        raw_dates = sorted(df['ds'].dropna().unique())
        unique_dates_str = [pd.to_datetime(d).strftime("%Y-%m-%d") for d in raw_dates]

        init_sliding_window_state(unique_dates_str)
        
        if "selected_start_date" not in st.session_state or "selected_end_date" not in st.session_state:
            sync_date_widgets(unique_dates_str)
        
        # --- Widget Input Rentang Waktu ---
        st.markdown("#### :material/date_range: Filter Rentang Waktu")
        st.text_input(
            "Panjang Window (misal: 120 atau 20%):",
            key="window_size_input",
            on_change=lambda: on_window_change(unique_dates_str)
        )

        col_min, col_max = st.columns(2)
        with col_min:
            st.selectbox(
                "Tanggal Mulai",
                options=unique_dates_str,
                key="selected_start_date",
                on_change=lambda: on_start_date_change(unique_dates_str)
            )
        with col_max:
            st.selectbox(
                "Tanggal Akhir",
                options=unique_dates_str,
                key="selected_end_date",
                on_change=lambda: on_end_date_change(unique_dates_str)
            )

        st.info(
            f"Rentang terpilih sebanyak **{st.session_state.window_size}** titik data"
        )

        st.divider()
        
        # Target kolom
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
        
        # Pilih unique_id
        unique_ids = df['unique_id'].unique()
        st.selectbox(
            "Pilih Unique ID",
            options=unique_ids,
            key="selected_unique_id",
        )

        # Seleksi fitur
        st.selectbox(
            "Pilih Metode Korelasi",
            options=["Spearman", "Kendall", "Pearson", "Mutual Information"],
            key="corr_method",
        )

if df is not None:
    start_dt = pd.to_datetime(st.session_state.get('selected_start_date'))
    end_dt = pd.to_datetime(st.session_state.get('selected_end_date'))

    if pd.notnull(start_dt) and pd.notnull(end_dt):
        df = df[(df['ds'] >= start_dt) & (df['ds'] <= end_dt)].copy()
    else:
        df = df.copy()

    st.session_state['df'] = df

    row1_dataset.render(df)
    row2_card_info.render(df)
    row3_statistik.render(df)
    row4_boxplot.render(df)
    row5_histogram.render(df)
    row6_grafik_series.render(df)
    row7_grafik_pola_musiman.render(df)
    row8_korelasi_fitur.render(df)
