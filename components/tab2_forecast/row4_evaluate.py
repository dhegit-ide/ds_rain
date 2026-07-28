import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from utilsforecast.losses import mae, rmse, mse, smape
from utilsforecast.evaluation import evaluate
from utils.data_loader import r2


def render(cv_df):
    st.subheader(":material/leaderboard: Evaluasi Metrik")
    st.markdown("##### **Dataset Evaluasi**")
    metrics_df = evaluate(
        cv_df.drop(columns='cutoff'), 
        metrics=[mae,rmse,mse,smape,r2]
    )
    st.dataframe(metrics_df.round(3))

    selected_pred = st.session_state['selected_pred']
    selected_unique_id = st.session_state['selected_unique_id']

    st.markdown(f"##### **Prediksi `{selected_pred}` Global**")
    st.caption(f":material/info: Performa rata-rata Prediksi `{selected_pred}` di semua Unique ID. Gunakan kontrol di sidebar untuk memilih Prediksi")

    # mengambil nilai tiap kolom prediksi (global)
    global_df = metrics_df[[ "metric", selected_pred ]]
    mae_val   = global_df.loc[global_df['metric'] == 'mae', selected_pred].mean()
    rmse_val  = global_df.loc[global_df['metric'] == 'rmse', selected_pred].mean()
    mse_val   = global_df.loc[global_df['metric'] == 'mse', selected_pred].mean()
    smape_val = global_df.loc[global_df['metric'] == 'smape', selected_pred].mean()
    r2_val    = global_df.loc[global_df['metric'] == 'r2', selected_pred].mean()

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("MAE (Global)", f"{mae_val:.3f}", border=True)
    col2.metric("RMSE (Global)", f"{rmse_val:.3f}", border=True)
    col3.metric("MSE (Global)", f"{mse_val:.3f}", border=True)
    col4.metric("SMAPE (Global)", f"{smape_val*100:.2f}%", border=True)  # persen
    col5.metric("R² (Global)", f"{r2_val:.3f}", border=True)


    st.markdown(f"##### **Prediksi `{selected_pred}` Unique ID `{selected_unique_id}`**")
    st.caption(":material/info: Performa prediksi berdasarkan Unique ID terpilih. Gunakan kontrol di sidebar untuk memilih Prediksi & Unique ID")

    # filter sesuai unique_id
    df_sel = metrics_df[metrics_df['unique_id'] == selected_unique_id]
    mae_val   = df_sel.loc[df_sel['metric'] == 'mae', selected_pred].values[0]
    rmse_val  = df_sel.loc[df_sel['metric'] == 'rmse', selected_pred].values[0]
    mse_val   = df_sel.loc[df_sel['metric'] == 'mse', selected_pred].values[0]
    smape_val = df_sel.loc[df_sel['metric'] == 'smape', selected_pred].values[0]
    r2_val    = df_sel.loc[df_sel['metric'] == 'r2', selected_pred].values[0]

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("MAE", f"{mae_val:.3f}", border=True)
    col2.metric("RMSE", f"{rmse_val:.3f}", border=True)
    col3.metric("MSE", f"{mse_val:.3f}", border=True)
    col4.metric("SMAPE", f"{smape_val*100:.2f}%", border=True)
    col5.metric("R²", f"{r2_val:.3f}", border=True)

    
    st.markdown(f"##### **Metrik {selected_unique_id}**")
    st.caption(":material/info: Gunakan kontrol di sidebar untuk memilih Unique ID")

    pred_cols = [c for c in cv_df.columns if c not in ['unique_id','ds','cutoff','y']]
    metrics = metrics_df['metric'].unique().tolist()

    df_sel = metrics_df[metrics_df['unique_id'] == selected_unique_id]

    # pivot: index = model (pred_cols), columns = metric
    eval_table = df_sel.set_index('metric')[pred_cols].T
    eval_table.index.name = "Kolom Prediksi"

    # ubah nama kolom biar lebih rapi
    eval_table = eval_table.rename(columns={
        'mae': 'MAE',
        'mse': 'MSE',
        'rmse': 'RMSE',
        'smape': 'sMAPE',
        'r2': 'R²'
    })
    st.dataframe(eval_table.round(3))

    with st.expander(f":material/description: Ringkasan Evaluasi Metrik **{selected_unique_id}**"):
        desc_lines = []
        best_counts = {}

        for metric in eval_table.columns:
            if metric in ["MAE","MSE","RMSE","sMAPE"]:
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
