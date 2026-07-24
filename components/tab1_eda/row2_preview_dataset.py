import streamlit as st
from utilsforecast.plotting import plot_series

def render(df):
    target_column = st.session_state.get('target_column', None)

    st.subheader(":material/table_view: Preview Dataset")
    st.dataframe(df)

    with st.container(border=True):
        st.subheader(":material/show_chart: Visualisasi Series")
        try:
            fig = plot_series(df, target_col=target_column, engine='plotly')
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig)
        except Exception as e:
            st.warning(f"⚠️ Error visualisasi series: {e}")

    st.divider()