import streamlit as st
import pandas as pd
import plotly.express as px

def render(cv_df):
    selected_unique_id = st.session_state['selected_unique_id']
    
    st.subheader(":material/description: Statistik Cross Validation")
    st.markdown(f"##### **{selected_unique_id}**")

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

    with st.container(border=True):    
        st.subheader(":material/candlestick_chart: Boxplot Distribusi")
        st.markdown(f"##### **{selected_unique_id}**")
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