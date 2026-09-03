import streamlit as st
import plotly.express as px

def render(df):
    target_column = st.session_state.get('target_column', None)
    selected_unique_id = st.session_state['selected_unique_id']

    st.subheader(":material/show_chart: Grafik Pola Musiman Variabel Utama per Tahun")
    st.caption(f":green-badge[Unique ID: {selected_unique_id}] :green-badge[Target kolom: {target_column}]")
    st.caption(":material/info: Gunakan kontrol di sidebar untuk memilih Unique ID & Target Kolom")

    df_plot = df[df['unique_id'] == selected_unique_id].copy()
    df_plot['year'] = df_plot['ds'].dt.year
    df_plot['month'] = df_plot['ds'].dt.month
    
    # rata-rata per bulan per tahun
    monthly_by_year = df_plot.groupby(['year','month'])[target_column].sum().reset_index()

    # plot interaktif dengan legend per tahun
    fig = px.line(monthly_by_year, 
                x='month', y=target_column, 
                color='year', 
                markers=True,
                labels={'month':'Bulan', target_column:f'Target [{target_column}]','year':'Tahun'},
                )

    # garis tahun jadi dashed
    for trace in fig.data:
        if trace.name != f'Mean {selected_unique_id} 2006–2025':
            trace.line.update(dash='dash')
    
    # garis rata-rata keseluruhan
    overall_mean = df_plot.groupby('month')[target_column].mean().reset_index()
    fig.add_scatter(x=overall_mean['month'], 
                    y=overall_mean[target_column], 
                    mode='lines+markers',
                    line=dict(color='black', width=3),
                    name=f'Mean {selected_unique_id} 2006–2025')

    # ubah label bulan jadi Jan–Dec
    fig.update_xaxes(tickmode='array', tickvals=list(range(1,13)),
                    ticktext=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'])

    st.plotly_chart(fig, use_container_width=True)
    st.divider()