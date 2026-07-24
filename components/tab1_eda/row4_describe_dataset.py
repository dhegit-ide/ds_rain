import streamlit as st
import plotly.express as px

def render(df):
    st.subheader(":material/description: Statistik Deskriptif")
    target_column = st.session_state.get('target_column', None)
    if target_column:
        wilayah_stats = df.groupby('unique_id').agg({target_column: ['count', 'mean', 'std', 'min', 'max', 'sum']}).round(2)
        wilayah_stats.columns = ['Jumlah Data', 'Rata-rata', 'Std. Dev.', 'Minimum', 'Maksimum', 'Total']
        wilayah_stats = wilayah_stats.sort_values('Total', ascending=False)

        st.dataframe(wilayah_stats.reset_index())

    with st.container(border=True):    
        st.subheader(":material/candlestick_chart: Boxplot Distribusi")
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
            
        # DESKRIPSI BOXPLOT KESELURUHAN
        with st.expander(":material/description: Ringkasan Distribusi Data"):
            data_series = df[target_column].dropna()
            q1 = data_series.quantile(0.25)
            q3 = data_series.quantile(0.75)
            median = data_series.median()
            iqr = q3 - q1
            lower_bound = max(q1 - 1.5 * iqr, 0)
            upper_bound = q3 + 1.5 * iqr
            outliers = data_series[data_series > upper_bound]
            unique_id_count = df['unique_id'].nunique()

            desc_text = (
                f"Secara keseluruhan, kolom `{target_column}` dari **{unique_id_count}** group "
                f"memiliki nilai tengah (_median_) sebesar **{median:.2f}**, "
                f"dengan sebaran data utama berkumpul di rentang **{q1:.2f}** "
                f"hingga **{q3:.2f}** (_Q1–Q3_). "
            )
            if len(outliers) > 0:
                desc_text += (
                    f"Terdapat **{len(outliers)}** data pencilan (_outlier_) "
                    f"di atas batas normal **{upper_bound:.2f}**. "
                    f"Nilai maksimum mencapai **{data_series.max():.2f}**, "
                    f"menunjukkan adanya nilai ekstrem."
                )
            else: desc_text += "Tidak terdapat pencilan (_outlier_) yang terdeteksi."

            st.markdown(desc_text)
            st.markdown("**Detail per Group:**")
            for wilayah, subset in df.groupby("unique_id"):
                series = subset[target_column].dropna()
                q1 = series.quantile(0.25)
                q3 = series.quantile(0.75)
                median = series.median()
                iqr = q3 - q1
                lower_bound = max(q1 - 1.5 * iqr, 0)
                upper_bound = q3 + 1.5 * iqr
                outliers = series[series > upper_bound]
                n_data = len(series)

                desc_text = (
                    f"- **{wilayah}** → median **{median:.2f}**, "
                    f"rentang utama **{q1:.2f}–{q3:.2f}**. "
                )
                if len(outliers) > 0:
                    desc_text += (
                        f"Terdeteksi **{len(outliers)}** outlier dari total **{n_data}** data "
                        f"(di atas {upper_bound:.2f}), maksimum **{series.max():.2f}**."
                    )
                else: desc_text += f"Tidak ada outlier dari total **{n_data}** data."
                st.markdown(desc_text)

    st.divider()