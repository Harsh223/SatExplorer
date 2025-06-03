import streamlit as st
import pandas as pd
import os
from datetime import datetime

from data_loader import load_satcat_data, get_satcat_update_date
from utils import get_date_confidence
from constants import TAB_NAMES, APP_TITLE

# Import tab renderers
def import_tab_renderers():
    from tabs.overview_tab import render_tab as render_overview
    from tabs.sattype_tab import render_tab as render_sattype
    from tabs.advanced_filters_tab import render_tab as render_advanced_filters
    from tabs.raw_data_tab import render_tab as render_raw_data
    from tabs.help_tab import render_tab as render_help
    from tabs.size_trends_tab import render_tab as render_size_trends
    from tabs.custom_analysis_tab import render_tab as render_custom_analysis
    from tabs.data_source_tab import render_tab as render_data_source
    return [
        render_overview,
        render_sattype,
        render_advanced_filters,
        render_raw_data,
        render_help,
        render_size_trends,
        render_custom_analysis,
        render_data_source
    ]

if __name__ == "__main__":
    st.set_page_config(page_title=APP_TITLE, layout="wide", initial_sidebar_state="auto")
    st.title(APP_TITLE)

    data_file = 'satcat.html'

    df, file_update_date = load_satcat_data(data_file)

    if df is None or df.empty:
        st.warning("No data loaded from satcat.html.")
        st.stop()

    # Add Date Confidence column if not present
    if 'LDate' in df.columns and 'DateConfidence' not in df.columns:
        df['DateConfidence'] = df['LDate'].apply(get_date_confidence)

    # Tabs
    renderers = import_tab_renderers()
    tabs = st.tabs(TAB_NAMES)
    for i, render_tab in enumerate(renderers):
        with tabs[i]:
            if TAB_NAMES[i] == "Data Source":
                render_tab(df, file_update_date)
            else:
                render_tab(df)
    st.markdown('<div style="text-align:center; color:gray; margin-top:2em;">Made with ❤️ by Harsh Kumar</div>', unsafe_allow_html=True)
