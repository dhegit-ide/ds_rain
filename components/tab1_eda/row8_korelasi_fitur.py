import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.feature_selection import mutual_info_regression
import numpy as np

import numpy as np

CORR_THRESHOLDS = [
    (0.8, "sangat kuat"),
    (0.6, "kuat"),
    (0.4, "sedang"),
    (0.2, "lemah"),
    (0.0, "sangat lemah"),
]
MULTIKOLINIER_THRESHOLD = 0.8   # |r| di atas ini dianggap redundan
WEAK_FEATURE_THRESHOLD = 0.1    # |r| di bawah ini dianggap lemah


def _label_strength(value):
    """Beri label kekuatan berdasarkan nilai absolut korelasi."""
    abs_v = abs(value)
    for threshold, label in CORR_THRESHOLDS:
        if abs_v >= threshold:
            return label
    return "sangat lemah"


def _build_corr_insights(scores_filtered, corr_method, target_column):
    """2 poin insight: (1) fitur positif & negatif terkuat, (2) fitur positif & negatif terlemah."""
    
    # Mutual Information tidak punya arah (+/-), jadi skip
    if corr_method == "Mutual Information":
        top = scores_filtered.iloc[0]
        return [(
            "markdown",
            f"- Fitur **{scores_filtered.index[0]}** "
            f"memiliki skor tertinggi (**MI = {top:.3f}**) terhadap `{target_column}`."
        )]
    
    # --- Pisahkan fitur positif dan negatif ---
    pos_features = scores_filtered[scores_filtered > 0].sort_values(ascending=False)
    neg_features = scores_filtered[scores_filtered < 0].sort_values(ascending=True)
    
    insights = []
    
    # --- Poin 1: Positif TERKUAT & Negatif TERKUAT ---
    if len(pos_features) > 0 and len(neg_features) > 0:
        pos_strong = pos_features.index[0]
        pos_strong_val = pos_features.iloc[0]
        neg_strong = neg_features.index[0]           # ascending → paling negatif
        neg_strong_val = neg_features.iloc[0]
        
        insights.append((
            "markdown",
            f"- Fitur `{pos_strong}` memiliki hubungan "
            f"positif {_label_strength(pos_strong_val)} (r = {pos_strong_val:.3f}), "
            f"sedangkan fitur `{neg_strong}` memiliki hubungan "
            f"negatif {_label_strength(neg_strong_val)} (r = {neg_strong_val:.3f}) "
            f"terhadap `{target_column}`."
        ))
    
    # --- Poin 2: Positif TERLEMAH & Negatif TERLEMAH ---
    if len(pos_features) > 0 and len(neg_features) > 0:
        pos_weak = pos_features.index[-1]            # descending → paling kecil positif
        pos_weak_val = pos_features.iloc[-1]
        neg_weak = neg_features.index[-1]            # ascending → paling dekat 0 (negatif lemah)
        neg_weak_val = neg_features.iloc[-1]
        
        insights.append((
            "markdown",
            f"- Fitur `{pos_weak}` memiliki hubungan "
            f"positif-{_label_strength(pos_weak_val)} (r = {pos_weak_val:.3f}), "
            f"sedangkan fitur `{neg_weak}` memiliki hubungan "
            f"negatif {_label_strength(neg_weak_val)} (r = {neg_weak_val:.3f}) "
            f"terhadap `{target_column}`."
        ))
    
    # --- Fallback: kalau semua fitur hanya positif atau hanya negatif ---
    if not insights:
        strongest = scores_filtered.iloc[0]
        weakest = scores_filtered.iloc[-1]
        arah = "positif" if strongest > 0 else "negatif"
        insights.append((
            "markdown",
            f"- Semua fitur memiliki hubungan **{arah}** "
            f"terhadap `{target_column}`. Yang terkuat adalah **{scores_filtered.index[0]}** "
            f"(r = {strongest:.3f}, {_label_strength(strongest)}), "
            f"sedangkan yang terlemah adalah **{scores_filtered.index[-1]}** "
            f"(r = {weakest:.3f}, {_label_strength(weakest)})."
        ))
    
    return insights


def render(df):
    target_column = st.session_state.get('target_column', None)
    corr_method = st.session_state.get('corr_method', 'Spearman')
    if df is not None and target_column:
         # hitung skor sesuai metode
        if corr_method in ["Pearson", "Spearman", "Kendall"]:
            scores = df.corr(method=corr_method.lower(), numeric_only=True)[target_column].drop(target_column)
            scores_filtered = scores.sort_values(ascending=False)
        else:  # Mutual Information
            X = df.drop(columns=[target_column, "ds", "unique_id"], errors="ignore")
            y = df[target_column]
            mi_scores = mutual_info_regression(X, y, random_state=17)
            scores_filtered = pd.Series(mi_scores, index=X.columns).sort_values(ascending=False)

        # tampilkan tabel & heatmap
        col1, col2 = st.columns(2)
        with col1:
            with st.container(border=True, height=450):
                st.subheader(f":material/table: Tabel Korelasi {corr_method}")
                st.caption(":material/info: Gunakan kontrol di sidebar untuk memilih Metode Korelasi")
                score_df = pd.DataFrame({
                    "Fitur": scores_filtered.index,
                    "Skor": scores_filtered.values
                })
                st.dataframe(score_df, use_container_width=True)
                selected_features = score_df["Fitur"].tolist() + [target_column]
                st.caption(f"Rentang skor {corr_method}: [{scores_filtered.min():.3f}, {scores_filtered.max():.3f}]")

        with col2:
            with st.container(border=True, height=450):
                st.subheader(f":material/linked_services: Heatmap Korelasi {corr_method}")
                corr_matrix = df[selected_features].corr(numeric_only=True)
                fig = px.imshow(
                    corr_matrix,
                    text_auto=True,
                    aspect="equal",
                    color_continuous_scale="RdBu",
                    origin="lower"
                )
                fig.update_xaxes(showticklabels=False)
                fig.update_yaxes(showticklabels=False)
                st.plotly_chart(fig, use_container_width=True)

        # --- Setelah blok col1, col2 (visualisasi) selesai ---
        st.markdown(f"**:material/lightbulb: Ringkasan Analisis Korelasi {corr_method}:**")
        
        if not scores_filtered.empty:
            insights = _build_corr_insights(scores_filtered, corr_method, target_column)
        for tipe, teks in insights:
            if tipe == "markdown":
                st.info(teks)
            else:
                st.info(teks)
    else:
        st.warning(":material/warning: Target kolom belum dipilih atau data belum tersedia.")
           