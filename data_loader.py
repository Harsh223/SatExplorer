import os
import re
import pandas as pd
import streamlit as st
from datetime import datetime

try:
    import requests
except ImportError:
    requests = None

def get_satcat_update_date(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('# Updated'):
                    m = re.search(r'# Updated (\d{4} [A-Za-z]{3}\s+\d{1,2})', line)
                    if m:
                        return m.group(1).strip()
    except Exception:
        pass
    return None

def get_satcat_update_date_from_content(content):
    for line in content.splitlines():
        if line.startswith('# Updated'):
            m = re.search(r'# Updated (\d{4} [A-Za-z]{3}\s+\d{1,2})', line)
            if m:
                return m.group(1).strip()
    return None

def parse_satcat_html(html_file):
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    pre_matches = re.findall(r'<PRE>(.*?)</PRE>', content, re.DOTALL)
    if len(pre_matches) < 2:
        st.error("Could not find at least two PRE tags in the HTML file.")
        return pd.DataFrame()
    header_text = pre_matches[0].strip()
    for m in pre_matches[1:]:
        data_text = m.strip()
        if data_text:
            break
    else:
        st.error("No data found in PRE tags after header.")
        return pd.DataFrame()
    header_positions = []
    column_names = []
    for match in re.finditer(r'\S+', header_text):
        header_positions.append(match.start())
        column_names.append(match.group())
    header_positions.append(len(header_text) + 1)
    data_lines = [line for line in data_text.split('\n') if line.strip() and not line.strip().startswith('#') and re.match(r'^S\d+', line.strip())]
    data_rows = []
    for line in data_lines:
        row = []
        for i in range(len(column_names)):
            start = header_positions[i]
            end = header_positions[i+1] if i+1 < len(header_positions) else len(line)+1
            if start < len(line):
                if end <= len(line):
                    field = line[start:end].strip()
                else:
                    field = line[start:].strip()
            else:
                field = ""
            row.append(field)
        data_rows.append(row)
    df = pd.DataFrame(data_rows, columns=column_names)
    if 'Type' in df.columns:
        df['CoarseType'] = df['Type'].astype(str).str[0]
        for i in range(12):
            df[f'SatType_{i+1}'] = df['Type'].astype(str).str[i].replace({'': '-', ' ': '-'})
        df['SatType_1_2'] = df['Type'].astype(str).str[:2]
    if 'LDate' in df.columns:
        df['LaunchYear'] = df['LDate'].astype(str).str.extract(r'(\d{4})').astype(float)
    for col in ['Mass', 'Perigee', 'Apogee', 'Inc']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

def fetch_and_update_satcat(data_file, web_url):
    if requests is None:
        st.error("The 'requests' library is required to download the file. Please install it with 'pip install requests'.")
        return None
    try:
        resp = requests.get(web_url, timeout=30)
        resp.raise_for_status()
        fetched_date = get_satcat_update_date_from_content(resp.text)
        st.info(f"Fetched SATCAT update date: **{fetched_date if fetched_date else 'Unknown'}**")
        with open(data_file, 'wb') as f:
            f.write(resp.content)
        st.success("Downloaded and replaced local satcat.html with the latest SATCAT from the web.")
        return parse_satcat_html(data_file)
    except Exception as e:
        st.error(f"Failed to download SATCAT from web: {e}. Using local file if available.")
        if os.path.exists(data_file):
            return parse_satcat_html(data_file)
        return None

def load_satcat_data(data_file):
    """
    Loads the SATCAT data file, parses it, and returns (DataFrame, update_date_str).
    Returns (None, None) if file is missing or cannot be parsed.
    """
    if not os.path.exists(data_file):
        st.error(f"SATCAT file '{data_file}' not found.")
        return None, None
    try:
        df = parse_satcat_html(data_file)
        update_date = get_satcat_update_date(data_file)
        return df, update_date
    except Exception as e:
        st.error(f"Failed to load or parse '{data_file}': {e}")
        return None, None
