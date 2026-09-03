import streamlit as st

def render(df):
    st.subheader(":material/description: Statistik Deskriptif")
    target_column = st.session_state.get('target_column', None)
    if target_column:
        wilayah_stats = df.groupby('unique_id').agg({target_column: ['count', 'mean', 'std', 'min', 'max', 'sum']}).round(2)
        wilayah_stats.columns = ['Jumlah Data', 'Rata-rata', 'Std. Dev.', 'Minimum', 'Maksimum', 'Total']
        wilayah_stats = wilayah_stats.sort_values('Total', ascending=False)

        st.dataframe(wilayah_stats.reset_index())
    
    st.divider()