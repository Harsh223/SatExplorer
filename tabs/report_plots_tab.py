import streamlit as st
import plotly.express as px
import pandas as pd

def render_tab(df):
    st.header("Publication Figures for Launch Trends Analysis")
    st.info("""
    This tab generates all the plots referenced in the academic LaTeX subsection on satellite launch trends analysis. 
    Each plot corresponds to a specific figure in the report and is optimized for publication quality.
    
    **Note:** These plots use international standard satellite mass classifications. Use the filters below to select object types and time range.
    """)
    
    # Object Type (CoarseType) selector - exactly like Size Trends tab
    coarse_types_all = df['CoarseType'].dropna().unique().tolist() if 'CoarseType' in df.columns else []
    default_coarse = ['P'] if 'P' in coarse_types_all else coarse_types_all
    selected_coarse = st.multiselect("Object Type (CoarseType)", coarse_types_all, default=default_coarse, help="Select which object types to include in all plots. 'P' = Payload (satellite)", key="report_plots_coarse_type")
    
    # Year range selector - exactly like Size Trends tab
    if 'LaunchYear' not in df.columns or df['LaunchYear'].dropna().empty:
        st.warning("No LaunchYear data available. Cannot show trends.")
        return
    else:
        min_year, max_year = int(df['LaunchYear'].min()), int(df['LaunchYear'].max())
        default_start = max_year - 9 if max_year - 9 > min_year else min_year
        year_range = st.slider("Select Year Range", min_year, max_year, (default_start, max_year), key="report_plots_year_range")
        
        # Apply filters
        df_filtered = df[(df['LaunchYear'] >= year_range[0]) & (df['LaunchYear'] <= year_range[1])]
        if selected_coarse:
            df_filtered = df_filtered[df_filtered['CoarseType'].isin(selected_coarse)]
    
    # Add international standard size classification
    def size_class(mass):
        if pd.isna(mass): 
            return 'Unknown'
        if mass < 1: 
            return 'Femtosatellite (0.1-1 kg)'
        if mass <= 10: 
            return 'Picosatellite (1-10 kg)'
        if mass <= 100: 
            return 'Nanosatellite (10-100 kg)'
        if mass <= 1000: 
            return 'Microsatellite (100-1000 kg)'
        if mass <= 5000: 
            return 'Small Satellite (1000-5000 kg)'
        if mass <= 10000: 
            return 'Medium Satellite (5000-10000 kg)'
        return 'Large Satellite (>10000 kg)'
    
    df_filtered['SizeClass'] = df_filtered['Mass'].apply(size_class)
    
    # Figure 1: Satellite Launch Trends by Size Classification (fig:size_class_trends)
    st.subheader("Figure 1: Satellite Launch Trends by Size Classification")
    st.markdown("*Temporal evolution of satellite launch trends categorized by international standard size classifications*")
    
    size_counts = df_filtered.groupby(['LaunchYear', 'SizeClass']).size().reset_index(name='Count')
    
    # Define consistent color scheme for size classes
    size_class_colors = {
        'Femtosatellite (0.1-1 kg)': '#FF6B6B',
        'Picosatellite (1-10 kg)': '#4ECDC4', 
        'Nanosatellite (10-100 kg)': '#45B7D1',
        'Microsatellite (100-1000 kg)': '#96CEB4',
        'Small Satellite (1000-5000 kg)': '#FFEAA7',
        'Medium Satellite (5000-10000 kg)': '#DDA0DD',
        'Large Satellite (>10000 kg)': '#FF8C94',
        'Unknown': '#95A5A6'
    }
    
    fig1 = px.bar(size_counts, x='LaunchYear', y='Count', color='SizeClass', 
                  title='Satellite Launch Trends by Size Classification (1957-2025)',
                  labels={'LaunchYear': 'Launch Year', 'Count': 'Number of Satellites Launched'},
                  color_discrete_map=size_class_colors)
    fig1.update_layout(
        xaxis_title="Launch Year",
        yaxis_title="Number of Satellites Launched",
        legend_title="Satellite Size Classification",
        font=dict(size=12),
        height=500,
        showlegend=True
    )
    st.plotly_chart(fig1, use_container_width=True)
    
    # Figure 2: Leading Satellite Manufacturers by Launch Volume (fig:manufacturer_trends)
    st.subheader("Figure 2: Leading Satellite Manufacturers by Launch Volume")
    st.markdown("*Annual launch volume trends for the ten leading satellite manufacturers*")
    
    if 'Manufacturer' in df_filtered.columns:
        # Get top 10 manufacturers by total launches
        manu_totals = df_filtered.groupby('Manufacturer').size().sort_values(ascending=False)
        top_10_manus = manu_totals.head(10).index.tolist()
        
        # Filter data to top manufacturers and group by year
        df_top_manu = df_filtered[df_filtered['Manufacturer'].isin(top_10_manus)]
        manu_counts = df_top_manu.groupby(['LaunchYear', 'Manufacturer']).size().reset_index(name='Count')
        
        fig2 = px.bar(manu_counts, x='LaunchYear', y='Count', color='Manufacturer',
                      title='Leading Satellite Manufacturers by Launch Volume (Top 10)',
                      labels={'LaunchYear': 'Launch Year', 'Count': 'Number of Satellites Launched'})
        fig2.update_layout(
            xaxis_title="Launch Year",
            yaxis_title="Number of Satellites Launched", 
            legend_title="Manufacturer",
            font=dict(size=12),
            height=500
        )
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.warning("No Manufacturer data available for this plot.")
    
    # Figure 3: Annual Space Object Launch Trends (fig:launch_trends)
    st.subheader("Figure 3: Annual Space Object Launch Trends")
    st.markdown("*Historical evolution of annual space object launches demonstrating accelerating launch activity*")
    
    annual_launches = df_filtered.groupby('LaunchYear').size().reset_index(name='Count')
    
    fig3 = px.line(annual_launches, x='LaunchYear', y='Count',
                   title='Annual Satellite Launch Trends (1957-2025)',
                   labels={'LaunchYear': 'Launch Year', 'Count': 'Number of Satellites Launched'})
    fig3.update_layout(
        xaxis_title="Launch Year",
        yaxis_title="Number of Satellites Launched",
        font=dict(size=12),
        height=400
    )
    fig3.update_traces(line=dict(width=3, color='#2E86AB'))
    st.plotly_chart(fig3, use_container_width=True)
    
    # Figure 4: Orbital Class Preferences Over Time (fig:orbit_trends)
    st.subheader("Figure 4: Orbital Class Preferences Over Time")
    st.markdown("*Temporal evolution of orbital class preferences showing shifting utilization patterns*")
    
    if 'OpOrbitOQU' in df_filtered.columns:
        orbit_counts = df_filtered.groupby(['LaunchYear', 'OpOrbitOQU']).size().reset_index(name='Count')
        
        fig4 = px.bar(orbit_counts, x='LaunchYear', y='Count', color='OpOrbitOQU',
                      title='Orbital Class Preferences Over Time (1990-2025)',
                      labels={'LaunchYear': 'Launch Year', 'Count': 'Number of Satellites Launched'})
        fig4.update_layout(
            xaxis_title="Launch Year",
            yaxis_title="Number of Satellites Launched",
            legend_title="Orbital Class",
            font=dict(size=12),
            height=500
        )
        st.plotly_chart(fig4, use_container_width=True)
    else:
        st.warning("No orbital class (OpOrbitOQU) data available for this plot.")
    
    # Figure 5: Orbital Distribution by Satellite Size (fig:orbit_by_size)
    st.subheader("Figure 5: Orbital Distribution by Satellite Size")
    st.markdown("*Distribution of satellite size categories across orbital regimes*")
    
    if 'OpOrbitOQU' in df_filtered.columns:
        orbit_size_counts = df_filtered.groupby(['SizeClass', 'OpOrbitOQU']).size().reset_index(name='Count')
        
        fig5 = px.bar(orbit_size_counts, x='SizeClass', y='Count', color='OpOrbitOQU',
                      title='Orbital Distribution by Satellite Size Category',
                      labels={'SizeClass': 'Satellite Size Class', 'Count': 'Number of Satellites'})
        fig5.update_layout(
            xaxis_title="Satellite Size Classification",
            yaxis_title="Number of Satellites",
            legend_title="Orbital Class",
            font=dict(size=12),
            height=500
        )
        fig5.update_xaxes(tickangle=45)
        st.plotly_chart(fig5, use_container_width=True)
    else:
        st.warning("No orbital class (OpOrbitOQU) data available for this plot.")
    
    # Figure 6: Main Orbital Class Utilization Trends (fig:main_orbit_trends)
    st.subheader("Figure 6: Main Orbital Class Utilization Trends")
    st.markdown("*Evolution of primary orbital class utilization patterns*")
    
    if 'OpOrbitOQU' in df_filtered.columns:
        # Extract main orbital class (before the '/' character)
        df_filtered_copy = df_filtered.copy()
        df_filtered_copy['MainOrbitClass'] = df_filtered_copy['OpOrbitOQU'].astype(str).str.split('/').str[0]
        
        main_orbit_counts = df_filtered_copy.groupby(['LaunchYear', 'MainOrbitClass']).size().reset_index(name='Count')
        
        fig6 = px.bar(main_orbit_counts, x='LaunchYear', y='Count', color='MainOrbitClass',
                      title='Main Orbital Class Utilization Trends (2000-2025)',
                      labels={'LaunchYear': 'Launch Year', 'Count': 'Number of Satellites Launched'})
        fig6.update_layout(
            xaxis_title="Launch Year",
            yaxis_title="Number of Satellites Launched",
            legend_title="Main Orbital Class",
            font=dict(size=12),
            height=500
        )
        st.plotly_chart(fig6, use_container_width=True)
    else:
        st.warning("No orbital class (OpOrbitOQU) data available for this plot.")
    
    # Figure 7: Orbital Classes by Satellite Size Category (fig:main_orbit_by_size)
    st.subheader("Figure 7: Orbital Classes by Satellite Size Category")
    st.markdown("*Distribution of primary orbital classes across satellite size categories*")
    
    if 'OpOrbitOQU' in df_filtered.columns:
        df_filtered_copy = df_filtered.copy()
        df_filtered_copy['MainOrbitClass'] = df_filtered_copy['OpOrbitOQU'].astype(str).str.split('/').str[0]
        
        main_orbit_size_counts = df_filtered_copy.groupby(['SizeClass', 'MainOrbitClass']).size().reset_index(name='Count')
        
        fig7 = px.bar(main_orbit_size_counts, x='SizeClass', y='Count', color='MainOrbitClass',
                      title='Main Orbital Classes by Satellite Size Category',
                      labels={'SizeClass': 'Satellite Size Class', 'Count': 'Number of Satellites'})
        fig7.update_layout(
            xaxis_title="Satellite Size Classification",
            yaxis_title="Number of Satellites",
            legend_title="Main Orbital Class",
            font=dict(size=12),
            height=500
        )
        fig7.update_xaxes(tickangle=45)
        st.plotly_chart(fig7, use_container_width=True)
    else:
        st.warning("No orbital class (OpOrbitOQU) data available for this plot.")
    
    # Summary statistics for reference
    st.subheader("Summary Statistics for Report")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Satellites Analyzed", len(df_filtered))
    
    with col2:
        if 'LaunchYear' in df_filtered.columns:
            latest_year = df_filtered['LaunchYear'].max()
            recent_launches = len(df_filtered[df_filtered['LaunchYear'] == latest_year])
            st.metric(f"Launches in {int(latest_year)}", recent_launches)
    
    with col3:
        if 'Manufacturer' in df_filtered.columns:
            unique_manufacturers = df_filtered['Manufacturer'].nunique()
            st.metric("Unique Manufacturers", unique_manufacturers)
    
    with col4:
        if 'OpOrbitOQU' in df_filtered.columns:
            unique_orbits = df_filtered['OpOrbitOQU'].nunique()
            st.metric("Unique Orbital Classes", unique_orbits)
    
    st.markdown("---")
    st.markdown("""
    **Note for Academic Publication:**
    - All plots are generated using the SatExplorer tool developed for this research
    - Data source: Global Satellite Catalog (SATCAT) maintained by the US Space Surveillance Network
    - Satellite classifications follow international standards (ITU/aerospace industry)
    - Analysis focuses on payload objects (satellites) only, excluding debris and rocket stages
    """)
