import streamlit as st
import plotly.express as px

def render_tab(df):
    st.header("Advanced Filters & Byte-level Exploration")
    st.info("""
    Use these filters to select objects by any SatType byte. Each byte gives extra detail about the object's role, status, or special flags. See the Help/Glossary tab for full explanations.
    """)
    filter_cols = [f'SatType_{i+1}' for i in range(12) if f'SatType_{i+1}' in df.columns]
    adv_filtered_df = df.copy()
    col1, col2 = st.columns(2)
    with col1:
        for col in filter_cols[:6]:
            unique_vals = adv_filtered_df[col].dropna().unique().tolist()
            selected = st.multiselect(f"Filter {col}", unique_vals, default=unique_vals)
            adv_filtered_df = adv_filtered_df[adv_filtered_df[col].isin(selected)]
    with col2:
        for col in filter_cols[6:]:
            unique_vals = adv_filtered_df[col].dropna().unique().tolist()
            selected = st.multiselect(f"Filter {col}", unique_vals, default=unique_vals)
            adv_filtered_df = adv_filtered_df[adv_filtered_df[col].isin(selected)]
    st.markdown("**Filtered Data Table (Advanced)**")
    st.dataframe(adv_filtered_df, use_container_width=True)
    st.markdown("**Byte 1/2/3 Distribution in Filtered Data**")
    for b in [1,2,3]:
        colname = f'SatType_{b}'
        if colname in adv_filtered_df.columns:
            fig = px.histogram(adv_filtered_df, x=colname, title=f'Byte {b} Distribution', color=colname)
            st.plotly_chart(fig, use_container_width=True)
