import streamlit as st
import plotly.express as px

def render_tab(df):
    st.header("SatType Analysis (Bytes 1, 2, 3)")
    st.info("""
    Analyze the SatType code's first three bytes: Coarse Type, Type Modifier, and Attach Flag. Use the filters below to focus on specific types or years.
    """)
    st.markdown("**Filter by Launch Year and Coarse Type**")
    coarse_types = df['CoarseType'].dropna().unique().tolist() if 'CoarseType' in df.columns else []
    selected_types = st.multiselect("Coarse Type", coarse_types, default=coarse_types, key='sattype_coarse')
    years = df['LaunchYear'].dropna().astype(int).unique() if 'LaunchYear' in df.columns else []
    if len(years) > 0:
        min_year, max_year = int(years.min()), int(years.max())
        year_range = st.slider("Launch Year Range", min_year, max_year, (min_year, max_year), key='sattype_year')
    else:
        year_range = (None, None)
    sattype_df = df.copy()
    if selected_types:
        sattype_df = sattype_df[sattype_df['CoarseType'].isin(selected_types)]
    if year_range[0] is not None:
        sattype_df = sattype_df[(sattype_df['LaunchYear'] >= year_range[0]) & (sattype_df['LaunchYear'] <= year_range[1])]
    # Byte 1
    st.subheader("Byte 1: Coarse Type Distribution")
    st.info("""
    Byte 1 of the SatType code tells you the main category of the object:
    - **P**: Payload (satellite or experiment)
    - **C**: Component (part of a larger object)
    - **R**: Rocket stage
    - **D**: Fragmentation debris
    - **S**: Suborbital payload
    - **X**: Deleted entry
    - **Z**: Spurious entry
    """)
    if 'SatType_1' in sattype_df.columns:
        fig1 = px.histogram(sattype_df, x='SatType_1', title='Coarse Type (Byte 1) Distribution', color='SatType_1')
        st.plotly_chart(fig1, use_container_width=True)
        st.dataframe(sattype_df['SatType_1'].value_counts().rename_axis('Coarse Type').reset_index(name='Count'))
    else:
        st.info("No SatType_1 data available.")
    # Byte 2
    st.subheader("Byte 2: Type Modifier Distribution")
    st.info("""
    Byte 2 modifies the main type. For example:
    - **A**: Alias entry (special record for leased or jointly owned satellite)
    - **H**: Spaceship with humans aboard at launch
    - **P**: Spaceship test flight without crew
    - **X**: Non-standard payload
    - **R1-R5**: Rocket stage number
    - **C**: Cargo placeholder
    - **D**: Deployer for separately integrated payload
    """)
    if 'SatType_2' in sattype_df.columns:
        fig2 = px.histogram(sattype_df, x='SatType_2', title='Type Modifier (Byte 2) Distribution', color='SatType_2')
        st.plotly_chart(fig2, use_container_width=True)
        st.dataframe(sattype_df['SatType_2'].value_counts().rename_axis('Type Modifier').reset_index(name='Count'))
        st.markdown("**Combined Byte 1/2 Analysis**")
        if 'SatType_1_2' in sattype_df.columns:
            fig2b = px.histogram(sattype_df, x='SatType_1_2', title='Combined Byte 1/2 Distribution', color='SatType_1_2')
            st.plotly_chart(fig2b, use_container_width=True)
            st.dataframe(sattype_df['SatType_1_2'].value_counts().rename_axis('Byte 1-2').reset_index(name='Count'))
    else:
        st.info("No SatType_2 data available.")
    # Byte 3
    st.subheader("Byte 3: Attach Flag Distribution")
    st.info("""
    Byte 3 describes why an object is attached to its parent:
    - **A**: Permanently attached
    - **F**: Stuck attached by mistake
    - **S**: Expected to separate in future
    - **T**: Never flew free but transferred
    - **I**: Internal (remains inside another object)
    """)
    if 'SatType_3' in sattype_df.columns:
        fig3 = px.histogram(sattype_df, x='SatType_3', title='Attach Flag (Byte 3) Distribution', color='SatType_3')
        st.plotly_chart(fig3, use_container_width=True)
        st.dataframe(sattype_df['SatType_3'].value_counts().rename_axis('Attach Flag').reset_index(name='Count'))
    else:
        st.info("No SatType_3 data available.")
