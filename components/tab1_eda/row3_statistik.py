import streamlit as st

def render(df):
    with st.expander(":material/description: Tabel Statistik Deskriptif", expanded=False):
        target_column = st.session_state.get('target_column', None)
        if target_column and target_column in df.columns:
            # Mengelompokkan berdasarkan unique_id dan menghitung statistik deskriptif bawaan describe()
            wilayah_stats = df.groupby('unique_id')[target_column].describe().round(2)
            
            # Mengubah nama kolom ke Bahasa Indonesia
            wilayah_stats = wilayah_stats.rename(columns={
                'count': 'Jumlah Data',
                'mean': 'Rata-rata',
                'std': 'Std. Dev.',
                'min': 'Minimum',
                '25%': 'Q1 (25%)',
                '50%': 'Median (50%)',
                '75%': 'Q3 (75%)',
                'max': 'Maksimum'
            })
            
            # Urutkan berdasarkan Rata-rata atau statistik lain yang diinginkan
            wilayah_stats = wilayah_stats.sort_values('Rata-rata', ascending=False)
            
            st.dataframe(wilayah_stats.reset_index(), use_container_width=True)
            
    st.divider()