import streamlit as st
from utilsforecast.losses import mae, rmse, mse, smape
from utilsforecast.evaluation import evaluate
from utils.data_loader import r2


def render(cv_df):
    selected_pred = st.session_state['selected_pred']
    selected_unique_id = st.session_state['selected_unique_id']

    st.subheader(f":material/assignment_globe: Ringkasan Kinerja Global")
    st.caption(f":green-badge[Prediksi: {selected_pred}]")
    st.caption(":material/info: Gunakan kontrol di sidebar untuk memilih prediksi lainnya")

    metrics_df = evaluate(
        cv_df.drop(columns='cutoff'), 
        metrics=[mae,rmse,mse,smape,r2]
    )
    
    global_df = metrics_df[[ "metric", selected_pred ]]
    mae_val   = global_df.loc[global_df['metric'] == 'mae', selected_pred].mean()
    rmse_val  = global_df.loc[global_df['metric'] == 'rmse', selected_pred].mean()
    mse_val   = global_df.loc[global_df['metric'] == 'mse', selected_pred].mean()
    smape_val = global_df.loc[global_df['metric'] == 'smape', selected_pred].mean()
    r2_val    = global_df.loc[global_df['metric'] == 'r2', selected_pred].mean()

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("MAE (Global)", f"{mae_val:.2f}", border=True)
    col2.metric("RMSE (Global)", f"{rmse_val:.2f}", border=True)
    col3.metric("MSE (Global)", f"{mse_val:.2f}", border=True)
    col4.metric("SMAPE (Global)", f"{smape_val*100:.2f}%", border=True)  # persen
    col5.metric("R² (Global)", f"{r2_val:.2f}", border=True)

    st.divider()