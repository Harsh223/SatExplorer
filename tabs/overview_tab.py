import streamlit as st
import numpy as np
import plotly.express as px
from utils import get_date_confidence

def render_tab(df):
    st.header("Overview")
    st.markdown("""
    Welcome to the Satellite Catalog Explorer! This dashboard lets you explore and analyze the global satellite catalog. Use the filters and charts to answer questions about satellite types, launches, and more. Hover over info icons for explanations.
    """)
    st.subheader("Filtered Data Table")
    st.info("""
    **What is this table?**
    This table shows satellites and space objects from the global catalog. You can filter by type and launch year below.
    """)
    coarse_types = df['CoarseType'].dropna().unique().tolist() if 'CoarseType' in df.columns else []
    selected_types = st.multiselect("Coarse Type", coarse_types, default=coarse_types)
    years = df['LaunchYear'].dropna().astype(int).unique() if 'LaunchYear' in df.columns else []
    if len(years) > 0:
        min_year, max_year = int(years.min()), int(years.max())
        year_range = st.slider("Launch Year Range", min_year, max_year, (min_year, max_year))
    else:
        year_range = (None, None)
    filtered_df = df.copy()
    if selected_types:
        filtered_df = filtered_df[filtered_df['CoarseType'].isin(selected_types)]
    if year_range[0] is not None:
        filtered_df = filtered_df[(filtered_df['LaunchYear'] >= year_range[0]) & (filtered_df['LaunchYear'] <= year_range[1])]
    st.dataframe(filtered_df.assign(DateConfidence=filtered_df['LDate'].apply(get_date_confidence)) if 'LDate' in filtered_df.columns else filtered_df, use_container_width=True)
    st.subheader("Charts")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Satellite Type Distribution**  6f0\ufe0f")
        st.info("""
        **What does this chart show?**
        This pie chart shows the proportion of each main object type (payload, rocket stage, debris, etc.) in the catalog. 'Payload' means a satellite or experiment, 'Rocket' is a launch vehicle stage, and 'Debris' is a fragment or component.
        """)
        if 'CoarseType' in filtered_df.columns and not filtered_df['CoarseType'].isna().all():
            fig = px.pie(filtered_df, names='CoarseType', title='Satellite Type Distribution')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No CoarseType data available.")
    with col2:
        st.markdown("**Launches per Year**  680")
        st.info("""
        **What does this chart show?**
        This line chart shows how many objects were launched each year. It helps you see trends in space activity over time.
        """)
        if 'LaunchYear' in filtered_df.columns and not filtered_df['LaunchYear'].isna().all():
            launches = filtered_df['LaunchYear'].dropna().astype(int).value_counts().sort_index()
            fig = px.line(x=launches.index, y=launches.values, labels={'x': 'Year', 'y': 'Launches'}, title='Launches per Year')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No LaunchYear data available.")
    st.subheader("Mass Distribution")
    st.info("""
    **What does this chart show?**
    This histogram shows the distribution of object masses (in kilograms). It helps you see if most objects are small, large, or somewhere in between.
    """)
    if 'Mass' in filtered_df.columns and not filtered_df['Mass'].isna().all():
        mass_data = filtered_df['Mass'].dropna()
        if len(mass_data) > 1:
            q75, q25 = np.percentile(mass_data, [75, 25])
            iqr = q75 - q25
            bin_width = 2 * iqr / (len(mass_data) ** (1/3)) if iqr > 0 else (mass_data.max() - mass_data.min()) / 20
            if bin_width > 0:
                bins = int(np.ceil((mass_data.max() - mass_data.min()) / bin_width))
            else:
                bins = 10
        else:
            bins = 10
        fig = px.histogram(filtered_df, x='Mass', nbins=bins, title='Mass Distribution (kg)', labels={"Mass": "Mass (kg)"})
        fig.update_xaxes(dtick=500)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No Mass data available.")
    st.subheader("Basic Statistics")
    st.info("""
    **What does this table show?**
    This table summarizes the main statistics (like average, min, max) for each column in the filtered data.
    """)
    try:
        st.write(filtered_df.describe(include='all').transpose())
    except Exception as e:
        st.warning(f"Could not compute statistics: {e}")
