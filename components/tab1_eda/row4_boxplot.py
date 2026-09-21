import streamlit as st
import plotly.express as px

def render(df):
    st.subheader(":material/candlestick_chart: Distribusi Boxplot", help="Distribusi boxplot digunakan untuk menganalisis tingkat persebaran yang terlihat dari median, rentang, kuartil, serta mendeteksi outlier")

    target_column = st.session_state.get("target_column", None)
    col1, col2 = st.columns(2)
    
    with col1:
        with st.container(border=True, height=450):    
            fig_box = px.box(
                df,
                x="unique_id",
                y=target_column,
                color="unique_id",
                color_discrete_sequence=px.colors.qualitative.Set2,
                points="outliers"
            )
            fig_box.update_layout(
                height=400,
                xaxis_title="Group",
                yaxis_title=target_column,
                showlegend=True,
                margin=dict(l=10, r=10, t=40, b=10),
                xaxis=dict(
                    tickangle=90,
                    title_font=dict(size=12),
                ),
                boxgap=0.3,
                boxgroupgap=0.3,
            )
            st.plotly_chart(fig_box, use_container_width=True)

    with col2:
        with st.container(border=True, height=450):
            st.markdown("**:material/lightbulb: Detail per Group:**")
            for uid, subset in df.groupby("unique_id"):
                series = subset[target_column].dropna()
                q1 = series.quantile(0.25)
                q3 = series.quantile(0.75)
                median = series.median()
                iqr = q3 - q1
                lower_bound = max(q1 - 1.5 * iqr, 0)
                upper_bound = q3 + 1.5 * iqr
                outliers = series[series > upper_bound]
                n_data = len(series)
                desc_text = (f"- **{uid}:** ")
                desc_text += (f"Terdeteksi **{len(outliers)}** outlier dari atas _upper-bound_, dengan rentang data **{series.min():.1f} – {series.max():.1f}**")
                st.info(desc_text)
    
    st.divider()