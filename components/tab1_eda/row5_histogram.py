import streamlit as st
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import gaussian_kde, skew
from scipy.signal import find_peaks

def render(df):
    st.subheader(":material/candlestick_chart: Distribusi Histogram", help="Distribusi histogram digunakan untuk menganalisis distribusi frekuensi dan pola penyebaran data berdasarkan interval nilai tertentu")
    
    target_column = st.session_state.get("target_column", None)
    col1, col2 = st.columns(2)
    
    with col1:
        with st.container(border=True, height=450):
            fig_hist = px.histogram(
                df,
                x=target_column,
                color="unique_id",
                color_discrete_sequence=px.colors.qualitative.Set2,
                barmode="overlay",
            )

            unique_ids = df["unique_id"].unique()
            colors = px.colors.qualitative.Set2

            for i, uid in enumerate(unique_ids):
                group_data = df[df["unique_id"] == uid][target_column].values

                if len(group_data) > 1 and len(np.unique(group_data)) > 1:
                    kde = gaussian_kde(group_data)
                    x_range = np.linspace(group_data.min(), group_data.max(), 200)
                    
                    bin_width = (group_data.max() - group_data.min()) / 30
                    scale_factor = len(group_data) * bin_width
                    kde_values = kde(x_range) * scale_factor

                    # Garis KDE
                    fig_hist.add_trace(
                        go.Scatter(
                            x=x_range,
                            y=kde_values,
                            mode="lines",
                            name=str(uid),
                            legendgroup=str(uid),  
                            showlegend=False,  
                            line=dict(color=colors[i % len(colors)], width=2.5),
                        )
                    )

            fig_hist.update_layout(
                height=400,
                xaxis_title=target_column,
                yaxis_title="Frekuensi",
                showlegend=True,
                margin=dict(l=10, r=10, t=40, b=10),
            )

            st.plotly_chart(fig_hist, use_container_width=True)

    with col2:
        with st.container(border=True, height=450):
            max_val = df[target_column].max()
            fixed_bins = np.arange(-10, max_val + 30, 20)

            st.markdown("**:material/lightbulb: Detail per Group:**")

            # 1. Batas bin secara GLOBAL (sama persis dengan grafik)
            max_val = df[target_column].max()
            fixed_bins = np.arange(-10, max_val + 30, 20)

            for uid, subset in df.groupby("unique_id"):
                group_vals = subset[target_column].dropna().values
                total_bulan = len(group_vals)
                
                if total_bulan > 1:
                    counts_g, bin_edges_g = np.histogram(group_vals, bins=fixed_bins)

                    # ========================================================
                    # DETEKSI PUNCAK DENGAN SCIPY (JAUH LEBIH AKURAT)
                    # ========================================================
                    # prominence=5: Puncak harus menonjol minimal 5 unit dari lembah terdekat
                    # distance=3: Jarak minimal antar puncak adalah 3 bin (misal 60 mm)
                    peaks_idx, properties = find_peaks(counts_g, prominence=5, distance=8)

                    peaks = []
                    # Threshold minimal 5% dari total data agar tidak mendeteksi noise
                    threshold = max(5, total_bulan * 0.05) 

                    for idx in peaks_idx:
                        if counts_g[idx] >= threshold:
                            peaks.append({
                                'start': bin_edges_g[idx],
                                'end': bin_edges_g[idx+1],
                                'freq': counts_g[idx]
                            })

                    # Fallback jika tidak ada puncak yang lolos threshold
                    if not peaks:
                        max_idx_g = np.argmax(counts_g)
                        peaks.append({
                            'start': bin_edges_g[max_idx_g],
                            'end': bin_edges_g[max_idx_g + 1],
                            'freq': counts_g[max_idx_g]
                        })

                    # Klasifikasi Bentuk
                    num_peaks = len(peaks)
                    if num_peaks == 1:
                        bentuk = "Unimodal (1 puncak)"
                    elif num_peaks == 2:
                        bentuk = "Bimodal (2 puncak)"
                    else:
                        bentuk = f"Multimodal ({num_peaks} puncak)"

                    # Kemiringan
                    g_skew = skew(group_vals)
                    if abs(g_skew) < 0.5:
                        skew_label = "cukup merata"
                    elif g_skew >= 0.5:
                        skew_label = "miring ke kanan (ekor di kanan)"
                    else:
                        skew_label = "miring ke kiri (ekor di kiri)"

                    # Susun Teks
                    teks_puncak = ""
                    for p in peaks:
                        teks_puncak += f"**{int(p['start'])}–{int(p['end'])} mm** ({p['freq']} bulan), "
                    teks_puncak = teks_puncak.rstrip(", ")

                    st.info(
                        f"- **{uid}:** memiliki pola **{bentuk}** pada rentang {teks_puncak}, serta sebaran data yang {skew_label}"
                    )
    st.divider()