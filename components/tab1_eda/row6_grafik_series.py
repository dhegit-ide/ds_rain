import streamlit as st
import numpy as np
from scipy.stats import linregress
from utilsforecast.plotting import plot_series

def render(df):
    st.subheader(f":material/show_chart: Grafik Tren Umum Variabel Utama", help="Grafik tren umum digunakan untuk menganalisis pola perubahan nilai variabel dari waktu ke waktu berdasarkan interval waktu tertentu")
    
    target_column = st.session_state.get('target_column', None)
    selected_unique_id = st.session_state['selected_unique_id']

    with st.container(border=True):
        st.caption(f":green-badge[Unique ID: {selected_unique_id}] :green-badge[Target kolom: {target_column}]")
        st.caption(":material/info: Gunakan kontrol di sidebar untuk memilih Unique ID & Target Kolom")
        try:
            fig = plot_series(df, target_col=target_column, ids=[selected_unique_id], engine='plotly')
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig)
        except Exception as e:
            st.warning(f"⚠️ Error Grafik Tren Umum Variabel Utama: {e}")
            
    st.markdown("**:material/lightbulb: Ringkasan Analisis Tren:**")
    try:
        # Filter data berdasarkan unique_id dan buang nilai kosong
        filtered_df = df[ (df["unique_id"] == selected_unique_id) & (df[target_column].notna()) ].copy()

        if len(filtered_df) > 1:
            series = filtered_df[target_column]

            x = np.arange(len(series))
            slope, intercept, r_val, p_val, std_err = linregress(x, series.values)

            # Klasifikasi Arah Tren berdasarkan nilai Slope
            if slope > 0.5:
                trend_text = "menunjukkan **tren meningkat**"
            elif slope < -0.5:
                trend_text = "menunjukkan **tren menurun**"
            else:
                trend_text = "cenderung **stabil / mendatar**"

            # Nilai Statistik Utama
            avg_val = series.mean()
            min_idx = series.idxmin()
            max_idx = series.idxmax()

            min_val = series.loc[min_idx]
            max_val = series.loc[max_idx]

            # Format tanggal agar tampilan lebih rapi (misal: 'YYYY-MM' atau 'YYYY-MM-DD')
            time_col = "ds" if "ds" in filtered_df.columns else "date"
            min_date = str(filtered_df.loc[min_idx, time_col])[:7]
            max_date = str(filtered_df.loc[max_idx, time_col])[:7]

            # Tampilkan Narasi Analisis
            st.info(
                f"- Pergerakan nilai `{target_column}` untuk **{selected_unique_id}** secara keseluruhan {trend_text} "
                f"dengan nilai rata-rata sebesar **{avg_val:.1f}**."
            )
            st.info(
                f"- Data bergerak fluktuatif dengan pola musiman di rentang nilai terendah **{min_val:.1f}** "
                f"(terjadi pada **{min_date}**) hingga puncak maksimum sebesar **{max_val:.1f}** "
                f"(terjadi pada **{max_date}**)."
            )
        else:
            st.info(
                "Data tidak cukup untuk melakukan analisis tren."
            )
    except Exception as desc_err:
        st.warning(f"Gagal memuat deskripsi tren: {desc_err}")

    st.divider()