import streamlit as st
import pandas as pd
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


    # Tampilkan 5 Card Horizontal
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


    # Insight Text
    # with st.container(border=True):
    best_models = [best_mae_model, best_rmse_model, best_mse_model, best_smape_model, best_r2_model]

    best_counts = pd.Series(best_models).value_counts()
    overall_best_model = best_counts.idxmax()
    overall_best_count = best_counts.max()

    st.markdown(f"**:material/lightbulb: Ringkasan Evaluasi Metrik {selected_unique_id}:**")
    st.info(
        f"- Secara keseluruhan, model **{overall_best_model}** paling konsisten unggul "
        f"({overall_best_count} dari 5 metrik)."
    )