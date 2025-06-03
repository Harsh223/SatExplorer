import streamlit as st


def render_tab(df):
    st.header("Raw Data Table")
    st.info("""
    This table shows all columns and raw data for each object. Use it for detailed inspection or export.
    """)
    st.dataframe(df, use_container_width=True)
