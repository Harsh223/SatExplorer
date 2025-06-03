import streamlit as st
import plotly.express as px
import pandas as pd

def render_tab(df):
    st.header("Satellite Size & Launch Trends")
    st.info("""
    Explore launches by satellite size, launch provider, and orbit class. Use the sliders to set the time range.
    
    **Size classes:**
    - CubeSat: 1-16 kg
    - MicroSat: 16-100 kg
    - SmallSat: 100-500 kg
    - MediumSat: 500-1000 kg
    - LargeSat: >1000 kg
    """)
    coarse_types_all = df['CoarseType'].dropna().unique().tolist() if 'CoarseType' in df.columns else []
    default_coarse = ['P'] if 'P' in coarse_types_all else coarse_types_all
    selected_coarse = st.multiselect("Object Type (CoarseType)", coarse_types_all, default=default_coarse, help="Select which object types to include in all plots. 'P' = Payload (satellite)")
    if 'LaunchYear' not in df.columns or df['LaunchYear'].dropna().empty:
        st.warning("No LaunchYear data available. Cannot show trends.")
    else:
        min_year, max_year = int(df['LaunchYear'].min()), int(df['LaunchYear'].max())
        default_start = max_year - 9 if max_year - 9 > min_year else min_year
        year_range = st.slider("Select Year Range", min_year, max_year, (default_start, max_year))
        df_time = df[(df['LaunchYear'] >= year_range[0]) & (df['LaunchYear'] <= year_range[1])]
        if selected_coarse:
            df_time = df_time[df_time['CoarseType'].isin(selected_coarse)]
        def size_class(mass):
            if pd.isna(mass): return 'Unknown'
            if mass <= 16: return 'CubeSat'
            if mass <= 100: return 'MicroSat'
            if mass <= 500: return 'SmallSat'
            if mass <= 1000: return 'MediumSat'
            return 'LargeSat'
        df_time = df_time.copy()
        df_time['SizeClass'] = df_time['Mass'].apply(size_class)
        st.subheader("1. Satellites Launched by Size Class (per Year)")
        size_counts = df_time.groupby(['LaunchYear', 'SizeClass']).size().reset_index(name='Count')
        fig1 = px.bar(size_counts, x='LaunchYear', y='Count', color='SizeClass', barmode='stack',
                     title='Satellites Launched by Size Class per Year')
        st.plotly_chart(fig1, use_container_width=True)
        st.subheader("2. Launches by Company/Manufacturer Over Time")
        if 'Manufacturer' in df_time.columns:
            manu_counts = df_time.groupby(['LaunchYear', 'Manufacturer']).size().reset_index(name='Count')
            top_manus = manu_counts.groupby('Manufacturer')['Count'].sum().sort_values(ascending=False).head(10).index
            manu_counts = manu_counts[manu_counts['Manufacturer'].isin(top_manus)]
            fig2 = px.bar(manu_counts, x='LaunchYear', y='Count', color='Manufacturer', barmode='stack',
                         title='Top 10 Manufacturers by Launches per Year')
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("No Manufacturer data available.")
        st.subheader("3. Popular Orbits Over Time and by Size Class")
        if 'OpOrbitOQU' in df_time.columns:
            orbit_counts = df_time.groupby(['LaunchYear', 'OpOrbitOQU', 'SizeClass']).size().reset_index(name='Count')
            fig3 = px.bar(orbit_counts, x='LaunchYear', y='Count', color='OpOrbitOQU', barmode='stack',
                         title='Popular Orbits Over Time')
            st.plotly_chart(fig3, use_container_width=True)
            fig4 = px.bar(orbit_counts, x='SizeClass', y='Count', color='OpOrbitOQU', barmode='stack',
                         title='Popular Orbits by Satellite Size Class')
            st.plotly_chart(fig4, use_container_width=True)
        else:
            st.info("No OpOrbitOQU (Orbit Class) data available.")
        st.subheader("4. Popular Orbits (Main Class Only) Over Time and by Size Class")
        if 'OpOrbitOQU' in df_time.columns:
            df_time['MainOrbitClass'] = df_time['OpOrbitOQU'].astype(str).str.split('/').str[0]
            main_orbit_counts = df_time.groupby(['LaunchYear', 'MainOrbitClass', 'SizeClass']).size().reset_index(name='Count')
            fig5 = px.bar(main_orbit_counts, x='LaunchYear', y='Count', color='MainOrbitClass', barmode='stack',
                         title='Popular Orbits (Main Class Only) Over Time')
            st.plotly_chart(fig5, use_container_width=True)
            fig6 = px.bar(main_orbit_counts, x='SizeClass', y='Count', color='MainOrbitClass', barmode='stack',
                         title='Popular Orbits (Main Class Only) by Satellite Size Class')
            st.plotly_chart(fig6, use_container_width=True)
        else:
            st.info("No OpOrbitOQU (Orbit Class) data available.")
