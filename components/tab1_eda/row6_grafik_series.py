import streamlit as st
from utilsforecast.plotting import plot_series

def render(df):
    st.subheader(f":material/show_chart: Grafik Tren Umum Variabel Utama")
    
    target_column = st.session_state.get('target_column', None)
    selected_unique_id = st.session_state['selected_unique_id']

    with st.container(border=True):
        st.caption(f":green-badge[Unique ID: {selected_unique_id}] :green-badge[Target kolom: {target_column}]")
        st.caption(":material/info: Gunakan kontrol di sidebar untuk memilih Unique ID & Target Kolom")
        try:
            fig = plot_series(df, target_col=target_column, ids=[selected_unique_id], engine='plotly')
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig)
        except Exception as e:
            st.warning(f"⚠️ Error Grafik Tren Umum Variabel Utama: {e}")

    st.divider()