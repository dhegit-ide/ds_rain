import streamlit as st
import plotly.express as px

def render(cv_df):
    selected_unique_id = st.session_state['selected_unique_id']
    df_sel = cv_df[cv_df['unique_id'] == selected_unique_id]
    forecast_cols = [c for c in df_sel.columns if c not in ['unique_id','ds','cutoff']]
    
    st.subheader(":material/candlestick_chart: Visualisasi Sebaran Data Hasil Cross Validation")
    st.caption(f":green-badge[Unique ID: {selected_unique_id}]")
    st.caption(":material/info: Gunakan kontrol di sidebar untuk memilih Unique ID")

    with st.container(border=True):
        df_long = df_sel.melt(
            id_vars=['ds','unique_id','cutoff'],
            value_vars=forecast_cols,
            var_name='forecast',
            value_name='value'
        )
        fig_box = px.box(
            df_long,
            x="forecast",
            y="value",
            color="forecast",
            points="outliers",
            color_discrete_sequence=px.colors.qualitative.Set2,
        )
        fig_box.update_layout(
            height=400,
            xaxis_title="Forecast",
            yaxis_title="Value",
            showlegend=True,
            margin=dict(l=10, r=10, t=40, b=10),
            xaxis=dict(
                tickangle=90,
                title_font=dict(size=12),
            ),
            boxgap=0.3,
            boxgroupgap=0.3,
        )

        st.plotly_chart(fig_box)

        # DESKRIPSI BOXPLOT
        with st.expander(":material/description: Ringkasan Distribusi Data"):
            for col in forecast_cols:
                series = df_sel[col].dropna()
                if series.empty:
                    continue
                q1 = series.quantile(0.25)
                q3 = series.quantile(0.75)
                median = series.median()
                iqr = q3 - q1
                lower_bound = max(q1 - 1.5 * iqr, 0)
                upper_bound = q3 + 1.5 * iqr
                outliers = series[series > upper_bound]

                desc_text = (
                    f"- **{col}** → median **{median:.2f}**, "
                    f"rentang utama **{q1:.2f}–{q3:.2f}**. "
                )
                if len(outliers) > 0:
                    desc_text += (
                        f"Terdeteksi **{len(outliers)}** outlier "
                        f"(di atas {upper_bound:.2f}), maksimum **{series.max():.2f}**."
                    )
                else:
                    desc_text += "Tidak ada outlier terdeteksi."
                st.markdown(desc_text)

    st.divider()