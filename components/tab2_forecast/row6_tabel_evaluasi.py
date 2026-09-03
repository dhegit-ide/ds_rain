import streamlit as st
from utilsforecast.losses import mae, rmse, mse, smape
from utilsforecast.evaluation import evaluate
from utils.data_loader import r2


def render(cv_df):
    st.subheader(":material/leaderboard: Tabel Evaluasi Metrik")
    metrics_df = evaluate(
        cv_df.drop(columns='cutoff'), 
        metrics=[mae,rmse,mse,smape,r2]
    )
    st.dataframe(metrics_df.round(3))

    st.divider()