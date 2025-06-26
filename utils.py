import re
import pandas as pd

def get_date_confidence(ldate):
    if pd.isna(ldate):
        return "Unknown"
    s = str(ldate)
    if '?' in s:
        return "Uncertain"
    if 's' in s:
        return "Scheduled (not confirmed)"
    if re.search(r'\d{4} [A-Za-z]{3} \d{1,2} \d{4}:\d{2}:\d{2}', s):
        return "Exact to second"
    if re.search(r'\d{4} [A-Za-z]{3} \d{1,2} \d{4}', s):
        return "Exact to minute"
    if re.search(r'\d{4} [A-Zael]{3} \d{1,2}', s):
        return "Exact to day"
    if re.search(r'\d{4} [A-Za-z]{3}', s):
        return "Exact to month"
    if re.search(r'\d{4}', s):
        return "Exact to year"
    return "Other/Unknown"

def size_class(mass):
    if pd.isna(mass): return 'Unknown'
    if mass < 1: return 'Femtosatellite'
    if mass <= 10: return 'Picosatellite'
    if mass <= 100: return 'Nanosatellite'
    if mass <= 1000: return 'Microsatellite'
    if mass <= 5000: return 'Small Satellite'
    if mass <= 10000: return 'Medium Satellite'
    return 'Large Satellite'
