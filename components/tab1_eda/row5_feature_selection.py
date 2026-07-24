import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.feature_selection import mutual_info_regression

def render(df):    
    target_column = st.session_state.get('target_column', None)
    corr_method = st.session_state.get('corr_method', 'pearson')
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
        col1, col2 = st.columns([1,1])
        with col1:
            with st.container(border=True, height=450):
                st.subheader(f":material/table: Tabel Korelasi {corr_method}")
                score_df = pd.DataFrame({
                    "Fitur": scores_filtered.index,
                    "Skor": scores_filtered.values
                })
                st.dataframe(score_df, use_container_width=True, height=320)
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
    else:
        st.warning(":material/warning: Target kolom belum dipilih atau data belum tersedia.")

    st.divider()
           