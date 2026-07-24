import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from utilsforecast.losses import mae, rmse, mse, mape
from utilsforecast.evaluation import evaluate
from utils.data_loader import r2


def render(cv_df):
    st.subheader(":material/leaderboard: Evaluasi Metrik")
    st.markdown("##### **Dataset Evaluasi**")
    metrics_df = evaluate(
        cv_df.drop(columns='cutoff'), 
        metrics=[mae,rmse,mse,mape,r2]
    )
    st.dataframe(metrics_df.round(3))

    selected_unique_id = st.session_state['selected_unique_id']
    st.markdown(f"##### **Metrik {selected_unique_id}**")

    pred_cols = [c for c in cv_df.columns if c not in ['unique_id','ds','cutoff','y']]
    metrics = metrics_df['metric'].unique().tolist()

    df_sel = metrics_df[metrics_df['unique_id'] == selected_unique_id]

    # pivot: index = model (pred_cols), columns = metric
    eval_table = df_sel.set_index('metric')[pred_cols].T
    eval_table.index.name = "Kolom Prediksi"

    # ubah nama kolom biar lebih rapi
    eval_table = eval_table.rename(columns={
        'mae': 'MAE',
        'mape': 'MAPE (%)',
        'mse': 'MSE',
        'rmse': 'RMSE',
        'r2': 'R²'
    })
    st.dataframe(eval_table.round(3))

    with st.expander(f":material/description: Ringkasan Evaluasi Metrik **{selected_unique_id}**"):
        desc_lines = []
        best_counts = {}

        for metric in eval_table.columns:
            if metric in ["MAE","MAPE (%)","MSE","RMSE"]:
                best_model = eval_table[metric].idxmin()
                best_score = eval_table[metric].min()
                worst_model = eval_table[metric].idxmax()
                worst_score = eval_table[metric].max()
                desc_lines.append(
                    f"- **{metric}** → terbaik **{best_model}** ({best_score:.3f}), "
                    f"terburuk **{worst_model}** ({worst_score:.3f})"
                )
            elif metric == "R²":
                best_model = eval_table[metric].idxmax()
                best_score = eval_table[metric].max()
                worst_model = eval_table[metric].idxmin()
                worst_score = eval_table[metric].min()
                desc_lines.append(
                    f"- **{metric}** → tertinggi **{best_model}** ({best_score:.3f}), "
                    f"terendah **{worst_model}** ({worst_score:.3f})"
                )

            # hitung hanya best model
            best_counts[best_model] = best_counts.get(best_model, 0) + 1

        # tentukan model dominan
        dominant_model = max(best_counts, key=best_counts.get)
        dominant_count = best_counts[dominant_model]

        desc_lines.append(f"\nSecara keseluruhan, model **{dominant_model}** paling konsisten unggul ({dominant_count} metrik).")

        # tampilkan sebagai bullet list
        st.markdown("\n" + "\n".join(desc_lines))
