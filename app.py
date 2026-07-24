import streamlit as st

st.set_page_config(
    page_title="Forecasting Demo",
    page_icon=":chart_with_upwards_trend:",
    layout="wide",
)

pg = st.navigation(
    [
        st.Page("app_pages/tab1_eda.py", title="Overview Dataset", icon=":material/dashboard:", default=True),
        st.Page("app_pages/tab2_forecast.py", title="Forecasting", icon=":material/bar_chart:"),
    ]
)
pg.run()
