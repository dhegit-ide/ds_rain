import streamlit as st
import plotly.express as px
from utils.detect_freq import detect_and_summary

MONTH_LABELS = {
    1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "Mei", 6: "Jun",
    7: "Jul", 8: "Agu", 9: "Sep", 10: "Okt", 11: "Nov", 12: "Des",
}

def _build_insights(df_plot, overall_mean, target_column, selected_unique_id, min_year, max_year):
    """Mengembalikan list of string insight berdasarkan analisis musiman."""
    insights = []

    # --- Statistik dasar ---
    max_row = overall_mean.loc[overall_mean[target_column].idxmax()]
    min_row = overall_mean.loc[overall_mean[target_column].idxmin()]
    max_month = MONTH_LABELS[int(max_row["month"])]
    min_month = MONTH_LABELS[int(min_row["month"])]
    max_val, min_val = max_row[target_column], min_row[target_column]

    freq, _, _, total, unit = detect_and_summary(df_plot)
    grand_mean = overall_mean[target_column].mean()

    # --- Insight 1: Puncak & Lembah ---
    insights.append(
        f"Selama periode **{min_year}–{max_year}** (**{total} {unit}**), "
        f"**rata-rata** `{target_column}` di **{selected_unique_id}** mencapai puncaknya pada bulan "
        f"**{max_month} ({max_val:.1f})** dan terendah pada  bulan **{min_month} ({min_val:.1f})**."
    )

    # --- Insight 2: Pola Musiman ---
    if (max_val - min_val) > (grand_mean * 0.5):
        wet = [MONTH_LABELS[m] for m in overall_mean.loc[overall_mean[target_column] > grand_mean, "month"]]
        dry = [MONTH_LABELS[m] for m in overall_mean.loc[overall_mean[target_column] <= grand_mean, "month"]]
        insights.append(
            f"- Pola musiman menunjukkan bahwa musim basah cenderung terjadi pada bulan **{', '.join(wet)}**, "
            f"sedangkan musim kering berlangsung pada bulan **{', '.join(dry)}**."
        )
    else:
        insights.append("- Pola musiman menunjukkan curah hujan relatif merata sepanjang tahun.")

    # --- Insight 3: Variabilitas ---
    monthly_std = df_plot.groupby('month')[target_column].std()
    max_std_month = MONTH_LABELS[int(monthly_std.idxmax())]
    insights.append(
        f"- Tingkat ketidakpastian curah hujan antar tahun tercatat paling tinggi pada bulan **{max_std_month}** "
        f"karena memiliki nilai fluktuasi terbesar dengan standar deviasi **{monthly_std.max():.1f}**)."
    )

    # --- Insight 4: Tahun Ekstrem ---
    yearly_totals = df_plot.groupby('year')[target_column].sum()
    insights.append(
        f"- Tahun **{yearly_totals.idxmax()}** menjadi periode paling basah, "
        f"sedangkan periode paling kering terjadi pada tahun **{yearly_totals.idxmin()}**."
    )

    # --- Insight 5: Dinamika Puncak ---
    peak_months = (
        df_plot.loc[df_plot.groupby('year')[target_column].idxmax(), 'month']
        .unique()
    )
    if len(peak_months) > 1:
        peak_names = ', '.join(sorted(MONTH_LABELS[int(m)] for m in peak_months))
        insights.append(f"- Puncak curah hujan tercatat cukup dinamis karena posisinya bergeser setiap tahun dan pernah terjadi pada bulan **{peak_names}**.")
    else:
        insights.append(
            f"- Pola puncak curah hujan tercatat sangat konsisten karena selalu terjadi pada bulan "
            f"**{MONTH_LABELS[int(peak_months[0])]}** setiap tahunnya."
        )
    return insights


def render(df):
    target_column = st.session_state.get('target_column')
    selected_unique_id = st.session_state.get('selected_unique_id')

    st.subheader(":material/show_chart: Grafik Pola Musiman Variabel Utama per Tahun", help="Grafik yang menampilkan pola musiman dari variabel target pada setiap Unique ID")
    with st.container(border=True):
        st.caption(f":green-badge[Unique ID: {selected_unique_id}] :green-badge[Target kolom: {target_column}]")
        st.caption(":material/info: Gunakan kontrol di sidebar untuk memilih Unique ID & Target Kolom")

        # --- Preprocessing ---
        df_plot = df[df['unique_id'] == selected_unique_id].copy()
        df_plot['year'] = df_plot['ds'].dt.year
        df_plot['month'] = df_plot['ds'].dt.month

        min_year, max_year = df_plot['year'].min(), df_plot['year'].max()
        mean_label = f"Mean {selected_unique_id} {min_year}–{max_year}"

        monthly_by_year = df_plot.groupby(['year', 'month'])[target_column].sum().reset_index()
        overall_mean = df_plot.groupby('month')[target_column].mean().reset_index()

        # --- Kontrol UI ---
        hide_years = st.toggle(
            "Sembunyikan garis lainnya",
            value=False,
        )

        # --- Plot ---
        fig = px.line(
            monthly_by_year,
            x='month', y=target_column, color='year', markers=True,
            labels={'month': 'Bulan', target_column: f'Target [{target_column}]', 'year': 'Tahun'},
        )
        fig.update_traces(line=dict(dash='dash'))
        fig.add_scatter(
            x=overall_mean["month"], y=overall_mean[target_column],
            mode="lines+markers", line=dict(color="black", width=3),
            name=mean_label,
        )

        # Visibility: 1 loop saja
        for trace in fig.data:
            if trace.name != mean_label:
                trace.visible = "legendonly" if hide_years else True

        fig.update_xaxes(
            tickmode='array',
            tickvals=list(range(1, 13)),
            ticktext=list(MONTH_LABELS.values()),
        )
        
        st.plotly_chart(fig, use_container_width=True)

    # --- Ringkasan Otomatis ---
    st.markdown("**:material/lightbulb: Ringkasan Analisis Musiman:**")
    if overall_mean.empty:
        st.info("Data tidak tersedia untuk membuat ringkasan.")
    else:
        insights = _build_insights(
            df_plot, overall_mean, target_column, selected_unique_id, min_year, max_year
        )
        for i, insight in enumerate(insights):
            if i == 0:
                st.markdown(insight)
            else:
                st.info(insight)

    st.divider()