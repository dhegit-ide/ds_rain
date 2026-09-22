import streamlit as st
import pandas as pd
import numpy as np
from utilsforecast.losses import mae, rmse, mse, smape
from utilsforecast.evaluation import evaluate
from utils.data_loader import r2

def render(cv_df):
    selected_unique_id = st.session_state.get('selected_unique_id', cv_df['unique_id'].iloc[0])

    metrics_df = evaluate(
        cv_df.drop(columns='cutoff'), 
        metrics=[mae, rmse, mse, smape, r2]
    )

    pred_cols = [c for c in cv_df.columns if c not in ['unique_id', 'ds', 'cutoff', 'y']]
    df_sel = metrics_df[metrics_df['unique_id'] == selected_unique_id]
    eval_table = df_sel.set_index('metric')[pred_cols].T

    # 2. Cari Model Terbaik & Nilainya
    # Error metrics (MAE, RMSE, MSE, sMAPE) -> Nilai terendah (idxmin)
    # Accuracy metric (R2) -> Nilai tertinggi (idxmax)
    best_mae_model = eval_table['mae'].idxmin()
    best_mae_val = eval_table.loc[best_mae_model, 'mae']

    best_rmse_model = eval_table['rmse'].idxmin()
    best_rmse_val = eval_table.loc[best_rmse_model, 'rmse']

    best_mse_model = eval_table['mse'].idxmin()
    best_mse_val = eval_table.loc[best_mse_model, 'mse']

    best_smape_model = eval_table['smape'].idxmin()
    best_smape_val = eval_table.loc[best_smape_model, 'smape']

    best_r2_model = eval_table['r2'].idxmax()
    best_r2_val = eval_table.loc[best_r2_model, 'r2']


    with st.container(border=True):
        st.markdown(":material/table: **Hasil Evaluasi Model**")
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            with st.container(border=True, gap="xxsmall"):
                st.metric(label=r"$MAE$ (_lowest_)", value=f"{best_mae_val:.2f}", help=r"**Mean Absolute Error ($MAE$)** merupakan rata-rata selisih absolut antara nilai aktual dan prediksi. Metrik ini tidak rentan terhadap nilai ekstrem (outlier)")
                st.write(f":blue-badge[{best_mae_model}]")
        with col2:
            with st.container(border=True, gap="xxsmall"):
                st.metric(label=r"$RMSE$ (_lowest_)", value=f"{best_rmse_val:.2f}", help=r"**Root Mean Squared Error ($RMSE$)** merupakan akar dari rata-rata kuadrat selisih antara nilai aktual dan prediksi. Metrik ini menggunakan skala asli data meskipun tetap memberikan bobot lebih besar pada kesalahan yang lebih besar (outlier)")
                st.write(f":blue-badge[{best_rmse_model}]")
        with col3:
            with st.container(border=True, gap="xxsmall"):
                st.metric(label=r"$MSE$ (_lowest_)", value=f"{best_mse_val:.2f}", help=r"**Mean Squared Error ($MSE$)** merupakan rata-rata dari kuadrat selisih antara nilai aktual dan prediksi. Metrik ini memberikan bobot lebih besar pada kesalahan yang lebih besar (outlier)")
                st.write(f":blue-badge[{best_mse_model}]")
        with col4:
            with st.container(border=True, gap="xxsmall"):
                st.metric(label=r"$sMAPE$ (_lowest_)", value=f"{best_smape_val * 100:.1f}%" if best_smape_val <= 1 else f"{best_smape_val:.2f}%", help=r"**Symmetric Mean Absolute Percentage Error ($sMAPE$)** merupakan versi simetris dari MAPE. Metrik ini mengukur persentase kesalahan relatif yang dinormalisasi oleh rata-rata nilai aktual dan prediksi, sehingga lebih stabil saat nilai aktual mendekati nol")
                st.write(f":blue-badge[{best_smape_model}]")
        with col5:
            with st.container(border=True, gap="xxsmall"):
                st.metric(label=r"$R^2$ (_highest_)", value=f"{best_r2_val:.2f}", help=r"**Coefficient of Determination ($R^2$)** mengukur proporsi varians dalam variabel dependen yang dapat diprediksi dari variabel independen. Nilai $R^2$ berkisar antara 0 hingga 1, di mana nilai yang lebih tinggi menunjukkan kecocokan model yang lebih baik dengan data")
                st.write(f":blue-badge[{best_r2_model}]")

        st.divider()
        def highlight_best(data):
            # Buat DataFrame gaya kosong
            style_df = pd.DataFrame('', index=data.index, columns=data.columns)
            
            # Untuk MAE, RMSE, MSE, sMAPE -> nilai terkecil yang terbaik
            for col in ['mae', 'rmse', 'mse', 'smape']:
                if col in data.columns:
                    min_val = data[col].min()
                    style_df[col] = np.where(data[col] == min_val, 'background-color: #e8f2ff; color:#0b65ae', '')
            
            # Untuk R2 -> nilai terbesar yang terbaik
            if 'r2' in data.columns:
                max_val = data['r2'].max()
                style_df['r2'] = np.where(data['r2'] == max_val, 'background-color: #e8f2ff; color:#0b65ae', '')
                
            return style_df

        # Pengaturan Format Kolom (sMAPE diubah ke format persentase)
        styled_eval_table = eval_table.style.apply(highlight_best, axis=None).format({
            'mae': '{:.2f}',
            'rmse': '{:.2f}',
            'mse': '{:.2f}',
            'smape': '{:.1%}' if eval_table['smape'].max() <= 1 else '{:.2f}%',
            'r2': '{:.2f}'
        })

        st.dataframe(styled_eval_table, use_container_width=True)

    # -------------------------------------------------------------
    # Insight Text
    # -------------------------------------------------------------
    best_models = [best_mae_model, best_rmse_model, best_mse_model, best_smape_model, best_r2_model]

    best_counts = pd.Series(best_models).value_counts()
    overall_best_model = best_counts.idxmax()
    overall_best_count = best_counts.max()

    if best_r2_val >= 0.75:
        r2_summary = f"sebesar **{best_r2_val:.2f}** menunjukkan model memiliki **kemampuan penjelasan variasi data yang sangat kuat**."
    elif 0.50 <= best_r2_val < 0.75:
        r2_summary = f"sebesar **{best_r2_val:.2f}** menunjukkan model memiliki **kemampuan penjelasan variasi data yang moderat/cukup baik**."
    elif 0.0 < best_r2_val < 0.50:
        r2_summary = f"sebesar **{best_r2_val:.2f}** tergolong **rendah**, artinya model hanya mampu menjelaskan sebagian kecil variasi data."
    else:
        r2_summary = f"sebesar **{best_r2_val:.2f}** tergolong **sangat buruk/negatif**, menandakan performa prediksi model lebih buruk daripada sekadar menggunakan rata-rata data."

    with st.container(border=True):
        st.markdown(f"**:material/lightbulb: Ringkasan Evaluasi Metrik {selected_unique_id}:**")
        st.info(
            f"- Secara keseluruhan, model **{overall_best_model}** paling konsisten unggul "
            f"(**{overall_best_count} dari 5** metrik)."
        )
        st.info(f"- Untuk nilai **$R^2$ ({best_r2_model})** {r2_summary}")