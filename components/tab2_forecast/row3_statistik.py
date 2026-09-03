import streamlit as st
import pandas as pd

def render(cv_df):
    selected_unique_id = st.session_state['selected_unique_id']
    
    st.subheader(":material/description: Statistik Cross Validation")
    st.caption(f":green-badge[Unique ID: {selected_unique_id}]")
    st.caption(":material/info: Gunakan kontrol di sidebar untuk memilih Unique ID")

    df_sel = cv_df[cv_df['unique_id'] == selected_unique_id]
    forecast_cols = [c for c in df_sel.columns if c not in ['unique_id','ds','cutoff']]
    rows = []
    for col in forecast_cols:
        series = df_sel[col].dropna()
        rows.append({
            "forecast": col,
            "Jumlah Data": series.count(),
            "Rata-rata": series.mean(),
            "Std. Dev.": series.std(),
            "Minimum": series.min(),
            "Maksimum": series.max(),
            "Total": series.sum()
        })
    stats_df = pd.DataFrame(rows)
    stats_df = stats_df.round(3)
    def highlight_y(row): return ['background-color: lightblue' if row['forecast'] == 'y' else '' for _ in row]
    styled = stats_df.style.apply(highlight_y, axis=1)
    st.dataframe(styled)

    st.divider()