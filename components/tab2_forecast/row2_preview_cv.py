import streamlit as st
import pandas as pd
from utilsforecast.plotting import plot_series

def render(cv_df):
    if not pd.api.types.is_datetime64_any_dtype(cv_df['ds']):
        cv_df['ds'] = pd.to_datetime(cv_df['ds'], errors='coerce')
    selected_unique_id = st.session_state['selected_unique_id']
    
    st.subheader(":material/table_view: Preview Dataset")
    st.dataframe(cv_df)

    with st.container(border=True):
        st.subheader(":material/show_chart: Visualisasi Forecast")
        st.caption(":material/info: Gunakan kontrol di sidebar untuk memilih Unique ID")
        pred_cols = [c for c in cv_df.columns if c not in ['unique_id','ds','cutoff','y']]
        if len(pred_cols) == 0:
            st.warning(":material/warning: Tidak ada kolom hasil prediksi model ditemukan.")
            return
        fig = plot_series(
                    df=cv_df[['unique_id','ds','y']],
                    forecasts_df=cv_df.drop(columns=['cutoff', 'y']),
                    ids=[selected_unique_id],
                    engine='plotly'
        )
        fig.update_layout(showlegend=True)
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader(":material/show_chart: Visualisasi Forecast (100 data terakhir)")
        st.caption(":material/info: Gunakan kontrol di sidebar untuk memilih Unique ID")
        last_100_ds = cv_df['ds'].drop_duplicates().nlargest(100)
        df_filtered = cv_df[(cv_df['unique_id'] == selected_unique_id) & (cv_df['ds'].isin(last_100_ds))]

        fig2 = plot_series(
            df=df_filtered[['unique_id','ds','y']],
            forecasts_df=df_filtered[['unique_id','ds'] + pred_cols],
            ids=[selected_unique_id],
            engine='plotly'
        )
        fig2.update_layout(showlegend=True)
        st.plotly_chart(fig2, use_container_width=True)
    
    st.divider()