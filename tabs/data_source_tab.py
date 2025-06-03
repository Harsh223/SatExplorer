import streamlit as st
import os
from datetime import datetime
from constants import SATCAT_URL
from data_loader import fetch_and_update_satcat, parse_satcat_html, get_satcat_update_date

def render_tab(df, file_update_date=None):
    st.header("Data Source & Update")
    st.markdown("""
    You can load the latest SATCAT file from the web (planet4589.org) or use the local file (`satcat.html`).
    """)
    data_file = 'satcat.html'
    file_update_date = get_satcat_update_date(data_file)
    if os.name == "nt":
        today_str = datetime.now().strftime('%Y %b %#d')
    else:
        today_str = datetime.now().strftime('%Y %b %-d')
    st.info(f"Current SATCAT file update date: **{file_update_date if file_update_date else 'Unknown'}**")
    load_web = False
    if st.button("Load Latest SATCAT from Web"):
        if file_update_date and file_update_date == today_str:
            st.warning("The SATCAT file is already up-to-date for today. Downloading again is usually not necessary.")
            if st.confirm("Are you sure you want to download the file again?"):
                load_web = True
        else:
            load_web = True
    if load_web:
        df_new = fetch_and_update_satcat(data_file, SATCAT_URL)
        if df_new is not None:
            st.success("SATCAT data updated and loaded.")
        else:
            st.error("Failed to update SATCAT data from the web.")
    st.caption("If the file is already up-to-date, you will see a warning.")
    # TODO: Wire up fetch logic if needed
