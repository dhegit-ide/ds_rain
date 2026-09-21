import streamlit as st
import pandas as pd

def render(cv_df):
    st.divider()
    with st.expander(":material/table_view: Lihat Sampel Data Peramalan", expanded=True):
        st.dataframe(cv_df, use_container_width=True)
        
        # Pastikan kolom 'ds' berformat datetime
        if not pd.api.types.is_datetime64_any_dtype(cv_df['ds']):
            cv_df['ds'] = pd.to_datetime(cv_df['ds'], errors='coerce')
        
        # 1. Rentang Tanggal
        min_date = cv_df['ds'].min()
        max_date = cv_df['ds'].max()
        
        # 2. Deteksi Frekuensi Data & Pemetaan Unit Durasi
        freq_inferred = pd.infer_freq(cv_df['ds'].sort_values().drop_duplicates())
        
        freq_info = {
            'ME': ('Monthly', 'Bulan'),
            'M': ('Monthly', 'Bulan'),
            'MS': ('Monthly', 'Bulan'),
            'D': ('Daily', 'Hari'),
            'B': ('Business Daily', 'Hari Kerja'),
            'W': ('Weekly', 'Minggu'),
            'QE': ('Quarterly', 'Triwulan'),
            'QS': ('Quarterly', 'Triwulan'),
            'YE': ('Yearly', 'Tahun'),
            'YS': ('Yearly', 'Tahun')
        }
        
        freq_label, unit_suffix = freq_info.get(
            freq_inferred, 
            (freq_inferred if freq_inferred else "Custom", "Periode")
        )

        # 3. Hitung Total Durasi Sesuai Frekuensi
        if unit_suffix == 'Bulan':
            total_duration = (max_date.year - min_date.year) * 12 + (max_date.month - min_date.month) + 1
        elif unit_suffix in ['Hari', 'Hari Kerja']:
            total_duration = (max_date - min_date).days + 1
        elif unit_suffix == 'Minggu':
            total_duration = int((max_date - min_date).days / 7) + 1
        elif unit_suffix == 'Tahun':
            total_duration = max_date.year - min_date.year + 1
        else:
            total_duration = cv_df['ds'].nunique()

        # 4. Hitung Forecast Horizon & Total Skenario Model
        # Horizon = Jumlah tanggal peramalan unik per cutoff/unique_id
        if 'cutoff' in cv_df.columns:
            first_cutoff = cv_df['cutoff'].iloc[0]
            horizon = cv_df[cv_df['cutoff'] == first_cutoff]['ds'].nunique()
        else:
            horizon = cv_df['ds'].nunique()

        # Total Model = Jumlah kolom selain metadata bawaan
        base_cols = {'unique_id', 'ds', 'cutoff', 'y'}
        model_cols = [col for col in cv_df.columns if col not in base_cols]
        total_models = len(model_cols)

        st.divider()
        
        # Tampilan 5 Kolom Sejajar
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.caption(":material/calendar_month: **Periode Waktu**")
            st.write(f":blue-badge[{min_date.strftime('%d %b %Y')} - {max_date.strftime('%d %b %Y')}]")
            
        with col2:
            st.caption(":material/timer: **Frekuensi Data**")
            st.write(f":blue-badge[{freq_label}]")

        with col3:
            st.caption(":material/hourglass_empty: **Durasi Data**")
            st.write(f":blue-badge[{total_duration} {unit_suffix}]")

        with col4:
            st.caption(":material/trending_up: **Horizon**")
            st.write(f":blue-badge[{horizon} {unit_suffix}]")

        with col5:
            st.caption(":material/schema: **Skenario Model**")
            st.write(f":blue-badge[{total_models} Model]")

    st.divider()